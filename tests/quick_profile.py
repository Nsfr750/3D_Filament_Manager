import cProfile
import pstats
import os
import sys
import time
from datetime import datetime

def profile_function(func, *args, **kwargs):
    """
    Profile a function and print detailed performance statistics.
    
    This function uses cProfile to measure the performance of the given function,
    including execution time and detailed call statistics. It prints a formatted
    report showing the most time-consuming parts of the function.
    
    Args:
        func (callable): The function to profile.
        *args: Variable length argument list to pass to the function.
        **kwargs: Arbitrary keyword arguments to pass to the function.
        
    Returns:
        The return value of the profiled function.
        
    Example:
        >>> def example_func(n):
        ...     return sum(range(n))
        >>> profile_function(example_func, 1000000)
    """
    pr = cProfile.Profile()
    pr.enable()
    
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start_time
    
    pr.disable()
    
    # Print basic timing
    print(f"\n{'='*80}")
    print(f"FUNCTION: {func.__name__}")
    print(f"Time taken: {elapsed:.4f} seconds")
    print(f"{'='*80}")
    
    # Print profile stats
    ps = pstats.Stats(pr, stream=sys.stdout)
    ps.sort_stats('cumulative')
    ps.print_stats(20)  # Top 20 functions by cumulative time
    
    return result

def main():
    """
    Main function to run performance profiling on key application components.
    
    This function sets up and executes a series of performance tests on the
    FilamentManager class, including initialization, loading filaments, searching,
    and retrieving filament data. Results are printed to the console.
    
    The profiling includes:
    1. FilamentManager initialization
    2. Loading filament data
    3. Retrieving all filaments
    4. Searching filaments (if any are loaded)
    5. Retrieving a single filament (if available)
    
    Note:
        This function modifies sys.path to ensure proper module imports.
    """
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    print("Profiling 3D Filament Manager...\n")
    
    # 1. Profile FilamentManager initialization
    from src.data.filament_manager import FilamentManager
    
    def init_filament_manager():
        """Initialize a new FilamentManager instance."""
        return FilamentManager()
    
    manager = profile_function(init_filament_manager)
    
    # 2. Profile loading filaments
    def load_filaments():
        """Load all filament data into the manager."""
        return manager.load_filaments()
    
    profile_function(load_filaments)
    
    # 3. Profile getting all filaments
    def get_all_filaments():
        """Retrieve metadata for all filaments."""
        return manager.get_all_filaments()
    
    filaments = profile_function(get_all_filaments)
    
    # 4. Profile searching filaments (if we have some)
    if filaments:
        def search_filaments():
            """Search for filaments matching a query."""
            return manager.search_filaments("PLA")
        
        profile_function(search_filaments)
    
    # 5. Profile getting a single filament
    if filaments:
        sample_filament = next(iter(filaments.values()))
        
        def get_single_filament():
            """Retrieve detailed data for a single filament."""
            return manager.get_filament(sample_filament['filename'])
        
        profile_function(get_single_filament)
    
    print("\nProfiling complete!")

    # 4. Profile UI initialization (if needed)
    if '--ui' in sys.argv:
        import tkinter as tk
        from src.app import FilamentManagerApp
        
        def init_ui():
            """Initialize the UI application."""
            root = tk.Tk()
            root.withdraw()
            return FilamentManagerApp(root)
        
        app = profile_function(init_ui)
        
        # Clean up
        if hasattr(app, 'root'):
            app.root.destroy()

if __name__ == "__main__":
    main()
