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

def time_function(func, *args, **kwargs):
    """Time a function and return its result and execution time."""
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start_time
    return result, elapsed

def analyze_filament_loading():
    """Analyze the performance of filament loading."""
    print("\n" + "="*80)
    print("ANALYZING FILAMENT LOADING PERFORMANCE")
    print("="*80)
    
    from src.data.filament_manager import FilamentManager
    
    # 1. Initialize FilamentManager
    manager, init_time = time_function(FilamentManager)
    print(f"\n1. FilamentManager initialization: {init_time:.4f} seconds")
    
    # 2. Load filaments
    (loaded, corrupted), load_time = time_function(manager.load_filaments)
    print(f"2. Loaded {loaded} filaments ({corrupted} corrupted): {load_time:.4f} seconds")
    print(f"   Average time per filament: {load_time/max(1, loaded):.6f} seconds")
    
    # 3. Get all filaments
    filaments, get_time = time_function(manager.get_all_filaments)
    print(f"3. Retrieved {len(filaments)} filaments from memory: {get_time:.6f} seconds")
    
    # 4. Profile search operations
    print("\n4. Search Performance:")
    search_terms = ["pla", "petg", "abs", "tpu", "nylon"]
    
    for term in search_terms:
        start = time.time()
        count = sum(1 for f in filaments.values() 
                   if term in f.get('material', '').lower() or 
                      term in f.get('brand', '').lower() or
                      term in f.get('color', '').lower())
        elapsed = time.time() - start
        print(f"   - Search '{term}': {count} results in {elapsed:.6f} seconds")
    
    return {
        'init_time': init_time,
        'load_time': load_time,
        'get_time': get_time,
        'total_filaments': loaded,
        'corrupted': corrupted
    }

def profile_ui_operations():
    """Profile UI-related operations."""
    print("\n" + "="*80)
    print("PROFILING UI OPERATIONS")
    print("="*80)
    
    import tkinter as tk
    from src.app import FilamentManagerApp
    
    # 1. Create root window
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # 2. Initialize app with profiling
    print("\nProfiling application initialization...")
    pr = cProfile.Profile()
    pr.enable()
    
    app = FilamentManagerApp(root)
    
    pr.disable()
    
    # Print profile results
    s = pstats.Stats(pr)
    s.sort_stats('cumulative')
    print("\nTop 20 functions by cumulative time:")
    s.print_stats(20)
    
    # Clean up
    root.destroy()

def main():
    """Run performance analysis."""
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    print("\n" + "="*80)
    print("3D FILAMENT MANAGER - PERFORMANCE ANALYSIS")
    print("="*80)
    
    # Run filament loading analysis
    metrics = analyze_filament_loading()
    
    # Run UI profiling
    if '--ui' in sys.argv:
        profile_ui_operations()
    
    # Print recommendations
    print("\n" + "="*80)
    print("PERFORMANCE RECOMMENDATIONS")
    print("="*80)
    
    print("\n1. FILAMENT LOADING OPTIMIZATIONS:")
    if metrics['load_time'] > 1.0:
        print("   - Implement lazy loading for filament profiles")
        print("   - Add caching for parsed filament data")
        print(f"   - Consider parallel processing for loading {metrics['total_filaments']} filaments")
    
    print("\n2. MEMORY USAGE OPTIMIZATIONS:")
    print("   - Implement a cache with LRU eviction policy")
    print("   - Load filament data on demand rather than all at once")
    
    print("\n3. UI RESPONSIVENESS:")
    print("   - Move file I/O operations to a background thread")
    print("   - Add loading indicators for long-running operations")
    
    print("\n4. SEARCH PERFORMANCE:")
    print("   - Implement an index for faster searching")
    print("   - Add debouncing for search-as-you-type functionality")

if __name__ == "__main__":
    main()
