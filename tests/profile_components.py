import cProfile
import pstats
import os
import sys
import time
from datetime import datetime

def save_profile(pr, name):
    """
    Save profiling results to a file with a timestamp.
    
    This function takes a cProfile.Profile object and saves its data to a .prof file
    in the 'profile_results' directory. The filename includes the provided name
    and a timestamp.
    
    Args:
        pr (cProfile.Profile): The profiler instance containing profiling data
        name (str): Base name to use for the output file
        
    Returns:
        str: The path to the saved profile file
        
    Example:
        >>> pr = cProfile.Profile()
        >>> pr.enable()
        >>> # Code to profile
        >>> pr.disable()
        >>> save_profile(pr, 'my_profile')
    """
    os.makedirs('profile_results', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'profile_results/{name}_{timestamp}.prof'
    pr.dump_stats(filename)
    print(f"Profile saved to {filename}")
    return filename

def print_top_functions(pr, count=20):
    """
    Print the most time-consuming functions from a profile.
    
    This function analyzes profiling data and prints a formatted list of functions
    sorted by cumulative time spent in each function (including subcalls).
    
    Args:
        pr (cProfile.Profile): The profiler instance containing profiling data
        count (int, optional): Number of top functions to display. Defaults to 20.
        
    The output shows for each function:
    - Total number of calls
    - Total time spent in the function (including subcalls)
    - Time per call
    - Cumulative time
    - Function name and location
    """
    s = pstats.Stats(pr, stream=sys.stdout)
    s.sort_stats('cumulative')
    print("\nTop functions by cumulative time:")
    s.print_stats(count)

def profile_filament_operations():
    """
    Profile the performance of filament data loading and management operations.
    
    This function measures and reports on:
    - Time to initialize the FilamentManager
    - Time to load filament data from disk
    - Number of successfully loaded and corrupted filaments
    
    The profiling data is saved to a timestamped .prof file in the 'profile_results'
    directory, and a summary is printed to the console.
    
    Returns:
        FilamentManager: The initialized FilamentManager instance
        
    Example:
        >>> manager = profile_filament_operations()
        # Performs profiling and returns the manager instance
    """
    from src.data.filament_manager import FilamentManager
    
    print("\n" + "="*80)
    print("PROFILING FILAMENT OPERATIONS")
    print("="*80)
    
    # Initialize the manager
    pr = cProfile.Profile()
    pr.enable()
    
    manager = FilamentManager()
    
    # Load filaments
    start = time.time()
    loaded, corrupted = manager.load_filaments()
    load_time = time.time() - start
    
    pr.disable()
    
    print(f"Loaded {loaded} filaments ({corrupted} corrupted) in {load_time:.4f} seconds")
    
    # Save and print profile
    save_profile(pr, 'filament_load')
    print_top_functions(pr)
    
    return manager

def profile_ui_operations():
    """
    Profile the performance of UI initialization and operations.
    
    This function measures and reports on:
    - Time to initialize the main application window
    - Memory usage during UI initialization
    - Performance of UI component creation
    
    The function creates a hidden Tkinter root window to avoid showing the UI
    during profiling. Profiling data is saved to a timestamped .prof file in
    the 'profile_results' directory.
    
    Note:
        This function will create and destroy a Tkinter root window.
        It should not be called from within an existing Tkinter application.
    """
    import tkinter as tk
    from src.app import FilamentManagerApp
    
    print("\n" + "="*80)
    print("PROFILING UI OPERATIONS")
    print("="*80)
    
    # Create root window
    root = tk.Tk()
    root.withdraw()
    
    # Profile app initialization
    pr = cProfile.Profile()
    pr.enable()
    
    start = time.time()
    app = FilamentManagerApp(root)
    init_time = time.time() - start
    
    pr.disable()
    
    print(f"App initialized in {init_time:.4f} seconds")
    
    # Save and print profile
    save_profile(pr, 'app_init')
    print_top_functions(pr)
    
    # Clean up
    root.destroy()

def main():
    """
    Execute all profiling tasks and generate performance reports.
    
    This is the main entry point for the component profiling script. It:
    1. Sets up the Python path to ensure proper module imports
    2. Creates a 'profile_results' directory if it doesn't exist
    3. Runs all defined profiling tasks in sequence
    4. Saves detailed profiling data to disk
    
    The function runs the following profiling tasks:
    - profile_filament_operations(): Profiles filament data loading
    - profile_ui_operations(): Profiles UI initialization
    
    To run a specific profiling task, call the individual function directly.
    """
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Create profile results directory
    os.makedirs('profile_results', exist_ok=True)
    
    # Run the profilers
    profile_filament_operations()
    profile_ui_operations()

if __name__ == "__main__":
    main()
