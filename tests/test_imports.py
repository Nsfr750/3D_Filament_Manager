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

def test_imports():
    try:
        logger.info("Testing imports...")
        
        # Test basic imports
        import config
        logger.info("✅ Successfully imported config")
        
        from data import filament_manager
        logger.info("✅ Successfully imported filament_manager")
        
        # Test FilamentManager initialization
        fm = filament_manager.FilamentManager()
        logger.info("✅ Successfully created FilamentManager instance")
        
        # Test getting filaments
        filaments = fm.get_all_filaments()
        logger.info(f"✅ Successfully retrieved {len(filaments)} filaments")
        
        # Print first few filaments if available
        if filaments:
            logger.info("\nSample filaments:")
            for i, (filename, data) in enumerate(list(filaments.items())[:3]):
                logger.info(f"{i+1}. {filename}")
                logger.info(f"   Brand: {data.get('brand', 'N/A')}")
                logger.info(f"   Material: {data.get('material', 'N/A')}")
                logger.info(f"   Color: {data.get('color', 'N/A')}")
        
        logger.info("\n✅ All imports and basic functionality tests passed!")
        
    except Exception as e:
        logger.error(f"❌ Error during imports: {e}", exc_info=True)

if __name__ == "__main__":
    test_imports()
