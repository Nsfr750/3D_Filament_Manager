import tkinter as tk
from tkinter import ttk
from .lang import tr

def show_help_dialog(parent, dark_mode=False):
    """
    Display the Help dialog box with application usage instructions.
    
    This function creates a modal dialog window that provides users with information
    on how to use the application. The dialog supports both light and dark themes
    and presents help items in a bulleted list format.
    
    Args:
        parent: The parent Tkinter window that will own this dialog.
        dark_mode: If True, uses dark theme colors; otherwise uses light theme.
                  Defaults to False.
                  
    The help dialog includes instructions for:
    - Main interface navigation
    - Sorting filament lists
    - Searching for filaments
    - Selecting filaments
    - Adding new filaments
    - Editing existing filaments
    - Importing/exporting filament data
    
    The dialog is centered on screen and made modal to ensure users read the help
    information before continuing to use the application.
    """
    dialog = tk.Toplevel(parent)
    dialog.title(tr('help_dialog_title'))
    
    # Apply theme
    bg_color = "#2b2b2b" if dark_mode else "#f0f0f0"
    fg_color = "#ffffff" if dark_mode else "#000000"
    
    dialog.configure(bg=bg_color)
    
    # Create main frame
    main_frame = ttk.Frame(dialog, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Configure style
    style = ttk.Style()
    style.configure('Help.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 10))
    style.configure('Title.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 12, 'bold'))
    style.configure('Bullet.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 10))
    
    # Add title
    title_label = ttk.Label(main_frame, text=tr('help_title'), style='Title.TLabel')
    title_label.pack(pady=(0, 15))
    
    # Add help items
    help_items = [
        tr('help_main_list'),
        tr('help_sort'),
        tr('help_search'),
        tr('help_select'),
        tr('help_add'),
        tr('help_edit'),
        tr('help_import_export')
    ]
    
    for item in help_items:
        item_frame = ttk.Frame(main_frame)
        item_frame.pack(anchor='w', pady=2, fill=tk.X)
        
        # Add bullet point
        bullet = ttk.Label(item_frame, text="•", style='Bullet.TLabel')
        bullet.pack(side=tk.LEFT, padx=(0, 5))
        
        # Add item text
        label = ttk.Label(item_frame, text=item, style='Help.TLabel', wraplength=350, justify=tk.LEFT)
        label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Add close button
    close_button = ttk.Button(main_frame, text=tr('close'), command=dialog.destroy)
    close_button.pack(pady=(20, 0))
    
    # Center the dialog
    dialog.update_idletasks()
    width = 450
    height = 400
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    # Make the dialog modal
    dialog.transient(parent)
    dialog.grab_set()
    parent.wait_window(dialog)
