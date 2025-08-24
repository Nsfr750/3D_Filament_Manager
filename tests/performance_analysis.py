import os
import sys
import time
import cProfile
import pstats
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceAnalyzer:
    """Analyze performance of key application components."""
    
    def __init__(self):
        self.results = {}
        self.start_time = None
        self.profiler = cProfile.Profile()
        
    def start_timer(self):
        """Start the performance timer."""
        self.start_time = time.time()
        
    def measure_section(self, name: str):
        """Measure time taken for a section of code."""
        if self.start_time is None:
            self.start_timer()
            return
            
        elapsed = time.time() - self.start_time
        self.results[name] = elapsed
        logger.info(f"{name}: {elapsed:.4f} seconds")
        self.start_timer()
        
    def profile_function(self, func, *args, **kwargs):
        """Profile a function and return its result and stats."""
        self.profiler.enable()
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            # Get stats
            s = io.StringIO()
            ps = pstats.Stats(self.profiler, stream=s).sort_stats('cumulative')
            ps.print_stats(10)  # Top 10 functions
            stats = s.getvalue()
            
            return result, elapsed, stats
            
        finally:
            self.profiler.disable()
            self.profiler.clear()

def analyze_filament_loading():
    """Analyze the performance of filament loading."""
    from src.data.filament_manager import FilamentManager
    from src.config import FDM_DIR
    
    analyzer = PerformanceAnalyzer()
    
    # 1. Initialize FilamentManager
    analyzer.start_timer()
    manager = FilamentManager()
    analyzer.measure_section("FilamentManager initialization")
    
    # 2. Load filaments
    loaded, corrupted = manager.load_filaments()
    analyzer.measure_section(f"Loaded {loaded} filaments ({corrupted} corrupted)")
    
    # 3. Get all filaments
    filaments = manager.get_all_filaments()
    analyzer.measure_section(f"Retrieved {len(filaments)} filaments from memory")
    
    # 4. Search performance
    import random
    search_terms = ["pla", "petg", "abs", "tpu", "nylon"]
    
    for term in search_terms:
        start = time.time()
        count = sum(1 for f in filaments.values() 
                   if term in f.get('material', '').lower() or 
                      term in f.get('brand', '').lower() or
                      term in f.get('color', '').lower())
        elapsed = time.time() - start
        logger.info(f"Search for '{term}' found {count} results in {elapsed:.6f}s")
    
    return analyzer.results

def analyze_ui_performance():
    """Analyze the performance of UI components."""
    import tkinter as tk
    from src.app import FilamentManagerApp
    
    analyzer = PerformanceAnalyzer()
    
    # 1. Create root window
    analyzer.start_timer()
    root = tk.Tk()
    root.withdraw()  # Hide the window
    analyzer.measure_section("Created Tk root window")
    
    # 2. Initialize app
    app = FilamentManagerApp(root)
    analyzer.measure_section("Initialized FilamentManagerApp")
    
    # 3. Load initial data
    app.load_initial_data()
    analyzer.measure_section("Loaded initial data")
    
    # Clean up
    root.destroy()
    
    return analyzer.results

def main():
    """Run performance analysis."""
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    print("="*80)
    print("3D FILAMENT MANAGER - PERFORMANCE ANALYSIS")
    print("="*80)
    
    # Run analyses
    print("\nANALYZING FILAMENT LOADING PERFORMANCE")
    print("-"*60)
    loading_metrics = analyze_filament_loading()
    
    print("\nANALYZING UI PERFORMANCE")
    print("-"*60)
    ui_metrics = analyze_ui_performance()
    
    # Print summary
    print("\n" + "="*80)
    print("PERFORMANCE SUMMARY")
    print("="*80)
    
    print("\nFILAMENT LOADING:")
    for name, time_taken in loading_metrics.items():
        print(f"  {name}: {time_taken:.4f} seconds")
    
    print("\nUI INITIALIZATION:")
    for name, time_taken in ui_metrics.items():
        print(f"  {name}: {time_taken:.4f} seconds")
    
    print("\nRECOMMENDATIONS:")
    print("1. Optimize filament loading by implementing lazy loading")
    print("2. Add caching for frequently accessed filament data")
    print("3. Profile search functionality with larger datasets")
    print("4. Consider implementing background loading for UI elements")

if __name__ == "__main__":
    import io  # For StringIO in profile_function
    main()
