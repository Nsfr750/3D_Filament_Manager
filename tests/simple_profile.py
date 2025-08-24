import cProfile
import pstats
import io
import os
import sys
import time
from datetime import datetime

def time_it(func):
    """Decorator to time function execution."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def profile_app():
    """Run the application with profiling enabled."""
    # CPU Profiling
    pr = cProfile.Profile()
    pr.enable()
    
    try:
        # Import and run the main application
        from src.app import FilamentManagerApp
        import tkinter as tk
        
        # Create the root window
        root = tk.Tk()
        root.title("Profiling 3D Filament Manager")
        
        # Create the application
        print("Creating application...")
        app = FilamentManagerApp(root)
        print("Application created")
        
        # Simulate some common user interactions
        simulate_user_interactions(app)
        
    except Exception as e:
        print(f"Error during profiling: {e}")
    finally:
        # Clean up
        if 'root' in locals() and root.winfo_exists():
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
    """Simulate common user interactions for profiling."""
    print("\nSimulating user interactions...")
    
    # Simulate loading the main window
    print("Updating main window...")
    app.root.update()
    print("- Main window updated")
    
    # Simulate theme toggle if available
    if hasattr(app, 'toggle_theme'):
        print("\nToggling theme...")
        app.toggle_theme()
        app.root.update()
        app.toggle_theme()  # Toggle back
        print("- Theme toggled")
    
    # Simulate language change if available
    if hasattr(app, 'change_language'):
        print("\nChanging languages...")
        for lang in ['en', 'it', 'en']:
            print(f"- Changing to {lang}...")
            app.change_language(lang)
            app.root.update()
    
    # Simulate dialog interactions
    dialogs = [
        ('show_help', 'help_window'),
        ('show_about', 'about_window'),
        ('show_sponsor', 'sponsor_window')
    ]
    
    for method, window_attr in dialogs:
        if hasattr(app, method):
            try:
                print(f"\nOpening {method}...")
                getattr(app, method)()
                window = getattr(app, window_attr, None)
                if window and hasattr(window, 'winfo_exists') and window.winfo_exists():
                    window.destroy()
                print(f"- {method} completed")
            except Exception as e:
                print(f"- Error in {method}: {e}")

def generate_profile_report(profile_file, output_file):
    """Generate a human-readable profile report."""
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

if __name__ == "__main__":
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    profile_app()
