#!/usr/bin/env python
"""
Release script for SiteJuicer.

This script helps automate the release process by:
1. Updating the version number in __init__.py
2. Updating the CHANGELOG.md with the release date
3. Creating a git tag for the release
4. Building the distribution packages
5. Uploading to PyPI (if confirmed)

Usage:
    python scripts/release.py [--dry-run]
"""

import argparse
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

# Ensure we're running from the project root
os.chdir(Path(__file__).parent.parent)

def get_current_version():
    """Extract the current version from __init__.py."""
    with open("__init__.py", "r") as f:
        content = f.read()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        sys.exit("Could not find version string in __init__.py")
    return match.group(1)

def update_version(new_version):
    """Update the version in __init__.py."""
    with open("__init__.py", "r") as f:
        content = f.read()
    
    content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{new_version}"',
        content
    )
    
    with open("__init__.py", "w") as f:
        f.write(content)
    
    print(f"Updated version in __init__.py to {new_version}")

def update_changelog(version):
    """Update the CHANGELOG.md with the release date."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    with open("CHANGELOG.md", "r") as f:
        content = f.read()
    
    # Replace the unreleased header with the version and date
    content = re.sub(
        rf"## \[{version}\] - Unreleased",
        f"## [{version}] - {today}",
        content
    )
    
    with open("CHANGELOG.md", "w") as f:
        f.write(content)
    
    print(f"Updated CHANGELOG.md with release date {today}")

def create_git_tag(version, dry_run=False):
    """Create a git tag for the release."""
    tag = f"v{version}"
    
    if dry_run:
        print(f"Would create git tag: {tag}")
        return
    
    subprocess.run(["git", "add", "__init__.py", "CHANGELOG.md"], check=True)
    subprocess.run(["git", "commit", "-m", f"Bump version to {version}"], check=True)
    subprocess.run(["git", "tag", "-a", tag, "-m", f"Release {version}"], check=True)
    
    print(f"Created git tag: {tag}")
    print("Remember to push with: git push && git push --tags")

def build_package(dry_run=False):
    """Build the distribution packages."""
    if dry_run:
        print("Would build distribution packages")
        return
    
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "build", "twine"], check=True)
    subprocess.run(["python", "-m", "build"], check=True)
    
    print("Built distribution packages")

def upload_to_pypi(dry_run=False):
    """Upload the distribution packages to PyPI."""
    if dry_run:
        print("Would upload to PyPI")
        return
    
    confirm = input("Upload to PyPI? [y/N] ").lower() == "y"
    if confirm:
        subprocess.run(["python", "-m", "twine", "upload", "dist/*"], check=True)
        print("Uploaded to PyPI")
    else:
        print("Skipped uploading to PyPI")

def main():
    parser = argparse.ArgumentParser(description="Release script for SiteJuicer")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes")
    args = parser.parse_args()
    
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    
    # Prompt for new version
    new_version = input(f"Enter new version (current: {current_version}): ")
    if not new_version:
        sys.exit("No version specified")
    
    # Confirm
    if not args.dry_run:
        confirm = input(f"Release version {new_version}? [y/N] ").lower() == "y"
        if not confirm:
            sys.exit("Release cancelled")
    
    # Update version and changelog
    update_version(new_version)
    update_changelog(new_version)
    
    # Create git tag
    create_git_tag(new_version, args.dry_run)
    
    # Build package
    build_package(args.dry_run)
    
    # Upload to PyPI
    upload_to_pypi(args.dry_run)
    
    print("Release process completed!")

if __name__ == "__main__":
    main() 