"""
Service layer for the 3D Filament Manager.

This package contains service classes that implement business logic and coordinate
between the data layer and the UI layer.
"""

from .backup_service import BackupService

__all__ = ['BackupService']
