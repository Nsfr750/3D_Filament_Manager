"""
Backup management dialog for the 3D Filament Manager.

Provides a user interface for creating, restoring, and managing backups.
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Optional, Callable, Dict, Any
import logging

from src.services.backup_service import backup_service
from src.config import backup_config, APP_NAME
from src.ui.lang import tr
from src.ui.theme import get_theme

class BackupDialog(tk.Toplevel):
    """
    Dialog for managing application backups.
    """
    
    def __init__(self, parent, on_backup_complete: Optional[Callable] = None):
        """
        Initialize the backup dialog.
        
        Args:
            parent: Parent window
            on_backup_complete: Optional callback when a backup is created
        """
        super().__init__(parent)
        
        self.parent = parent
        self.on_backup_complete = on_backup_complete
        self.logger = logging.getLogger(__name__)
        
        self.title(f"{tr('backup_management')} - {APP_NAME}")
        self.geometry("800x600")
        self.minsize(600, 400)
        
        # Apply theme with fallback
        try:
            self.theme = get_theme()
            bg_color = self.theme.get('bg', '#f0f0f0')  # Default light gray
        except Exception as e:
            self.logger.warning(f"Could not load theme: {e}")
            bg_color = '#f0f0f0'  # Default light gray
            self.theme = {}
            
        self.configure(bg=bg_color)
        
        self._create_widgets()
        self._load_backups()
        
        # Center the dialog on the parent window
        self.transient(parent)
        self.grab_set()
        self._center_on_parent()
    
    def _create_widgets(self) -> None:
        """Create and arrange the dialog widgets."""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Backup controls frame
        ctrl_frame = ttk.LabelFrame(main_frame, text=tr('create_backup'), padding=10)
        ctrl_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Backup options
        self.include_logs = tk.BooleanVar(value=backup_config.include_logs)
        ttk.Checkbutton(
            ctrl_frame,
            text=tr('include_logs'),
            variable=self.include_logs
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # Create backup button
        ttk.Button(
            ctrl_frame,
            text=tr('create_backup_now'),
            command=self._create_backup,
            style='Accent.TButton'
        ).pack(fill=tk.X, pady=(5, 0))
        
        # Restore frame
        restore_frame = ttk.LabelFrame(main_frame, text=tr('restore_backup'), padding=10)
        restore_frame.pack(fill=tk.BOTH, expand=True)
        
        # Backup list
        columns = ('date', 'size', 'path')
        self.backup_tree = ttk.Treeview(
            restore_frame,
            columns=columns,
            show='headings',
            selectmode='browse',
            height=10
        )
        
        # Configure columns
        self.backup_tree.heading('date', text=tr('date'), anchor=tk.W)
        self.backup_tree.heading('size', text=tr('size'), anchor=tk.W)
        self.backup_tree.heading('path', text=tr('path'), anchor=tk.W)
        
        self.backup_tree.column('date', width=150, stretch=False)
        self.backup_tree.column('size', width=100, stretch=False)
        self.backup_tree.column('path', width=300, stretch=True)
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(restore_frame, orient=tk.VERTICAL, command=self.backup_tree.yview)
        x_scroll = ttk.Scrollbar(restore_frame, orient=tk.HORIZONTAL, command=self.backup_tree.xview)
        self.backup_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Grid layout for treeview and scrollbars
        self.backup_tree.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        restore_frame.columnconfigure(0, weight=1)
        restore_frame.rowconfigure(0, weight=1)
        
        # Button frame
        btn_frame = ttk.Frame(restore_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky='ew')
        
        # Restore button
        self.restore_btn = ttk.Button(
            btn_frame,
            text=tr('restore_selected'),
            command=self._restore_backup,
            state=tk.DISABLED,
            style='Accent.TButton'
        )
        self.restore_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Delete button
        self.delete_btn = ttk.Button(
            btn_frame,
            text=tr('delete_selected'),
            command=self._delete_backup,
            state=tk.DISABLED
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Import button
        ttk.Button(
            btn_frame,
            text=tr('import_backup'),
            command=self._import_backup
        ).pack(side=tk.LEFT, padx=5)
        
        # Close button
        ttk.Button(
            btn_frame,
            text=tr('close'),
            command=self.destroy
        ).pack(side=tk.RIGHT)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        self.backup_tree.bind('<<TreeviewSelect>>', self._on_selection_change)
        
        # Configure grid weights for the main window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
    
    def _load_backups(self) -> None:
        """Load and display the list of available backups."""
        # Clear existing items
        for item in self.backup_tree.get_children():
            self.backup_tree.delete(item)
        
        # Get and sort backups (newest first)
        backups = backup_service.list_backups()
        backups.sort(key=lambda x: x['modified'], reverse=True)
        
        # Add backups to the treeview
        for backup in backups:
            try:
                dt = datetime.fromisoformat(backup['modified'])
                date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                size_mb = backup['size_bytes'] / (1024 * 1024)
                size_str = f"{size_mb:.2f} MB"
                
                self.backup_tree.insert(
                    '', tk.END,
                    values=(date_str, size_str, backup['path']),
                    tags=('backup',)
                )
            except Exception as e:
                self.logger.error(f"Error loading backup {backup.get('path', 'unknown')}: {e}")
        
        # Update status
        count = len(backups)
        if count == 0:
            self.status_var.set(tr('no_backups_found'))
        else:
            self.status_var.set(tr('backups_found', count=count))
    
    def _on_selection_change(self, event=None) -> None:
        """Handle selection changes in the backup list."""
        selection = self.backup_tree.selection()
        state = tk.NORMAL if selection else tk.DISABLED
        
        self.restore_btn.config(state=state)
        self.delete_btn.config(state=state)
    
    def _create_backup(self) -> None:
        """Create a new backup."""
        try:
            self.status_var.set(tr('creating_backup') + '...')
            self.update_idletasks()
            
            backup_path = backup_service.create_backup(
                include_logs=self.include_logs.get()
            )
            
            if backup_path:
                self.status_var.set(tr('backup_created_successfully'))
                self._load_backups()  # Refresh the list
                
                if self.on_backup_complete:
                    self.on_backup_complete(backup_path)
            else:
                self.status_var.set(tr('failed_to_create_backup'))
                
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}", exc_info=True)
            messagebox.showerror(
                tr('error'),
                tr('failed_to_create_backup_detailed', error=str(e)),
                parent=self
            )
            self.status_var.set(tr('error_occurred'))
    
    def _restore_backup(self) -> None:
        """Restore the selected backup."""
        selection = self.backup_tree.selection()
        if not selection:
            return
            
        # Get the backup path from the selected item
        item = self.backup_tree.item(selection[0])
        backup_path = item['values'][2]  # Path is the third column
        
        if not backup_path or not os.path.exists(backup_path):
            messagebox.showerror(
                tr('error'),
                tr('backup_file_not_found'),
                parent=self
            )
            return
        
        # Confirm before restoring
        if not messagebox.askyesno(
            tr('confirm_restore'),
            tr('confirm_restore_message'),
            parent=self
        ):
            return
        
        try:
            self.status_var.set(tr('restoring_backup') + '...')
            self.update_idletasks()
            
            success = backup_service.restore_backup(backup_path)
            
            if success:
                self.status_var.set(tr('backup_restored_successfully'))
                messagebox.showinfo(
                    tr('success'),
                    tr('restore_completed_restart'),
                    parent=self
                )
                
                # Close the application to apply changes
                self.quit()
            else:
                self.status_var.set(tr('failed_to_restore_backup'))
                
        except Exception as e:
            self.logger.error(f"Error restoring backup: {e}", exc_info=True)
            messagebox.showerror(
                tr('error'),
                tr('failed_to_restore_backup_detailed', error=str(e)),
                parent=self
            )
            self.status_var.set(tr('error_occurred'))
    
    def _delete_backup(self) -> None:
        """Delete the selected backup."""
        selection = self.backup_tree.selection()
        if not selection:
            return
            
        # Get the backup path from the selected item
        item = self.backup_tree.item(selection[0])
        backup_path = item['values'][2]  # Path is the third column
        
        if not backup_path or not os.path.exists(backup_path):
            messagebox.showerror(
                tr('error'),
                tr('backup_file_not_found'),
                parent=self
            )
            return
        
        # Confirm before deleting
        if not messagebox.askyesno(
            tr('confirm_delete'),
            tr('confirm_delete_backup'),
            parent=self
        ):
            return
        
        try:
            os.remove(backup_path)
            self.status_var.set(tr('backup_deleted_successfully'))
            self._load_backups()  # Refresh the list
            
        except Exception as e:
            self.logger.error(f"Error deleting backup: {e}", exc_info=True)
            messagebox.showerror(
                tr('error'),
                tr('failed_to_delete_backup_detailed', error=str(e)),
                parent=self
            )
            self.status_var.set(tr('error_occurred'))
    
    def _import_backup(self) -> None:
        """Import a backup from a file."""
        file_path = filedialog.askopenfilename(
            parent=self,
            title=tr('select_backup_file'),
            filetypes=[
                (tr('backup_files'), '*.zip'),
                (tr('all_files'), '*.*')
            ]
        )
        
        if not file_path:
            return
        
        try:
            # Copy the file to the backup directory
            import shutil
            import os
            
            filename = os.path.basename(file_path)
            dest_path = os.path.join(backup_config.backup_dir, filename)
            
            # Ensure the destination filename is unique
            counter = 1
            base, ext = os.path.splitext(filename)
            while os.path.exists(dest_path):
                dest_path = os.path.join(
                    backup_config.backup_dir,
                    f"{base}_{counter}{ext}"
                )
                counter += 1
            
            shutil.copy2(file_path, dest_path)
            self.status_var.set(tr('backup_imported_successfully'))
            self._load_backups()  # Refresh the list
            
        except Exception as e:
            self.logger.error(f"Error importing backup: {e}", exc_info=True)
            messagebox.showerror(
                tr('error'),
                tr('failed_to_import_backup_detailed', error=str(e)),
                parent=self
            )
            self.status_var.set(tr('error_occurred'))
    
    def _center_on_parent(self) -> None:
        """Center the dialog on the parent window."""
        if not self.parent:
            return
            
        self.update_idletasks()
        
        # Get the parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get the dialog size
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        
        # Calculate position to center on parent
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        # Apply the position
        self.geometry(f"+{x}+{y}")


def show_backup_dialog(parent, on_backup_complete: Optional[Callable] = None) -> None:
    """
    Show the backup management dialog.
    
    Args:
        parent: Parent window
        on_backup_complete: Optional callback when a backup is created
    """
    dialog = BackupDialog(parent, on_backup_complete)
    dialog.transient(parent)
    dialog.grab_set()
    parent.wait_window(dialog)
