import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
from src.version_info import APP_VERSION
from .lang import tr

def show_about_dialog(parent, dark_mode=False):
    """
    Display the About dialog box with application information.
    
    This function creates a modal dialog window that shows information about the application,
    including version, author, and a brief description. The dialog supports both light and
    dark themes.
    
    Args:
        parent: The parent Tkinter window that will own this dialog.
        dark_mode: If True, uses dark theme colors; otherwise uses light theme.
                  Defaults to False.
                  
    The dialog includes:
    - Application title
    - Version information
    - Author information
    - Description text
    - A close button
    
    The dialog is centered on screen and made modal to prevent interaction with
    the parent window until closed.
    """
    dialog = tk.Toplevel(parent)
    dialog.title(tr('about_dialog_title'))
    
    # Apply theme
    bg_color = "#2b2b2b" if dark_mode else "#f0f0f0"
    fg_color = "#ffffff" if dark_mode else "#000000"
    
    dialog.configure(bg=bg_color)
    
    # Create main container frame
    container = ttk.Frame(dialog)
    container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Create left frame for logo
    left_frame = ttk.Frame(container)
    left_frame.pack(side=tk.LEFT, padx=(0, 20))
    
    # Load and display logo
    try:
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'assets', 'logo.png')
        if os.path.exists(logo_path):
            # Open and resize the image
            img = Image.open(logo_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            
            # Create label to display the logo
            logo_label = ttk.Label(left_frame, image=logo_img)
            logo_label.image = logo_img  # Keep a reference
            logo_label.pack(pady=10)
    except Exception as e:
        print(f"Error loading logo: {e}")
    
    # Create right frame for text content
    main_frame = ttk.Frame(container)
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Configure style
    style = ttk.Style()
    style.configure('About.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 10))
    style.configure('Title.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 12, 'bold'))
    
    # Add title
    title_label = ttk.Label(main_frame, text=tr('app_title'), style='Title.TLabel')
    title_label.pack(anchor='w', pady=(0, 10))
    
    # Add version info
    version_label = ttk.Label(main_frame, text=f"{tr('version')}: {APP_VERSION}", style='About.TLabel')
    version_label.pack(anchor='w', pady=2)
    
    # Add author info
    author_label = ttk.Label(main_frame, text=f"{tr('created_by')}: Nsfr750", style='About.TLabel')
    author_label.pack(anchor='w', pady=2)
    
    # Add description
    description_label = ttk.Label(
        main_frame, 
        text=tr('about_description'),
        style='About.TLabel',
        wraplength=350,
        justify=tk.LEFT
    )
    description_label.pack(pady=(10, 20), fill=tk.X)
    
    # Add close button
    close_button = ttk.Button(main_frame, text=tr('close'), command=dialog.destroy)
    close_button.pack(pady=(10, 0))
    
    # Center the dialog
    dialog.update_idletasks()
    width = 500  # Increased width to accommodate the logo
    height = 300  # Slightly increased height
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    dialog.minsize(width, height)  # Prevent the dialog from being resized too small
    
    # Make the dialog modal
    dialog.transient(parent)
    dialog.grab_set()
    parent.wait_window(dialog)
