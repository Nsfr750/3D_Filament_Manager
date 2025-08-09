import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, List
import tkinter.font as tkFont

from src.ui.lang import tr, get_available_languages, get_language


class MainWindow(ttk.Frame):
    """The main window of the application."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.columns = ("Filename", "Brand", "Material", "Color", "Remaining")
        self.sort_by = 'brand'  # Default sort column
        self.sort_order = 'asc'  # Default sort order
        self.lang_var = tk.StringVar(value=get_language())

        self._create_menu()
        self.setup_ui()

    def _create_menu(self):
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=tr('reload_filaments'), command=self.controller.reload_filaments)
        file_menu.add_command(label=tr('import_filaments'), command=self.controller.import_from_zip)
        file_menu.add_command(label=tr('export_filaments'), command=self.controller.export_to_zip)
        file_menu.add_separator()
        file_menu.add_command(label=tr('exit'), command=self.parent.quit)
        menubar.add_cascade(label=tr('file'), menu=file_menu)

        lang_menu = tk.Menu(menubar, tearoff=0)
        lang_name_map = {'en': 'english', 'it': 'italian'}
        for lang_code in get_available_languages():
            lang_name = tr(lang_name_map.get(lang_code, lang_code))
            lang_menu.add_radiobutton(
                label=lang_name,
                value=lang_code,
                variable=self.lang_var,
                command=lambda: self.controller.change_language(self.lang_var.get())
            )
        menubar.add_cascade(label=tr('language_menu'), menu=lang_menu)


        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_checkbutton(
            label=tr('dark_mode'),
            command=self.controller.toggle_theme,
            variable=tk.BooleanVar(value=getattr(self.controller, 'dark_mode', True))
        )
        menubar.add_cascade(label=tr('view'), menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label=tr('help'), command=self.controller.show_help)
        help_menu.add_command(label=tr('about'), command=self.controller.show_about)
        help_menu.add_command(label=tr('sponsor'), command=self.controller.show_sponsor_dialog)
        menubar.add_cascade(label=tr('help'), menu=help_menu)

    def setup_ui(self):
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self._create_left_panel(main_frame)
        self._create_right_panel(main_frame)

    def _create_left_panel(self, parent):
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
        details_notebook = ttk.Notebook(parent)
        details_notebook.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        details_tab = ttk.Frame(details_notebook)
        properties_tab = ttk.Frame(details_notebook)
        slicer_tab = ttk.Frame(details_notebook)

        details_notebook.add(details_tab, text=tr('details_title'))
        details_notebook.add(properties_tab, text=tr('properties_title'))
        details_notebook.add(slicer_tab, text=tr('slicer_settings'))

        self.details_text = tk.Text(details_tab, wrap='word', state='disabled')
        self.details_text.pack(expand=True, fill='both')

        self.properties_text = tk.Text(properties_tab, wrap='word', state='disabled')
        self.properties_text.pack(expand=True, fill='both')

        self.slicer_settings_text = tk.Text(slicer_tab, wrap='word', state='disabled')
        self.slicer_settings_text.pack(expand=True, fill='both')

    def update_filament_list(self, filaments: Dict[str, Any]):
        self.filament_list.delete(*self.filament_list.get_children())

        sort_by_key = self.sort_by.lower().replace(' ', '_')
        if sort_by_key == 'filename':
            sort_key_func = lambda item: item[0].lower()
        elif sort_by_key == 'remaining':
            sort_key_func = lambda item: self._safe_float(item[1].get('remaining_quantity', 0))
        else:
            sort_key_func = lambda item: str(item[1].get(sort_by_key, '')).lower()

        sorted_filaments = sorted(filaments.items(), key=sort_key_func, reverse=self.sort_order == 'desc')

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
                    remaining_text,
                ))
        self._adjust_column_widths()

    def _adjust_column_widths(self):
        for col in self.columns:
            max_width = tkFont.Font().measure(self.filament_list.heading(col)['text'])
            for item_id in self.filament_list.get_children():
                cell_value = self.filament_list.set(item_id, col)
                required_width = tkFont.Font().measure(str(cell_value))
                if required_width > max_width:
                    max_width = required_width
            self.filament_list.column(col, width=max_width + 20, anchor='w')

    def update_details_panel(self, data: Dict[str, Any]):
        self.clear_details_panel()

        def _safe_format(value, format_spec, default_val=tr('not_available')):
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
        for widget in [self.details_text, self.properties_text, self.slicer_settings_text]:
            widget.config(state='normal')
            widget.delete('1.0', tk.END)
            widget.config(state='disabled')

    def get_search_query(self) -> str:
        return self.search_var.get()

    def _safe_float(self, value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
