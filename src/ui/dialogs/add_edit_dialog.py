"""
Add/Edit Filament Dialog

This module provides a dialog for adding new filaments or editing existing ones.
"""
import tkinter as tk
from tkinter import ttk, messagebox

class AddEditDialog(tk.Toplevel):
    """
    A modal dialog for adding new filaments or editing existing ones.
    
    This dialog provides a form with fields for all filament properties including:
    - Basic information (brand, material, color, description)
    - Physical properties (diameter, density)
    - Quantity and cost information
    - Custom slicer settings in a text area
    
    The dialog can be used in two modes:
    1. Add mode: When creating a new filament (filament_data is None)
    2. Edit mode: When modifying an existing filament (filament_data contains current values)
    """

    def __init__(self, parent, controller, title="Add/Edit Filament", filament_data=None, original_filename=None):
        """
        Initialize the Add/Edit Filament dialog.
        
        Args:
            parent: The parent Tkinter window
            controller: The controller that will handle the filament data
            title: Dialog title (default: "Add/Edit Filament")
            filament_data: Dictionary containing existing filament data for editing,
                         or None for creating a new filament
            original_filename: Original filename if editing, None for new filaments
        """
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.controller = controller
        self.filament_data = filament_data or {}
        self.original_filename = original_filename
        self.entries = {}
        self.result = None

        body = ttk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.buttonbox()

        if self.initial_focus:
            self.initial_focus.focus_set()

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+" + str(parent.winfo_rootx() + 50) +
                     "+" + str(parent.winfo_rooty() + 50))
        self.wait_window(self)

    def body(self, master):
        """Create dialog body. Returns the widget that should have initial focus."""
        # Create a notebook for organizing the form into tabs
        notebook = ttk.Notebook(master)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Basic Info Tab
        basic_frame = ttk.Frame(notebook, padding=5)
        notebook.add(basic_frame, text="Basic Info")
        self._create_basic_info_fields(basic_frame)

        # Physical Properties Tab
        props_frame = ttk.Frame(notebook, padding=5)
        notebook.add(props_frame, text="Properties")
        self._create_properties_fields(props_frame)

        # Quantity & Cost Tab
        qty_frame = ttk.Frame(notebook, padding=5)
        notebook.add(qty_frame, text="Quantity & Cost")
        self._create_quantity_fields(qty_frame)

        # Slicer Settings Tab
        slicer_frame = ttk.Frame(notebook, padding=5)
        notebook.add(slicer_frame, text="Slicer Settings")
        self._create_slicer_fields(slicer_frame)

        return next(iter(self.entries.values())) if self.entries else None

    def _create_basic_info_fields(self, parent):
        """Create fields for basic filament information."""
        fields = [
            ("Brand", "brand", ""),
            ("Material", "material", ""),
            ("Color", "color", ""),
            ("Description", "description", ""),
            ("Vendor", "vendor", ""),
            ("Vendor SKU", "vendor_sku", ""),
            ("Purchase Date", "purchase_date", ""),
            ("Purchase Location", "purchase_location", "")
        ]
        
        for i, (label, key, default) in enumerate(fields):
            row = ttk.Frame(parent)
            row.pack(fill=tk.X, padx=5, pady=5)
            ttk.Label(row, text=label + ":").pack(side=tk.LEFT)
            
            entry = ttk.Entry(row)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)
            
            # Set default value if in edit mode
            if self.filament_data and key in self.filament_data:
                entry.insert(0, str(self.filament_data[key]))
            else:
                entry.insert(0, str(default))
                
            self.entries[key] = entry

    def _create_properties_fields(self, parent):
        """Create fields for filament physical properties."""
        fields = [
            ("Diameter (mm)", "diameter", "1.75"),
            ("Density (g/cm³)", "density", "1.24"),
            ("Melting Point (°C)", "melting_point", ""),
            ("Glass Transition Temp. (°C)", "glass_transition_temp", ""),
            ("Tensile Strength (MPa)", "tensile_strength", ""),
            ("Flexural Modulus (MPa)", "flexural_modulus", ""),
            ("Impact Strength (J/m)", "impact_strength", "")
        ]
        
        for i, (label, key, default) in enumerate(fields):
            row = ttk.Frame(parent)
            row.pack(fill=tk.X, padx=5, pady=5)
            ttk.Label(row, text=label + ":").pack(side=tk.LEFT)
            
            entry = ttk.Entry(row)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)
            
            if self.filament_data and key in self.filament_data:
                entry.insert(0, str(self.filament_data[key]))
            else:
                entry.insert(0, str(default))
                
            self.entries[key] = entry

    def _create_quantity_fields(self, parent):
        """Create fields for quantity and cost information."""
        fields = [
            ("Initial Weight (g)", "initial_weight", "1000"),
            ("Remaining Weight (g)", "remaining_weight", "1000"),
            ("Price", "price", ""),
            ("Price per Unit", "price_per_unit", ""),
            ("Currency", "currency", "EUR"),
            ("Purchase URL", "purchase_url", "")
        ]
        
        for i, (label, key, default) in enumerate(fields):
            row = ttk.Frame(parent)
            row.pack(fill=tk.X, padx=5, pady=5)
            ttk.Label(row, text=label + ":").pack(side=tk.LEFT)
            
            entry = ttk.Entry(row)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)
            
            if self.filament_data and key in self.filament_data:
                entry.insert(0, str(self.filament_data[key]))
            else:
                entry.insert(0, str(default))
                
            self.entries[key] = entry

    def _create_slicer_fields(self, parent):
        """Create fields for slicer settings."""
        # Create a frame with a scrollbar for the text area
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add a label
        ttk.Label(frame, text="Custom Slicer Settings (JSON format):").pack(anchor=tk.W)
        
        # Create a Text widget with scrollbars
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        yscroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
        xscroll = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        
        self.slicer_text = tk.Text(
            text_frame,
            wrap=tk.NONE,
            yscrollcommand=yscroll.set,
            xscrollcommand=xscroll.set,
            height=10,
            width=50
        )
        
        yscroll.config(command=self.slicer_text.yview)
        xscroll.config(command=self.slicer_text.xview)
        
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.slicer_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Load existing slicer settings if in edit mode
        if self.filament_data and "slicer_settings" in self.filament_data:
            import json
            try:
                settings = json.dumps(self.filament_data["slicer_settings"], indent=2)
                self.slicer_text.insert(tk.END, settings)
            except (TypeError, ValueError):
                self.slicer_text.insert(tk.END, str(self.filament_data["slicer_settings"]))

    def buttonbox(self):
        """Add standard button box."""
        box = ttk.Frame(self)
        
        ok_btn = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        ok_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        cancel_btn = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.bind("<Return>", lambda event: self.ok())
        self.bind("<Escape>", lambda event: self.cancel())
        
        box.pack()

    def ok(self, event=None):
        """Process the form when OK is clicked."""
        if not self.validate():
            self.initial_focus.focus_set()
            return
            
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        """Close the dialog."""
        if self.master:
            self.master.focus_set()
        self.destroy()

    def validate(self):
        """Validate the form data."""
        # Basic validation - check required fields
        required = ["brand", "material", "diameter", "density"]
        for field in required:
            if field in self.entries and not self.entries[field].get().strip():
                messagebox.showwarning(
                    "Validation Error",
                    f"{field.replace('_', ' ').title()} is a required field.",
                    parent=self
                )
                return False
                
        # Validate numeric fields
        try:
            float(self.entries["diameter"].get())
            float(self.entries["density"].get())
            if self.entries["initial_weight"].get():
                float(self.entries["initial_weight"].get())
            if self.entries["remaining_weight"].get():
                float(self.entries["remaining_weight"].get())
            if self.entries["price"].get():
                float(self.entries["price"].get())
            if self.entries["price_per_unit"].get():
                float(self.entries["price_per_unit"].get())
        except ValueError as e:
            messagebox.showerror(
                "Validation Error",
                "Please enter valid numeric values for all numeric fields.",
                parent=self
            )
            return False
            
        return True

    def apply(self):
        """Process the form data and return the result."""
        result = {}
        
        # Get all values from entry fields
        for key, widget in self.entries.items():
            result[key] = widget.get().strip()
            
        # Get slicer settings from text area
        slicer_text = self.slicer_text.get("1.0", tk.END).strip()
        if slicer_text:
            try:
                import json
                result["slicer_settings"] = json.loads(slicer_text)
            except json.JSONDecodeError:
                # If not valid JSON, store as plain text
                result["slicer_settings"] = slicer_text
        
        # Convert numeric fields
        for key in ["diameter", "density", "initial_weight", "remaining_weight",
                   "price", "price_per_unit"]:
            if key in result and result[key]:
                result[key] = float(result[key])
        
        # Add original filename if in edit mode
        if self.original_filename:
            result["original_filename"] = self.original_filename
            
        self.result = result

    def get_result(self):
        """Return the form data as a dictionary."""
        return self.result
