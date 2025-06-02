# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2025-06-02

### ⚙️ Miscellaneous Tasks

- *(release)* Switch to dynamic versioning and fix Makefile targets

## [0.1.1] - 2025-06-02

### 📚 Documentation

- Update changelog
- Update changelog

### ⚙️ Miscellaneous Tasks

- Trigger PyPI publish on tag push
- Use twine for PyPI upload on tag push

## [0.1.0] - 2025-06-02

### 🚀 Features

- *(core)* Modularize doctor checks and standardize diagnostic result format
- *(core)* Add modular checks and API compatibility with diagnostic output
- *(example)* Add basic hello world Azure Function (HTTP trigger)
- *(assets)* Add official logo assets for Azure Functions Doctor

### 🐛 Bug Fixes

- *(makefile)* Add cross-platform uv detection with pip fallback
- *(makefile)* Prevent NUL file creation on Windows when checking for uv
- *(cli)* Explicitly register diagnose command and fix CLI entrypoint

### 💼 Other

- Add hatch-based release and publish automation
- *(pyproject)* Configure tox environments in pyproject.toml
- *(makefile)* Add tox target for multi-version testing
- *(hatch)* Fix packaging path and add metadata for PyPI
- Add changelog generation and release process to Makefile and docs site

### 🚜 Refactor

- Rename package from azure_function_doctor to azure_functions_doctor
- Clean up tool configs and improve Makefile portability
- *(makefile)* Extract Windows clean commands into scripts
- Migrate CLI from Typer to Click and fix typecheck/lint issues
- *(cli)* Migrate CLI from Click to Typer
- *(cli)* Improve diagnose command with rich output and verbose option
- Modularize check logic and add handler registry
- Restructure check logic and improve test coverage
- *(core)* Restructure rule logic and output handling

### 📚 Documentation

- Update module name in documentation to azure_functions_doctor
- Update site name in mkdocs config to match new package name
- Update README to reflect renamed package path
- Add module-level and function docstrings
- *(changelog)* Add initial changelog with current features and setup history
- Add CLI usage, development guide, and diagnostics roadmap with mkdocs config
- Update diagnostic checklist with unified table and official references
- Update development and usage guides
- *(examples)* Add README for basic-hello Azure Function example
- *(readme)* Update main README with installation, usage, and example links
- Integrate API auto-documentation using mkdocstrings
- Add MkDocs config, Makefile target, and GitHub Pages deployment workflow
- Update project title and links for renamed repo
- Update CLI usage, main docs, and add CONTRIBUTING guide
- Update README and remove old logo assets
- Update README and add relocated logo_assets directory
- Enlarge logo size in README for better visibility
- Enlarge logo size in README for better visibility
- Enlarge logo in README and finalize CLI doc structure
- Update mkdocs.yml to reflect new repository name
- Add GitHub workflow, PyPI, coverage, license, and download badges to README
- Add release process guide and git-cliff config
- *(example)* Update README for basic-hello with Python model v2 instructions
- Add changelog for v0.1.0
- Update changelog
- Reflect latest commits in CHANGELOG.md

### 🎨 Styling

- *(pyproject)* Increase line length limit from 100 to 120 for Black and Ruff

### 🧪 Testing

- Migrate to pytest and update Makefile test command
- Convert test_doctor to pytest format
- *(cli)* Rewrite CLI tests using subprocess to verify full entrypoint

### ⚙️ Miscellaneous Tasks

- Initial project setup with CLI, Makefile, docs, and packaging
- Apply full initial setup with CLI, testing, and formatting tools
- Add pre-commit, coverage, and CI configuration
- Finalize dev environment setup and update documentation
- Add .editorconfig for consistent code style
- Update .editorconfig for markdown and YAML handling
- Update pyproject.toml for renamed package and mypy/ruff config
- Update hatch build path to match renamed package
- Update coverage config to match renamed package
- Fix missing venv setup for uv-based environment
- Fix missing venv setup in GitHub Actions with uv
- Update pyproject.toml configuration
- *(clean)* Remove .tox and htmlcov in Windows clean-all script
- *(release)* Add commitizen configuration and Makefile targets for patch/minor/major
- *(build)* Migrate to full Hatch-based workflow with unified Makefile and CI
- *(build)* Improve Hatch environment and pyproject.toml structure
- *(dev)* Pin tool versions and unify configuration
- *(build)* Organize pyproject.toml and include py.typed for PEP 561 support
- Fix artifact upload conflict by including Python version in name
- *(pyproject)* Configure docs environment and ensure Python 3.9 compatibility
- Update logo assets with new design
- Add GitHub Actions release workflow
- Fix project name to 'azure-functions-doctor' across all files
- Update PyPI classifiers to include Python 3.11 and 3.12

<!-- generated by git-cliff -->
