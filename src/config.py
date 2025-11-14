import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from src.version import __version__, __display_version__
from dataclasses import dataclass, field, asdict
from enum import Enum

# Get the absolute path of the project root directory
# This assumes the script is run from the project's root or the src directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application version (imported from version_info.py)

# Application data directories
APP_DATA_DIR = os.path.join(os.path.expanduser("~"), ".3d_filament_manager")
BACKUP_DIR = os.path.join(APP_DATA_DIR, "backups")
LOG_DIR = os.path.join(APP_DATA_DIR, "logs")
CONFIG_DIR = os.path.join(APP_DATA_DIR, "config")
FDM_DIR = os.path.join(APP_DATA_DIR, "fdm")

# Configuration files
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")

# Ensure all required directories exist
def ensure_directories_exist():
    """Ensure all required application directories exist."""
    os.makedirs(APP_DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(FDM_DIR, exist_ok=True)

# Backup configuration
class BackupFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ON_STARTUP = "on_startup"
    ON_EXIT = "on_exit"
    MANUAL = "manual"

@dataclass
class BackupConfig:
    """Configuration for automatic backups."""
    enabled: bool = True
    frequency: BackupFrequency = BackupFrequency.WEEKLY
    max_backups: int = 10
    include_logs: bool = True
    backup_on_startup: bool = True
    backup_on_exit: bool = True
    last_backup: Optional[str] = None
    backup_dir: str = BACKUP_DIR
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'enabled': self.enabled,
            'frequency': self.frequency.value,
            'max_backups': self.max_backups,
            'include_logs': self.include_logs,
            'backup_on_startup': self.backup_on_startup,
            'backup_on_exit': self.backup_on_exit,
            'last_backup': self.last_backup,
            'backup_dir': self.backup_dir
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackupConfig':
        """Create from dictionary."""
        config = cls()
        for key, value in data.items():
            if hasattr(config, key):
                if key == 'frequency' and value is not None:
                    setattr(config, key, BackupFrequency(value))
                else:
                    setattr(config, key, value)
        return config

# Default settings
DEFAULT_SETTINGS = {
    "dark_mode": True,
    "language": "en",
    "backup": {
        "enabled": True,
        "frequency": "weekly",
        "max_backups": 10,
        "include_logs": True,
        "backup_on_startup": True,
        "backup_on_exit": True,
        "last_backup": None,
        "backup_dir": os.path.join(PROJECT_ROOT, "backups")
    }
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

# Initialize backup config
backup_config = BackupConfig.from_dict(settings.get('backup', {}))

# Application Info
APP_NAME = "3D Filament Manager"
APP_VERSION = get_version()

# Ensure backup directory exists
os.makedirs(backup_config.backup_dir, exist_ok=True)
