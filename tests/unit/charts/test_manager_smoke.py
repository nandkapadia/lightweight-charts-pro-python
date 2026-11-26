"""Smoke tests for chart managers and BaseChart serialization."""

import pandas as pd

from lightweight_charts_pro.charts.base_chart import BaseChart
from lightweight_charts_pro.charts.managers.price_scale_manager import PriceScaleManager
from lightweight_charts_pro.charts.managers.series_manager import SeriesManager
from lightweight_charts_pro.charts.managers.trade_manager import TradeManager
from lightweight_charts_pro.charts.options import (
    ChartOptions,
    PriceScaleOptions,
    TradeVisualizationOptions,
)
from lightweight_charts_pro.charts.series.line import LineSeries
from lightweight_charts_pro.data.line_data import LineData
from lightweight_charts_pro.data.ohlcv_data import OhlcvData
from lightweight_charts_pro.data.trade import TradeData


def _ohlcv_row() -> OhlcvData:
    """One OHLCV bar used by price/volume smoke tests."""
    return OhlcvData(
        time=1640995200,
        open=100.0,
        high=110.0,
        low=90.0,
        close=105.0,
        volume=1000.0,
    )


def _trade() -> TradeData:
    """One closed trade used by frontend-config smoke tests."""
    return TradeData(
        entry_time=1640995200,
        entry_price=100.0,
        exit_time=1641081600,
        exit_price=110.0,
        is_profitable=True,
        id="t1",
    )


class TestManagerSmoke:
    """Small checks that managers construct, store, and serialize."""

    def test_price_scale_manager_overlay(self):
        """Overlay scales round-trip through serialization."""
        manager = PriceScaleManager()
        manager.add_overlay_scale("volume", PriceScaleOptions(visible=False))

        assert manager.has_overlay_scale("volume")
        assert "overlayPriceScales" in manager.validate_and_serialize()

    def test_trade_manager_empty_and_with_trades(self):
        """No trades serializes as None; a trade serializes as a list."""
        manager = TradeManager()
        assert manager.to_frontend_config() is None

        manager.add_trades([_trade()])
        config = manager.to_frontend_config()

        assert config is not None
        assert config["trades"][0]["entryPrice"] == 100.0

    def test_line_price_volume_from_ohlcv_objects(self):
        """Line price series stores close as LineData.value, not raw OHLCV."""
        manager = SeriesManager()
        manager.add_price_volume_series([_ohlcv_row()], None, price_type="line")

        price = manager.series[0]
        assert isinstance(price, LineSeries)
        assert isinstance(price.data[0], LineData)
        assert price.data[0].value == 105.0
        assert price.asdict()["data"][0]["value"] == 105.0
        assert len(manager.series) == 2

    def test_line_price_volume_maps_close_column(self):
        """DataFrame close column is mapped to LineSeries value."""
        frame = pd.DataFrame(
            {
                "time": [1640995200],
                "open": [100.0],
                "high": [110.0],
                "low": [90.0],
                "close": [105.0],
                "volume": [1000.0],
            }
        )
        manager = SeriesManager()
        manager.add_price_volume_series(frame, column_mapping=None, price_type="line")

        assert isinstance(manager.series[0].data[0], LineData)
        assert manager.series[0].data[0].value == 105.0

    def test_missing_pane_id_groups_as_pane_zero(self):
        """Series configs without paneId stay on pane 0 and keep pane order."""
        missing = LineSeries(data=[LineData(time=1, value=1.0)])
        legacy = LineSeries(data=[LineData(time=1, value=2.0)])
        explicit = LineSeries(data=[LineData(time=1, value=3.0)])
        missing.asdict = lambda: {  # type: ignore[method-assign]
            "type": "line",
            "data": [],
            "options": {"zIndex": 2},
            "name": "missing",
        }
        legacy.asdict = lambda: {  # type: ignore[method-assign]
            "type": "line",
            "data": [],
            "options": {"paneId": 2, "zIndex": 0},
            "name": "legacy",
        }
        explicit.asdict = lambda: {  # type: ignore[method-assign]
            "type": "line",
            "data": [],
            "options": {"zIndex": 0},
            "paneId": 1,
            "name": "explicit",
        }
        manager = SeriesManager([missing, explicit, legacy])

        names = [item["name"] for item in manager.to_frontend_configs()]
        assert names == ["missing", "explicit", "legacy"]

    def test_series_manager_get_series_info_for_pane_filtering(self):
        """get_series_info_for_pane filters by pane_id and uses display_name."""
        pane0_series = LineSeries(data=[LineData(time=1, value=1.0)], pane_id=0)
        pane0_series.display_name = "Primary"
        pane1_series = LineSeries(data=[LineData(time=1, value=2.0)], pane_id=1)
        pane1_series.display_name = "Secondary"

        manager = SeriesManager([pane0_series, pane1_series])
        info0 = manager.get_series_info_for_pane(0)
        info1 = manager.get_series_info_for_pane(1)

        assert len(info0) == 1
        assert info0[0]["displayName"] == "Primary"
        assert len(info1) == 1
        assert info1[0]["displayName"] == "Secondary"

    def test_base_chart_manager_sync_group_zero(self):
        """group_id=0 targets sync_groups['0'], not default_sync."""
        from lightweight_charts_pro.charts.base_chart_manager import BaseChartManager

        manager = BaseChartManager()
        assert manager.default_sync.crosshair is False
        assert "0" not in manager.sync_groups

        manager.enable_crosshair_sync(group_id=0)
        assert "0" in manager.sync_groups
        assert manager.sync_groups["0"].crosshair is True
        assert manager.default_sync.crosshair is False


class TestBaseChartIntegration:
    """Constructor series, options updates, and trade config shape."""

    def test_constructor_series_auto_creates_price_scale(self):
        """series= uses add_series, so a custom scale id is created."""
        overlay = LineSeries(
            data=[LineData(time=1, value=1.0)],
            price_scale_id="indicator",
        )
        chart = BaseChart(
            series=[
                LineSeries(data=[LineData(time=1, value=2.0)]),
                overlay,
            ]
        )

        assert len(chart.series) == 2
        assert chart._price_scale_manager.has_overlay_scale("indicator")

    def test_options_setter_updates_price_scale_manager(self):
        """Replacing options points the manager at the new scales."""
        chart = BaseChart()
        left = PriceScaleOptions(visible=True)
        chart.options = ChartOptions(left_price_scale=left)

        assert chart._price_scale_manager.left_price_scale is left

    def test_update_options_uses_options_update(self):
        """update_options applies nested dicts and replaced price scales."""
        chart = BaseChart()
        right = PriceScaleOptions(visible=False)
        chart.update_options(height=222, right_price_scale=right)
        chart.update_options(layout={"text_color": "#abcabc"})

        assert chart.options.height == 222
        assert chart.options.layout.text_color == "#abcabc"
        assert chart._price_scale_manager.right_price_scale is right

    def test_to_frontend_config_unpacks_trades(self):
        """Trades and visualization options are siblings on the chart object."""
        chart = BaseChart()
        chart.options.trade_visualization = TradeVisualizationOptions()
        chart.add_trades([_trade()])

        chart_obj = chart.to_frontend_config()["charts"][0]

        assert isinstance(chart_obj["trades"], list)
        assert chart_obj["trades"][0]["entryPrice"] == 100.0
        assert "tradeVisualizationOptions" in chart_obj
        assert "trades" not in chart_obj["chart"]
