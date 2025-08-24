import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, List, Optional
import tkinter.font as tkFont

from src.ui.lang import tr, get_available_languages, get_language


class MainWindow(ttk.Frame):
    """
    The main window of the 3D Filament Manager application.
    
    This class handles the main user interface including the filament list, search,
    and detailed filament information display. It coordinates with the controller
    for data operations and updates the UI accordingly.
    
    Attributes:
        parent: The parent Tkinter widget.
        controller: The application controller handling business logic.
        columns: Tuple of column names for the filament list.
        sort_by: Current column to sort by.
        sort_order: Current sort order ('asc' or 'desc').
        lang_var: Tkinter variable for the selected language.
        loading_frame: Frame for the loading indicator.
        loading_label: Label showing loading message.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.columns = ("Filename", "Brand", "Material", "Color", "Remaining")
        self.sort_by = 'brand'  # Default sort column
        self.sort_order = 'asc'  # Default sort order
        self.lang_var = tk.StringVar(value=get_language())

        # Initialize loading indicator
        self.loading_frame = None
        self.loading_label = None
        
        self._create_menu()
        self.setup_ui()

    def show_loading(self, show: bool, message: str = "Loading...") -> None:
        """Show or hide the loading indicator.
        
        Args:
            show: Whether to show the loading indicator
            message: Optional message to display while loading
        """
        if show:
            if not self.loading_frame:
                # Create loading frame
                self.loading_frame = ttk.Frame(self.parent, style='Loading.TFrame')
                self.loading_frame.place(relx=0.5, rely=0.5, anchor='center')
                
                # Add loading label
                self.loading_label = ttk.Label(
                    self.loading_frame,
                    text=message,
                    font=('Arial', 10, 'bold'),
                    style='Loading.TLabel'
                )
                self.loading_label.pack(pady=10)
                
                # Add progress bar
                self.progress = ttk.Progressbar(
                    self.loading_frame,
                    mode='indeterminate',
                    length=200
                )
                self.progress.pack(pady=5)
                self.progress.start(10)
            else:
                # Update existing loading message
                self.loading_label.config(text=message)
                
            # Bring to front
            self.loading_frame.lift()
        elif self.loading_frame:
            # Hide loading frame
            self.loading_frame.destroy()
            self.loading_frame = None
            self.loading_label = None
    
    def _create_menu(self):
        """
        Create and configure the main menu bar.
        
        Sets up the following menus:
        - File: Reload, import/export filaments, exit
        - Language: Language selection with flag icons
        - View: Theme toggle
        - Help: Help, about, and sponsor information
        """
        # Create menubar with tk.Menu
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        # File menu with icons
        file_menu = tk.Menu(menubar, tearoff=0)
        
        # Add menu items with icons
        file_menu.add_command(
            label=f"🔄 {tr('reload_filaments')}",
            command=self.controller.reload_filaments
        )
        
        # Add Backup submenu
        backup_menu = tk.Menu(file_menu, tearoff=0)
        backup_menu.add_command(
            label=f"💾 {tr('create_backup')}",
            command=self.controller.create_backup
        )
        backup_menu.add_command(
            label=f"⏮️ {tr('restore_backup')}",
            command=self.controller.restore_backup
        )
        backup_menu.add_command(
            label=f"📋 {tr('manage_backups')}",
            command=self.controller.manage_backups
        )
        file_menu.add_cascade(label=f"🔒 {tr('backup')}", menu=backup_menu)
        
        file_menu.add_separator()
        file_menu.add_command(
            label=f"⬆️ {tr('import_filaments')}",
            command=self.controller.import_from_zip
        )
        file_menu.add_command(
            label=f"⬇️ {tr('export_filaments')}",
            command=self.controller.export_to_zip
        )
        file_menu.add_separator()
        file_menu.add_command(
            label=f"🚪 {tr('exit')}",
            command=self.parent.quit
        )
        menubar.add_cascade(label=tr('file'), menu=file_menu)

        # Language menu with flag icons
        lang_menu = tk.Menu(menubar, tearoff=0)
        lang_name_map = {
            'en': ('english', '🇬🇧'),
            'it': ('italian', '🇮🇹')
        }
        
        for lang_code in get_available_languages():
            lang_name, flag_icon = lang_name_map.get(lang_code, (lang_code, '🌐'))
            lang_name = tr(lang_name)
            lang_menu.add_radiobutton(
                label=f"{flag_icon} {lang_name}",
                value=lang_code,
                variable=self.lang_var,
                command=lambda: self.controller.change_language(self.lang_var.get())
            )
        menubar.add_cascade(label=tr('language_menu'), menu=lang_menu)

        # View menu with theme toggle
        view_menu = tk.Menu(menubar, tearoff=0)
        self.dark_mode_var = tk.BooleanVar(value=getattr(self.controller, 'dark_mode', True))
        
        def update_theme_icon():
            theme_icon = '🌙' if self.dark_mode_var.get() else '☀️'
            view_menu.entryconfig(0, label=f"{theme_icon} {tr('dark_mode')}")
            
        view_menu.add_checkbutton(
            label=f"{'🌙' if self.dark_mode_var.get() else '☀️'} {tr('dark_mode')}",
            command=lambda: [self.controller.toggle_theme(), update_theme_icon()],
            variable=self.dark_mode_var
        )
        self.dark_mode_var.trace_add('write', lambda *_: update_theme_icon())
        menubar.add_cascade(label=tr('view'), menu=view_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        
        # Add Price Tracker
        tools_menu.add_command(
            label=f"📊 {tr('price_tracker')}",
            command=self.controller.show_price_tracker
        )
        
        # Add Barcode Utility if available
        if hasattr(self.controller, 'show_barcode_utility'):
            tools_menu.add_command(
                label=f"📱 {tr('barcode_utility')}",
                command=self.controller.show_barcode_utility
            )
            
        # Only show the Tools menu if there are available tools
        if tools_menu.index('end') is not None:
            menubar.add_cascade(label=tr('tools'), menu=tools_menu)
        
        # Help menu with icons
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label=f"❓ {tr('help')}",
            command=self.controller.show_help
        )
        help_menu.add_command(
            label=f"ℹ️ {tr('about')}",
            command=self.controller.show_about
        )
        help_menu.add_command(
            label=f"❤️ {tr('sponsor')}",
            command=self.controller.show_sponsor_dialog
        )
        menubar.add_cascade(label=tr('help'), menu=help_menu)
        

    def setup_ui(self):
        """
        Set up the main user interface components.
        
        Creates the main application layout with left and right panels:
        - Left panel: Filament list with search and action buttons
        - Right panel: Detailed filament information in tabs
        """
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self._create_left_panel(main_frame)
        self._create_right_panel(main_frame)

    def _create_left_panel(self, parent):
        """
        Create the left panel containing the filament list and controls.
        
        Args:
            parent: The parent widget for this panel.
            
        The panel includes:
        - Search box for filtering filaments
        - Sortable list of filaments
        - Action buttons (Add, Edit, Delete)
        """
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)

        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        search_frame.columnconfigure(1, weight=1)
        ttk.Label(search_frame, text=tr('search_label')).grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        self.search_var.trace_add('write', lambda *args: self.controller.filter_filaments())

        self.filament_list = ttk.Treeview(list_frame, columns=self.columns, show="headings")
        self.column_map = {
            'Filename': 'col_filename',
            'Brand': 'col_brand',
            'Material': 'col_material',
            'Color': 'col_color',
            'Remaining': 'col_remaining',
        }
        for col in self.columns:
            self.filament_list.heading(col, text=tr(self.column_map.get(col, col)), command=lambda c=col: self.controller.sort_filaments(c))
        self.filament_list.grid(row=1, column=0, sticky="nsew")
        self.filament_list.bind('<<TreeviewSelect>>', self.controller.on_filament_select)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.filament_list.yview)
        self.filament_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        ttk.Button(button_frame, text=tr('add_filament'), command=self.controller.add_filament).grid(row=0, column=0, sticky="ew", padx=(0, 2))
        ttk.Button(button_frame, text=tr('edit_filament'), command=self.controller.edit_filament).grid(row=0, column=1, sticky="ew", padx=(2, 0))
        ttk.Button(button_frame, text=tr('delete_filament'), command=self.controller.delete_filament).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2,0))

    def _create_right_panel(self, parent):
        """
        Create the right panel showing detailed filament information.
        
        Args:
            parent: The parent widget for this panel.
            
        The panel includes a notebook with three tabs:
        - Details: Basic filament information
        - Properties: Physical and usage properties
        - Slicer Settings: 3D printing parameters
        """
        details_notebook = ttk.Notebook(parent)
        details_notebook.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        details_tab = ttk.Frame(details_notebook)
        properties_tab = ttk.Frame(details_notebook)
        slicer_tab = ttk.Frame(details_notebook)

        details_notebook.add(details_tab, text=tr('details_title'))
        details_notebook.add(properties_tab, text=tr('properties_title'))
        details_notebook.add(slicer_tab, text=tr('slicer_settings'))

        # Configure text tags for styling
        text_widgets = []
        
        # Details tab
        self.details_text = tk.Text(details_tab, wrap='word', state='disabled', padx=10, pady=10)
        self.details_text.pack(expand=True, fill='both')
        text_widgets.append(self.details_text)
        
        # Properties tab
        self.properties_text = tk.Text(properties_tab, wrap='word', state='disabled', padx=10, pady=10)
        self.properties_text.pack(expand=True, fill='both')
        text_widgets.append(self.properties_text)
        
        # Slicer settings tab
        self.slicer_settings_text = tk.Text(slicer_tab, wrap='word', state='disabled', padx=10, pady=10)
        self.slicer_settings_text.pack(expand=True, fill='both')
        text_widgets.append(self.slicer_settings_text)
        
        # Configure tags for consistent styling
        for widget in text_widgets:
            widget.tag_configure('bold', font=('TkDefaultFont', 10, 'bold'))
            widget.tag_configure('normal', font=('TkDefaultFont', 10))

    def update_filament_list(self, filaments: Dict[str, Any]):
        """Update the filament list with the given filament data.
        
        Args:
            filaments: Dictionary mapping filenames to filament data
        """
        self.filament_list.delete(*self.filament_list.get_children())

        # Sort the filaments
        sort_by_key = self.sort_by.lower().replace(' ', '_')
        if sort_by_key == 'filename':
            sort_key_func = lambda item: item[0].lower()
        elif sort_by_key == 'remaining':
            sort_key_func = lambda item: self._safe_float(item[1].get('remaining_quantity', 0))
        else:
            sort_key_func = lambda item: str(item[1].get(sort_by_key, '')).lower()

        sorted_filaments = sorted(filaments.items(), key=sort_key_func, reverse=self.sort_order == 'desc')

        # Add filaments to the list
        for filename, data in sorted_filaments:
            try:
                remaining_qty = float(data.get('remaining_quantity', 0))
                remaining_text = f"{remaining_qty:.1f} g"
            except (ValueError, TypeError):
                remaining_text = tr('not_available')

            self.filament_list.insert(
                '', 'end', iid=filename,
                values=(
                    filename,
                    data.get('brand', ''),
                    data.get('material', ''),
                    data.get('color', ''),
                    remaining_text
                )
            )
        
        # Adjust column widths
        self._adjust_column_widths()

    def update_details_panel(self, data: Dict[str, Any]) -> None:
        """Update the details panel with filament information.
        
        Args:
            data: Dictionary containing filament data
        """
        self.clear_details_panel()

        def _safe_format(value, format_spec: str, default_val: str = tr('not_available')) -> str:
            """Safely format a numeric value with a format specifier.
            
            Args:
                value: The value to format
                format_spec: The format specification string
                default_val: Default value if conversion fails
                
            Returns:
                Formatted string or default value
            """
            try:
                return format(float(value), format_spec)
            except (ValueError, TypeError):
                return default_val

        details_content = (
            f"{tr('detail_brand')}: {data.get('brand', tr('not_available'))}\n"
            f"{tr('detail_material')}: {data.get('material', tr('not_available'))}\n"
            f"{tr('detail_color')}: {data.get('color', tr('not_available'))}\n"
            f"{tr('detail_description')}: {data.get('description', tr('not_available'))}"
        )
        self.details_text.config(state='normal')
        self.details_text.insert('1.0', details_content)
        self.details_text.config(state='disabled')

        properties_content = (
            f"{tr('detail_diameter')}: {_safe_format(data.get('diameter'), '.2f')} mm\n"
            f"{tr('detail_density')}: {_safe_format(data.get('density'), '.2f')} g/cm³\n"
            f"{tr('detail_cost_per_kg')}: ${_safe_format(data.get('cost_per_kg'), '.2f')}\n"
            f"{tr('detail_cost_per_meter')}: ${_safe_format(data.get('cost_per_meter'), '.4f')}\n"
            f"{tr('detail_initial_qty')}: {_safe_format(data.get('initial_quantity'), '.1f')} g\n"
            f"{tr('detail_remaining_qty')}: {_safe_format(data.get('remaining_quantity'), '.1f')} g\n"
            f"{tr('detail_last_used')}: {data.get('last_used', tr('never'))}"
        )
        self.properties_text.config(state='normal')
        self.properties_text.insert('1.0', properties_content)
        self.properties_text.config(state='disabled')

        slicer_content = data.get('slicer_settings', tr('no_slicer_settings'))
        self.slicer_settings_text.config(state='normal')
        self.slicer_settings_text.insert('1.0', slicer_content)
        self.slicer_settings_text.config(state='disabled')

    def clear_details_panel(self):
        """
        Clear all content from the details panel tabs.
        
        Resets the text in all detail tabs to be empty and disabled.
        """
        for widget in [self.details_text, self.properties_text, self.slicer_settings_text]:
            widget.config(state='normal')
            widget.delete('1.0', tk.END)
            widget.config(state='disabled')

    def get_search_query(self) -> str:
        """
        Get the current search query from the search box.
        
        Returns:
            str: The current search text entered by the user.
        """
        return self.search_var.get()

    def _safe_float(self, value):
        """Safely convert a value to float, returning 0.0 on failure.
        
        Args:
            value: The value to convert to float
            
        Returns:
            float: The converted value, or 0.0 if conversion fails
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def _adjust_column_widths(self):
        """Adjust column widths based on content."""
        # Set minimum width based on column header
        for col in self.columns:
            self.filament_list.column(col, width=tkFont.Font().measure(col.title()) + 20)
        
        # Adjust width based on content
        for item in self.filament_list.get_children():
            values = self.filament_list.item(item, 'values')
            for i, value in enumerate(values):
                if i < len(self.columns):
                    col = self.columns[i]
                    width = tkFont.Font().measure(str(value)) + 20
                    if self.filament_list.column(col, 'width') < width:
                        self.filament_list.column(col, width=width)
