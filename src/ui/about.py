from tkinter import messagebox
from src.config import APP_VERSION
import tkinter as tk
from tkinter import ttk
from .version import get_version
from .lang import tr

def show_about_dialog(parent):
    """Displays the About dialog box."""
    about_message = (
        f"{tr('app_title')}\n\n"
        f"{tr('version')}: {APP_VERSION}\n"
        f"{tr('created_by')}: Nsfr750\n\n"
        f"{tr('about_description')}"
    )
    messagebox.showinfo(tr('about_dialog_title'), about_message, parent=parent)
