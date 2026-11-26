"""Gradient ribbon series for streamlit-lightweight-charts.

This module provides the GradientRibbonSeries class for creating ribbon charts
that display upper and lower bands with gradient fill areas based on gradient values.
"""

import math
from typing import Any

import pandas as pd

from lightweight_charts_pro.charts.series.ribbon import RibbonSeries
from lightweight_charts_pro.data.gradient_ribbon import GradientRibbonData
from lightweight_charts_pro.type_definitions import ChartType
from lightweight_charts_pro.utils import chainable_property


@chainable_property("gradient_start_color", str, validator="color")
@chainable_property("gradient_end_color", str, validator="color")
@chainable_property("normalize_gradients", bool)
class GradientRibbonSeries(RibbonSeries):
    """Gradient ribbon series for lightweight charts.

    This class represents a ribbon series that displays upper and lower bands
    with gradient fill areas based on gradient values. It extends RibbonSeries
    with gradient fill capabilities, allowing for dynamic color transitions
    based on data values.

    The GradientRibbonSeries supports various styling options including separate
    line styling for each band via LineOptions, and gradient color effects based
    on data values.

    Attributes:
        upper_line: LineOptions instance for upper band styling.
        lower_line: LineOptions instance for lower band styling.
        fill_visible: Whether to display the fill area.
        gradient_start_color: Starting color for gradient fills (minimum value).
        gradient_end_color: Ending color for gradient fills (maximum value).
        normalize_gradients: Whether to normalize gradient values to 0-1 range.
        price_lines: List of PriceLineOptions for price lines (set after construction)
        price_format: PriceFormatOptions for price formatting (set after construction)
        markers: List of markers to display on this series (set after construction)

    """

    DATA_CLASS = GradientRibbonData

    def __init__(
        self,
        data: list[GradientRibbonData] | pd.DataFrame | pd.Series,
        column_mapping: dict | None = None,
        visible: bool = True,
        price_scale_id: str = "",
        pane_id: int | None = 0,
        gradient_start_color: str = "#4CAF50",
        gradient_end_color: str = "#F44336",
        normalize_gradients: bool = False,
    ):
        """Initialize GradientRibbonSeries.

        Args:
            data: List of data points or DataFrame
            column_mapping: Column mapping for DataFrame conversion
            visible: Whether the series is visible
            price_scale_id: ID of the price scale
            pane_id: The pane index this series belongs to
            gradient_start_color: Starting color for gradient fills
            gradient_end_color: Ending color for gradient fills
            normalize_gradients: Whether to normalize gradient values to 0-1 range

        """
        super().__init__(
            data=data,
            column_mapping=column_mapping,
            visible=visible,
            price_scale_id=price_scale_id,
            pane_id=pane_id,
        )

        # Cache attrs exist before option assignment so setters can invalidate them.
        self._gradient_bounds: tuple[float, float] | None = None
        self._normalized_cache: dict | None = None

        # Property assignment runs the chainable color/bool validators.
        self.gradient_start_color = gradient_start_color
        self.gradient_end_color = gradient_end_color
        self.normalize_gradients = normalize_gradients

    @property
    def chart_type(self) -> ChartType:
        """Get the chart type for this series."""
        return ChartType.GRADIENT_RIBBON

    def __setattr__(self, name: str, value: object) -> None:
        """Set an attribute and drop the normalized cache on data or option changes."""
        super().__setattr__(name, value)
        if name in ("_normalized_cache", "_gradient_bounds"):
            return
        if (
            getattr(self, "_normalized_cache", None) is None
            and getattr(self, "_gradient_bounds", None) is None
        ):
            return
        super().__setattr__("_normalized_cache", None)
        super().__setattr__("_gradient_bounds", None)

    def _invalidate_cache(self) -> None:
        """Invalidate the normalized data cache.

        This method should be called whenever the data changes to ensure
        the cached normalized results are recalculated on the next asdict() call.
        """
        self._normalized_cache = None
        self._gradient_bounds = None

    def update(self, updates: dict):
        """Override update to invalidate cache when data changes.

        Args:
            updates: Dictionary of updates to apply.

        Returns:
            Self for method chaining.

        """
        # Invalidate cache before updating
        self._invalidate_cache()
        # Call parent update
        return super().update(updates)

    @property
    def data(self):
        """Get the series data."""
        return self._data if hasattr(self, "_data") else []

    @data.setter
    def data(self, value):
        """Set the series data and invalidate cache.

        Args:
            value: New data to set.

        """
        self._data = value
        self._invalidate_cache()

    def _calculate_gradient_bounds(self) -> None:
        """Calculate min/max gradient values for normalization with optimized performance."""
        if not self.data:
            self._gradient_bounds = None
            return

        # Ultra-optimized single-pass min/max tracking
        min_grad = float("inf")
        max_grad = float("-inf")
        valid_count = 0

        # Single pass with inline min/max tracking - no list building
        for data_point in self.data:
            # Type check: ensure data point has gradient attribute
            if not hasattr(data_point, "gradient"):
                continue
            gradient = data_point.gradient  # type: ignore[attr-defined]
            if (
                gradient is not None
                and isinstance(gradient, (int, float))
                and not math.isnan(gradient)  # Not NaN
                and gradient != float("inf")
                and gradient != float("-inf")
            ):
                # Update min/max inline - no list operations
                min_grad = min(min_grad, gradient)
                max_grad = max(max_grad, gradient)
                valid_count += 1
                continue

        # Set bounds efficiently - only if we found valid values
        if valid_count > 0:
            self._gradient_bounds = (min_grad, max_grad)
        else:
            self._gradient_bounds = None

    def _compute_normalized_dict(self) -> dict:
        """Compute the normalized dictionary (expensive operation).

        This method performs the actual gradient normalization computation.
        It's called only when the cache is invalid.

        Returns:
            dict: The serialized dictionary with normalized gradients.

        """
        data_dict = super().asdict()

        # Remove inherited fill_color - gradient ribbon uses
        # gradientStartColor/gradientEndColor instead
        data_dict.get("options", {}).pop("fillColor", None)

        if self._normalize_gradients:
            # Calculate bounds if not already calculated
            if self._gradient_bounds is None:
                self._calculate_gradient_bounds()

            if self._gradient_bounds:
                min_grad, max_grad = self._gradient_bounds
                range_grad = max_grad - min_grad

                if range_grad > 0:  # Avoid division by zero
                    # Ultra-optimized normalization with minimal function calls
                    data_items = data_dict["data"]
                    range_grad_inv = 1.0 / range_grad  # Pre-calculate inverse

                    for item in data_items:  # Remove enumerate for speed
                        gradient = item.get("gradient")
                        if gradient is not None:
                            # Since we already validated in _calculate_gradient_bounds,
                            # we can trust the gradient values here
                            try:
                                # Use pre-calculated inverse for faster division
                                normalized = (gradient - min_grad) * range_grad_inv
                                # Fast clamping using conditional expression
                                item["gradient"] = (
                                    0.0 if normalized < 0.0 else (min(normalized, 1.0))
                                )
                            except (TypeError, ValueError):
                                item.pop("gradient", None)

        return data_dict

    def add_marker(self, marker: Any) -> "GradientRibbonSeries":
        """Add a marker and invalidate the cache.

        Args:
            marker: Marker to add.

        Returns:
            Self for method chaining.

        """
        self._invalidate_cache()
        return super().add_marker(marker)  # type: ignore[return-value]

    def add_markers(self, markers: list[Any]) -> "GradientRibbonSeries":
        """Add markers and invalidate the cache.

        Args:
            markers: List of markers to add.

        Returns:
            Self for method chaining.

        """
        self._invalidate_cache()
        return super().add_markers(markers)  # type: ignore[return-value]

    def add_price_line(self, price_line: Any) -> "GradientRibbonSeries":
        """Add a price line and invalidate the cache.

        Args:
            price_line: Price line to add.

        Returns:
            Self for method chaining.

        """
        self._invalidate_cache()
        return super().add_price_line(price_line)  # type: ignore[return-value]

    def add_price_lines(self, price_lines: list[Any]) -> "GradientRibbonSeries":
        """Add price lines and invalidate the cache.

        Args:
            price_lines: List of price lines to add.

        Returns:
            Self for method chaining.

        """
        self._invalidate_cache()
        return super().add_price_lines(price_lines)  # type: ignore[return-value]

    @staticmethod
    def _overlay_fingerprint(items: list | None) -> tuple:
        """Build a cheap content fingerprint for markers or price lines.

        Detects in-place list edits that would not go through ``__setattr__``.
        """
        if not items:
            return ()
        fingerprint: list = []
        for item in items:
            if isinstance(item, dict):
                fingerprint.append(tuple(sorted(item.items())))
                continue
            if hasattr(item, "asdict") and callable(item.asdict):
                try:
                    data = item.asdict()
                    fingerprint.append(
                        tuple(sorted(data.items())) if isinstance(data, dict) else repr(data)
                    )
                    continue
                except (TypeError, ValueError, AttributeError):
                    pass
            fingerprint.append(repr(item))
        return tuple(fingerprint)

    def _cache_copy(self) -> dict:
        """Return a shallow copy of the normalized cache with copied lists."""
        assert self._normalized_cache is not None
        return {
            key: (list(value) if isinstance(value, list) else value)
            for key, value in self._normalized_cache.items()
        }

    def asdict(self):
        """Override to include normalized gradients with caching for performance.

        Returns cached normalized results if available, otherwise computes and caches them.
        This optimization prevents O(2n) iterations on every serialization call.

        Returns a shallow copy so callers cannot mutate the live cache.

        Returns:
            dict: The serialized dictionary with normalized gradients.

        """
        if self._normalized_cache is not None:
            current_markers = getattr(self, "markers", []) or []
            current_price_lines = getattr(self, "price_lines", []) or []
            cached_markers = self._normalized_cache.get("markers", [])
            cached_price_lines = self._normalized_cache.get("priceLines", [])
            if (
                self._overlay_fingerprint(current_markers)
                != self._overlay_fingerprint(cached_markers)
                or self._overlay_fingerprint(current_price_lines)
                != self._overlay_fingerprint(cached_price_lines)
            ):
                self._invalidate_cache()
            else:
                return self._cache_copy()

        self._normalized_cache = self._compute_normalized_dict()
        return self._cache_copy()
