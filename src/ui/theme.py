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

def get_theme():
    """
    Get the current theme settings.
    
    Returns:
        dict: A dictionary containing the current theme settings.
    """
    return {
        'dark_mode': {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'accent': '#1e88e5',
            'entry_bg': '#3c3c3c',
            'button_bg': '#3c3c3c',
            'button_fg': '#ffffff',
            'button_active_bg': '#1e88e5',
            'button_active_fg': '#ffffff',
            'tree_bg': '#3c3c3c',
            'tree_fg': '#ffffff',
            'tree_selected_bg': '#1e88e5',
            'tree_selected_fg': '#ffffff',
            'tree_heading_bg': '#2b2b2b',
            'tree_heading_fg': '#ffffff',
            'tree_heading_active_bg': '#1e88e5',
            'tree_heading_active_fg': '#ffffff',
            'tab_bg': '#2b2b2b',
            'tab_fg': '#ffffff',
            'tab_selected_bg': '#1e88e5',
            'tab_selected_fg': '#ffffff',
            'tab_active_bg': '#1e88e5',
            'tab_active_fg': '#ffffff',
            'tab_active_fill': '#1e88e5',
        },
        'light_mode': {
            'bg': '#f0f0f0',
            'fg': '#000000',
            'accent': '#0078d7',
            'entry_bg': '#ffffff',
            'button_bg': '#f0f0f0',
            'button_fg': '#000000',
            'button_active_bg': '#e5f3ff',
            'button_active_fg': '#000000',
            'tree_bg': '#ffffff',
            'tree_fg': '#000000',
            'tree_selected_bg': '#0078d7',
            'tree_selected_fg': '#ffffff',
            'tree_heading_bg': '#f0f0f0',
            'tree_heading_fg': '#000000',
            'tree_heading_active_bg': '#e0e0e0',
            'tree_heading_active_fg': '#000000',
            'tab_bg': '#f0f0f0',
            'tab_fg': '#000000',
            'tab_selected_bg': '#ffffff',
            'tab_selected_fg': '#000000',
            'tab_active_bg': '#e0e0e0',
            'tab_active_fg': '#000000',
            'tab_active_fill': '#ffffff',
        }
    }

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
    # Get theme settings
    theme = get_theme()['light_mode']
    
    # Reset to default theme
    style = ttk.Style(root)
    style.theme_use('default')
    
    # Apply theme to root window
    root.configure(bg=theme['bg'])
    
    # Configure base styles
    style.configure('.',
                  background=theme['bg'],
                  foreground=theme['fg'],
                  fieldbackground=theme['entry_bg'],
                  selectbackground=theme['accent'],
                  selectforeground=theme['tree_selected_fg'],
                  insertcolor=theme['fg'])
    
    # Configure specific widgets
    style.configure('TButton',
                  background=theme['button_bg'],
                  foreground=theme['button_fg'])
    
    style.map('TButton',
             background=[('active', theme['button_active_bg'])],
             foreground=[('active', theme['button_active_fg'])])
    
    style.map('TEntry',
             fieldbackground=[('readonly', theme['bg'])])
    
    style.map('TCombobox',
             fieldbackground=[('readonly', theme['entry_bg'])],
             selectbackground=[('readonly', theme['accent'])],
             selectforeground=[('readonly', theme['tree_selected_fg'])])
    
    style.configure('Treeview',
                  background=theme['tree_bg'],
                  fieldbackground=theme['tree_bg'],
                  foreground=theme['tree_fg'])
    
    style.map('Treeview',
             background=[('selected', theme['tree_selected_bg'])],
             foreground=[('selected', theme['tree_selected_fg'])])
    
    style.configure('Treeview.Heading',
                  background=theme['tree_heading_bg'],
                  foreground=theme['tree_heading_fg'],
                  relief='flat')
    
    style.map('Treeview.Heading',
             background=[('active', theme['tree_heading_active_bg'])],
             foreground=[('active', theme['tree_heading_active_fg'])])
    
    style.configure('TNotebook',
                  background=theme['bg'])
    
    style.configure('TNotebook.Tab',
                  background=theme['tab_bg'],
                  foreground=theme['tab_fg'],
                  padding=[10, 5])
    
    style.map('TNotebook.Tab',
             background=[('selected', theme['tab_selected_bg']),
                       ('active', theme['tab_active_bg'])],
             foreground=[('selected', theme['tab_selected_fg']),
                       ('active', theme['tab_active_fg'])],
             expand=[('selected', [1, 1, 1, 0])])
