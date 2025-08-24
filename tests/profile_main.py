import cProfile
import pstats
import io
import os
import sys
import time
from datetime import datetime

def profile_function(func, *args, **kwargs):
    """Profile a single function call."""
    pr = cProfile.Profile()
    pr.enable()
    
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start_time
    
    pr.disable()
    
    # Create results directory if it doesn't exist
    os.makedirs('profile_results', exist_ok=True)
    
    # Generate profile filename
    func_name = func.__name__
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    profile_file = f'profile_results/{func_name}_{timestamp}.prof'
    
    # Save the raw profile data
    pr.dump_stats(profile_file)
    
    # Generate and print a simple report
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    
    print(f"\n{'='*80}")
    print(f"PROFILING: {func_name}")
    print(f"Time taken: {elapsed:.4f} seconds")
    print(f"{'='*80}")
    
    # Print top 20 functions by cumulative time
    ps.print_stats(20)
    print(s.getvalue())
    
    # Save detailed report
    with open(f'profile_results/{func_name}_report_{timestamp}.txt', 'w') as f:
        f.write(f"Profile report for {func_name}\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Time taken: {elapsed:.4f} seconds\n\n")
        
        # Save top 50 functions by cumulative time
        f.write("TOP 50 FUNCTIONS BY CUMULATIVE TIME\n")
        f.write("="*50 + "\n")
        ps.sort_stats('cumulative').print_stats(50, file=f)
        
        # Save top 50 functions by time per call
        f.write("\n\nTOP 50 FUNCTIONS BY TIME PER CALL\n")
        f.write("="*50 + "\n")
        ps.sort_stats('time').print_stats(50, file=f)
    
    print(f"Profile data saved to {profile_file}")
    print(f"Full report saved to profile_results/{func_name}_report_{timestamp}.txt")
    
    return result

def profile_app():
    """Profile the main application."""
    try:
        # Import the application components
        import tkinter as tk
        from src.app import FilamentManagerApp
        
        # Create a root window
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Profile application initialization
        print("Profiling application initialization...")
        app = profile_function(FilamentManagerApp, root)
        
        # Profile data loading
        if hasattr(app, 'load_initial_data'):
            print("\nProfiling data loading...")
            profile_function(app.load_initial_data)
        
        # Profile theme toggling
        if hasattr(app, 'toggle_theme'):
            print("\nProfiling theme toggle...")
            profile_function(app.toggle_theme)
        
        # Clean up
        root.destroy()
        
    except Exception as e:
        print(f"Error during profiling: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Create profile results directory
    os.makedirs('profile_results', exist_ok=True)
    
    # Run the profiler
    profile_app()
