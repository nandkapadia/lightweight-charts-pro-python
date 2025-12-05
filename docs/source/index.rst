Lightweight Charts Pro Python Documentation
============================================

**Lightweight Charts Pro Python** is a framework-agnostic Python library for creating
professional financial charts using TradingView's Lightweight Charts library.

.. image:: https://img.shields.io/pypi/v/lightweight-charts-pro.svg
   :target: https://pypi.org/project/lightweight-charts-pro/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/lightweight-charts-pro.svg
   :target: https://pypi.org/project/lightweight-charts-pro/
   :alt: Python versions

.. image:: https://img.shields.io/github/license/your-username/lightweight-charts-pro-python.svg
   :target: https://github.com/your-username/lightweight-charts-pro-python/blob/main/LICENSE
   :alt: License

Features
--------

* 📊 **Comprehensive Chart Types**: Candlestick, line, area, histogram, bar, and more
* 🎨 **Full Customization**: Complete control over colors, styles, and layouts
* 📈 **Financial Data Support**: OHLC, OHLCV, and custom data formats
* 🔄 **Real-time Updates**: Stream data updates to charts
* 🎯 **Framework-Agnostic**: Works with Streamlit, Dash, Flask, Django, or standalone
* 📱 **Responsive**: Mobile-friendly and adaptive layouts
* ⚡ **High Performance**: Optimized for large datasets
* 🧪 **Well-Tested**: Comprehensive test coverage

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install lightweight-charts-pro

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from lightweight_charts_pro import LineSeries, LineData

   # Create some data
   data = [
       LineData(time="2024-01-01", value=100.0),
       LineData(time="2024-01-02", value=105.0),
       LineData(time="2024-01-03", value=103.0),
   ]

   # Create a line series
   series = LineSeries(data=data)
   series.color = "#2196F3"
   series.line_width = 2

   # Serialize for frontend
   chart_config = series.asdict()

Documentation Sections
----------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   getting-started
   user-guide/index
   examples/index

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   autoapi/index

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Support
-------

- **Documentation**: https://lightweight-charts-pro-python.readthedocs.io/
- **Issues**: https://github.com/your-username/lightweight-charts-pro-python/issues
- **Discussions**: https://github.com/your-username/lightweight-charts-pro-python/discussions

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.
