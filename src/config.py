import os
from src.ui.version import get_version

# Get the absolute path of the project root directory
# This assumes the script is run from the project's root or the src directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Correctly define the path to the filament data directory
FDM_DIR = os.path.join(PROJECT_ROOT, "fdm")

# Define the path for log files
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

# Application Info
APP_VERSION = get_version()
