"""Sphinx configuration for Lightweight Charts Pro Python documentation.

This configuration file sets up Sphinx to generate comprehensive HTML documentation
from the Google-style docstrings in the codebase.
"""

import os
import sys
from datetime import datetime

# Add the project root to sys.path for autodoc
sys.path.insert(0, os.path.abspath("../.."))

# ==============================================================================
# Project Information
# ==============================================================================

project = "Lightweight Charts Pro Python"
copyright = f"{datetime.now().year}, Lightweight Charts Pro Contributors"
author = "Lightweight Charts Pro Contributors"

# The full version, including alpha/beta/rc tags
release = "0.1.0"
version = "0.1.0"

# ==============================================================================
# General Configuration
# ==============================================================================

# Add any Sphinx extension module names here
extensions = [
    # Core Sphinx extensions
    "sphinx.ext.autodoc",  # Auto-generate docs from docstrings
    "sphinx.ext.napoleon",  # Support for Google-style docstrings
    "sphinx.ext.viewcode",  # Add links to source code
    "sphinx.ext.intersphinx",  # Link to other project docs
    "sphinx.ext.autosummary",  # Generate summary tables
    "sphinx.ext.coverage",  # Check documentation coverage
    # Third-party extensions
    "sphinx_rtd_theme",  # Read the Docs theme
    "sphinx_copybutton",  # Add copy button to code blocks
    "myst_parser",  # Markdown support
    # AutoAPI for automatic API documentation
    "autoapi.extension",
]

# ==============================================================================
# Napoleon Settings (Google-style docstrings)
# ==============================================================================

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = None

# ==============================================================================
# AutoAPI Configuration
# ==============================================================================

autoapi_dirs = ["../../lightweight_charts_pro"]
autoapi_type = "python"
autoapi_template_dir = "_templates/autoapi"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_ignore = [
    "*/tests/*",
    "*/test_*.py",
    "*conftest.py",
]
autoapi_add_toctree_entry = True
autoapi_keep_files = False

# ==============================================================================
# Autodoc Configuration
# ==============================================================================

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# ==============================================================================
# Intersphinx Configuration
# ==============================================================================

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# ==============================================================================
# Template and Source Configuration
# ==============================================================================

templates_path = ["_templates"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
master_doc = "index"
exclude_patterns = []
pygments_style = "sphinx"

# ==============================================================================
# HTML Output Configuration
# ==============================================================================

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = [
    "custom.css",
]

html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "style_nav_header_background": "#2980B9",
    # Toc options
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

html_context = {
    "display_github": True,
    "github_user": "your-username",  # Update with actual GitHub username
    "github_repo": "lightweight-charts-pro-python",
    "github_version": "main",
    "conf_py_path": "/docs/source/",
}

html_logo = None  # Add path to logo if available
html_favicon = None  # Add path to favicon if available

# ==============================================================================
# Additional Configuration
# ==============================================================================

# If true, `todo` and `todoList` produce output
todo_include_todos = True

# Output file base name for HTML help builder
htmlhelp_basename = "LightweightChartsProPythondoc"

# Copybutton configuration
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True

# MyST Parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_image",
]
