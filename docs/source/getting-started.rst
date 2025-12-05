Getting Started
===============

This guide will help you get started with Lightweight Charts Pro Python.

Installation
------------

Requirements
~~~~~~~~~~~~

- Python 3.10 or higher
- pandas >= 2.0.0
- numpy >= 1.24.0

Install from PyPI
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install lightweight-charts-pro

Install from Source
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/your-username/lightweight-charts-pro-python.git
   cd lightweight-charts-pro-python
   pip install -e .

Basic Concepts
--------------

Data Models
~~~~~~~~~~~

The library provides data models for different chart types:

- **LineData**: Single value data points for line/area charts
- **OhlcData**: Open, High, Low, Close data for bar charts
- **CandlestickData**: OHLC data with optional colors for candlestick charts
- **HistogramData**: Single value data for histogram/volume charts

.. code-block:: python

   from lightweight_charts_pro.data import (
       LineData,
       CandlestickData,
       HistogramData,
   )

   # Line data
   line_point = LineData(time="2024-01-01", value=100.0)

   # Candlestick data
   candle = CandlestickData(
       time="2024-01-01",
       open=100.0,
       high=105.0,
       low=98.0,
       close=103.0,
   )

   # Histogram data
   volume = HistogramData(time="2024-01-01", value=1000000, color="#26a69a")

Series Types
~~~~~~~~~~~~

Series represent different visualization types:

- **LineSeries**: Line charts
- **AreaSeries**: Area charts with fill
- **CandlestickSeries**: Candlestick charts
- **HistogramSeries**: Bar/volume charts
- **BarSeries**: OHLC bar charts
- **BaselineSeries**: Baseline charts
- **BandSeries**: Band/range charts
- **RibbonSeries**: Ribbon charts with upper/lower bands

.. code-block:: python

   from lightweight_charts_pro.charts.series import (
       LineSeries,
       CandlestickSeries,
       HistogramSeries,
   )

   # Create series with data
   line_series = LineSeries(data=line_data)
   candle_series = CandlestickSeries(data=candle_data)
   volume_series = HistogramSeries(data=volume_data)

First Chart
-----------

Creating a Simple Line Chart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from lightweight_charts_pro import LineSeries, LineData

   # Prepare data
   data = [
       LineData(time="2024-01-01", value=100.0),
       LineData(time="2024-01-02", value=105.0),
       LineData(time="2024-01-03", value=103.0),
       LineData(time="2024-01-04", value=108.0),
       LineData(time="2024-01-05", value=110.0),
   ]

   # Create and configure series
   series = LineSeries(data=data)
   series.color = "#2196F3"
   series.line_width = 2
   series.title = "Price"

   # Serialize for frontend
   chart_config = series.asdict()

Creating a Candlestick Chart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from lightweight_charts_pro import CandlestickSeries, CandlestickData

   # Prepare OHLC data
   data = [
       CandlestickData(
           time="2024-01-01",
           open=100.0,
           high=105.0,
           low=98.0,
           close=103.0,
       ),
       CandlestickData(
           time="2024-01-02",
           open=103.0,
           high=108.0,
           low=102.0,
           close=106.0,
       ),
   ]

   # Create and configure series
   series = CandlestickSeries(data=data)
   series.up_color = "#26a69a"  # Green for bullish
   series.down_color = "#ef5350"  # Red for bearish
   series.title = "BTC/USD"

Using with pandas DataFrame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from lightweight_charts_pro import CandlestickSeries

   # Load data from CSV
   df = pd.read_csv("ohlc_data.csv")
   df["time"] = pd.to_datetime(df["timestamp"])

   # Create series from DataFrame
   series = CandlestickSeries(
       data=df,
       column_mapping={
           "time": "time",
           "open": "open",
           "high": "high",
           "low": "low",
           "close": "close",
       },
   )

Next Steps
----------

- :doc:`user-guide/index` - Learn about advanced features
- :doc:`examples/index` - See complete examples
- :doc:`autoapi/index` - Explore the API reference

Common Issues
-------------

Import Errors
~~~~~~~~~~~~~

If you encounter import errors, ensure you have installed all dependencies:

.. code-block:: bash

   pip install pandas>=2.0.0 numpy>=1.24.0

Type Errors
~~~~~~~~~~~

The library uses type hints extensively. For the best development experience,
use a type checker like mypy:

.. code-block:: bash

   pip install mypy
   mypy your_code.py
