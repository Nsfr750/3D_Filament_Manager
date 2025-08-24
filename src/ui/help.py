import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
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
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
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
    style.configure('Help.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 10))
    style.configure('Title.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 14, 'bold'))
    style.configure('Bullet.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 10))
    
    # Add title
    title_label = ttk.Label(main_frame, text=tr('help_title'), style='Title.TLabel')
    title_label.pack(anchor='w', pady=(0, 15))
    
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
    
    # Create a frame for the scrollable content
    canvas = tk.Canvas(main_frame, bg=bg_color, highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    for item in help_items:
        item_frame = ttk.Frame(scrollable_frame)
        item_frame.pack(anchor='w', pady=4, fill=tk.X, padx=(0, 10))
        
        # Add bullet point with a larger, colored dot
        bullet_canvas = tk.Canvas(item_frame, width=15, height=15, bg=bg_color, highlightthickness=0)
        bullet_canvas.pack(side=tk.LEFT, padx=(0, 8))
        bullet_canvas.create_oval(3, 3, 12, 12, fill="#4285F4", outline="")  # Google Blue
        
        # Add item text with better styling
        label = ttk.Label(
            item_frame, 
            text=item, 
            style='Help.TLabel', 
            wraplength=350, 
            justify=tk.LEFT
        )
        label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Add close button
    close_button = ttk.Button(main_frame, text=tr('close'), command=dialog.destroy)
    close_button.pack(pady=(20, 0))
    
    # Center the dialog
    dialog.update_idletasks()
    width = 600  # Increased width to accommodate the logo and better text layout
    height = 500  # Increased height for better content visibility
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    dialog.minsize(width, 400)  # Prevent the dialog from being resized too small
    
    # Make the dialog modal
    dialog.transient(parent)
    dialog.grab_set()
    parent.wait_window(dialog)
