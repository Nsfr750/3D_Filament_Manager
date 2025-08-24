"""
Barcode Dialog

This module provides a dialog for barcode generation and scanning.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Callable, Tuple
import os
import barcode
from barcode.writer import ImageWriter
from pathlib import Path
import tempfile
from PIL import Image, ImageTk

class BarcodeDialog(tk.Toplevel):
    """
    A dialog for barcode-related operations.
    
    This dialog provides functionality for:
    - Generating barcodes for filaments
    - Scanning barcodes to identify filaments
    - Managing barcode-filament associations
    """
    
    def __init__(self, parent, on_scan_callback: Optional[Callable] = None):
        """
        Initialize the BarcodeDialog.
        
        Args:
            parent: The parent Tkinter window
            on_scan_callback: Optional callback function when a barcode is scanned
        """
        super().__init__(parent)
        self.transient(parent)
        self.title("Barcode Utility")
        self.parent = parent
        self.on_scan_callback = on_scan_callback
        
        # Dialog properties
        self.geometry("500x300")
        self.resizable(True, True)
        
        # Create UI elements
        self._create_widgets()
        
        # Set focus to the barcode entry
        self.after(100, self.barcode_entry.focus_set)
        
        # Bind Enter key to generate barcode
        self.barcode_entry.bind('<Return>', self._on_generate)
        
        # Center the dialog
        self._center_on_parent()
        
        # Make the dialog modal
        self.grab_set()
        
    def _create_widgets(self):
        """Create and arrange the dialog widgets."""
        # Main container
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barcode input
        input_frame = ttk.LabelFrame(main_frame, text="Barcode Data", padding="5")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Enter barcode text:").pack(side=tk.LEFT, padx=5)
        self.barcode_entry = ttk.Entry(input_frame)
        self.barcode_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.barcode_entry.focus()
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Scan button
        self.scan_btn = ttk.Button(
            btn_frame,
            text=" Scan Barcode",
            command=self._on_scan,
            state=tk.NORMAL
        )
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        generate_btn = ttk.Button(
            btn_frame,
            text=" Generate Barcode",
            command=self._on_generate
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Save button (initially disabled)
        self.save_btn = ttk.Button(
            btn_frame,
            text=" Save Barcode",
            command=self._save_barcode,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Barcode display area with scrollbars
        barcode_frame = ttk.Frame(main_frame)
        barcode_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Add a canvas with scrollbars
        canvas = tk.Canvas(barcode_frame, bd=0, highlightthickness=0)
        vsb = ttk.Scrollbar(barcode_frame, orient="vertical", command=canvas.yview)
        hsb = ttk.Scrollbar(barcode_frame, orient="horizontal", command=canvas.xview)
        
        self.barcode_label = ttk.Label(canvas, anchor=tk.CENTER, justify=tk.CENTER)
        self.barcode_label.pack(fill=tk.BOTH, expand=True)
        
        # Configure the canvas
        canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        canvas.create_window((0, 0), window=self.barcode_label, anchor="nw", tags=("barcode_container",))
        
        # Grid layout
        canvas.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        barcode_frame.columnconfigure(0, weight=1)
        barcode_frame.rowconfigure(0, weight=1)
        
        # Bind mouse wheel for scrolling
        def _on_mousewheel(event):
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")
                
        # Bind to mouse wheel (Windows/Linux)
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Bind to mouse wheel (Linux)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)
        
        # Update scroll region when the barcode image changes
        def _configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        canvas.bind("<Configure>", _configure_canvas)
        
        # Status bar
        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
    def _center_on_parent(self):
        """Center the dialog on the parent window."""
        self.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"+{x}+{y}")
    
    def _on_scan(self):
        """Handle barcode scan event."""
        try:
            # Open file dialog to select an image
            file_path = filedialog.askopenfilename(
                title="Select Barcode Image",
                filetypes=[
                    ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"),
                    ("All files", "*.*")
                ]
            )
            
            if not file_path:
                return  # User cancelled
                
            self.status_label.config(
                text="Scanning barcode...",
                foreground="blue"
            )
            self.update()  # Update UI
            
            # Import pyzbar only when needed
            from pyzbar.pyzbar import decode
            from PIL import Image
            
            # Open and decode the image
            img = Image.open(file_path)
            decoded_objects = decode(img)
            
            if not decoded_objects:
                self.show_error("No barcode found in the selected image")
                return
                
            # Get the first barcode found
            barcode_data = decoded_objects[0].data.decode('utf-8')
            barcode_type = decoded_objects[0].type
            
            # Update the entry field with the scanned barcode
            self.barcode_entry.delete(0, tk.END)
            self.barcode_entry.insert(0, barcode_data)
            
            # Display the scanned barcode image
            self._display_barcode(file_path)
            
            # Call the callback if provided
            if self.on_scan_callback:
                self.on_scan_callback(barcode_data)
                
            self.show_success(f"Scanned {barcode_type} barcode: {barcode_data}")
            
        except ImportError:
            self.show_error("pyzbar library not installed. Install with: pip install pyzbar")
        except Exception as e:
            self.show_error(f"Error scanning barcode: {str(e)}")
    
    def _on_generate(self, event=None):
        """Handle generate barcode event."""
        barcode_text = self.barcode_entry.get().strip()
        if not barcode_text:
            self.show_error("Please enter text to generate barcode")
            return
            
        try:
            self.status_label.config(
                text="Generating barcode...",
                foreground="blue"
            )
            self.update()  # Force UI update
            
            # Generate barcode
            barcode_type = "code128"  # Default barcode type
            barcode_class = barcode.get_barcode_class(barcode_type)
            
            # Create temporary directory for barcode image
            with tempfile.TemporaryDirectory() as temp_dir:
                # Generate barcode
                barcode_instance = barcode_class(barcode_text, writer=ImageWriter())
                
                # Save to temp file
                filename = barcode_instance.save(
                    os.path.join(temp_dir, 'barcode'),
                    options={
                        'write_text': True,
                        'module_width': 0.2,
                        'module_height': 15,
                        'font_size': 10,
                        'text_distance': 5,
                    }
                )
                
                # Load and display the generated barcode
                self._display_barcode(filename)
                
                # Enable save button
                self.save_btn.config(state=tk.NORMAL)
                
                self.show_success("Barcode generated successfully!")
                
        except Exception as e:
            self.show_error(f"Error generating barcode: {str(e)}")
            # self.logger.exception("Barcode generation failed")
    
    def _display_barcode(self, image_path: str):
        """Display the generated barcode image."""
        try:
            # Open and resize the image
            img = Image.open(image_path)
            
            # Calculate new size while maintaining aspect ratio
            max_size = (400, 200)
            img.thumbnail(max_size, Image.LANCZOS)
            
            # Convert to PhotoImage
            self.barcode_image = ImageTk.PhotoImage(img)
            
            # Update the label with the new image
            self.barcode_label.config(image=self.barcode_image)
            self.barcode_label.image = self.barcode_image  # Keep a reference!
            
            # Store the image path for saving
            self._last_barcode_path = image_path
            
        except Exception as e:
            self.show_error(f"Error displaying barcode: {str(e)}")
            # self.logger.exception("Failed to display barcode")
    
    def show_error(self, message: str):
        """Display an error message.
        
        Args:
            message: The error message to display
        """
        self.status_label.config(
            text=message,
            foreground="red"
        )
    
    def _save_barcode(self):
        """Save the generated barcode to a file."""
        if not hasattr(self, '_last_barcode_path') or not self._last_barcode_path:
            self.show_error("No barcode to save")
            return
            
        try:
            # Get save path from user
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg;*.jpeg"),
                    ("All files", "*.*")
                ],
                initialfile="barcode.png"
            )
            
            if save_path:
                # Copy the temporary file to the selected location
                import shutil
                shutil.copy2(self._last_barcode_path, save_path)
                self.show_success(f"Barcode saved to {save_path}")
                
        except Exception as e:
            self.show_error(f"Error saving barcode: {str(e)}")
            self.logger.exception("Failed to save barcode")
    
    def show_success(self, message: str):
        """Display a success message.
        
        Args:
            message: The success message to display
        """
        self.status_label.config(
            text=message,
            foreground="green"
        )
