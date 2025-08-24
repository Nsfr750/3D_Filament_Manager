import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from src.ui.version import get_version

# Get the absolute path of the project root directory
# This assumes the script is run from the project's root or the src directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Correctly define the path to the filament data directory
FDM_DIR = os.path.join(PROJECT_ROOT, "fdm")

# Define the path for log files
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")

# Default settings
DEFAULT_SETTINGS = {
    "dark_mode": True,
    "language": "en"
}

def load_settings() -> Dict[str, Any]:
    """Load settings from settings.json or create with default values if not exists."""
    try:
        # Create config directory if it doesn't exist
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        if not os.path.exists(SETTINGS_FILE):
            # Create default settings file if it doesn't exist
            save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS.copy()
            
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            
        # Ensure all default settings exist
        updated = False
        for key, value in DEFAULT_SETTINGS.items():
            if key not in settings:
                settings[key] = value
                updated = True
                
        if updated:
            save_settings(settings)
            
        return settings
        
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading settings: {e}")
        return DEFAULT_SETTINGS.copy()

def save_settings(settings: Dict[str, Any]) -> bool:
    """Save settings to settings.json."""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        return True
    except (TypeError, IOError) as e:
        print(f"Error saving settings: {e}")
        return False

def get_setting(key: str, default: Any = None) -> Any:
    """Get a specific setting value by key."""
    settings = load_settings()
    return settings.get(key, default)

def update_setting(key: str, value: Any) -> bool:
    """Update a specific setting and save to file."""
    settings = load_settings()
    if settings.get(key) != value:
        settings[key] = value
        return save_settings(settings)
    return True

# Load settings when module is imported
settings = load_settings()

# Application Info
APP_VERSION = get_version()
