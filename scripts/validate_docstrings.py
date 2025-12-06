#!/usr/bin/env python3
"""Validate that all docstrings follow Google style and have required sections.

This script checks that:
- All public functions/methods have docstrings
- Docstrings follow Google style format
- Functions with parameters have Args section
- Functions with return values have Returns section
- Classes have proper class-level docstrings

Usage:
    python scripts/validate_docstrings.py file1.py file2.py ...
    pre-commit hook: automatically validates changed files

Exit codes:
    0: All docstrings valid
    1: Validation errors found

"""

import ast
import re
import sys
from pathlib import Path


class DocstringValidator:
    """Validator for Google-style docstrings.

    This class parses Python files and validates that all public functions,
    methods, and classes have proper Google-style docstrings with required
    sections.

    Attributes:
        errors (List[str]): List of validation error messages.
        warnings (List[str]): List of validation warning messages.

    """

    def __init__(self):
        """Initialize the docstring validator."""
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate_file(self, filepath: Path) -> bool:
        """Validate all docstrings in a Python file.

        Args:
            filepath (Path): Path to the Python file to validate.

        Returns:
            bool: True if all validations pass, False otherwise.

        """
        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            # Parse the Python file
            tree = ast.parse(content, filename=str(filepath))

            # Visit all nodes
            self._visit_node(tree, filepath)

            return len(self.errors) == 0

        except SyntaxError as e:
            self.errors.append(f"{filepath}: Syntax error - {e}")
            return False

    def _visit_node(self, node: ast.AST, filepath: Path, parent_name: str = ""):
        """Recursively visit AST nodes and validate docstrings.

        Args:
            node (ast.AST): AST node to visit.
            filepath (Path): Path to the source file.
            parent_name (str): Name of parent class/function.

        """
        # Check classes
        if isinstance(node, ast.ClassDef):
            self._validate_class(node, filepath, parent_name)

        # Check functions
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self._validate_function(node, filepath, parent_name)

        # Recursively visit child nodes
        for child in ast.iter_child_nodes(node):
            child_parent = (
                f"{parent_name}.{node.name}" if hasattr(node, "name") else parent_name
            )
            self._visit_node(child, filepath, child_parent)

    def _validate_class(self, node: ast.ClassDef, filepath: Path, parent_name: str):
        """Validate a class docstring.

        Args:
            node (ast.ClassDef): Class node to validate.
            filepath (Path): Path to the source file.
            parent_name (str): Name of parent scope.

        """
        # Skip private classes
        if node.name.startswith("_"):
            return

        full_name = f"{parent_name}.{node.name}" if parent_name else node.name

        # Check for docstring
        docstring = ast.get_docstring(node)
        if not docstring:
            self.errors.append(
                f"{filepath}:{node.lineno}: Class {full_name} missing docstring"
            )
            return

        # Validate docstring format
        self._validate_docstring_format(
            docstring, full_name, filepath, node.lineno, is_class=True
        )

    def _validate_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        filepath: Path,
        parent_name: str,
    ):
        """Validate a function/method docstring.

        Args:
            node (ast.FunctionDef | ast.AsyncFunctionDef): Function node to validate.
            filepath (Path): Path to the source file.
            parent_name (str): Name of parent class.

        """
        # Skip private functions and special methods (except __init__)
        if node.name.startswith("_") and node.name not in ("__init__", "__post_init__"):
            return

        full_name = f"{parent_name}.{node.name}" if parent_name else node.name

        # Check for docstring
        docstring = ast.get_docstring(node)
        if not docstring:
            self.errors.append(
                f"{filepath}:{node.lineno}: Function {full_name} missing docstring"
            )
            return

        # Get function arguments (excluding 'self' and 'cls')
        args = [arg.arg for arg in node.args.args if arg.arg not in ("self", "cls")]

        # Check if function has return statement
        has_return = self._has_return_statement(node)

        # Validate docstring format
        self._validate_docstring_format(
            docstring,
            full_name,
            filepath,
            node.lineno,
            args=args,
            has_return=has_return,
        )

    def _validate_docstring_format(
        self,
        docstring: str,
        name: str,
        filepath: Path,
        lineno: int,
        is_class: bool = False,
        args: list[str] = None,
        has_return: bool = False,
    ):
        """Validate Google-style docstring format.

        Args:
            docstring (str): Docstring to validate.
            name (str): Name of the function/class.
            filepath (Path): Path to the source file.
            lineno (int): Line number of the definition.
            is_class (bool): Whether validating a class docstring.
            args (List[str] | None): List of function argument names.
            has_return (bool): Whether function has return statement.

        """
        args = args or []

        # Check for summary line
        lines = docstring.strip().split("\n")
        if not lines or not lines[0].strip():
            self.errors.append(
                f"{filepath}:{lineno}: {name} - Docstring must start with summary line"
            )

        # Check for Args section if function has arguments
        if args and not is_class:
            if not re.search(r"^\s*Args:\s*$", docstring, re.MULTILINE):
                self.errors.append(
                    f"{filepath}:{lineno}: {name} - Missing 'Args:' section for function with arguments"
                )
            else:
                # Validate that all args are documented
                for arg in args:
                    if not re.search(rf"^\s*{arg}\s*\(.*?\):", docstring, re.MULTILINE):
                        self.warnings.append(
                            f"{filepath}:{lineno}: {name} - Argument '{arg}' not documented in Args section"
                        )

        # Check for Returns section if function returns something
        if has_return and not is_class:
            if not re.search(r"^\s*Returns:\s*$", docstring, re.MULTILINE):
                self.warnings.append(
                    f"{filepath}:{lineno}: {name} - Missing 'Returns:' section for function with return statement"
                )

        # Check for Attributes section in classes
        if is_class:
            # This is optional but good practice
            if not re.search(r"^\s*Attributes:\s*$", docstring, re.MULTILINE):
                # Not an error, just informational
                pass

    def _has_return_statement(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> bool:
        """Check if a function has a return statement with a value.

        Args:
            node (ast.FunctionDef | ast.AsyncFunctionDef): Function node to check.

        Returns:
            bool: True if function has return statement with value.

        """
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value is not None:
                return True
        return False

    def print_results(self):
        """Print validation results to stdout."""
        if self.errors:
            print("\n❌ Docstring Validation Errors:")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print("\n⚠️  Docstring Validation Warnings:")
            for warning in self.warnings:
                print(f"  {warning}")

        if not self.errors and not self.warnings:
            print("✅ All docstrings validated successfully!")


def main():
    """Validate docstrings in validation script.

    Returns:
        int: Exit code (0 for success, 1 for errors).

    """
    if len(sys.argv) < 2:
        print("Usage: python validate_docstrings.py file1.py file2.py ...")
        return 1

    validator = DocstringValidator()

    # Validate each file
    all_valid = True
    for filepath_str in sys.argv[1:]:
        filepath = Path(filepath_str)

        # Skip test files
        if "test_" in filepath.name or filepath.parts and "tests" in filepath.parts:
            continue

        if not filepath.exists():
            print(f"Warning: {filepath} does not exist")
            continue

        if not validator.validate_file(filepath):
            all_valid = False

    # Print results
    validator.print_results()

    # Return exit code
    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
