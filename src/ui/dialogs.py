import tkinter as tk
from tkinter import ttk, messagebox

class AddEditDialog(tk.Toplevel):
    """A dialog for adding or editing a filament."""

    def __init__(self, parent, controller, title="Add/Edit Filament", filament_data=None, original_filename=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.controller = controller
        self.filament_data = filament_data
        self.original_filename = original_filename

        self.entries = {}

        body = ttk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=10, pady=10)

        self.buttonbox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry(f"+{(parent.winfo_rootx() + 50)}+{(parent.winfo_rooty() + 50)}")
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        master.columnconfigure(1, weight=1)

        labels = [
            "Brand", "Material", "Color", "Description",
            "Diameter (mm)", "Density (g/cm³)", "Initial Quantity (g)",
            "Used Quantity (g)", "Cost (€/kg)"
        ]

        for i, text in enumerate(labels):
            key = text.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("€/", "").replace("/", "")
            label = ttk.Label(master, text=text + ":")
            label.grid(row=i, column=0, sticky=tk.W, pady=2, padx=(0, 10))
            entry = ttk.Entry(master, width=40)
            entry.grid(row=i, column=1, sticky=tk.EW, pady=2)
            self.entries[key] = entry

        slicer_frame = ttk.LabelFrame(master, text="Slicer Settings")
        slicer_frame.grid(row=len(labels), column=0, columnspan=2, sticky="ew", pady=(10, 0), ipady=5)
        slicer_frame.columnconfigure(0, weight=1)
        slicer_frame.rowconfigure(0, weight=1)
        self.slicer_text = tk.Text(slicer_frame, height=8, width=50, wrap=tk.WORD)
        self.slicer_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        if self.filament_data:
            self._populate_fields()

        return self.entries["brand"]

    def _populate_fields(self):
        # Helper to safely get and convert data to string for UI
        def get_str(key, default=''):
            # Ensure that we handle None gracefully by converting to the default
            value = self.filament_data.get(key)
            if value is None:
                return str(default)
            return str(value)

        self.entries['brand'].insert(0, get_str('brand'))
        self.entries['material'].insert(0, get_str('material'))
        self.entries['color'].insert(0, get_str('color'))
        self.entries['description'].insert(0, get_str('description'))
        self.entries['diameter_mm'].insert(0, get_str('diameter', '1.75'))
        self.entries['density_gcm³'].insert(0, get_str('density', '1.24'))
        self.entries['initial_quantity_g'].insert(0, get_str('initial_quantity', '1000'))
        self.entries['used_quantity_g'].insert(0, get_str('used_quantity', '0'))
        self.entries['cost_kg'].insert(0, get_str('cost_per_kg', '20'))
        
        slicer_settings = self.filament_data.get('slicer_settings', '')
        if slicer_settings:
            self.slicer_text.insert('1.0', slicer_settings)

    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(box, text="Cancel", width=10, command=self.cancel).pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.master.focus_set()
        self.destroy()

    def validate(self):
        for key, entry in self.entries.items():
            if 'quantity' in key or 'cost' in key or 'diameter' in key or 'density' in key:
                try:
                    float(entry.get())
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Please enter a valid number for {key.replace('_', ' ').title()}.")
                    return False
        if not self.entries['brand'].get():
             messagebox.showerror("Invalid Input", "Brand cannot be empty.")
             return False
        return True

    def apply(self):
        # Map widget keys back to data model keys for saving
        key_map = {
            "diameter_mm": "diameter",
            "density_gcm³": "density",
            "initial_quantity_g": "initial_quantity",
            "used_quantity_g": "used_quantity",
            "cost_kg": "cost_per_kg"
        }
        
        data = {}
        for widget_key, entry in self.entries.items():
            # Map to data key, or use original if not in map (e.g., 'brand')
            data_key = key_map.get(widget_key, widget_key)
            data[data_key] = entry.get()
            
        data['slicer_settings'] = self.slicer_text.get('1.0', tk.END).strip()
        self.controller.save_filament(data, self.original_filename)
