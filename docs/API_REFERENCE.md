# API Reference

This document provides detailed information about the 3D Filament Manager's API, including classes, methods, and their usage.

## Table of Contents
1. [Core Classes](#core-classes)
   - [FilamentManagerApp](#filamentmanagerapp)
   - [FilamentManager](#filamentmanager)
   - [MainWindow](#mainwindow)
2. [Data Models](#data-models)
3. [UI Components](#ui-components)
4. [Utilities](#utilities)

## Core Classes

### FilamentManagerApp

The main application controller class that manages the application lifecycle and coordinates between different components.

**Location**: `src/app.py`

#### Key Methods

```python
def __init__(self, root):
    """
    Initialize the FilamentManager application.
    
    Args:
        root: The root Tkinter window.
    """

def run(self):
    """Start the application main loop."""

def _load_settings(self):
    """Load application settings from settings file."""

def _save_settings(self):
    """Save current settings to file."""

def add_filament(self, filament_data):
    """
    Add a new filament to the inventory.
    
    Args:
        filament_data (dict): Dictionary containing filament properties.
    """

def edit_filament(self, filament_id, new_data):
    """
    Edit an existing filament.
    
    Args:
        filament_id: ID of the filament to edit
        new_data: Dictionary of updated filament properties
    """

def delete_filament(self, filament_id):
    """
    Delete a filament from the inventory.
    
    Args:
        filament_id: ID of the filament to delete
    """
```

### FilamentManager

Handles all data operations related to filament management.

**Location**: `src/data/filament_manager.py`

#### Key Methods

```python
def __init__(self, data_file=None):
    """
    Initialize the FilamentManager.
    
    Args:
        data_file (str, optional): Path to the data file. Defaults to None.
    """

def load_filaments(self):
    """Load filaments from the data file."""

def save_filaments(self):
    """Save current filaments to the data file."""

def get_filament(self, filament_id):
    """
    Get a filament by ID.
    
    Args:
        filament_id: ID of the filament to retrieve
    """

def get_all_filaments(self, filters=None):
    """
    Get all filaments matching optional filters.
    
    Args:
        filters (dict, optional): Dictionary of filters to apply
    """
```

### MainWindow

The main application window class.

**Location**: `src/ui/main_window.py`

#### Key Methods

```python
def __init__(self, root, app):
    """
    Initialize the main window.
    
    Args:
        root: The root Tkinter window
        app: Reference to the main application
    """

def create_widgets(self):
    """Create and arrange all UI elements."""

def update_filament_list(self, filaments=None):
    """
    Update the filament list display.
    
    Args:
        filaments: List of filaments to display. If None, reloads all.
    """

def on_filament_select(self, event):
    """Handle filament selection event."""
```

## Data Models

### Filament

Represents a single filament spool.

**Location**: `src/data/models.py`

#### Properties
- `id`: Unique identifier
- `material`: Material type (PLA, ABS, PETG, etc.)
- `color`: Filament color
- `brand`: Manufacturer brand
- `weight`: Current weight in grams
- `purchase_date`: Date of purchase
- `purchase_price`: Purchase price in local currency
- `notes`: Additional notes

## UI Components

### AddEditDialog

Dialog for adding or editing filament entries.

**Location**: `src/ui/dialogs/add_edit_dialog.py`

### BarcodeDialog

Dialog for barcode scanning functionality.

**Location**: `src/ui/dialogs/barcode_dialog.py`

### PriceTrackerDialog

Dialog for tracking filament prices.

**Location**: `src/ui/dialogs/price_tracker_dialog.py`

## Utilities

### BackupManager

Handles application data backup and restore operations.

**Location**: `src/utils/backup_manager.py`

### ErrorLogger

Manages application error logging.

**Location**: `src/utils/error_logger.py`

### Config

Application configuration and constants.

**Location**: `src/config.py`

---

For more detailed information about specific components, please refer to the source code documentation.
