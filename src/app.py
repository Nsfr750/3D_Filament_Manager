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
    """
    Main application controller for the 3D Filament Manager.
    
    This class manages the main application window, user interactions, and coordinates
    between the data layer (FilamentManager) and the UI layer (MainWindow).
    
    Attributes:
        root: The root Tkinter window.
        logger: Logger instance for application logging.
        settings_file: Path to the settings JSON file.
        settings: Dictionary containing application settings.
        dark_mode: Boolean indicating if dark mode is enabled.
        data_manager: Instance of FilamentManager for data operations.
        main_window: Main application window UI component.
    """

    def __init__(self, root):
        """
        Initialize the FilamentManager application.
        
        Args:
            root: The root Tkinter window.
        """
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
        """Load initial filament data with progress feedback."""
        self.logger.info("Loading initial data...")
        
        # Show loading indicator
        self.main_window.show_loading(True, "Loading filament data...")
        
        try:
            # Update the view - FilamentManager already loaded metadata in __init__
            self.update_view()
            
            # Get the count of loaded filaments
            loaded_count = len(self.data_manager.get_all_filaments())
            self.logger.info(f"Successfully loaded {loaded_count} filaments")
            
        except Exception as e:
            self.logger.error(f"Error loading initial data: {e}")
            messagebox.showerror("Error", "Failed to load filament data. Check logs for details.")
        finally:
            # Hide loading indicator
            self.main_window.show_loading(False)
            
    def reload_filaments(self):
        """Reload all filament data from disk."""
        self.logger.info("Reloading filaments from disk.")
        self.load_initial_data()

    def update_view(self):
        """Update the view with filtered and sorted filaments."""
        query = self.main_window.get_search_query().strip()
        
        # Use the search index for faster searching
        if query:
            filaments = self.data_manager.search_filaments(query)
        else:
            filaments = self.data_manager.get_all_filaments()
            
        # Apply sorting
        self._apply_sorting(filaments)
        
        # Update the UI
        self.main_window.update_filament_list(filaments)
        
    def _apply_sorting(self, filaments: dict) -> None:
        """Apply sorting to the filaments dictionary in-place."""
        if not filaments:
            return
            
        sort_key = self.main_window.sort_by.lower()
        reverse = self.main_window.sort_order == 'desc'
        
        # Create a list of tuples (sort_key, filename) for sorting
        items = []
        for filename, data in filaments.items():
            if sort_key == 'filename':
                sort_value = filename.lower()
            else:
                sort_value = str(data.get(sort_key, '')).lower()
            items.append((sort_value, filename, data))
        
        # Sort the items
        items.sort(key=lambda x: x[0], reverse=reverse)
        
        # Rebuild the filaments dictionary in sorted order
        filaments.clear()
        for _, filename, data in items:
            filaments[filename] = data

    def sort_filaments(self, column):
        """
        Sort the filament list by the specified column.
        
        Toggles between ascending and descending order if the same column is clicked
        multiple times. Updates the view to reflect the new sort order.
        
        Args:
            column (str): The column name to sort by.
        """
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
        # Use get_filament to load full data on demand
        filament_data = self.data_manager.get_filament(filename)
        if filament_data:
            self.main_window.update_details_panel(filament_data)
        else:
            self.main_window.clear_details_panel()

    def filter_filaments(self, *args):
        """
        Apply the current search filter to the filament list.
        
        This method is typically called when the search criteria changes.
        It triggers an update of the view with the filtered results.
        
        Args:
            *args: Variable length argument list (unused, for callback compatibility).
        """
        self.update_view()

    def add_filament(self):
        """
        Open the dialog to add a new filament.
        
        Creates and displays a new AddEditDialog in 'add' mode.
        The user can enter details for a new filament profile.
        """
        self.logger.info("Opening 'Add New Filament' dialog.")
        AddEditDialog(self.root, self, title="Add New Filament")

    def edit_filament(self):
        """
        Open the dialog to edit the selected filament.
        
        Retrieves the currently selected filament's data and opens an
        AddEditDialog pre-populated with the filament's current values.
        
        Shows a warning if no filament is selected.
        """
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
        """
        Save filament data to disk.
        
        Handles both new filament creation and updates to existing filaments.
        Reloads the filament list after successful save.
        
        Args:
            data (dict): Dictionary containing the filament's data.
            original_filename (str, optional): Filename of the filament being updated.
                                             If None, a new filament is created.
        """
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
        """
        Display the sponsor/donation dialog.
        
        Shows information about supporting the project through donations
        or other means of sponsorship.
        """
        self.logger.info("Showing Sponsor dialog.")
        from src.ui.sponsor import show_sponsor_dialog
        show_sponsor_dialog(self.root, dark_mode=self.dark_mode)

    def run(self):
        """
        Start the main application event loop.
        
        This method should be called after initializing the application
        to begin processing user input and updating the UI.
        """
        self.root.mainloop()
