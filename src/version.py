"""
Version information for the 3D Filament Manager application.

This module provides version information and related utilities.
"""

from src.ui.version import get_version, get_version_info

# Version information
APP_VERSION = get_version()
VERSION_INFO = get_version_info()

# Expose version components for easy access
VERSION_MAJOR = VERSION_INFO['major']
VERSION_MINOR = VERSION_INFO['minor']
VERSION_PATCH = VERSION_INFO['patch']
VERSION_QUALIFIER = VERSION_INFO['qualifier']
