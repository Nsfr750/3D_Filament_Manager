import os
import sys
import traceback
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any
import tkinter as tk
from tkinter import messagebox

class ErrorLogger:
    """Utility class for handling application errors and logging."""
    
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
    LOG_FILE = os.path.join(LOG_DIR, "error.log")
    
    @classmethod
    def setup_logging(cls) -> None:
        """Set up logging configuration."""
        try:
            os.makedirs(cls.LOG_DIR, exist_ok=True)
            
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(cls.LOG_FILE, encoding='utf-8'),
                    logging.StreamHandler(sys.stderr)
                ]
            )
            
            for handler in logging.root.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.setLevel(logging.DEBUG)
            
            def handle_exception(exc_type, exc_value, exc_traceback):
                if not issubclass(exc_type, KeyboardInterrupt):
                    logging.critical(
                        "Uncaught exception",
                        exc_info=(exc_type, exc_value, exc_traceback)
                    )
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
            
            sys.excepthook = handle_exception
            
        except Exception as e:
            print(f"Failed to set up logging: {str(e)}", file=sys.stderr)
    
    @classmethod
    def log_error(
        cls,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        level: str = "error"
    ) -> str:
        """Log an error with context information."""
        try:
            error_id = datetime.now().strftime("%Y%m%d%H%M%S")
            logger = logging.getLogger("ErrorLogger")
            
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "error_id": error_id,
                "error_type": error.__class__.__name__,
                "error_message": str(error),
                "traceback": traceback.format_exc(),
                "context": context or {}
            }
            
            log_message = f"Error {error_id}: {error.__class__.__name__}: {str(error)}"
            if context:
                log_message += f"\nContext: {json.dumps(context, indent=2, default=str)}"
            
            log_level = getattr(logging, level.upper(), logging.ERROR)
            logger.log(log_level, log_message, exc_info=True)
            
            error_file = os.path.join(cls.LOG_DIR, f"error_{error_id}.json")
            try:
                with open(error_file, 'w', encoding='utf-8') as f:
                    json.dump(log_data, f, indent=2, ensure_ascii=False, default=str)
            except Exception as e:
                logger.error(f"Failed to write detailed error log: {str(e)}")
            
            return error_id
        except Exception as e:
            logger = logging.getLogger("ErrorLogger")
            logger.critical(f"Failed to log error: {str(e)}")
            return "unknown"

    @classmethod
    def show_error_dialog(
        cls,
        parent,
        error: Exception,
        title: str = "Error",
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Show a user-friendly error dialog with error details."""
        error_id = cls.log_error(error, context, level="error")
        
        error_type = error.__class__.__name__
        error_message = str(error)
        
        # Format a user-friendly message
        if context and 'message' in context:
            details = context['message']
        else:
            details = f"{error_type}: {error_message}"
        
        full_message = f"{title}\n\n{details}\n\nError ID: {error_id}"
        
        # Show messagebox
        messagebox.showerror(title, full_message, parent=parent)

# Set up logging when module is imported
ErrorLogger.setup_logging()
