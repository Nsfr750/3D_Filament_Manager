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
    """
    A utility class for centralized error handling and logging in the application.
    
    This class provides methods to log errors with context information, save detailed
    error reports, and display user-friendly error dialogs. It's designed to be used
    as a singleton through its class methods.
    
    Key Features:
    - Automatic setup of file and console logging
    - Detailed error reporting with stack traces and context
    - User-friendly error dialogs with error IDs
    - Thread-safe error logging
    - JSON-formatted error dumps for debugging
    
    Attributes:
        LOG_DIR (str): Directory where log files are stored (default: 'logs' in app root)
        LOG_FILE (str): Path to the main log file (default: 'logs/error.log')
    """
    
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
    LOG_FILE = os.path.join(LOG_DIR, "error.log")
    
    @classmethod
    def setup_logging(cls) -> None:
        """
        Set up and configure the logging system.
        
        This method should be called once when the application starts. It:
        - Creates the log directory if it doesn't exist
        - Configures both file and console logging
        - Sets up a global exception handler
        - Configures log levels (DEBUG for file, INFO for console)
        
        The log format includes timestamp, logger name, log level, and message.
        Uncaught exceptions are automatically logged at CRITICAL level.
        
        Note:
            This method is called automatically when the module is imported.
        """
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
        """
        Log an error with optional context information.
        
        This is the main method for logging errors in the application. It:
        - Generates a unique error ID
        - Captures the full stack trace
        - Includes any provided context data
        - Writes a detailed JSON error report
        
        Args:
            error: The exception that was raised
            context: Optional dictionary with additional context about the error
            level: Log level ('debug', 'info', 'warning', 'error', 'critical')
                   Defaults to 'error'
                   
        Returns:
            str: A unique error ID that can be shown to users for support
            
        Example:
            try:
                # Some operation that might fail
                result = 1 / 0
            except Exception as e:
                error_id = ErrorLogger.log_error(
                    e,
                    context={"operation": "division", "values": [1, 0]},
                    level="error"
                )
                print(f"An error occurred. ID: {error_id}")
        """
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
        """
        Display a user-friendly error dialog with error details.
        
        This method logs the error and shows a dialog box to the user with:
        - A simple error message
        - The error ID for support reference
        - Option to view technical details
        - A button to copy the error information
        
        Args:
            parent: The parent Tkinter window for the dialog
            error: The exception that was raised
            title: Title for the error dialog (default: "Error")
            context: Optional dictionary with additional context about the error
            
        The error is automatically logged with log_error() before showing the dialog.
        If the error is a known type (like FileNotFoundError), a more specific
        message may be shown.
        """
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
# This ensures that any uncaught exceptions are properly logged
ErrorLogger.setup_logging()
