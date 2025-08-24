"""
Theme configuration for the 3D Filament Manager application.

This module provides functions to apply different visual themes to the Tkinter-based
user interface, including light and dark modes. The theming is applied consistently
across all Tkinter and ttk widgets to ensure a cohesive look and feel.

The module uses the 'clam' theme as a base for dark mode and the default theme
for light mode, with custom styling for various widgets.
"""
import tkinter as tk
from tkinter import ttk

def apply_dark_theme(root):
    """
    Apply a dark theme to the application.
    
    This function configures all Tkinter and ttk widgets to use a dark color scheme
    with light text. The theme is designed to be easy on the eyes in low-light
    conditions.
    
    Args:
        root: The root Tkinter window to apply the theme to.
        
    The dark theme includes:
    - Dark background colors (#2b2b2b)
    - Light text colors (#ffffff)
    - Blue accent color (#1e88e5)
    - Styled buttons, entries, comboboxes, and treeview widgets
    - Custom styling for notebook tabs and other UI elements
    """
    # Background colors
    bg_color = "#2b2b2b"
    fg_color = "#ffffff"
    accent_color = "#1e88e5"
    
    # Configure the main window
    root.configure(bg=bg_color)
    
    # Create and configure ttk style
    style = ttk.Style(root)
    style.theme_use('clam')  # Use a theme that supports ttk styles
    
    # Configure the main frame style
    style.configure('.',
                  background=bg_color,
                  foreground=fg_color,
                  fieldbackground=bg_color,
                  selectbackground=accent_color,
                  selectforeground=fg_color,
                  insertcolor=fg_color,
                  troughcolor=bg_color,
                  highlightthickness=0,
                  borderwidth=0)
    
    # Configure TFrame
    style.configure('TFrame', background=bg_color)
    
    # Configure TLabel
    style.configure('TLabel',
                   background=bg_color,
                   foreground=fg_color)
    
    # Configure TButton
    style.configure('TButton',
                   background=bg_color,
                   foreground=fg_color,
                   borderwidth=1,
                   relief='flat')
    style.map('TButton',
             background=[('active', '#3b3b3b')],
             foreground=[('active', fg_color)])
    
    # Configure TEntry
    style.configure('TEntry',
                   fieldbackground='#3b3b3b',
                   foreground=fg_color,
                   insertcolor=fg_color)
    
    # Configure TCombobox
    style.configure('TCombobox',
                   fieldbackground='#3b3b3b',
                   background=bg_color,
                   foreground=fg_color,
                   arrowcolor=fg_color)
    style.map('TCombobox',
             fieldbackground=[('readonly', '#3b3b3b')],
             selectbackground=[('readonly', '!focus', bg_color)],
             selectforeground=[('readonly', '!focus', fg_color)])
    
    # Configure TNotebook
    style.configure('TNotebook', background=bg_color)
    style.configure('TNotebook.Tab',
                   background=bg_color,
                   foreground=fg_color,
                   padding=[10, 5])
    style.map('TNotebook.Tab',
             background=[('selected', '#1e88e5'), ('active', '#3b3b3b')],
             foreground=[('selected', fg_color), ('active', fg_color)])
    
    # Configure Treeview
    style.configure('Treeview',
                   background='#3b3b3b',
                   foreground=fg_color,
                   fieldbackground=bg_color,
                   borderwidth=0)
    style.map('Treeview',
             background=[('selected', accent_color)],
             foreground=[('selected', fg_color)])
    
    # Configure Treeview Heading
    style.configure('Treeview.Heading',
                   background='#3b3b3b',
                   foreground=fg_color,
                   relief='flat')
    style.map('Treeview.Heading',
             background=[('active', '#4b4b4b')])

def apply_light_theme(root):
    """
    Apply a light theme to the application.
    
    This function resets the application to use the default Tkinter/ttk theme,
    which provides a light color scheme with dark text. This is the default
    appearance of the application.
    
    Args:
        root: The root Tkinter window to apply the theme to.
        
    The light theme uses the system's default Tkinter theme with minimal
    custom styling to ensure a clean, native look across different platforms.
    """
    # Reset to default theme
    style = ttk.Style()
    style.theme_use('default')
    
    # Configure the main window
    root.configure(bg='#f0f0f0')
    
    # Configure ttk style
    style.configure('.',
                  background='#f0f0f0',
                  foreground='#000000',
                  fieldbackground='#ffffff',
                  selectbackground='#0078d7',
                  selectforeground='#ffffff',
                  insertcolor='#000000',
                  troughcolor='#e0e0e0',
                  highlightthickness=0,
                  borderwidth=0)
    
    # Reset specific widget styles to default
    for widget in ['TFrame', 'TLabel', 'TButton', 'TEntry', 'TCombobox', 'TNotebook', 'Treeview']:
        style.configure(widget, **style.configure('.'))
