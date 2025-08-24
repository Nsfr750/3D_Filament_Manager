"""
Dialog windows for the 3D Filament Manager.

This package contains all dialog windows used in the application,
including the backup dialog and any other modal dialogs.
"""

# Import dialogs
from .add_edit_dialog import AddEditDialog
from .backup_dialog import show_backup_dialog
from .price_tracker_dialog import PriceTrackerDialog

# Make barcode dialog optional
BarcodeDialog = None
try:
    from .barcode_dialog import BarcodeDialog
except ImportError:
    import logging
    logging.warning("Barcode module not available. Barcode functionality will be disabled.")

try:
    from .price_tracker_dialog import PriceTrackerDialog
except ImportError as e:
    import logging
    logging.warning(f"Price tracker dialog import failed: {e}")
    PriceTrackerDialog = None

__all__ = [
    'AddEditDialog',
    'show_backup_dialog',
    'BarcodeDialog',
    'PriceTrackerDialog'
]
