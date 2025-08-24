"""
User Interface package for the 3D Filament Manager.

This package contains all the UI components including the main window,
dialogs, and other user interface elements.
"""

# Import main UI components
from .main_window import MainWindow
from .about import show_about_dialog
from .help import show_help_dialog
from .sponsor import show_sponsor_dialog

__all__ = [
    'MainWindow',
    'show_about_dialog',
    'show_help_dialog',
    'show_sponsor_dialog'
]
