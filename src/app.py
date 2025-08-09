import tkinter as tk
from tkinter import messagebox, filedialog
import logging
import json
import os

from src.data.filament_manager import FilamentManager
from src.ui.main_window import MainWindow
from src.ui.dialogs import AddEditDialog
from src.config import APP_VERSION
from src.ui.about import show_about_dialog
from src.ui.help import show_help_dialog
from src.ui.sponsor import show_sponsor_dialog
from src.ui.lang import set_language, tr
from src.ui.theme import apply_dark_theme, apply_light_theme

class FilamentManagerApp:
    """Main application controller."""

    def __init__(self, root):
        self.root = root
        self.logger = logging.getLogger(__name__)
        
        # Load settings
        self.settings_file = 'settings.json'
        self.settings = self._load_settings()
        
        # Apply theme
        self.dark_mode = self.settings.get('dark_mode', True)
        self._apply_theme()
        
        self.data_manager = FilamentManager()
        self.main_window = MainWindow(root, self)
        
        self.load_initial_data()

    def load_initial_data(self):
        self.logger.info("Loading initial data...")
        loaded_count, corrupted_count = self.data_manager.load_filaments()
        self.update_view()
        if corrupted_count > 0:
            messagebox.showwarning(
                "Load Warning",
                f"{loaded_count} filaments loaded successfully.\n"
                f"{corrupted_count} files were corrupted and could not be loaded. "
                "Check logs for details."
            )

    def update_view(self):
        filaments = self.data_manager.get_all_filaments()
        query = self.main_window.get_search_query().lower()

        if query:
            filtered_filaments = {}
            for filename, data in filaments.items():
                if (query in str(data.get('brand', '')).lower() or
                    query in str(data.get('material', '')).lower() or
                    query in str(data.get('color', '')).lower() or
                    query in filename.lower()):
                    filtered_filaments[filename] = data
            filaments = filtered_filaments

        self.main_window.update_filament_list(filaments)

    def sort_filaments(self, column):
        if self.main_window.sort_by == column:
            self.main_window.sort_order = 'desc' if self.main_window.sort_order == 'asc' else 'asc'
        else:
            self.main_window.sort_by = column
            self.main_window.sort_order = 'asc'
        self.update_view()

    def on_filament_select(self, event=None):
        """Handle filament selection in the list."""
        selected_items = self.main_window.filament_list.selection()
        if not selected_items:
            self.main_window.clear_details_panel()
            return

        filename = selected_items[0]
        self.show_details(filename)

    def show_details(self, filename):
        """Show details for a given filament."""
        filament_data = self.data_manager.get_all_filaments().get(filename)
        if filament_data:
            self.main_window.update_details_panel(filament_data)
        else:
            self.main_window.clear_details_panel()

    def filter_filaments(self, *args):
        self.update_view()

    def add_filament(self):
        self.logger.info("Opening 'Add New Filament' dialog.")
        AddEditDialog(self.root, self, title="Add New Filament")

    def edit_filament(self):
        selected_items = self.main_window.filament_list.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a filament to edit.")
            return
        
        filename = selected_items[0]
        filament_data = self.data_manager.get_all_filaments().get(filename)
        if filament_data:
            self.logger.info(f"Opening 'Edit Filament' dialog for {filename}.")
            AddEditDialog(self.root, self, title=tr('edit_dialog_title'), filament_data=filament_data, original_filename=filename)

    def delete_filament(self):
        """Delete the selected filament."""
        selected_items = self.main_window.filament_list.selection()
        if not selected_items:
            messagebox.showwarning(tr('no_filament_selected_msg'), tr('no_filament_selected_msg'))
            return

        filename = selected_items[0]
        if messagebox.askyesno(tr('confirm_deletion_title'), tr('confirm_deletion_msg')):
            try:
                self.data_manager.delete_filament(filename)
                self.logger.info(f"Filament '{filename}' deleted successfully.")
                self.load_initial_data()
            except Exception as e:
                self.logger.error(f"Failed to delete filament '{filename}': {e}")
                messagebox.showerror(tr('error_title'), f"{tr('delete_error_msg')}\n{e}")

    def save_filament(self, data, original_filename=None):
        self.logger.info(f"Saving filament data. Original filename: {original_filename}")
        try:
            self.data_manager.save_filament(data, original_filename)
            self.logger.info("Filament saved successfully. Reloading data.")
            self.load_initial_data()
        except Exception as e:
            self.logger.error(f"Failed to save filament: {e}")
            messagebox.showerror(tr('error_title'), f"{tr('save_error_msg')}\n{e}")

    def change_language(self, lang_code):
        """Change the application language and prompt for a restart."""
        self.logger.info(f"Language changed to {lang_code}.")
        set_language(lang_code)
        messagebox.showinfo(
            tr('language_change_title'),
            tr('language_change_msg')
        )
        self.root.destroy()

    def import_from_zip(self):
        """Import filament profiles from a zip archive."""
        filepath = filedialog.askopenfilename(
            title=tr('import_zip_title'),
            filetypes=(("Zip files", "*.zip"), ("All files", "*.*"))
        )
        if not filepath:
            return
        try:
            self.data_manager.import_from_zip(filepath)
            self.reload_filaments()
            messagebox.showinfo(tr('import_success_title'), tr('import_success_msg'))
        except Exception as e:
            self.logger.error(f"Failed to import from zip: {e}")
            messagebox.showerror(tr('import_error_title'), f"{tr('import_error_msg')}\n{e}")

    def export_to_zip(self):
        """Export all filament profiles to a zip archive."""
        filepath = filedialog.asksaveasfilename(
            title=tr('export_zip_title'),
            defaultextension=".zip",
            filetypes=(("Zip files", "*.zip"), ("All files", "*.*"))
        )
        if not filepath:
            return
        try:
            self.data_manager.export_to_zip(filepath)
            messagebox.showinfo(tr('export_success_title'), tr('export_success_msg'))
        except Exception as e:
            self.logger.error(f"Failed to export filaments: {e}")
            messagebox.showerror(tr('export_error_title'), f"{tr('export_error_msg')}\n{e}")

    def reload_filaments(self):
        """Reload all filament data from disk."""
        self.logger.info("Reloading filaments from disk.")
        self.load_initial_data()

    def _load_settings(self):
        """Load application settings from file."""
        default_settings = {
            'dark_mode': True,
            'language': 'en'
        }
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return {**default_settings, **json.load(f)}
            except Exception as e:
                self.logger.error(f"Error loading settings: {e}")
                return default_settings
        return default_settings
    
    def _save_settings(self):
        """Save current settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
    
    def toggle_theme(self):
        """Toggle between dark and light theme."""
        self.dark_mode = not self.dark_mode
        self.settings['dark_mode'] = self.dark_mode
        self._save_settings()
        self._apply_theme()
    
    def _apply_theme(self):
        """Apply the current theme based on settings."""
        if self.dark_mode:
            apply_dark_theme(self.root)
        else:
            apply_light_theme(self.root)
    
    def show_about(self):
        """Show the about dialog."""
        from src.ui.about import show_about_dialog
        show_about_dialog(self.root, dark_mode=self.dark_mode)

    def show_help(self):
        """Show the help dialog."""
        self.logger.info("Showing Help dialog.")
        from src.ui.help import show_help_dialog
        show_help_dialog(self.root, dark_mode=self.dark_mode)

    def show_sponsor_dialog(self):
        self.logger.info("Showing Sponsor dialog.")
        from src.ui.sponsor import show_sponsor_dialog
        show_sponsor_dialog(self.root, dark_mode=self.dark_mode)

    def run(self):
        self.root.mainloop()
