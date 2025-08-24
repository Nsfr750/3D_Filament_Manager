"""
Version information for the 3D Filament Manager application.

This module provides version information in a way that avoids circular imports.
"""

# Version components
VERSION_MAJOR = 1
VERSION_MINOR = 1
VERSION_PATCH = 1
VERSION_QUALIFIER = ''

def get_version() -> str:
    """
    Generate a full version string in MAJOR.MINOR.PATCH[-QUALIFIER] format.
    
    Returns:
        str: Formatted version string with optional qualifier.
    """
    version_parts = [str(VERSION_MAJOR), str(VERSION_MINOR), str(VERSION_PATCH)]
    version_str = '.'.join(version_parts)
    
    if VERSION_QUALIFIER:
        version_str += f'-{VERSION_QUALIFIER}'
        
    return version_str

def get_version_info() -> dict:
    """
    Get detailed version information as a dictionary.
    
    Returns:
        dict: A dictionary containing version components with these keys:
            - major (int): Major version number
            - minor (int): Minor version number
            - patch (int): Patch version number
            - qualifier (str): Version qualifier if any, else empty string
            - full_version (str): Complete version string
    """
    return {
        'major': VERSION_MAJOR,
        'minor': VERSION_MINOR,
        'patch': VERSION_PATCH,
        'qualifier': VERSION_QUALIFIER,
        'full_version': get_version()
    }

# Full version string
APP_VERSION = get_version()

# Version info dictionary
VERSION_INFO = get_version_info()
