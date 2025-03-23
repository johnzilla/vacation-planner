# Code Quality Setup Guide

This document provides guidance on setting up code quality tools for the Vacation Planner application, including linting, formatting, and pre-commit hooks.

## Python Code Quality Tools

### Flake8 (Linting)

Create a `.flake8` file in the `backend/` directory:

```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv,build,dist
ignore = E203,W503
per-file-ignores =
    __init__.py:F401
```

### Black (Formatting)

Create a `pyproject.toml` file in the `backend/` directory:

```toml
[tool.black]
line-length = 100
target-version = ['py39']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

### isort (Import Sorting)

Add to the `pyproject.toml` file:

```toml
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
```

### Installation

Add these tools to your development dependencies:

```bash
pip install flake8 black isort
```

Or add them to a `requirements-dev.txt` file:

```
flake8==6.1.0
black==23.9.1
isort==5.12.0
```

## JavaScript/Svelte Code Quality Tools

### ESLint (Linting)

Create a `.eslintrc.js` file in the `frontend/web/` directory:

```javascript
module.exports = {
  root: true,
  extends: [
    'eslint:recommended',
    'plugin:svelte/recommended'
  ],
  parserOptions: {
    sourceType: 'module',
    ecmaVersion: 2020,
    extraFileExtensions: ['.svelte']
  },
  env: {
    browser: true,
    es2017: true,
    node: true
  },
  rules: {
    // Custom rules
    'no-unused-vars': ['error', { 'argsIgnorePattern': '^_' }],
    'no-console': ['warn', { allow: ['warn', 'error'] }]
  },
  overrides: [
    {
      files: ['*.svelte'],
      parser: 'svelte-eslint-parser'
    }
  ]
};
```

### Prettier (Formatting)

Create a `.prettierrc` file in the `frontend/web/` directory:

```json
{
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2,
  "semi": true,
  "svelteSortOrder": "options-scripts-markup-styles",
  "svelteStrictMode": false,
  "svelteIndentScriptAndStyle": true,
  "plugins": ["prettier-plugin-svelte"]
}
```

### Installation

Add these tools to your development dependencies:

```bash
npm install --save-dev eslint eslint-plugin-svelte prettier prettier-plugin-svelte
```

Or add them to your `package.json`:

```json
"devDependencies": {
  "eslint": "^8.51.0",
  "eslint-plugin-svelte": "^2.34.0",
  "prettier": "^3.0.3",
  "prettier-plugin-svelte": "^3.0.3"
}
```

## Editor Configuration

Create an `.editorconfig` file in the root directory:

```ini
# EditorConfig is awesome: https://EditorConfig.org

# top-most EditorConfig file
root = true

# Unix-style newlines with a newline ending every file
[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true

# Python files
[*.py]
indent_style = space
indent_size = 4

# JavaScript, JSON, and Svelte files
[*.{js,json,svelte}]
indent_style = space
indent_size = 2

# Markdown files
[*.md]
trim_trailing_whitespace = false
```

## Pre-commit Hooks

Create a `.pre-commit-config.yaml` file in the root directory:

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

# Python hooks
-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
        files: "backend/.*\\.py$"

-   repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
    -   id: black
        files: "backend/.*\\.py$"

-   repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
    -   id: flake8
        files: "backend/.*\\.py$"

# JavaScript/Svelte hooks
-   repo: local
    hooks:
    -   id: eslint
        name: eslint
        entry: bash -c 'cd frontend/web && npx eslint'
        language: system
        files: "frontend/web/.*\\.(js|svelte)$"
        pass_filenames: true

    -   id: prettier
        name: prettier
        entry: bash -c 'cd frontend/web && npx prettier --write'
        language: system
        files: "frontend/web/.*\\.(js|json|svelte)$"
        pass_filenames: true
```

### Installation

Install pre-commit:

```bash
pip install pre-commit
```

Initialize pre-commit:

```bash
pre-commit install
```

## VS Code Integration

Create a `.vscode/settings.json` file in the root directory:

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[svelte]": {
    "editor.defaultFormatter": "svelte.svelte-vscode"
  },
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "eslint.validate": ["javascript", "svelte"]
}
```

## Usage

### Manual Usage

Run these commands to manually check and format your code:

#### Python (Backend)

```bash
# Check code style with flake8
cd backend
flake8 .

# Format code with black
black .

# Sort imports with isort
isort .
```

#### JavaScript/Svelte (Frontend)

```bash
# Check code style with eslint
cd frontend/web
npx eslint .

# Format code with prettier
npx prettier --write .
```

### Automated Usage

With pre-commit hooks installed, these checks will run automatically when you commit code.

## CI Integration

Add these checks to your CI pipeline to ensure code quality on every pull request. Example GitHub Actions workflow:

```yaml
name: Code Quality

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 black isort

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install Node.js dependencies
      run: |
        cd frontend/web
        npm install

    - name: Lint Python code
      run: |
        cd backend
        flake8 .
        black --check .
        isort --check .

    - name: Lint JavaScript/Svelte code
      run: |
        cd frontend/web
        npx eslint .
        npx prettier --check .
```

## Best Practices

1. **Consistent Coding Style**: Follow the established style guides for Python (PEP 8) and JavaScript.

2. **Regular Linting**: Run linters regularly during development, not just at commit time.

3. **Automated Formatting**: Use automated formatters to maintain consistent code style without manual effort.

4. **Documentation**: Document code style decisions and exceptions in the project documentation.

5. **Gradual Adoption**: If applying to an existing codebase, consider gradual adoption of style rules.
