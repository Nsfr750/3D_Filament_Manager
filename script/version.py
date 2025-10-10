"""
Version management for 3D Filament Manager.

This module provides version information and utilities following Semantic Versioning 2.0.0.
Used for build processes, deployment, and version tracking.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

# Version constants following Semantic Versioning 2.0.0
__version__ = "1.2.0"
__version_info__ = {
    "version": __version__,
    "major": 1,
    "minor": 2,
    "patch": 0,
    "prerelease": None,
    "build": None,
    "release_date": "2025-08-25"
}

def get_version() -> str:
    """
    Get the current version string.

    Returns:
        str: Version in format "major.minor.patch"
    """
    return __version__

def get_version_info() -> Dict[str, Any]:
    """
    Get detailed version information.

    Returns:
        Dict[str, Any]: Complete version information dictionary
    """
    return __version_info__.copy()

def get_semantic_version() -> str:
    """
    Get the semantic version string including prerelease and build metadata.

    Returns:
        str: Full semantic version string
    """
    version_parts = [__version__]

    if __version_info__["prerelease"]:
        version_parts.append(f"-{__version_info__['prerelease']}")

    if __version_info__["build"]:
        version_parts.append(f"+{__version_info__['build']}")

    return "".join(version_parts)

def is_compatible_version(other_version: str) -> bool:
    """
    Check if another version is compatible with current version.

    Args:
        other_version: Version string to check compatibility with

    Returns:
        bool: True if versions are compatible (same major version)
    """
    try:
        current_major = __version_info__["major"]
        other_major = int(other_version.split('.')[0])
        return current_major == other_major
    except (ValueError, IndexError):
        return False

def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns:
        Path: Absolute path to project root
    """
    # Assuming this file is in script/version.py
    current_path = Path(__file__).resolve()
    return current_path.parent.parent

def get_version_file_path() -> Path:
    """
    Get the path to the version file.

    Returns:
        Path: Path to this version file
    """
    return Path(__file__).resolve()

# Export main version constants for easy access
VERSION = __version__
VERSION_INFO = __version_info__
