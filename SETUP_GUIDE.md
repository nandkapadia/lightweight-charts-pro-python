# Complete Setup Guide

## 🎯 Quick Setup (5 minutes)

```bash
# 1. Install development dependencies
make install-dev

# 2. Install documentation dependencies
make install-docs

# 3. Install pre-commit hooks
make pre-commit

# 4. Verify setup
make test
make docs

# You're ready to develop! 🚀
```

## 📚 Complete Documentation Setup

### 1. Standard for User Documentation

Your project now follows industry-standard documentation practices:

#### **Sphinx + Read the Docs (Primary)**
- **Sphinx**: Documentation generation from code
- **Read the Docs**: Free hosting with versioning
- **URL**: `https://lightweight-charts-pro-python.readthedocs.io/`

**Features:**
- ✅ Automatic API reference from docstrings
- ✅ Versioned documentation (latest, stable, v0.1.0, etc.)
- ✅ PDF and ePub downloads
- ✅ Search functionality
- ✅ Mobile-responsive

#### **GitHub Pages (Alternative)**
- Static HTML hosting via GitHub
- **URL**: `https://your-username.github.io/lightweight-charts-pro-python/`
- Deployed automatically on push to main

#### **GitHub Wiki (Quick Reference)**
- Markdown-based quick reference
- Auto-updated from RST docs
- Good for FAQs and troubleshooting

### 2. CI/CD Automation

#### **Automatic Documentation Updates**

Documentation is built and deployed automatically:

**Triggers:**
- ✅ Push to `main` → Deploy to Read the Docs, GitHub Pages, and Wiki
- ✅ Push to `dev` → Build preview (Read the Docs only)
- ✅ Pull requests → Build check (no deployment)
- ✅ New release → Deploy versioned docs

**Workflows:**
```
.github/workflows/docs.yml       # Main documentation workflow
├── build                        # Build Sphinx docs
├── deploy-gh-pages              # Deploy to GitHub Pages
├── update-wiki                  # Update GitHub Wiki
└── link-check                   # Validate links
```

#### **What Happens Automatically:**

1. **On every push to main:**
   ```
   Code pushed → GitHub Actions triggered
   → Install dependencies
   → Build Sphinx documentation
   → Run doc validation (warnings, coverage, links)
   → Deploy to Read the Docs
   → Deploy to GitHub Pages
   → Update GitHub Wiki (Markdown conversion)
   → Notify if build fails
   ```

2. **On pull requests:**
   ```
   PR created → Build documentation
   → Check for warnings
   → Report build status
   → No deployment (preview only)
   ```

3. **On releases:**
   ```
   New tag (v0.2.0) → Build versioned docs
   → Deploy to Read the Docs (v0.2.0)
   → Update "stable" docs
   → Create downloadable PDF
   ```

### 3. Pre-commit Hooks

#### **Installed Hooks:**

**Code Formatting (Auto-fix):**
- ✅ `isort` - Import sorting with float-to-top
- ✅ `autoflake` - Remove unused imports/variables
- ✅ `black` - Code formatting (line-length 100)

**Linting (Enforced):**
- ✅ `ruff` - Fast Python linter
- ✅ `pylint` - Advanced linting
- ✅ `mypy` - Type checking

**Documentation (Validation):**
- ✅ `pydocstyle` - Docstring style checking
- ✅ `darglint` - Docstring argument validation
- ✅ `doc8` - RST linting
- ✅ Custom validator - Google-style enforcement

**Security:**
- ✅ `bandit` - Security vulnerability scanner
- ✅ `safety` - Dependency security checker

**Tests (On push only):**
- ✅ `pytest` - Run all tests
- ✅ `pytest-cov` - Coverage check (>90%)

**Commit Messages:**
- ✅ Conventional commits validation

#### **How It Works:**

```bash
# Before commit (automatic)
git add your_file.py
git commit -m "feat: add new feature"

→ isort runs (fixes imports)
→ autoflake runs (removes unused imports)
→ black runs (formats code)
→ ruff runs (checks for errors)
→ pylint runs (checks code quality)
→ mypy runs (checks types)
→ pydocstyle runs (validates docstrings)
→ darglint runs (validates Args match function signature)
→ bandit runs (security check)

If all pass → Commit succeeds ✅
If any fail → Commit blocked ❌ (fix and retry)
```

```bash
# Before push (additional checks)
git push

→ pytest runs (all tests)
→ coverage check (must be >90%)
→ sphinx-build runs (validates docs)
→ documentation coverage check

If all pass → Push succeeds ✅
If any fail → Push blocked ❌
```

## 🛠️ Development Workflow

### Daily Development

```bash
# 1. Start working on a feature
git checkout -b feature/my-feature

# 2. Write code with docstrings
# ... edit files ...

# 3. Auto-format code
make format

# 4. Run tests
make test

# 5. Commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: add my feature"

# 6. Push (additional hooks run)
git push origin feature/my-feature

# 7. Create pull request
# → Documentation build check runs
# → All CI checks must pass
```

### Documentation Workflow

```bash
# 1. Write code with Google-style docstrings
def my_function(param: str) -> int:
    """Do something amazing.

    Args:
        param (str): Description of parameter.

    Returns:
        int: Description of return value.
    """
    pass

# 2. Build docs locally
make docs

# 3. View in browser
open docs/build/html/index.html

# 4. For development with live reload
make docs-live
# → Opens at http://localhost:8000
# → Auto-reloads on file changes

# 5. Validate documentation
make docs-check
# → Checks for warnings
# → Checks for broken links
# → Checks documentation coverage

# 6. Push to main
git push origin main
# → Documentation auto-deployed to all platforms
```

## 📖 Documentation Best Practices

### Writing Good Docstrings

**✅ DO:**
```python
def calculate_total(items: List[Item], tax_rate: float = 0.0) -> float:
    """Calculate total price including tax.

    This function sums up all item prices and applies the specified
    tax rate to calculate the final total.

    Args:
        items (List[Item]): List of items to calculate total for.
            Each item must have a 'price' attribute.
        tax_rate (float, optional): Tax rate as a decimal (e.g., 0.08
            for 8% tax). Defaults to 0.0 (no tax).

    Returns:
        float: Total price including tax, rounded to 2 decimal places.

    Raises:
        ValueError: If tax_rate is negative.
        AttributeError: If any item doesn't have a 'price' attribute.

    Example:
        Calculate total with tax::

            >>> items = [Item(price=10.0), Item(price=20.0)]
            >>> calculate_total(items, tax_rate=0.08)
            32.40

    Note:
        Tax is calculated on the subtotal, not per item.
    """
```

**❌ DON'T:**
```python
def calculate_total(items, tax_rate=0.0):
    # Calculate total  ← Bad: No docstring
    pass

def calculate_total(items, tax_rate=0.0):
    """Calculate total."""  ← Bad: Too brief, missing Args/Returns
    pass
```

### Required Docstring Sections

| Item | Summary | Args | Returns | Example |
|------|---------|------|---------|---------|
| Module | ✅ Required | ➖ N/A | ➖ N/A | ✅ Recommended |
| Class | ✅ Required | ➖ N/A | ➖ N/A | ✅ Recommended |
| Function | ✅ Required | ✅ If has params | ✅ If returns | ✅ Recommended |
| Method | ✅ Required | ✅ If has params | ✅ If returns | ⚪ Optional |

## 🔍 Documentation Coverage Goals

- **Module-level docstrings**: 100%
- **Class docstrings**: 100%
- **Public function docstrings**: 100%
- **Args documentation**: 100% (all parameters documented)
- **Returns documentation**: 100% (all return values documented)

Check coverage:
```bash
make docs-check
cat docs/build/coverage/python.txt
```

## 🚀 Deployment

### Read the Docs Setup

1. **Connect Repository:**
   - Go to https://readthedocs.org/
   - Sign in with GitHub
   - Click "Import a Project"
   - Select `lightweight-charts-pro-python`

2. **Configure (Already done in `.readthedocs.yaml`):**
   - Python version: 3.10
   - Build formats: HTML, PDF, ePub
   - Install: `pip install -e . && pip install -r docs/requirements.txt`

3. **Activate:**
   - Click "Build version"
   - Wait for build to complete
   - Visit: `https://lightweight-charts-pro-python.readthedocs.io/`

4. **Automatic Updates:**
   - Push to `main` → Docs update automatically
   - Create release → Versioned docs created

### GitHub Pages Setup

1. **Enable GitHub Pages:**
   - Go to repository Settings
   - Pages → Source: "GitHub Actions"
   - Save

2. **First Deployment:**
   ```bash
   git push origin main
   # Wait for Actions to complete
   # Visit: https://your-username.github.io/lightweight-charts-pro-python/
   ```

3. **Automatic Updates:**
   - Every push to `main` updates GitHub Pages

### GitHub Wiki Setup

1. **Enable Wiki:**
   - Go to repository Settings
   - Features → Enable Wiki

2. **First Update:**
   ```bash
   git push origin main
   # Wiki automatically updated via Actions
   ```

## 🧪 Testing Documentation

### Local Testing

```bash
# Full documentation build
make docs

# Live reload server (development)
make docs-live

# Validate (warnings as errors)
cd docs && make strict

# Check links
cd docs && make linkcheck

# Coverage report
cd docs && make coverage
```

### CI Testing

Runs automatically on every push:
- ✅ Build succeeds without warnings
- ✅ No broken links
- ✅ Documentation coverage >95%
- ✅ Docstring validation passes

## 📦 Package Structure

```
lightweight-charts-pro-python/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Main CI workflow
│       └── docs.yml                  # Documentation workflow ← NEW
│
├── docs/                             # Documentation ← NEW
│   ├── source/
│   │   ├── conf.py                   # Sphinx config
│   │   ├── index.rst                 # Main page
│   │   ├── getting-started.rst
│   │   ├── contributing.rst
│   │   ├── changelog.rst
│   │   ├── user-guide/
│   │   ├── examples/
│   │   └── _static/
│   ├── Makefile
│   └── requirements.txt
│
├── scripts/                          # Utility scripts ← NEW
│   ├── convert_docs_to_wiki.py      # Wiki automation
│   └── validate_docstrings.py       # Docstring validator
│
├── lightweight_charts_pro/          # Main package (already documented! ✅)
├── tests/                            # Tests (already formatted! ✅)
│
├── .pre-commit-config.yaml           # Pre-commit config ← NEW
├── .readthedocs.yaml                 # RTD config ← NEW
├── DOCUMENTATION.md                  # Doc guide ← NEW
├── SETUP_GUIDE.md                    # This file ← NEW
└── Makefile                          # Enhanced with docs commands
```

## 🎓 Learning Resources

### Sphinx & RST
- [Sphinx Tutorial](https://www.sphinx-doc.org/en/master/tutorial/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [Sphinx Themes Gallery](https://sphinx-themes.org/)

### Google-Style Docstrings
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Napoleon Extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
- [Example Google Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

### Read the Docs
- [Read the Docs Guide](https://docs.readthedocs.io/)
- [RTD Tutorial](https://docs.readthedocs.io/en/stable/tutorial/)
- [.readthedocs.yaml Config](https://docs.readthedocs.io/en/stable/config-file/v2.html)

### Pre-commit
- [Pre-commit Documentation](https://pre-commit.com/)
- [Pre-commit Hooks List](https://pre-commit.com/hooks.html)
- [Writing Custom Hooks](https://pre-commit.com/#new-hooks)

## 🆘 Troubleshooting

### Documentation Build Fails

```bash
# Clean and rebuild
cd docs
make clean
make html

# Check for errors
make strict
```

### Pre-commit Hook Fails

```bash
# Run specific hook manually
pre-commit run black --all-files

# Skip hook temporarily (emergency only!)
git commit --no-verify

# Update hooks
pre-commit autoupdate
```

### Import Errors in Docs

```bash
# Ensure package is installed
pip install -e .

# Check sys.path in conf.py
python -c "import sys; print(sys.path)"
```

## 📞 Support

- **Documentation Issues**: Open GitHub issue with `documentation` label
- **Pre-commit Issues**: Check `.pre-commit-config.yaml`
- **CI/CD Issues**: Check GitHub Actions logs

---

## ✅ Next Steps

1. **Enable Read the Docs**: Connect your GitHub repository
2. **Enable GitHub Pages**: In repository settings
3. **Enable GitHub Wiki**: In repository settings
4. **Push to main**: Trigger first documentation build
5. **Share documentation**: Add badges to README

**You're all set! Happy documenting! 📚**
