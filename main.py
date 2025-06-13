import tkinter as tk
import logging
from src.app import FilamentManagerApp
from src.ui.lang import tr, _load_lang
from src.utils.error_logger import ErrorLogger

def main():
    # Load language first
    _load_lang()

    # Setup error logging first
    ErrorLogger.setup_logging()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("filament_manager.log"),
            logging.StreamHandler()
        ]
    )

    # Create the main application window
    root = tk.Tk()
    root.title(tr('title'))
    
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
