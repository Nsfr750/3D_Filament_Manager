import os
import sys
import logging

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
    # Define the FDM directory path
    fdm_dir = os.path.join(os.path.expanduser("~"), ".3d_filament_manager", "fdm")
    
    logger.info(f"Checking FDM directory: {fdm_dir}")
    
    # Check if directory exists
    if not os.path.exists(fdm_dir):
        logger.error(f"FDM directory does not exist: {fdm_dir}")
        # Try to create the directory
        try:
            os.makedirs(fdm_dir, exist_ok=True)
            logger.info(f"Created FDM directory: {fdm_dir}")
        except Exception as e:
            logger.error(f"Failed to create FDM directory: {e}")
            return
    
    # List files in the directory
    try:
        files = [f for f in os.listdir(fdm_dir) 
                if f.lower().endswith(('.fdm_material', '.xml'))]
        
        logger.info(f"Found {len(files)} filament files in {fdm_dir}")
        
        # Print first 10 files
        for i, file in enumerate(files[:10]):
            file_path = os.path.join(fdm_dir, file)
            file_size = os.path.getsize(file_path) / 1024  # Size in KB
            logger.info(f"  {i+1}. {file} ({file_size:.2f} KB)")
        
        if len(files) > 10:
            logger.info(f"  ... and {len(files) - 10} more files")
        
        # Check if any files are empty
        empty_files = [f for f in files if os.path.getsize(os.path.join(fdm_dir, f)) == 0]
        if empty_files:
            logger.warning(f"Found {len(empty_files)} empty files")
            for file in empty_files[:5]:
                logger.warning(f"  - {file}")
            if len(empty_files) > 5:
                logger.warning(f"  ... and {len(empty_files) - 5} more empty files")
    
    except Exception as e:
        logger.error(f"Error checking FDM directory: {e}")
        return

if __name__ == "__main__":
    main()
