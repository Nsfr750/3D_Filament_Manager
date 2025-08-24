"""
Price Tracker Dialog

This module provides a dialog for tracking filament prices over time.
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import os
from pathlib import Path

class PriceTrackerDialog(tk.Toplevel):
    """
    A dialog for tracking filament prices over time.
    
    This dialog provides functionality for:
    - Viewing price history for filaments
    - Adding new price entries
    - Analyzing price trends
    - Setting price alerts
    """
    
    def __init__(self, parent, filament_data: Optional[Dict] = None):
        """
        Initialize the PriceTrackerDialog.
        
        Args:
            parent: The parent Tkinter window
            filament_data: Optional dictionary containing filament data
        """
        super().__init__(parent)
        self.transient(parent)
        self.title("Filament Price Tracker")
        self.parent = parent
        self.filament_data = filament_data or {}
        self.price_history = self._load_price_history()
        
        # Dialog properties
        self.geometry("800x600")
        self.resizable(True, True)
        
        # Create UI elements
        self._create_widgets()
        self._update_display()
        
        # Center the dialog
        self._center_on_parent()
        
        # Make the dialog modal
        self.grab_set()
    
    def _create_widgets(self):
        """Create and arrange the dialog widgets."""
        # Main container with notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Price History Tab
        self.history_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.history_frame, text="Price History")
        self._create_history_tab()
        
        # Add Price Tab
        self.add_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.add_frame, text="Add Price")
        self._create_add_tab()
        
        # Analysis Tab
        self.analysis_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.analysis_frame, text="Price Analysis")
        self._create_analysis_tab()
        
        # Close button
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        close_btn = ttk.Button(
            btn_frame,
            text="Close",
            command=self.destroy
        )
        close_btn.pack(side=tk.RIGHT)
    
    def _create_history_tab(self):
        """Create the price history tab."""
        # Treeview for price history
        columns = ("date", "price", "currency", "vendor", "notes")
        self.history_tree = ttk.Treeview(
            self.history_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.history_tree.heading("date", text="Date")
        self.history_tree.heading("price", text="Price")
        self.history_tree.heading("currency", text="Currency")
        self.history_tree.heading("vendor", text="Vendor")
        self.history_tree.heading("notes", text="Notes")
        
        # Set column widths
        self.history_tree.column("date", width=120)
        self.history_tree.column("price", width=80, anchor=tk.E)
        self.history_tree.column("currency", width=80)
        self.history_tree.column("vendor", width=150)
        self.history_tree.column("notes", width=200)
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(
            self.history_frame,
            orient=tk.VERTICAL,
            command=self.history_tree.yview
        )
        x_scroll = ttk.Scrollbar(
            self.history_frame,
            orient=tk.HORIZONTAL,
            command=self.history_tree.xview
        )
        self.history_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Grid layout
        self.history_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        self.history_frame.rowconfigure(0, weight=1)
        self.history_frame.columnconfigure(0, weight=1)
    
    def _create_add_tab(self):
        """Create the add price tab."""
        # Form fields
        fields = [
            ("Price:", "price"),
            ("Currency:", "currency"),
            ("Vendor:", "vendor"),
            ("Notes:", "notes")
        ]
        
        self.entry_vars = {}
        
        # Create form
        for i, (label, field) in enumerate(fields):
            # Label
            ttk.Label(
                self.add_frame,
                text=label
            ).grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)
            
            # Entry
            if field == "notes":
                entry = tk.Text(self.add_frame, width=40, height=4)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky="nsew")
                self.entry_vars[field] = entry
            else:
                var = tk.StringVar()
                entry = ttk.Entry(self.add_frame, textvariable=var, width=40)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                self.entry_vars[field] = var
                
                # Set default currency
                if field == "currency":
                    var.set("EUR")  # Default to Euros
        
        # Add button
        add_btn = ttk.Button(
            self.add_frame,
            text="Add Price Entry",
            command=self._add_price_entry
        )
        add_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        self.add_frame.columnconfigure(1, weight=1)
        self.add_frame.rowconfigure(len(fields), weight=1)
    
    def _create_analysis_tab(self):
        """Create the price analysis tab with price visualization and statistics."""
        # Main container with analysis components
        container = ttk.Frame(self.analysis_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Analysis controls frame
        controls_frame = ttk.LabelFrame(container, text="Analysis Options", padding=10)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Time range selection
        ttk.Label(controls_frame, text="Time Range:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.time_range_var = tk.StringVar(value="6m")
        time_ranges = [
            ("1 Month", "1m"),
            ("3 Months", "3m"),
            ("6 Months", "6m"),
            ("1 Year", "1y"),
            ("All Time", "all")
        ]
        
        for i, (text, value) in enumerate(time_ranges):
            rb = ttk.Radiobutton(
                controls_frame,
                text=text,
                variable=self.time_range_var,
                value=value,
                command=self._update_analysis
            )
            rb.grid(row=0, column=i+1, padx=5, pady=2)
        
        # Analysis type selection
        ttk.Label(controls_frame, text="View:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.analysis_type_var = tk.StringVar(value="trend")
        analysis_types = [
            ("Price Trend", "trend"),
            ("Price Distribution", "distribution"),
            ("Vendor Comparison", "vendor")
        ]
        
        for i, (text, value) in enumerate(analysis_types):
            rb = ttk.Radiobutton(
                controls_frame,
                text=text,
                variable=self.analysis_type_var,
                value=value,
                command=self._update_analysis
            )
            rb.grid(row=1, column=i+1, padx=5, pady=2, sticky=tk.W)
        
        # Canvas for matplotlib figure
        self.analysis_canvas_frame = ttk.Frame(container)
        self.analysis_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(container, text="Price Statistics", padding=10)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Statistics labels
        self.stats_vars = {
            'min': tk.StringVar(value="Min: N/A"),
            'max': tk.StringVar(value="Max: N/A"),
            'avg': tk.StringVar(value="Average: N/A"),
            'last': tk.StringVar(value="Last Price: N/A"),
            'trend': tk.StringVar(value="30-Day Trend: N/A")
        }
        
        for i, (text, var) in enumerate(self.stats_vars.items()):
            ttk.Label(
                stats_frame,
                textvariable=var,
                font=('TkDefaultFont', 9, 'bold')
            ).grid(row=0, column=i, padx=10, pady=5, sticky=tk.W)
        
        # Initialize matplotlib figure
        self._init_plot()
        
        # Initial analysis update
        self._update_analysis()
    
    def _init_plot(self):
        """Initialize the matplotlib plot."""
        try:
            import matplotlib
            matplotlib.use('TkAgg')
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
            
            # Create figure and axis
            self.fig = Figure(figsize=(8, 4), dpi=100)
            self.ax = self.fig.add_subplot(111)
            
            # Create canvas
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.analysis_canvas_frame)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(fill=tk.BOTH, expand=True)
            
            # Initial empty plot
            self.ax.set_title("Price Trend")
            self.ax.set_xlabel("Date")
            self.ax.set_ylabel("Price")
            self.ax.grid(True)
            
        except ImportError:
            ttk.Label(
                self.analysis_canvas_frame,
                text="Matplotlib is required for price analysis.\nPlease install it with: pip install matplotlib",
                justify=tk.CENTER,
                foreground="red"
            ).pack(expand=True)
    
    def _update_analysis(self):
        """Update the analysis based on current selections."""
        if not hasattr(self, 'fig') or not hasattr(self, 'ax'):
            return
            
        # Clear previous plot
        self.ax.clear()
        
        # Get filtered price history
        prices = self._get_filtered_prices()
        
        if not prices:
            self.ax.text(0.5, 0.5, 'No price data available', 
                        horizontalalignment='center',
                        verticalalignment='center',
                        transform=self.ax.transAxes)
            self.canvas.draw()
            return
        
        # Update statistics
        self._update_statistics(prices)
        
        # Update plot based on analysis type
        analysis_type = self.analysis_type_var.get()
        
        if analysis_type == "trend":
            self._plot_price_trend(prices)
        elif analysis_type == "distribution":
            self._plot_price_distribution(prices)
        elif analysis_type == "vendor":
            self._plot_vendor_comparison(prices)
        
        # Redraw canvas
        self.fig.tight_layout()
        self.canvas.draw()
    
    def _get_filtered_prices(self):
        """Get price history filtered by selected time range."""
        if not self.price_history:
            return []
            
        # Get current filament's price history
        filament_id = self._get_filament_id()
        if filament_id not in self.price_history:
            return []
            
        prices = self.price_history[filament_id]
        
        # Apply time range filter
        time_range = self.time_range_var.get()
        if time_range == "all":
            return prices
            
        from datetime import datetime, timedelta
        
        now = datetime.now()
        if time_range == "1m":
            cutoff = now - timedelta(days=30)
        elif time_range == "3m":
            cutoff = now - timedelta(days=90)
        elif time_range == "6m":
            cutoff = now - timedelta(days=180)
        elif time_range == "1y":
            cutoff = now - timedelta(days=365)
        else:
            return prices
        
        return [p for p in prices if datetime.strptime(p['date'], '%Y-%m-%d %H:%M') >= cutoff]
    
    def _update_statistics(self, prices):
        """Update the statistics display."""
        if not prices:
            return
            
        # Calculate statistics
        price_values = [p['price'] for p in prices]
        min_price = min(price_values)
        max_price = max(price_values)
        avg_price = sum(price_values) / len(price_values)
        last_price = prices[-1]['price']
        
        # Calculate 30-day trend if we have enough data
        trend = "N/A"
        if len(prices) > 1:
            from datetime import datetime, timedelta
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_prices = [p for p in prices 
                           if datetime.strptime(p['date'], '%Y-%m-%d %H:%M') >= thirty_days_ago]
            
            if len(recent_prices) > 1:
                first = recent_prices[0]['price']
                last = recent_prices[-1]['price']
                change = ((last - first) / first) * 100
                trend = f"{'↑' if change >= 0 else '↓'} {abs(change):.1f}%"
        
        # Update UI
        self.stats_vars['min'].set(f"Min: {min_price:.2f} {prices[0].get('currency', '')}")
        self.stats_vars['max'].set(f"Max: {max_price:.2f} {prices[0].get('currency', '')}")
        self.stats_vars['avg'].set(f"Avg: {avg_price:.2f} {prices[0].get('currency', '')}")
        self.stats_vars['last'].set(f"Last: {last_price:.2f} {prices[0].get('currency', '')}")
        self.stats_vars['trend'].set(f"30-Day Trend: {trend}")
    
    def _plot_price_trend(self, prices):
        """Plot price trend over time."""
        from datetime import datetime
        
        # Prepare data
        dates = [datetime.strptime(p['date'], '%Y-%m-%d %H:%M') for p in prices]
        price_values = [p['price'] for p in prices]
        
        # Plot
        self.ax.plot(dates, price_values, 'b-', marker='o', markersize=4, linewidth=2)
        self.ax.set_title("Price Trend Over Time")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel(f"Price ({prices[0].get('currency', '')})")
        self.ax.grid(True)
        
        # Format x-axis dates
        self.fig.autofmt_xdate()
    
    def _plot_price_distribution(self, prices):
        """Plot price distribution histogram."""
        price_values = [p['price'] for p in prices]
        
        # Plot histogram
        self.ax.hist(price_values, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
        self.ax.set_title("Price Distribution")
        self.ax.set_xlabel(f"Price ({prices[0].get('currency', '')})")
        self.ax.set_ylabel("Frequency")
        self.ax.grid(True)
    
    def _plot_vendor_comparison(self, prices):
        """Plot price comparison by vendor."""
        from collections import defaultdict
        
        # Group prices by vendor
        vendor_prices = defaultdict(list)
        for p in prices:
            vendor = p.get('vendor', 'Unknown')
            vendor_prices[vendor].append(p['price'])
        
        if not vendor_prices:
            return
        
        # Calculate average price per vendor
        vendors = []
        avg_prices = []
        
        for vendor, vendor_data in vendor_prices.items():
            vendors.append(vendor)
            avg_prices.append(sum(vendor_data) / len(vendor_data))
        
        # Sort by average price
        sorted_data = sorted(zip(avg_prices, vendors))
        avg_prices, vendors = zip(*sorted_data)
        
        # Create bar chart
        y_pos = range(len(vendors))
        self.ax.barh(y_pos, avg_prices, color='skyblue', alpha=0.7)
        self.ax.set_yticks(y_pos)
        self.ax.set_yticklabels(vendors)
        self.ax.set_title("Average Price by Vendor")
        # Get currency from the first price entry in the original prices list
        currency = self.price_history[self._get_filament_id()][0].get('currency', '') if self.price_history.get(self._get_filament_id()) else ''
        self.ax.set_xlabel(f"Average Price ({currency})")
        self.ax.grid(True, axis='x')
    
    def _add_price_entry(self):
        """Add a new price entry to the history."""
        try:
            # Get values from form
            price = float(self.entry_vars["price"].get())
            currency = self.entry_vars["currency"].get().strip()
            vendor = self.entry_vars["vendor"].get().strip()
            notes = self.entry_vars["notes"].get("1.0", tk.END).strip()
            
            # Create entry
            entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "price": price,
                "currency": currency,
                "vendor": vendor,
                "notes": notes
            }
            
            # Add to history
            filament_id = self._get_filament_id()
            if filament_id not in self.price_history:
                self.price_history[filament_id] = []
            self.price_history[filament_id].append(entry)
            
            # Save to file
            self._save_price_history()
            
            # Update display
            self._update_display()
            
            # Clear form
            if "notes" in self.entry_vars:
                self.entry_vars["notes"].delete("1.0", tk.END)
            
            # Switch to history tab
            self.notebook.select(0)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid price: {str(e)}")
    
    def _update_display(self):
        """Update the price history display."""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add items from history
        filament_id = self._get_filament_id()
        if filament_id in self.price_history:
            for entry in self.price_history[filament_id]:
                self.history_tree.insert("", tk.END, values=(
                    entry.get("date", ""),
                    f"{entry.get('price', 0):.2f}",
                    entry.get("currency", ""),
                    entry.get("vendor", ""),
                    entry.get("notes", "")
                ))
    
    def _get_filament_id(self) -> str:
        """Get a unique ID for the current filament."""
        if not self.filament_data:
            return "default"
        
        # Create an ID from the filament's properties
        return f"{self.filament_data.get('brand', '')}_{self.filament_data.get('material', '')}_{self.filament_data.get('color', '')}"
    
    def _load_price_history(self) -> Dict:
        """Load price history from file."""
        history_file = self._get_history_file()
        if not history_file.exists():
            return {}
            
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            messagebox.sharning(
                "Warning",
                f"Could not load price history: {str(e)}"
            )
            return {}
    
    def _save_price_history(self):
        """Save price history to file."""
        history_file = self._get_history_file()
        try:
            with open(history_file, 'w') as f:
                json.dump(self.price_history, f, indent=2)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not save price history: {str(e)}"
            )
    
    def _get_history_file(self) -> Path:
        """Get the path to the price history file."""
        data_dir = Path.home() / ".3d_filament_manager"
        data_dir.mkdir(exist_ok=True)
        return data_dir / "price_history.json"
    
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
