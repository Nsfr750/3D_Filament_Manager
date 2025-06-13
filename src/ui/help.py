from tkinter import messagebox
from .lang import tr

def show_help_dialog(parent):
    """Displays the Help dialog box."""
    help_message = (
        f"{tr('help_title')}\n\n"
        f"- {tr('help_main_list')}\n"
        f"- {tr('help_sort')}\n"
        f"- {tr('help_search')}\n"
        f"- {tr('help_select')}\n"
        f"- {tr('help_add')}\n"
        f"- {tr('help_edit')}\n"
        f"- {tr('help_import_export')}"
    )
    messagebox.showinfo(tr('help_dialog_title'), help_message, parent=parent)
