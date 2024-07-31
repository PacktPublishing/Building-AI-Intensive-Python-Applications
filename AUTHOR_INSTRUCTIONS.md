# Instructions for Authors

These instructions are for the book authors to ensure consistently formatted and tested code across all chapters.

We will later delete this file before publishing the book.

## Adding your code examples

Create a chapter folder in the root of the repository, e.g. `Chapter 3`, and upload all your code in that folder. Add a `README.md` file in your chapter folder that gives an overview of the examples.

## Python Version

We'll aim for Python version `3.10.latest` (currently `3.10.14`). If any of the uploaded code examples uses `3.11` features, we can set the minimum version to `3.11.latest` instead.

### Testing code with different Python versions

If you want to test your code with a specific Python version, you can use [pyenv](https://github.com/pyenv/pyenv), a Python version manager that allows you to switch between different Python versions on your system.

Installation on Macs:

```
brew install pyenv
```

Then set up your shell environment with `pyenv`

For zsh:

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

Other shells:
See https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv

### Install and switch specific Python version

Once you have `pyenv` installed, you can install other python versions like so:

```
pyenv install 3.10.14
```

This installs 3.10.14 globally on your system.

If you want to use a version locally when changing into directory (creates a `.python_version` file):

```
pyenv local 3.10.14
```

## Third Party Dependencies

### Adding your dependencies

If your code depends on other Python packages, you need to add them to the top-level `requirements.txt` file with the following format:

```
<package>==<version>
```

For example:

```
tiktoken==0.7.0
```

If you have the package installed in your local environment and need to look up the version, you can use the `pip freeze` command, which will list all installed packages with their versions in the right format.

Only add the top-level packages you manually installed (using `pip install ...`), not their transient dependencies.

### Installing dependencies of all book chapters

To install all dependencies listed in the `requirements.txt` file, first create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Then install the dependencies:

```
pip install -r requirements.txt
```

To deactivate the virtual environment, run `deactivate`.

To delete the virtual environment, delete the local `venv` folder.

## Automatic Code Formatting and Linting

We will use [ruff](https://docs.astral.sh/ruff/) as the code formatter and linter.

### Installing and configuring ruff

`ruff` is already added to the `requirements.txt` file. If you have installed this (see previous section), you don't need to install it separately. Otherwise you can install `ruff` with

```
pip install ruff
```

The repo contains some formatting rules, configured in the `pyproject.toml` file with some basic rules enabled.

### Linting and formatting with ruff

#### From the command line

To lint code, run

```
ruff check
```

optionally with `--fix` argument for automatic fixing of issues.

To format code, run

```
ruff format
```

#### Editor Plugins

Many code editors have plugin support for the ruff formatter.

- For VSCode: https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff
- For PyCharm/JetBrains IDE: https://plugins.jetbrains.com/plugin/20574-ruff

You can configure your editor to automatically Format on Save, and to highlight linting errors (squiggly lines). Some of the linting problems are also fixable directly from the IDE (e.g. from the context menu).
