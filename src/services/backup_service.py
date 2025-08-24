"""
Backup service for managing automatic and manual backups of application data.
"""
import os
import shutil
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path
import json
import zipfile

from src.config import backup_config, PROJECT_ROOT, LOG_DIR, FDM_DIR, CONFIG_DIR, SETTINGS_FILE
from src.utils.error_logger import ErrorLogger
from src.version_info import get_version

class BackupService:
    """
    Service for managing application backups.
    
    Handles both automatic and manual backups, including scheduling,
    retention policies, and restoration of backups.
    """
    
    def __init__(self):
        """Initialize the backup service with configuration."""
        self.logger = logging.getLogger(__name__)
        self.config = backup_config
        self._ensure_backup_dir()
    
    def _ensure_backup_dir(self) -> None:
        """Ensure the backup directory exists."""
        os.makedirs(self.config.backup_dir, exist_ok=True)
    
    def create_backup(self, include_logs: Optional[bool] = None) -> Optional[str]:
        """
        Create a backup of the application data.
        
        Args:
            include_logs: Whether to include log files in the backup.
                         If None, uses the setting from config.
                         
        Returns:
            Path to the created backup file, or None if backup failed.
        """
        try:
            if include_logs is None:
                include_logs = self.config.include_logs
            
            # Create a timestamp for the backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"filament_manager_backup_{timestamp}.zip"
            backup_path = os.path.join(self.config.backup_dir, backup_name)
            
            # Create a temporary directory for the backup
            temp_dir = os.path.join(self.config.backup_dir, f"temp_backup_{timestamp}")
            os.makedirs(temp_dir, exist_ok=True)
            
            try:
                # Copy important directories and files
                self._copy_to_backup(FDM_DIR, temp_dir, 'fdm')
                self._copy_to_backup(CONFIG_DIR, temp_dir, 'config')
                
                if include_logs and os.path.exists(LOG_DIR):
                    self._copy_to_backup(LOG_DIR, temp_dir, 'logs')
                
                # Create a metadata file
                metadata = {
                    'version': get_version(),
                    'backup_date': datetime.now().isoformat(),
                    'include_logs': include_logs,
                    'app_version': get_version(),  # TODO: Import from version
                }
                
                with open(os.path.join(temp_dir, 'backup_metadata.json'), 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                # Create the zip archive
                self._create_zip_archive(temp_dir, backup_path)
                
                # Update the last backup timestamp
                self._update_last_backup(backup_path)
                
                # Clean up old backups if needed
                self._enforce_retention_policy()
                
                self.logger.info(f"Created backup: {backup_path}")
                return backup_path
                
            finally:
                # Clean up the temporary directory
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'create_backup',
                'include_logs': include_logs
            })
            self.logger.error(f"Failed to create backup: {e}")
            return None
    
    def restore_backup(self, backup_path: str, target_dir: Optional[str] = None) -> bool:
        """
        Restore application data from a backup.
        
        Args:
            backup_path: Path to the backup file to restore from.
            target_dir: Directory to restore to. If None, restores to original locations.
            
        Returns:
            True if restoration was successful, False otherwise.
        """
        try:
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"Backup file not found: {backup_path}")
            
            # Create a temporary directory for extraction
            temp_dir = os.path.join(self.config.backup_dir, f"temp_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            os.makedirs(temp_dir, exist_ok=True)
            
            try:
                # Extract the backup
                self._extract_zip_archive(backup_path, temp_dir)
                
                # Read metadata
                metadata_path = os.path.join(temp_dir, 'backup_metadata.json')
                if not os.path.exists(metadata_path):
                    raise ValueError("Invalid backup: missing metadata")
                
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                # Restore each directory
                for item in os.listdir(temp_dir):
                    if item == 'backup_metadata.json':
                        continue
                        
                    src = os.path.join(temp_dir, item)
                    dst = os.path.join(target_dir, item) if target_dir else None
                    
                    if item == 'fdm':
                        self._restore_directory(src, FDM_DIR, dst)
                    elif item == 'config':
                        # Don't restore settings.json to avoid overwriting current settings
                        self._restore_directory(
                            src, 
                            CONFIG_DIR, 
                            dst,
                            exclude_files=['settings.json']
                        )
                    elif item == 'logs' and os.path.exists(LOG_DIR):
                        self._restore_directory(src, LOG_DIR, dst)
                
                self.logger.info(f"Successfully restored backup from {backup_path}")
                return True
                
            finally:
                # Clean up the temporary directory
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'restore_backup',
                'backup_path': backup_path,
                'target_dir': target_dir
            })
            self.logger.error(f"Failed to restore backup: {e}")
            return False
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """
        List all available backups with their metadata.
        
        Returns:
            List of dictionaries containing backup information.
        """
        backups = []
        
        for filename in os.listdir(self.config.backup_dir):
            if filename.startswith('filament_manager_backup_') and filename.endswith('.zip'):
                filepath = os.path.join(self.config.backup_dir, filename)
                stat = os.stat(filepath)
                
                backups.append({
                    'filename': filename,
                    'path': filepath,
                    'size_bytes': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        # Sort by modification time (newest first)
        backups.sort(key=lambda x: x['modified'], reverse=True)
        return backups
    
    def _copy_to_backup(self, src: str, dest_dir: str, dest_name: str) -> None:
        """Copy a file or directory to the backup location."""
        dest_path = os.path.join(dest_dir, dest_name)
        
        if os.path.isfile(src):
            shutil.copy2(src, dest_path)
        elif os.path.isdir(src):
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.copytree(src, dest_path)
    
    def _create_zip_archive(self, source_dir: str, output_path: str) -> None:
        """Create a zip archive from a directory."""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
    
    def _extract_zip_archive(self, zip_path: str, dest_dir: str) -> None:
        """Extract a zip archive to a directory."""
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(dest_dir)
    
    def _restore_directory(self, src: str, dest: str, custom_dest: Optional[str] = None, 
                         exclude_files: Optional[List[str]] = None) -> None:
        """Restore a directory from backup."""
        target = custom_dest or dest
        
        if not os.path.exists(target):
            os.makedirs(target, exist_ok=True)
        
        exclude_files = exclude_files or []
        
        for item in os.listdir(src):
            if item in exclude_files:
                continue
                
            src_path = os.path.join(src, item)
            dest_path = os.path.join(target, item)
            
            if os.path.isdir(src_path):
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
    
    def _update_last_backup(self, backup_path: str) -> None:
        """Update the last backup timestamp in settings."""
        try:
            # Update the in-memory config
            self.config.last_backup = datetime.now().isoformat()
            
            # Update the settings file
            settings = {}
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
            
            if 'backup' not in settings:
                settings['backup'] = {}
                
            settings['backup']['last_backup'] = self.config.last_backup
            
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=4)
                
        except Exception as e:
            self.logger.error(f"Failed to update last backup timestamp: {e}")
    
    def _enforce_retention_policy(self) -> None:
        """Remove old backups according to the retention policy."""
        try:
            backups = self.list_backups()
            max_backups = self.config.max_backups
            
            if len(backups) <= max_backups:
                return
                
            # Sort by modification time (oldest first)
            backups.sort(key=lambda x: x['modified'])
            
            # Remove the oldest backups
            for backup in backups[:-max_backups]:
                try:
                    os.remove(backup['path'])
                    self.logger.info(f"Removed old backup: {backup['path']}")
                except Exception as e:
                    self.logger.error(f"Failed to remove old backup {backup['path']}: {e}")
                    
        except Exception as e:
            ErrorLogger.log_error(e, {'action': 'enforce_retention_policy'})
            self.logger.error(f"Failed to enforce retention policy: {e}")


# Singleton instance
backup_service = BackupService()
