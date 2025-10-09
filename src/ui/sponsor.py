import tkinter as tk
from tkinter import ttk
import webbrowser
from .lang import tr

def show_sponsor_dialog(parent, dark_mode=False):
    """
    Display the Sponsor dialog box with options to support the project.
    
    This function creates a modal dialog that provides users with various ways to support
    the development of the application. It includes buttons that link to different
    sponsorship platforms (GitHub Sponsors, Patreon, PayPal, etc.). The dialog supports
    both light and dark themes.
    
    Args:
        parent: The parent Tkinter window that will own this dialog.
        dark_mode: If True, uses dark theme colors; otherwise uses light theme.
                  Defaults to False.
                  
    The dialog includes:
    - A thank you message for using the application
    - Buttons to support the project through various platforms
    - Each button opens the corresponding URL in the default web browser
    - A close button to dismiss the dialog
    
    The dialog is centered on screen and made modal to ensure users see the support
    options before continuing to use the application.
    """
    dialog = tk.Toplevel(parent)
    dialog.title(tr('sponsor'))
    
    # Apply theme
    bg_color = "#2b2b2b" if dark_mode else "#f0f0f0"
    fg_color = "#ffffff" if dark_mode else "#000000"
    button_bg = "#3b3b3b" if dark_mode else "#e0e0e0"
    
    dialog.configure(bg=bg_color)
    
    # Create main frame
    main_frame = ttk.Frame(dialog, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Configure style
    style = ttk.Style()
    style.configure('Sponsor.TLabel', background=bg_color, foreground=fg_color, font=('Arial', 10))
    style.configure('Sponsor.TButton', background=button_bg, foreground=fg_color, padding=5)
    
    # Create message
    message = (
        f"{tr('thank_you_for_using')} {tr('app_title')}\n\n"
        f"{tr('if_you_find_useful')}\n"
        f"{tr('your_contribution_helps')}"
    )
    
    # Add message label
    label = ttk.Label(
        main_frame, 
        text=message, 
        style='Sponsor.TLabel',
        wraplength=350, 
        justify=tk.CENTER
    )
    label.pack(pady=(0, 20))
    
    # Create button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack()
    
    # Configure button style
    button_style = 'Accent.TButton' if hasattr(ttk.Style(), 'configure') else 'TButton'
    
    # Define buttons
    buttons = [
        (tr('sponsor_on_github'), "https://github.com/sponsors/Nsfr750"),
        (tr('buy_me_a_coffee'), "https://paypal.me/3dmega")
    ]
    
    # Add buttons
    for text, url in buttons:
        btn = ttk.Button(
            button_frame, 
            text=text, 
            style=button_style,
            command=lambda u=url: webbrowser.open(u)
        )
        btn.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
    
    # Add close button
    close_button = ttk.Button(
        main_frame, 
        text=tr('close'), 
        style=button_style,
        command=dialog.destroy
    )
    close_button.pack(pady=(20, 0))
    
    # Center the dialog
    dialog.update_idletasks()
    width = 400
    height = 450
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    # Make the dialog modal
    dialog.transient(parent)
    dialog.grab_set()
    parent.wait_window(dialog)
