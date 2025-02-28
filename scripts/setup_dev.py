#!/usr/bin/env python
"""
Development setup script for SiteJuicer.

This script helps automate the development environment setup by:
1. Creating a virtual environment if it doesn't exist
2. Installing the package in development mode
3. Installing development dependencies
4. Setting up pre-commit hooks

Usage:
    python scripts/setup_dev.py
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

# Ensure we're running from the project root
os.chdir(Path(__file__).parent.parent)

def create_venv():
    """Create a virtual environment if it doesn't exist."""
    venv_dir = "venv"
    
    if os.path.exists(venv_dir):
        print(f"Virtual environment already exists at {venv_dir}")
        return venv_dir
    
    print(f"Creating virtual environment at {venv_dir}...")
    subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
    print(f"Created virtual environment at {venv_dir}")
    
    return venv_dir

def get_venv_python(venv_dir):
    """Get the path to the Python executable in the virtual environment."""
    if platform.system() == "Windows":
        return os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        return os.path.join(venv_dir, "bin", "python")

def install_dev_dependencies(venv_python):
    """Install development dependencies."""
    print("Installing development dependencies...")
    
    # Install the package in development mode
    subprocess.run([venv_python, "-m", "pip", "install", "-e", "."], check=True)
    
    # Install development dependencies
    dev_packages = [
        "pytest",
        "pytest-cov",
        "black",
        "flake8",
        "isort",
        "mypy",
        "pre-commit",
        "build",
        "twine",
    ]
    
    subprocess.run([venv_python, "-m", "pip", "install"] + dev_packages, check=True)
    print("Installed development dependencies")

def setup_pre_commit(venv_python):
    """Set up pre-commit hooks."""
    if not os.path.exists(".pre-commit-config.yaml"):
        print("Creating .pre-commit-config.yaml...")
        with open(".pre-commit-config.yaml", "w") as f:
            f.write("""repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-docstrings]
""")
    
    print("Installing pre-commit hooks...")
    subprocess.run([venv_python, "-m", "pre_commit", "install"], check=True)
    print("Installed pre-commit hooks")

def main():
    """Run the development setup script."""
    print("Setting up development environment for SiteJuicer...")
    
    venv_dir = create_venv()
    venv_python = get_venv_python(venv_dir)
    
    install_dev_dependencies(venv_python)
    setup_pre_commit(venv_python)
    
    print("\nDevelopment environment setup complete!")
    print(f"\nTo activate the virtual environment, run:")
    if platform.system() == "Windows":
        print(f"    {venv_dir}\\Scripts\\activate")
    else:
        print(f"    source {venv_dir}/bin/activate")

if __name__ == "__main__":
    main() 