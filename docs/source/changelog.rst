Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

Added
~~~~~

Changed
~~~~~~~

Fixed
~~~~~

Deprecated
~~~~~~~~~~

Removed
~~~~~~~

Security
~~~~~~~~

[0.1.0] - 2024-12-06
--------------------

Added
~~~~~

- Initial release of lightweight-charts-pro-python
- Support for all major chart types:

  - Candlestick charts
  - Line charts
  - Area charts
  - Bar charts
  - Histogram charts
  - Baseline charts
  - Band charts
  - Ribbon charts
  - Gradient ribbon charts
  - Trend fill charts
  - Signal charts

- Comprehensive data models:

  - LineData, AreaData, BaselineData
  - OhlcData, OhlcvData
  - CandlestickData, BarData
  - HistogramData
  - SignalData, TrendFillData
  - RibbonData, GradientRibbonData, BandData

- Type definitions and enumerations:

  - ChartType, LineStyle, LineType
  - MarkerPosition, MarkerShape
  - PriceScaleMode, CrosshairMode
  - And many more configuration enums

- Chart options and configuration:

  - ChartOptions for global chart settings
  - LayoutOptions for chart layout
  - PriceScaleOptions for price axis
  - TimeScaleOptions for time axis
  - LocalizationOptions for i18n
  - TradeVisualizationOptions for trade display

- Utilities and helpers:

  - Case conversion (snake_case ↔ camelCase)
  - Color validation and manipulation
  - Data normalization and validation
  - Serialization utilities
  - Chainable property decorators

- Comprehensive test suite with >90% coverage
- Google-style docstrings throughout
- Type hints for all public APIs
- Framework-agnostic design

Documentation
~~~~~~~~~~~~~

- Sphinx documentation with Read the Docs theme
- API reference with automatic generation
- Getting started guide
- User guide with examples
- Contributing guide

.. _Unreleased: https://github.com/your-username/lightweight-charts-pro-python/compare/v0.1.0...HEAD
.. _0.1.0: https://github.com/your-username/lightweight-charts-pro-python/releases/tag/v0.1.0
