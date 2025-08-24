import cProfile
import pstats
import io
import os
import sys
import time
import psutil
import tracemalloc
from datetime import datetime
from functools import wraps

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def time_it(func):
    """
    Decorator that measures and prints the execution time of the decorated function.
    
    This decorator can be applied to any function to automatically measure and print
    how long the function takes to execute. The timing is printed in seconds with
    microsecond precision.
    
    Args:
        func (callable): The function to be decorated
        
    Returns:
        callable: The wrapped function with timing functionality
        
    Example:
        >>> @time_it
        >>> def example_function():
        ...     # Some time-consuming operations
        ...     return result
        >>> example_function()  # Will print execution time
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def profile_memory():
    """
    Context manager for profiling memory usage of a code block.
    
    This context manager uses tracemalloc to track memory allocations and prints
    a report of the top memory-consuming operations when the block exits.
    
    The report includes:
    - Filename and line number of memory allocations
    - Number of memory blocks allocated
    - Total size of allocated memory
    
    Yields:
        None: The context manager doesn't provide a value
        
    Example:
        >>> with profile_memory():
        ...     # Code to profile memory usage
        ...     data = [0] * 1000000  # Large allocation
    """
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    try:
        yield
    finally:
        snapshot2 = tracemalloc.take_snapshot()
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        print("\nMemory Profile:")
        print("-" * 50)
        for stat in top_stats[:10]:  # Show top 10 memory consumers
            print(stat)
        tracemalloc.stop()

def profile_app():
    """
    Run the 3D Filament Manager application with comprehensive profiling.
    
    This function performs the following profiling tasks:
    1. CPU profiling using cProfile
    2. Memory profiling using tracemalloc
    3. Tracks execution time of key operations
    
    The profiling data is saved to the 'profile_results' directory with timestamps.
    Two files are generated for each run:
    - A binary .prof file for detailed analysis
    - A text report with a summary of the profiling results
    
    The function also simulates common user interactions to profile typical usage
    patterns, including UI updates and theme toggles.
    
    Note:
        This function creates and destroys a Tkinter root window.
    """
    # CPU Profiling
    pr = cProfile.Profile()
    pr.enable()
    
    # Memory Profiling
    with profile_memory():
        # Import and run the main application
        from src.app import FilamentManagerApp
        import tkinter as tk
        
        # Create the root window
        root = tk.Tk()
        root.title("Profiling 3D Filament Manager")
        
        # Create the application
        app = FilamentManagerApp(root)
        
        # Simulate some common user interactions
        simulate_user_interactions(app)
        
        # Clean up
        root.destroy()
    
    pr.disable()
    
    # Create results directory if it doesn't exist
    os.makedirs('profile_results', exist_ok=True)
    
    # Save the raw profile data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    profile_file = f'profile_results/profile_{timestamp}.prof'
    pr.dump_stats(profile_file)
    
    # Generate and save a text report
    generate_profile_report(profile_file, f'profile_results/report_{timestamp}.txt')
    
    print(f"\nProfile data saved to {profile_file}")
    print(f"Profile report saved to profile_results/report_{timestamp}.txt")

@time_it
def simulate_user_interactions(app):
    """
    Simulate a series of common user interactions for performance testing.
    
    This function exercises various parts of the application to profile their
    performance under realistic usage scenarios. It's used in conjunction with
    the profiling tools to identify performance bottlenecks.
    
    The simulation includes:
    - Initial UI rendering
    - Theme toggling (if supported)
    - Language switching (if supported)
    - Window resizing and updates
    
    Args:
        app: The application instance to test
        
    The function prints progress messages to indicate which interactions are being
    simulated. Each interaction is timed using the @time_it decorator.
    """
    print("\nSimulating user interactions...")
    
    # Simulate loading the main window
    app.root.update()
    print("- Main window loaded")
    
    # Simulate theme toggle
    if hasattr(app, 'toggle_theme'):
        print("\nToggling theme...")
        app.toggle_theme()
        app.root.update()
        app.toggle_theme()  # Toggle back
        print("- Theme toggled")
    
    # Simulate language change
    if hasattr(app, 'change_language'):
        print("\nChanging languages...")
        for lang in ['en', 'it', 'en']:
            app.change_language(lang)
            app.root.update()
            print(f"- Changed to {lang}")
    
    # Simulate dialog interactions
    dialogs = [
        ('show_help', 'help_window'),
        ('show_about', 'about_window'),
        ('show_sponsor', 'sponsor_window')
    ]
    
    for method, window_attr in dialogs:
        if hasattr(app, method):
            print(f"\nOpening {method}...")
            getattr(app, method)()
            window = getattr(app, window_attr, None)
            if window and hasattr(window, 'winfo_exists') and window.winfo_exists():
                window.destroy()
            print(f"- {method} completed")

def generate_profile_report(profile_file, output_file):
    """
    Generate a human-readable report from profiling data.
    
    This function processes the binary profiling data and generates a formatted
    text report showing the most significant performance metrics, including:
    - Functions sorted by cumulative time
    - Number of calls per function
    - Time spent in each function
    - Caller/callee relationships
    
    Args:
        profile_file (str): Path to the .prof file containing profiling data
        output_file (str): Path where the report should be saved
        
    The report is designed to help identify performance bottlenecks in the
    application by highlighting the most time-consuming operations.
    """
    s = io.StringIO()
    ps = pstats.Stats(profile_file, stream=s)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        def write_section(title, sort_key='cumulative', limit=30):
            f.write(f"\n{'=' * 80}\n")
            f.write(f"{title.upper()}\n")
            f.write("-" * 80 + "\n")
            ps.sort_stats(sort_key)
            ps.print_stats(limit)
            f.write(s.getvalue())
            s.truncate(0)
            s.seek(0)
        
        # Write header
        f.write("=" * 80 + "\n")
        f.write("3D FILAMENT MANAGER - PROFILING REPORT\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Platform: {sys.platform}\n")
        f.write("=" * 80 + "\n")
        
        # System information
        f.write("\nSYSTEM INFORMATION\n")
        f.write("-" * 80 + "\n")
        f.write(f"CPU Cores: {psutil.cpu_count()}\n")
        f.write(f"Total RAM: {psutil.virtual_memory().total / (1024**3):.2f} GB\n")
        
        # Profile sections
        write_section("TOP FUNCTIONS BY CUMULATIVE TIME", 'cumulative')
        write_section("TOP FUNCTIONS BY TIME PER CALL", 'time')
        write_section("MOST FREQUENTLY CALLED FUNCTIONS", 'calls')
        
        # Callers/callees for top functions
        f.write("\n" + "=" * 80 + "\n")
        f.write("CALL GRAPH FOR TOP FUNCTIONS\n")
        f.write("-" * 80 + "\n")
        
        stats = pstats.Stats(profile_file)
        for func in stats.sort_stats('cumulative').fcn_list[:5]:
            f.write(f"\n{func[2]}\n")
            f.write("-" * len(str(func[2])) + "\n")
            
            f.write("\nCallers:\n")
            ps.print_callers(func[0], func[1], func[2])
            f.write("\nCallees:\n")
            ps.print_callees(func[0], func[1], func[2])
            f.write("\n" + "-" * 80 + "\n")
        
        # Memory usage summary
        f.write("\n" + "=" * 80 + "\n")
        f.write("MEMORY USAGE TIPS\n")
        f.write("-" * 80 + "\n")
        f.write("1. Look for functions with high memory allocation in the call graph\n")
        f.write("2. Check for memory leaks in frequently called functions\n")
        f.write("3. Consider using generators for large datasets\n")
        f.write("4. Look for opportunities to cache expensive computations\n")
        f.write("5. Profile memory usage over time for long-running operations\n")

if __name__ == "__main__":
    profile_app()
