Contributing Guide
==================

Thank you for your interest in contributing to Lightweight Charts Pro Python!

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a virtual environment
4. Install development dependencies

.. code-block:: bash

   git clone https://github.com/your-username/lightweight-charts-pro-python.git
   cd lightweight-charts-pro-python
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"

Development Workflow
--------------------

Pre-commit Hooks
~~~~~~~~~~~~~~~~

We use pre-commit hooks to ensure code quality. Install them with:

.. code-block:: bash

   pre-commit install

This will run formatters and linters before each commit.

Code Style
~~~~~~~~~~

We follow these coding standards:

- **Line width**: Maximum 100 characters
- **Docstrings**: Google-style format
- **Type hints**: Required for all functions and methods
- **Import organization**: Standard → Third Party → Local

The pre-commit hooks will automatically format your code with:

- **isort**: Import sorting with float-to-top
- **autoflake**: Remove unused imports and variables
- **black**: Code formatting
- **ruff**: Fast Python linter

Running Tests
~~~~~~~~~~~~~

Run the complete test suite:

.. code-block:: bash

   pytest

Run tests with coverage:

.. code-block:: bash

   pytest --cov=lightweight_charts_pro --cov-report=html

Run specific test files:

.. code-block:: bash

   pytest tests/unit/data/test_line_data.py

Type Checking
~~~~~~~~~~~~~

Run mypy for type checking:

.. code-block:: bash

   mypy lightweight_charts_pro

Documentation
~~~~~~~~~~~~~

Build the documentation locally:

.. code-block:: bash

   cd docs
   make html

View the documentation:

.. code-block:: bash

   open build/html/index.html  # On macOS
   # On Linux: xdg-open build/html/index.html
   # On Windows: start build/html/index.html

Live documentation server with auto-reload:

.. code-block:: bash

   make livehtml

Contribution Guidelines
-----------------------

Code Contributions
~~~~~~~~~~~~~~~~~~

1. **Create a new branch** for your feature or bugfix:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Write tests** for your changes:

   - All new code must have test coverage
   - Aim for >90% code coverage
   - Test both success and error cases

3. **Update documentation**:

   - Add Google-style docstrings to all new functions/classes
   - Update user guide if adding new features
   - Add examples if applicable

4. **Commit your changes**:

   .. code-block:: bash

      git add .
      git commit -m "feat: add new feature"

   Follow conventional commit format:

   - ``feat:``: New feature
   - ``fix:``: Bug fix
   - ``docs:``: Documentation changes
   - ``test:``: Test additions/changes
   - ``refactor:``: Code refactoring
   - ``perf:``: Performance improvements
   - ``chore:``: Maintenance tasks

5. **Push and create a pull request**:

   .. code-block:: bash

      git push origin feature/your-feature-name

Documentation Contributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Documentation improvements are always welcome!

- Fix typos and grammar
- Improve clarity and examples
- Add missing documentation
- Create tutorials and guides

Pull Request Process
--------------------

1. **Update the CHANGELOG.md** with your changes
2. **Ensure all tests pass** and coverage is maintained
3. **Update documentation** as needed
4. **Request review** from maintainers
5. **Address review comments** promptly

Your PR will be reviewed for:

- Code quality and style
- Test coverage
- Documentation completeness
- Backwards compatibility

Code Review Checklist
---------------------

Before submitting, ensure:

.. code-block:: text

   ☑ All tests pass (pytest)
   ☑ Type checking passes (mypy)
   ☑ Code coverage >= 90%
   ☑ Pre-commit hooks pass
   ☑ Documentation is updated
   ☑ CHANGELOG.md is updated
   ☑ Commit messages follow convention
   ☑ No merge conflicts

Reporting Issues
----------------

Bug Reports
~~~~~~~~~~~

Include:

- Python version
- Package version
- Minimal code to reproduce the issue
- Expected vs actual behavior
- Full error traceback

Feature Requests
~~~~~~~~~~~~~~~~

Describe:

- The use case for the feature
- How it would work
- Example API if applicable
- Why existing solutions don't work

Questions and Discussions
~~~~~~~~~~~~~~~~~~~~~~~~~

For questions, use GitHub Discussions instead of issues.

Code of Conduct
---------------

Be respectful and constructive:

- Use welcoming and inclusive language
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

License
-------

By contributing, you agree that your contributions will be licensed under
the MIT License.
