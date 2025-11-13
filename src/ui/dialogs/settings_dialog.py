import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Callable
import json
import os
from pathlib import Path
from tkinter import messagebox

from src.ui.lang import tr
from src.config import APP_DATA_DIR

class SettingsDialog(tk.Toplevel):
    """
    A dialog for managing application settings.
    
    This dialog allows users to configure various application settings
    such as theme, language, and backup preferences.
    
    Args:
        parent: The parent window.
        settings: Current application settings.
        on_save: Callback function to call when settings are saved.
    """
    
    def __init__(self, parent, settings: Dict[str, Any], on_save: Callable[[Dict[str, Any]], None]):
        super().__init__(parent)
        self.settings = settings.copy()
        self.on_save = on_save
        
        self.title(tr('settings'))
        self.geometry('600x500')
        self.resizable(True, True)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Center the dialog on the parent window
        self.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        self.geometry(f'+{x}+{y}')
        
        self._create_widgets()
        
        # Set focus to the dialog
        self.focus_set()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
    
    def _create_widgets(self):
        """Create and layout the settings dialog widgets."""
        # Create main container with padding
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for settings categories
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # General tab
        general_frame = ttk.Frame(notebook, padding=5)
        notebook.add(general_frame, text=tr('general'))
        self._create_general_tab(general_frame)
        
        # Backup tab
        backup_frame = ttk.Frame(notebook, padding=5)
        notebook.add(backup_frame, text=tr('backup'))
        self._create_backup_tab(backup_frame)
        
        # Paths tab
        paths_frame = ttk.Frame(notebook, padding=5)
        notebook.add(paths_frame, text=tr('paths'))
        self._create_paths_tab(paths_frame)
        
        # Buttons frame at the bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Save button
        save_btn = ttk.Button(
            button_frame, 
            text=tr('save'), 
            command=self._on_save,
            style='Accent.TButton' if 'ttkthemes' in str(ttk.Style().theme_names()) else 'TButton'
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        # Cancel button
        cancel_btn = ttk.Button(
            button_frame, 
            text=tr('cancel'), 
            command=self._on_cancel
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def _create_general_tab(self, parent):
        """Create the General settings tab."""
        # Theme settings
        theme_frame = ttk.LabelFrame(parent, text=tr('appearance'), padding=10)
        theme_frame.pack(fill=tk.X, pady=5)
        
        # Dark mode toggle
        self.dark_mode_var = tk.BooleanVar(value=self.settings.get('dark_mode', True))
        dark_mode_cb = ttk.Checkbutton(
            theme_frame,
            text=tr('dark_mode'),
            variable=self.dark_mode_var,
            command=self._toggle_theme_preview
        )
        dark_mode_cb.pack(anchor=tk.W, pady=2)
        
        # Language settings
        lang_frame = ttk.LabelFrame(parent, text=tr('language'), padding=10)
        lang_frame.pack(fill=tk.X, pady=5)
        
        self.language_var = tk.StringVar(value=self.settings.get('language', 'en'))
        
        # English
        en_btn = ttk.Radiobutton(
            lang_frame,
            text="English",
            value='en',
            variable=self.language_var
        )
        en_btn.pack(anchor=tk.W, pady=2)
        
        # Italian
        it_btn = ttk.Radiobutton(
            lang_frame,
            text="Italiano",
            value='it',
            variable=self.language_var
        )
        it_btn.pack(anchor=tk.W, pady=2)
    
    def _create_backup_tab(self, parent):
        """Create the Backup settings tab."""
        backup_settings = self.settings.get('backup', {})
        
        # Enable backups
        self.backup_enabled_var = tk.BooleanVar(value=backup_settings.get('enabled', True))
        backup_cb = ttk.Checkbutton(
            parent,
            text=tr('enable_backups'),
            variable=self.backup_enabled_var
        )
        backup_cb.pack(anchor=tk.W, pady=2)
        
        # Backup frequency
        ttk.Label(parent, text=tr('backup_frequency')).pack(anchor=tk.W, pady=(15, 5))
        
        self.backup_freq_var = tk.StringVar(value=backup_settings.get('frequency', 'daily'))
        
        freq_frame = ttk.Frame(parent)
        freq_frame.pack(fill=tk.X, pady=2)
        
        freq_options = [
            ('on_startup', 'on_startup'),
            ('daily', 'daily'),
            ('weekly', 'weekly'),
            ('monthly', 'monthly')
        ]
        
        for text, value in freq_options:
            rb = ttk.Radiobutton(
                freq_frame,
                text=tr(text),
                value=value,
                variable=self.backup_freq_var
            )
            rb.pack(anchor=tk.W, pady=2)
        
        # Max backups to keep
        ttk.Label(parent, text=tr('max_backups_to_keep')).pack(anchor=tk.W, pady=(15, 5))
        
        self.max_backups_var = tk.IntVar(value=backup_settings.get('max_backups', 10))
        max_backups_spin = ttk.Spinbox(
            parent,
            from_=1,
            to=100,
            textvariable=self.max_backups_var,
            width=5
        )
        max_backups_spin.pack(anchor=tk.W, pady=2)
    
    def _create_paths_tab(self, parent):
        """Create the Paths settings tab."""
        paths_settings = self.settings.get('paths', {})
        
        # Backup directory
        ttk.Label(parent, text=tr('backup_directory'), font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(5, 2))
        
        backup_frame = ttk.Frame(parent)
        backup_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.backup_dir_var = tk.StringVar(value=paths_settings.get('backup_dir', ''))
        backup_entry = ttk.Entry(backup_frame, textvariable=self.backup_dir_var)
        backup_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        def browse_backup_dir():
            dir_path = filedialog.askdirectory(
                title=tr('select_backup_directory'),
                initialdir=self.backup_dir_var.get() or os.path.expanduser('~')
            )
            if dir_path:
                self.backup_dir_var.set(dir_path)
        
        ttk.Button(
            backup_frame,
            text=tr('browse'),
            command=browse_backup_dir
        ).pack(side=tk.RIGHT)
        
        # FDM files directory
        ttk.Label(parent, text=tr('fdm_files_directory'), font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(15, 2))
        
        fdm_frame = ttk.Frame(parent)
        fdm_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.fdm_dir_var = tk.StringVar(value=paths_settings.get('fdm_dir', ''))
        fdm_entry = ttk.Entry(fdm_frame, textvariable=self.fdm_dir_var)
        fdm_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        def browse_fdm_dir():
            dir_path = filedialog.askdirectory(
                title=tr('select_fdm_directory'),
                initialdir=self.fdm_dir_var.get() or os.path.expanduser('~')
            )
            if dir_path:
                self.fdm_dir_var.set(dir_path)
        
        ttk.Button(
            fdm_frame,
            text=tr('browse'),
            command=browse_fdm_dir
        ).pack(side=tk.RIGHT)
        
        # Default paths note
        ttk.Label(
            parent,
            text=tr('default_paths_note'),
            style='Small.TLabel',
            wraplength=400
        ).pack(anchor=tk.W, pady=(15, 0))
    
    def _toggle_theme_preview(self):
        """Toggle between light and dark theme preview."""
        if self.dark_mode_var.get():
            self.style = ttk.Style()
            self.style.theme_use('default')
            if 'ttkthemes' in str(self.style.theme_names()):
                self.style.theme_use('equilux')
            self.configure(bg='#2e2e2e')
        else:
            self.style = ttk.Style()
            self.style.theme_use('default')
            if 'ttkthemes' in str(self.style.theme_names()):
                self.style.theme_use('arc')
            self.configure(bg='#f5f6f7')
    
    def _on_save(self):
        """Handle save button click."""
        # Update settings
        self.settings['dark_mode'] = self.dark_mode_var.get()
        self.settings['language'] = self.language_var.get()
        
        # Update backup settings
        self.settings['backup'] = {
            'enabled': self.backup_enabled_var.get(),
            'frequency': self.backup_freq_var.get(),
            'max_backups': self.max_backups_var.get(),
            'backup_on_startup': True,
            'backup_on_exit': True,
            'include_logs': True,
            'backup_dir': self.backup_dir_var.get() or 'backups'
        }
        
        # Update paths settings
        self.settings['paths'] = {
            'backup_dir': self.backup_dir_var.get() or 'backups',
            'fdm_dir': self.fdm_dir_var.get() or os.path.join(os.path.expanduser('~'), '.3d_filament_manager', 'fdm')
        }
        
        # Save settings
        self.on_save(self.settings)
        
        # Close the dialog
        self.destroy()
    
    def _on_cancel(self):
        """Handle cancel button click or window close."""
        self.destroy()

def show_settings_dialog(parent, settings: Dict[str, Any], on_save: Callable[[Dict[str, Any]], None]) -> None:
    """
    Show the settings dialog.
    
    Args:
        parent: The parent window.
        settings: Current application settings.
        on_save: Callback function called with new settings when saved.
    """
    dialog = SettingsDialog(parent, settings, on_save)
    parent.wait_window(dialog)
