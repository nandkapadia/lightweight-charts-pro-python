# Documentation Guide

This guide explains how to build, maintain, and contribute to the documentation
for Lightweight Charts Pro Python.

## 📚 Documentation Stack

- **Sphinx**: Documentation generation
- **Read the Docs**: Hosting and versioning
- **GitHub Pages**: Alternative hosting
- **GitHub Wiki**: Quick reference and guides
- **Google-style docstrings**: Source documentation

## 🚀 Quick Start

### Install Documentation Dependencies

```bash
# Install all documentation dependencies
pip install -r docs/requirements.txt

# Or install with development extras
pip install -e ".[dev]"
```

### Build Documentation Locally

```bash
# Build HTML documentation
cd docs
make html

# Open in browser
open build/html/index.html  # macOS
xdg-open build/html/index.html  # Linux
start build/html/index.html  # Windows
```

### Live Documentation Server

For development with auto-reload:

```bash
cd docs
make livehtml
# Opens at http://localhost:8000
```

## 📝 Writing Documentation

### Google-Style Docstrings

All code must use Google-style docstrings:

```python
def calculate_price(quantity: int, price: float, discount: float = 0.0) -> float:
    """Calculate total price with optional discount.

    This function calculates the total price for a given quantity and unit
    price, applying an optional discount percentage.

    Args:
        quantity (int): Number of items to purchase. Must be positive.
        price (float): Price per item in dollars. Must be positive.
        discount (float, optional): Discount percentage (0-100).
            Defaults to 0.0 (no discount).

    Returns:
        float: Total price after discount, rounded to 2 decimal places.

    Raises:
        ValueError: If quantity or price is negative, or if discount is
            not in the range [0, 100].

    Example:
        Calculate price with discount::

            >>> calculate_price(10, 5.00, discount=10.0)
            45.00

        Calculate price without discount::

            >>> calculate_price(5, 10.00)
            50.00

    Note:
        The discount is applied as a percentage. For example, a discount
        of 10.0 means 10% off.

    See Also:
        apply_coupon: Apply coupon codes for special discounts.

    """
    if quantity < 0 or price < 0:
        raise ValueError("Quantity and price must be non-negative")
    if not 0 <= discount <= 100:
        raise ValueError("Discount must be between 0 and 100")

    subtotal = quantity * price
    discount_amount = subtotal * (discount / 100)
    total = subtotal - discount_amount

    return round(total, 2)
```

### Required Docstring Sections

**For Functions/Methods:**
- Summary line (required)
- Extended description (recommended)
- `Args:` (if has parameters)
- `Returns:` (if returns value)
- `Raises:` (if raises exceptions)
- `Example:` (recommended)
- `Note:` (optional)
- `See Also:` (optional)

**For Classes:**
- Summary line (required)
- Extended description (recommended)
- `Attributes:` (required for data classes)
- `Example:` (recommended)
- `Note:` (optional)

**For Modules:**
- Summary paragraph (required)
- Extended description with key features
- Example usage
- Version/Author/License information

### RST Documentation Files

Add new guides in `docs/source/`:

```rst
My New Guide
============

Introduction paragraph explaining what this guide covers.

Section 1
---------

Content with subsections.

Subsection
~~~~~~~~~~

More detailed content.

Code Examples
-------------

.. code-block:: python

   from lightweight_charts_pro import LineSeries

   # Your example code
   series = LineSeries(data=data)

.. note::
   Important notes go in admonitions.

.. warning::
   Warnings for common pitfalls.

Links and References
--------------------

Link to API: :class:`~lightweight_charts_pro.charts.series.LineSeries`

External link: `TradingView <https://tradingview.com>`_
```

## 🔄 CI/CD Automation

### Automatic Documentation Deployment

Documentation is automatically built and deployed on:

**Triggers:**
- Push to `main` branch
- Push to `dev` branch
- Pull requests (build only, no deploy)
- New releases

**Deployments:**
- **Read the Docs**: Automatic on all branches
- **GitHub Pages**: On push to `main`
- **GitHub Wiki**: On push to `main`

### Manual Deployment

Trigger manual deployment:

```bash
# Via GitHub UI
Actions → Documentation → Run workflow

# Or push to main
git push origin main
```

### Versioned Documentation

Read the Docs automatically builds docs for:
- `latest` (main branch)
- `stable` (latest release)
- Each tagged release (v0.1.0, v0.2.0, etc.)

## 🧪 Documentation Testing

### Validate Documentation Builds

```bash
# Build with warnings as errors
cd docs
make strict

# Check for broken links
make linkcheck

# Check documentation coverage
make coverage
```

### Validate Docstrings

```bash
# Run docstring validator
python scripts/validate_docstrings.py lightweight_charts_pro/**/*.py

# Check docstring style
pydocstyle --convention=google lightweight_charts_pro

# Validate docstring arguments match code
darglint --docstring-style google lightweight_charts_pro
```

## 📊 Documentation Coverage

Check what's documented:

```bash
cd docs
make coverage
cat build/coverage/python.txt
```

Target: **100% documentation coverage** for public APIs.

## 🪝 Pre-commit Hooks

### Install Pre-commit

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Install commit message hook
pre-commit install --hook-type commit-msg
```

### Documentation Checks in Pre-commit

Pre-commit automatically runs:

1. **Docstring style**: `pydocstyle`
2. **Docstring arguments**: `darglint`
3. **RST linting**: `doc8`
4. **Documentation build**: `sphinx-build` (on push)
5. **Custom validation**: `validate_docstrings.py`

### Skip Hooks (Emergency Only)

```bash
# Skip all hooks
git commit --no-verify

# Skip specific hook
SKIP=pylint git commit
```

## 📖 Documentation Structure

```
docs/
├── source/
│   ├── conf.py                 # Sphinx configuration
│   ├── index.rst               # Documentation home
│   ├── getting-started.rst     # Installation & quickstart
│   ├── contributing.rst        # Contribution guide
│   ├── changelog.rst           # Version history
│   │
│   ├── user-guide/             # User guides
│   │   ├── index.rst
│   │   ├── basic-usage.rst
│   │   ├── advanced-features.rst
│   │   └── best-practices.rst
│   │
│   ├── examples/               # Example notebooks/scripts
│   │   ├── index.rst
│   │   ├── basic-charts.rst
│   │   └── advanced-charts.rst
│   │
│   ├── api/                    # API reference (auto-generated)
│   │   └── index.rst
│   │
│   ├── _static/                # Custom CSS, images
│   │   └── custom.css
│   │
│   └── _templates/             # Custom templates
│       └── autoapi/
│
├── build/                      # Generated documentation (gitignored)
├── requirements.txt            # Doc dependencies
└── Makefile                    # Build commands
```

## 🔧 Common Tasks

### Add New Section

1. Create RST file in `docs/source/`
2. Add to `toctree` in relevant index
3. Build and verify

### Add API Documentation

Automatic via AutoAPI! Just add Google-style docstrings to code.

### Update Examples

Add examples in `docs/source/examples/` as RST or Jupyter notebooks.

### Change Theme

Edit `docs/source/conf.py`:

```python
html_theme = "sphinx_rtd_theme"  # or "alabaster", "pydata_sphinx_theme", etc.
```

## 🐛 Troubleshooting

### Build Fails

```bash
# Clean and rebuild
cd docs
make clean
make html
```

### Import Errors

Ensure package is installed:

```bash
pip install -e .
```

### Broken Links

Check and fix:

```bash
make linkcheck
# Review: build/linkcheck/output.txt
```

### Missing AutoAPI

```bash
pip install sphinx-autoapi
```

## 📚 Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Read the Docs Guide](https://docs.readthedocs.io/)
- [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)

## 📧 Support

For documentation questions:

- GitHub Discussions: Technical questions
- GitHub Issues: Documentation bugs
- Pull Requests: Documentation improvements
