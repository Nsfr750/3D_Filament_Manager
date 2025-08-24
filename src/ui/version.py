"""
Version management for the 3D Filament Manager application.

This module handles version information following Semantic Versioning 2.0.0 (https://semver.org/).
It provides functions to retrieve version information in different formats and check version
compatibility.

Version numbers follow the MAJOR.MINOR.PATCH format:
- MAJOR: Incremented for incompatible API changes
- MINOR: Incremented for backward-compatible functionality
- PATCH: Incremented for backward-compatible bug fixes

An optional qualifier (alpha, beta, rc, etc.) can be added for pre-release versions.
"""
VERSION_MAJOR = 1
VERSION_MINOR = 1
VERSION_PATCH = 1

# Additional version qualifiers
VERSION_QUALIFIER = ''  # Could be 'alpha', 'beta', 'rc', or ''

def get_version() -> str:
    """
    Generate a full version string in MAJOR.MINOR.PATCH[-QUALIFIER] format.
    
    Examples:
        >>> get_version()
        '1.1.0'
        >>> # With qualifier
        '1.1.0-rc.1'
        
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
            
    Example:
        >>> get_version_info()
        {
            'major': 1,
            'minor': 1,
            'patch': 0,
            'qualifier': '',
            'full_version': '1.1.0'
        }
    """
    return {
        'major': VERSION_MAJOR,
        'minor': VERSION_MINOR,
        'patch': VERSION_PATCH,
        'qualifier': VERSION_QUALIFIER,
        'full_version': get_version()
    }

def check_version_compatibility(min_version: str) -> bool:
    """
    Check if the current version meets or exceeds a minimum required version.
    
    This is useful for checking plugin or data file compatibility with the current
    application version.
    
    Args:
        min_version: Minimum required version in 'MAJOR.MINOR.PATCH' format.
                    The qualifier is not considered in the comparison.
                    
    Returns:
        bool: True if current version is greater than or equal to min_version,
              False otherwise.
              
    Example:
        >>> check_version_compatibility('1.0.0')
        True  # If current version is 1.1.0
        >>> check_version_compatibility('2.0.0')
        False  # If current version is 1.1.0
    """
    current_parts = [VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH]
    min_parts = [int(part) for part in min_version.split('.')]
    
    for current, minimum in zip(current_parts, min_parts):
        if current > minimum:
            return True
        elif current < minimum:
            return False
    
    return True

# Expose version as a module-level attribute for easy access

def show_version(root: 'tk.Tk') -> None:
    """
    Display the current version in a modal message box.
    
    Args:
        root: The parent Tkinter window for the message box.
        
    This creates a simple dialog showing the application version to the user.
    The dialog is modal and must be dismissed before continuing to use the application.
    """
    from tkinter import messagebox
    messagebox.showinfo("Version", f"Current version: {get_version()}")

__version__ = get_version()
