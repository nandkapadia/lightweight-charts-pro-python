"""Price line options configuration for streamlit-lightweight-charts.

This module provides price line option classes for configuring
horizontal price lines on charts.
"""

from dataclasses import dataclass

from lightweight_charts_pro.charts.options.base_options import Options
from lightweight_charts_pro.exceptions import (
    ColorValidationError,
    TypeValidationError,
    ValueValidationError,
)
from lightweight_charts_pro.type_definitions.enums import LineStyle
from lightweight_charts_pro.utils import chainable_field, validated_field
from lightweight_charts_pro.utils.data_utils import is_valid_color


def _validate_hit_test_tolerance(value: float) -> float:
    """Reject negative hover tolerances.

    Args:
        value (float): Extra pixels around the line that still count as a hover.

    Returns:
        float: The unchanged tolerance.

    Raises:
        TypeValidationError: If the tolerance is not a number (bool is rejected).
        ValueValidationError: If the tolerance is negative.

    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeValidationError("hit_test_tolerance", "a number", type(value).__name__)
    if value < 0:
        raise ValueValidationError.non_negative_value("hit_test_tolerance", value)
    return value


@dataclass
@chainable_field("id", str)
@chainable_field("price", (int, float))
@chainable_field("color", str, validator="color")
@chainable_field("line_width", int)
@chainable_field("line_style", LineStyle)
@chainable_field("line_visible", bool)
@chainable_field("axis_label_visible", bool)
@chainable_field("title", str)
@chainable_field("axis_label_color", str, validator="color")
@chainable_field("axis_label_text_color", str, validator="color")
@validated_field(
    "hit_test_tolerance",
    (int, float),
    validator=_validate_hit_test_tolerance,
    allow_none=True,
)
class PriceLineOptions(Options):
    """Encapsulates style and configuration options for a price line.

    Matching TradingView's PriceLineOptions.

    See: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceLineOptions

    Attributes:
        id (Optional[str]): Optional ID of the price line.
        price (float): Price line's value.
        color (str): Price line's color (hex or rgba).
        line_width (int): Price line's width in pixels.
        line_style (LineStyle): Price line's style.
        line_visible (bool): Whether the line is displayed.
        axis_label_visible (bool): Whether the price value is shown on the price scale.
        title (str): Title for the price line on the chart pane.
        axis_label_color (Optional[str]): Background color for the axis label.
        axis_label_text_color (Optional[str]): Text color for the axis label.
        hit_test_tolerance (Optional[float]): Pixels beyond the line's stroke that still
            count as hovering it. None leaves the library default (7) in place.

    """

    id: str | None = None
    price: float = 0.0
    color: str = ""
    line_width: int = 1
    line_style: LineStyle = LineStyle.SOLID
    line_visible: bool = True
    axis_label_visible: bool = False
    title: str = ""
    axis_label_color: str | None = None
    axis_label_text_color: str | None = None
    hit_test_tolerance: float | None = None

    @staticmethod
    def _validate_color_static(color: str, property_name: str) -> str:
        """Validate color for decorator use with static method."""
        if color and not is_valid_color(color):
            raise ColorValidationError(property_name, color)
        return color
