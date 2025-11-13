"""PyInstaller build script for 3D Filament Manager.

This script automates the process of building a Windows executable using PyInstaller.
It handles version management, file cleanup, and proper packaging of assets.
"""

import logging
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

def get_version() -> Tuple[str, str]:
    """Get version information from version_info.py.

    Returns:
        Tuple containing (version_str, display_version)
        where version_str is in format '1.2.3.4' and display_version is a string.
        Returns ('0.0.0', '0.0.0') if version cannot be determined.
    """
    try:
        # Add src directory to path temporarily
        src_dir = Path('src').absolute()
        if not src_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {src_dir}")
            
        sys.path.insert(0, str(src_dir))
        try:
            from version_info import VERSION_INFO  # type: ignore
            
            # Get version from VERSION_INFO
            version = VERSION_INFO['version']
            
            # Ensure version has 4 components (major.minor.patch.build)
            version_parts = version.split('.')
            while len(version_parts) < 4:
                version_parts.append('0')
                
            version_str = '.'.join(version_parts[:4])
            return version_str, version
            
        except ImportError as e:
            logging.warning("Could not import version_info module: %s", e)
        except (KeyError, AttributeError) as e:
            logging.warning("version_info module is missing required attributes: %s", e)
        finally:
            # Remove the src directory from path
            if src_dir in sys.path:
                sys.path.remove(str(src_dir))
                
    except Exception as e:
        logging.error("Error getting version: %s", e, exc_info=True)
        
    # Fallback version
    return "1.2.0.0", "1.2.0"

def create_spec_file(version_str: str, display_version: str) -> None:
    """Create PyInstaller spec file with proper configuration.
    
    Args:
        version_str: Version string in format '1.2.3.4'
        display_version: Human-readable version string
        
    Raises:
        IOError: If spec file or version file cannot be written
    """
    # Data files to include with proper path handling
    datas: List[str] = []
    
    # Add assets if they exist
    assets_path = Path('src/assets/logo.png')
    if assets_path.exists():
        datas.append(f"('{assets_path.as_posix()}', 'assets')")
    
    # Add config files if directory exists
    config_path = Path('config')
    if config_path.is_dir() and any(config_path.glob('*.json')):
        datas.append("('config/*.json', 'config')")
    
    # Add FDM materials if directory exists
    fdm_path = Path('fdm')
    if fdm_path.is_dir():
        datas.append("('fdm/*', 'fdm')")
    
    # Add language files if the directory exists and contains JSON files
    lang_path = Path('lang')
    if lang_path.is_dir() and any(lang_path.glob('*.json')):
        datas.append("('lang/*.json', 'lang')")
    
    # Format the datas list as a string for the spec file
    datas_str = ',\n        '.join(datas)
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[
        {datas_str}
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.colorchooser',
        'tkinter.filedialog',
        'src',
        'src.ui',
        'src.utils',
        'lxml',
        'lxml.etree'
    ],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FDM-Mgr-{display_version}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/logo.png',
    version='version.txt',
    uac_admin=False,
)
"""
    # Create version file for Windows
    try:
        version_parts = [int(part) for part in version_str.split('.')[:4]]
        while len(version_parts) < 4:
            version_parts.append(0)
        version_tuple = tuple(version_parts)
        
        # Create version.txt content
        version_txt = f"""# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({version_tuple[0]}, {version_tuple[1]}, {version_tuple[2]}, {version_tuple[3]}),
    prodvers=({version_tuple[0]}, {version_tuple[1]}, {version_tuple[2]}, {version_tuple[3]}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '040904B0',
          [StringStruct('CompanyName', 'Tuxxle'),
           StringStruct('FileDescription', 'A tool for managing 3D FDM Filaments.'),
           StringStruct('FileVersion', '{version_str}'),
           StringStruct('InternalName', '3D Filament Manager'),
           StringStruct('LegalCopyright', '© 2024-2025 Nsfr750'),
           StringStruct('OriginalFilename', 'FDM-Mgr-{display_version}.exe'),
           StringStruct('ProductName', '3D Filament Manager'),
           StringStruct('ProductVersion', '{display_version}')])
      ]
    ),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)"""
        
        # Write version info to version.txt
        with open('version.txt', 'w', encoding='utf-8') as f:
            f.write(version_txt)
            
        logging.info("Created version.txt with version: %s", version_str)
        
        # Also create a simple version file for PyInstaller
        with open('VERSION', 'w', encoding='utf-8') as f:
            f.write(version_str)
        
        # Update spec content to include version.txt in the build
        spec_content = spec_content.replace(
            "version='version.txt',",
            "version='version.txt',\n    version_file='version.txt',"
        )
        
        # Write spec file
        with open('FDM-Mgr.spec', 'w', encoding='utf-8') as f:
            f.write(spec_content)
        logging.info("Created FDM-Mgr.spec")
        
    except Exception as e:
        error_msg = f"Error creating version or spec file: {e}"
        logging.error(error_msg)
        raise ValueError(error_msg) from e

def setup_logging() -> None:
    """Configure logging for the build process."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('build.log', mode='w', encoding='utf-8')
        ]
    )


def remove_readonly_files(func, path: str, _) -> None:
    """Remove readonly attribute and retry the operation.
    
    Args:
        func: Function to retry (usually os.unlink or os.rmdir)
        path: Path to the file or directory
        _: Unused parameter (required by shutil.rmtree)
    """
    try:
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
        func(path)
        logging.debug("Removed: %s", path)
    except Exception as e:
        logging.warning("Could not remove %s: %s", path, e)


def clean_directory(directory: Path) -> None:
    """Clean a directory by removing all its contents.
    
    Args:
        directory: Path to the directory to clean
    """
    if not directory.exists():
        logging.debug("Directory does not exist, skipping cleanup: %s", directory)
        return
        
    logging.info("Cleaning directory: %s", directory)
    for item in directory.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.chmod(stat.S_IWRITE | stat.S_IREAD)
                item.unlink()
                logging.debug("Removed file: %s", item)
            elif item.is_dir():
                shutil.rmtree(item, onerror=remove_readonly_files, ignore_errors=True)
                logging.debug("Removed directory: %s", item)
        except Exception as e:
            logging.warning("Could not remove %s: %s", item, e)


def ensure_directories() -> Tuple[Path, Path]:
    """Ensure required directories exist.
    
    Returns:
        Tuple of (build_dir, dist_dir) Path objects
    """
    required_dirs = [
        Path('config'),
        Path('logs'),
        Path('build'),
        Path('dist')
    ]
    
    for directory in required_dirs:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            logging.debug("Ensured directory exists: %s", directory)
        except OSError as e:
            logging.error("Failed to create directory %s: %s", directory, e)
            raise
    
    return Path('build'), Path('dist')


def run_pyinstaller() -> bool:
    """Run PyInstaller with the generated spec file.
    
    Returns:
        bool: True if PyInstaller completed successfully, False otherwise
    """
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "FDM-Mgr.spec"
    ]
    
    logging.info("Starting PyInstaller build...")
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        logging.debug("PyInstaller output:\n%s", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.error("PyInstaller failed with exit code %d", e.returncode)
        logging.error("PyInstaller stderr:\n%s", e.stderr)
        return False
    except Exception as e:
        logging.error("Error running PyInstaller: %s", str(e), exc_info=True)
        return False


def cleanup_temp_files() -> None:
    """Clean up temporary files after build."""
    temp_files = [
        Path('version.txt'),
        Path('FDM-Mgr.spec')
    ]
    
    for temp_file in temp_files:
        try:
            if temp_file.exists():
                temp_file.unlink()
                logging.debug("Removed temporary file: %s", temp_file)
        except Exception as e:
            logging.warning("Could not remove %s: %s", temp_file, e)


def main() -> None:
    """Main build function."""
    setup_logging()
    logging.info("Starting FDM-Mgr build process")
    
    try:
        # Ensure required directories exist
        build_dir, dist_dir = ensure_directories()
        
        # Clean previous builds
        clean_directory(build_dir)
        clean_directory(dist_dir)
        
        # Get version information
        version_str, display_version = get_version()
        logging.info("Building version: %s (build: %s)", display_version, version_str)
        
        # Create spec file
        logging.info("Creating PyInstaller spec file...")
        create_spec_file(version_str, display_version)
        
        # Run PyInstaller
        if run_pyinstaller():
            logging.info("Build completed successfully!")
            logging.info("Output directory: %s", dist_dir.absolute())
            print(f"\nBuild completed successfully!\nOutput directory: {dist_dir.absolute()}")
            return 0
        else:
            logging.error("Build failed!")
            print("\nBuild failed! Check build.log for details.")
            return 1
            
    except Exception as e:
        error_msg = f"Build failed: {str(e)}"
        logging.error(error_msg, exc_info=True)
        print(f"\n{error_msg}")
        return 1
    finally:
        # Always clean up temporary files
        cleanup_temp_files()
        logging.info("Build process completed")

if __name__ == "__main__":
    main()
