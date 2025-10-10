"""
Version information for 3D Filament Manager.

This module contains version constants and utility functions for version management.
Follows Semantic Versioning 2.0.0 specification.
"""

from typing import Dict, Any

# Current version information
APP_VERSION = "1.2.0"
VERSION_INFO: Dict[str, Any] = {
    "version": APP_VERSION,
    "major": 1,
    "minor": 2,
    "patch": 0,
    "release_date": "2025-08-25",
    "app_name": "3D Filament Manager",
    "description": "Desktop application for managing 3D printing filament inventory"
}

def get_version() -> str:
    """
    Get the current application version.

    Returns:
        str: The version string in format "major.minor.patch"
    """
    return APP_VERSION

def get_version_info() -> Dict[str, Any]:
    """
    Get detailed version information.

    Returns:
        Dict[str, Any]: Dictionary containing version details
    """
    return VERSION_INFO.copy()

def is_version_at_least(major: int, minor: int = 0, patch: int = 0) -> bool:
    """
    Check if current version is at least the specified version.

    Args:
        major: Major version to compare against
        minor: Minor version to compare against (default: 0)
        patch: Patch version to compare against (default: 0)

    Returns:
        bool: True if current version is at least the specified version
    """
    current_major, current_minor, current_patch = map(int, APP_VERSION.split('.'))

    if current_major > major:
        return True
    elif current_major == major:
        if current_minor > minor:
            return True
        elif current_minor == minor:
            return current_patch >= patch

    return False
