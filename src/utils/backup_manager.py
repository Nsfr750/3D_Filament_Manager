"""
Backup manager for 3D Filament Manager.

This module provides functionality for creating and managing automatic backups
of filament data and application settings.
"""
import os
import shutil
import zipfile
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

from src.utils.error_logger import ErrorLogger

class BackupManager:
    """
    Manages automatic and manual backups of filament data and settings.
    
    Features:
    - Create timestamped backup archives
    - Restore from existing backups
    - Automatic backup scheduling
    - Configurable retention policy
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the BackupManager with configuration.
        
        Args:
            config: Dictionary containing backup configuration
        """
        self.config = config or {
            'backup_dir': 'backups',
            'max_backups': 10,
            'auto_backup': True,
            'backup_on_exit': True,
            'include_logs': True
        }
        self.logger = logging.getLogger(__name__)
        
        # Ensure backup directory exists
        os.makedirs(self.config['backup_dir'], exist_ok=True)
    
    def create_backup(self, data_dir: str, include_logs: bool = True) -> str:
        """
        Create a backup of the application data.
        
        Args:
            data_dir: Directory containing data to back up
            include_logs: Whether to include log files in the backup
            
        Returns:
            str: Path to the created backup file
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f'filament_manager_backup_{timestamp}.zip'
            backup_path = os.path.join(self.config['backup_dir'], backup_name)
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add data directory
                for root, _, files in os.walk(data_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(data_dir))
                        zipf.write(file_path, arcname)
                
                # Add logs if requested
                if include_logs and self.config.get('include_logs', True):
                    log_dir = os.path.join('logs')
                    if os.path.exists(log_dir):
                        for log_file in os.listdir(log_dir):
                            log_path = os.path.join(log_dir, log_file)
                            if os.path.isfile(log_path):
                                zipf.write(log_path, f'logs/{log_file}')
                
                # Add metadata
                metadata = {
                    'timestamp': datetime.now().isoformat(),
                    'version': self._get_app_version(),
                    'data_dir': data_dir,
                    'include_logs': include_logs
                }
                zipf.writestr('backup_metadata.json', json.dumps(metadata, indent=2))
            
            self.logger.info(f'Backup created: {backup_path}')
            self._enforce_retention_policy()
            return backup_path
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'create_backup',
                'data_dir': data_dir,
                'include_logs': include_logs
            })
            raise
    
    def restore_backup(self, backup_path: str, target_dir: Optional[str] = None) -> None:
        """
        Restore application data from a backup.
        
        Args:
            backup_path: Path to the backup file to restore from
            target_dir: Directory to restore to (defaults to original location)
        """
        try:
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"Backup file not found: {backup_path}")
            
            # Extract to a temporary directory first
            temp_dir = os.path.join(self.config['backup_dir'], 'temp_restore')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            # Extract the backup
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Read metadata
            metadata_path = os.path.join(temp_dir, 'backup_metadata.json')
            if not os.path.exists(metadata_path):
                raise ValueError("Invalid backup: missing metadata")
                
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            # Determine target directory
            restore_dir = target_dir or metadata.get('data_dir')
            if not restore_dir:
                raise ValueError("Target directory not specified and not found in backup metadata")
            
            # Create backup of current data before restore
            if os.path.exists(restore_dir):
                backup_before_restore = os.path.join(
                    self.config['backup_dir'],
                    f'pre_restore_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                )
                shutil.copytree(restore_dir, backup_before_restore)
                self.logger.info(f"Created pre-restore backup at {backup_before_restore}")
            
            # Restore files
            for item in os.listdir(temp_dir):
                if item == 'backup_metadata.json':
                    continue
                    
                src = os.path.join(temp_dir, item)
                dst = os.path.join(restore_dir, os.path.basename(item))
                
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            
            self.logger.info(f"Successfully restored backup to {restore_dir}")
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'restore_backup',
                'backup_path': backup_path,
                'target_dir': target_dir
            })
            raise
            
        finally:
            # Clean up temporary directory
            if os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    self.logger.error(f"Failed to clean up temporary directory: {e}")
    
    def _enforce_retention_policy(self) -> None:
        """Remove old backups according to the retention policy."""
        try:
            backups = []
            for f in os.listdir(self.config['backup_dir']):
                if f.startswith('filament_manager_backup_') and f.endswith('.zip'):
                    path = os.path.join(self.config['backup_dir'], f)
                    mtime = os.path.getmtime(path)
                    backups.append((mtime, path))
            
            # Sort by modification time (oldest first)
            backups.sort()
            
            # Remove oldest backups if we're over the limit
            max_backups = self.config.get('max_backups', 10)
            while len(backups) > max_backups:
                _, oldest = backups.pop(0)
                try:
                    os.remove(oldest)
                    self.logger.info(f"Removed old backup: {oldest}")
                except Exception as e:
                    self.logger.error(f"Failed to remove old backup {oldest}: {e}")
                    
        except Exception as e:
            ErrorLogger.log_error(e, {'action': 'enforce_retention_policy'})
    
    def _get_app_version(self) -> str:
        """Get the current application version."""
        try:
            from script.version import __version__
            return __version__
        except ImportError:
            return "unknown"


def setup_automatic_backups(config: Optional[Dict[str, Any]] = None) -> BackupManager:
    """
    Set up automatic backup functionality.
    
    Args:
        config: Optional configuration overrides
        
    Returns:
        BackupManager: Configured backup manager instance
    """
    manager = BackupManager(config)
    
    # Set up automatic backup on application start
    if manager.config.get('auto_backup', True):
        try:
            data_dir = os.path.join('data')  # Adjust this to your data directory
            manager.create_backup(data_dir)
        except Exception as e:
            logging.error(f"Failed to create automatic backup: {e}")
    
    return manager
