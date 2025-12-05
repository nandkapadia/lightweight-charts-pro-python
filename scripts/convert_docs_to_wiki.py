#!/usr/bin/env python3
"""Convert RST documentation to Markdown for GitHub Wiki.

This script converts the RST documentation files to Markdown format suitable
for GitHub Wiki. It processes the documentation source files and generates
corresponding wiki pages.

Usage:
    python scripts/convert_docs_to_wiki.py

"""

import os
import re
import shutil
from pathlib import Path


def rst_to_markdown(rst_content: str) -> str:
    """Convert basic RST syntax to Markdown.

    Args:
        rst_content (str): RST formatted content.

    Returns:
        str: Markdown formatted content.

    Note:
        This is a simplified converter. For production use, consider using
        pandoc or a dedicated RST to Markdown conversion library.

    """
    # Convert headers
    # RST: Title\n====== → MD: # Title
    content = re.sub(r"(.+)\n=+\n", r"# \1\n\n", rst_content)
    content = re.sub(r"(.+)\n-+\n", r"## \1\n\n", rst_content)
    content = re.sub(r"(.+)\n~+\n", r"### \1\n\n", rst_content)

    # Convert code blocks
    # RST: .. code-block:: python → MD: ```python
    content = re.sub(r"\.\. code-block:: (\w+)\n", r"```\1\n", content)

    # Convert inline code
    # RST: ``code`` → MD: `code`
    content = re.sub(r"``([^`]+)``", r"`\1`", content)

    # Convert bold
    # RST: **bold** → MD: **bold** (same)

    # Convert italic
    # RST: *italic* → MD: _italic_
    content = re.sub(r"\*([^*]+)\*", r"_\1_", content)

    # Convert links
    # RST: `text <url>`_ → MD: [text](url)
    content = re.sub(r"`([^<]+)\s*<([^>]+)>`_", r"[\1](\2)", content)

    # Convert bullet lists (ensure proper spacing)
    content = re.sub(r"^- ", r"* ", content, flags=re.MULTILINE)

    # Remove RST directives that don't translate well
    content = re.sub(r"\.\. \w+::\s*\n", "", content)

    # Clean up excessive newlines
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content


def process_docs_to_wiki():
    """Process documentation files and convert them to wiki pages.

    Reads RST files from docs/source and converts them to Markdown files
    in the wiki directory.

    """
    # Define paths
    docs_source = Path("docs/source")
    wiki_dir = Path("wiki")

    # Ensure wiki directory exists
    wiki_dir.mkdir(exist_ok=True)

    # Files to process
    doc_files = [
        ("getting-started.rst", "Getting-Started.md"),
        ("contributing.rst", "Contributing.md"),
        ("changelog.rst", "Changelog.md"),
    ]

    # Process each file
    for rst_file, md_file in doc_files:
        rst_path = docs_source / rst_file
        md_path = wiki_dir / md_file

        # Check if RST file exists
        if not rst_path.exists():
            print(f"Warning: {rst_path} not found, skipping...")
            continue

        # Read RST content
        with open(rst_path, "r", encoding="utf-8") as f:
            rst_content = f.read()

        # Convert to Markdown
        md_content = rst_to_markdown(rst_content)

        # Write Markdown file
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"Converted {rst_file} → {md_file}")

    # Create wiki home page
    create_wiki_home(wiki_dir)

    print("Wiki pages updated successfully!")


def create_wiki_home(wiki_dir: Path):
    """Create the wiki home page with navigation.

    Args:
        wiki_dir (Path): Path to the wiki directory.

    """
    home_content = """# Lightweight Charts Pro Python Wiki

Welcome to the Lightweight Charts Pro Python documentation wiki!

## Quick Navigation

* [Getting Started](Getting-Started) - Installation and basic usage
* [Contributing Guide](Contributing) - How to contribute to the project
* [Changelog](Changelog) - Version history and changes

## External Links

* [Full Documentation](https://lightweight-charts-pro-python.readthedocs.io/) - Complete documentation on Read the Docs
* [GitHub Repository](https://github.com/your-username/lightweight-charts-pro-python) - Source code and issues
* [PyPI Package](https://pypi.org/project/lightweight-charts-pro/) - Install via pip

## Quick Start

Install the package:

```bash
pip install lightweight-charts-pro
```

Create your first chart:

```python
from lightweight_charts_pro import LineSeries, LineData

# Create data
data = [
    LineData(time="2024-01-01", value=100.0),
    LineData(time="2024-01-02", value=105.0),
]

# Create series
series = LineSeries(data=data)
series.color = "#2196F3"
```

## Support

For questions and discussions, please use:

* [GitHub Discussions](https://github.com/your-username/lightweight-charts-pro-python/discussions) - Ask questions
* [GitHub Issues](https://github.com/your-username/lightweight-charts-pro-python/issues) - Report bugs

## License

This project is licensed under the MIT License.
"""

    home_path = wiki_dir / "Home.md"
    with open(home_path, "w", encoding="utf-8") as f:
        f.write(home_content)

    print("Created wiki Home page")


if __name__ == "__main__":
    process_docs_to_wiki()
