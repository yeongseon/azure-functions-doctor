# Detect Python command
ifeq ($(OS),Windows_NT)
    PYTHON := $(shell where python)
    VENV_PYTHON := .venv/Scripts/python.exe
    UV_EXISTS := $(shell cmd /c "where uv >nul 2>&1 && echo yes || echo no")
else
    PYTHON := $(shell which python3)
    VENV_PYTHON := .venv/bin/python
    UV_EXISTS := $(shell command -v uv >/dev/null 2>&1 && echo yes || echo no)
endif

# ------------------------------
# 🔧 Environment Setup
# ------------------------------
.PHONY: venv
venv:
ifeq ($(UV_EXISTS),yes)
	@uv venv
else
	@$(PYTHON) -m venv .venv
endif
	@echo "✅ Virtual environment created at .venv"

.PHONY: install
install:
ifeq ($(UV_EXISTS),yes)
	@uv pip install -e ".[dev]"
else
	@echo "⚠️ uv not found, using pip"
	@$(VENV_PYTHON) -m pip install --upgrade pip
	@$(VENV_PYTHON) -m pip install -e ".[dev]"
endif

.PHONY: reset
reset: clean-all venv install
	@echo "🔁 Project reset complete."

# ------------------------------
# 🧹 Code Quality
# ------------------------------
.PHONY: format
format:
	@$(VENV_PYTHON) -m ruff format src tests
	@$(VENV_PYTHON) -m black src tests

.PHONY: lint
lint:
	@$(VENV_PYTHON) -m ruff check src tests

.PHONY: typecheck
typecheck:
	@$(VENV_PYTHON) -m mypy src tests

.PHONY: check
check: format lint typecheck test
	@echo "✅ All checks passed!"

.PHONY: precommit
precommit:
	@$(VENV_PYTHON) -m pre_commit run --all-files

.PHONY: precommit-install
precommit-install:
	@$(VENV_PYTHON) -m pre_commit install

# ------------------------------
# 🧪 Testing & Coverage
# ------------------------------
.PHONY: test
test:
	@$(VENV_PYTHON) -m pytest tests

.PHONY: coverage
coverage:
	@$(VENV_PYTHON) -m coverage run -m pytest
	@$(VENV_PYTHON) -m coverage report
	@$(VENV_PYTHON) -m coverage html
	@echo "📂 Open htmlcov/index.html in your browser to view the coverage report"

# ------------------------------
# 🧪 Multi-Version Test with tox
# ------------------------------
.PHONY: tox
tox:
	@$(VENV_PYTHON) -m tox

# ------------------------------
# 📦 Build & Release
# ------------------------------
.PHONY: build
build:
	@$(VENV_PYTHON) -m build

.PHONY: release
release:
	@cz bump --changelog

.PHONY: release-patch
release-patch:
	@cz bump --increment patch --changelog

.PHONY: release-minor
release-minor:
	@cz bump --increment minor --changelog

.PHONY: release-major
release-major:
	@cz bump --increment major --changelog

.PHONY: publish
publish:
	@hatch publish

# ------------------------------
# 📚 Documentation
# ------------------------------
.PHONY: docs
docs:
	@$(VENV_PYTHON) -m mkdocs serve

# ------------------------------
# 🩺 Diagnostic
# ------------------------------
.PHONY: doctor
doctor:
	@echo "🔍 Python version:"
	@$(VENV_PYTHON) --version
	@echo "🔍 Installed packages:"
	@$(VENV_PYTHON) -m pip list
	@echo "🔍 Azure Function Core Tools version:"
	@func --version || echo "⚠️ func not found. Install with: npm i -g azure-functions-core-tools@4"
	@echo "🔍 Pre-commit hook installed:"
	@$(VENV_PYTHON) -c "import os; print('✅ Yes' if os.path.exists('.git/hooks/pre-commit') else '❌ No')"

# ------------------------------
# 🧹 Clean
# ------------------------------
.PHONY: clean
ifeq ($(OS),Windows_NT)
clean:
	@cmd /c scripts\clean-win.bat
else
clean:
	@rm -rf *.egg-info dist build __pycache__ .pytest_cache
endif

.PHONY: clean-all
ifeq ($(OS),Windows_NT)
clean-all: clean
	@cmd /c scripts\clean-all-win.bat
else
clean-all: clean
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete
	rm -rf .mypy_cache .ruff_cache .pytest_cache .coverage coverage.xml .DS_Store
	rm -rf .tox htmlcov
endif

# ------------------------------
# 🆘 Help
# ------------------------------
.PHONY: help
help:
	@echo "📖 Available commands:" && \
	grep -E '^\.PHONY: ' Makefile | cut -d ':' -f2 | xargs -n1 echo "  - make"
