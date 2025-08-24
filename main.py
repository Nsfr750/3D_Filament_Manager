import tkinter as tk
import os
import logging
from src.app import FilamentManagerApp
from src.ui.lang import tr, _load_lang
from src.utils.error_logger import ErrorLogger

def main():
    # Load language first
    _load_lang()

    # Setup error logging first
    ErrorLogger.setup_logging()

    # Create the main application window
    root = tk.Tk()
    root.title(tr('title'))
    
    # Set application icon
    try:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo.png')
        if os.path.exists(icon_path):
            icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon)
    except Exception as e:
        logging.warning(f"Could not load application icon: {e}")
    
    # Center the window
    root.update_idletasks()
    width = 800
    height = 600
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Instantiate and run the application
    app = FilamentManagerApp(root)
    app.run()

if __name__ == "__main__":
    main()
