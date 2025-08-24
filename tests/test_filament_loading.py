import os
import sys
import logging
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    # Import FilamentManager after setting up the path
    from data.filament_manager import FilamentManager
    from config import FDM_DIR
    
    logger.info(f"FDM Directory: {FDM_DIR}")
    
    # Check if directory exists
    if not os.path.exists(FDM_DIR):
        logger.error(f"FDM directory does not exist: {FDM_DIR}")
        return
    
    # List files in the directory
    try:
        files = os.listdir(FDM_DIR)
        logger.info(f"Found {len(files)} files in {FDM_DIR}")
        for file in files[:10]:  # Show first 10 files
            logger.info(f"  - {file}")
        if len(files) > 10:
            logger.info(f"  ... and {len(files) - 10} more files")
    except Exception as e:
        logger.error(f"Error listing directory {FDM_DIR}: {e}")
        return
    
    # Initialize FilamentManager
    try:
        logger.info("Initializing FilamentManager...")
        fm = FilamentManager()
        
        # Get all filaments
        filaments = fm.get_all_filaments()
        logger.info(f"Loaded {len(filaments)} filaments")
        
        # Print first few filaments
        for i, (filename, data) in enumerate(filaments.items()):
            if i >= 5:  # Show first 5 filaments
                logger.info(f"  ... and {len(filaments) - 5} more filaments")
                break
            logger.info(f"\nFilament {i+1}:")
            logger.info(f"  Filename: {filename}")
            logger.info(f"  Brand: {data.get('brand', 'N/A')}")
            logger.info(f"  Material: {data.get('material', 'N/A')}")
            logger.info(f"  Color: {data.get('color', 'N/A')}")
            
    except Exception as e:
        logger.error(f"Error initializing FilamentManager: {e}", exc_info=True)

if __name__ == "__main__":
    main()
