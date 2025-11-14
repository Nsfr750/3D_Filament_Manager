import os
import sys
import tkinter as tk
from tkinter import ttk
from wand.image import Image as WandImage
from wand.display import display as wand_display
import io
import base64
from src.version_info import APP_VERSION
from .lang import tr

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    path = os.path.join(base_path, relative_path)
    print(f"Trying to load resource: {path}")  # Debug
    return path

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
        # Try to get the base path for PyInstaller
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            
            return os.path.join(base_path, relative_path)
        
        logo_path = resource_path(os.path.join('src', 'assets', 'logo.png'))
        print(f"Logo path: {logo_path}")  # Debug
        print(f"File exists: {os.path.exists(logo_path)}")  # Debug
        if os.path.exists(logo_path):
            # Usa Wand per aprire e ridimensionare l'immagine
            with WandImage(filename=logo_path) as img:
                # Ridimensiona mantenendo le proporzioni
                img.resize(100, 100)
                
                # Converti in formato PNG in memoria
                img.format = 'png'
                img_data = img.make_blob()
                
                # Crea un oggetto PhotoImage da usare con Tkinter
                b64_data = base64.b64encode(img_data).decode('utf-8')
                logo_img = tk.PhotoImage(data=b64_data)
                
                # Crea e mostra l'immagine
                logo_label = ttk.Label(left_frame, image=logo_img)
                logo_label.image = logo_img  # Mantieni un riferimento
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
    
    # Add close button with red background and white text
    style = ttk.Style()
    style.configure('Red.TButton', 
                   background='red', 
                   foreground='white',
                   font=('TkDefaultFont', 10, 'bold'))
    
    close_button = ttk.Button(
        main_frame, 
        text=tr('close'), 
        command=dialog.destroy,
        style='Red.TButton',
        width=10
    )
    close_button.pack(pady=(10, 0), side=tk.RIGHT)
    
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
