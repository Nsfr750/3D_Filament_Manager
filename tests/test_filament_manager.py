import os
import sys
import logging

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
    try:
        # Import FilamentManager after setting up the path
        from data.filament_manager import FilamentManager
        
        logger.info("Initializing FilamentManager...")
        fm = FilamentManager()
        
        # Get all filaments
        filaments = fm.get_all_filaments()
        logger.info(f"Successfully loaded {len(filaments)} filaments")
        
        # Print first 5 filaments
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
        logger.error(f"Error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
