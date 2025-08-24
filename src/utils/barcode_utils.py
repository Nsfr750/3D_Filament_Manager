"""
Barcode and QR code utilities for filament spool tracking.

This module provides functionality for generating and reading barcodes/QR codes
that can be attached to filament spools for easy identification and tracking.
"""
import os
import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from typing import Optional, Tuple, Dict, Any
import logging
from pathlib import Path
import json

from src.utils.error_logger import ErrorLogger

class SpoolBarcode:
    """
    Handles generation and reading of barcodes/QR codes for filament spools.
    """
    
    def __init__(self, output_dir: str = 'barcodes'):
        """
        Initialize the SpoolBarcode generator.
        
        Args:
            output_dir: Directory to save generated barcode images
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def generate_barcode(self, spool_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Generate a barcode for a filament spool.
        
        Args:
            spool_data: Dictionary containing spool data (must be JSON-serializable)
            filename: Optional custom filename (without extension)
            
        Returns:
            str: Path to the generated barcode image
        """
        try:
            # Convert data to JSON string
            data_str = json.dumps(spool_data, sort_keys=True)
            
            # Generate filename if not provided
            if not filename:
                spool_id = spool_data.get('id', 'unknown')
                filename = f"spool_{spool_id}"
            
            # Remove any invalid characters from filename
            filename = "".join(c for c in filename if c.isalnum() or c in ' _-').rstrip()
            
            # Generate barcode
            barcode = Code128(data_str, writer=ImageWriter())
            barcode_path = os.path.join(self.output_dir, filename)
            barcode_path = barcode.save(barcode_path, options={"write_text": False})
            
            self.logger.info(f"Generated barcode: {barcode_path}")
            return barcode_path
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'generate_barcode',
                'spool_data': str(spool_data)[:100]  # Log first 100 chars to avoid huge logs
            })
            raise
    
    def generate_qr_code(self, spool_data: Dict[str, Any], filename: Optional[str] = None, 
                        size: int = 10, border: int = 4) -> str:
        """
        Generate a QR code for a filament spool.
        
        Args:
            spool_data: Dictionary containing spool data (must be JSON-serializable)
            filename: Optional custom filename (without extension)
            size: QR code size (1-40, where 1 is 21x21 modules)
            border: Border size in modules (min 4 for QR codes)
            
        Returns:
            str: Path to the generated QR code image
        """
        try:
            # Convert data to JSON string
            data_str = json.dumps(spool_data, sort_keys=True)
            
            # Generate filename if not provided
            if not filename:
                spool_id = spool_data.get('id', 'unknown')
                filename = f"spool_qr_{spool_id}"
            
            # Remove any invalid characters from filename
            filename = "".join(c for c in filename if c.isalnum() or c in ' _-').rstrip()
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=border,
            )
            qr.add_data(data_str)
            qr.make(fit=True)
            
            # Save QR code
            img = qr.make_image(fill_color="black", back_color="white")
            qr_path = os.path.join(self.output_dir, f"{filename}.png")
            img.save(qr_path)
            
            self.logger.info(f"Generated QR code: {qr_path}")
            return qr_path
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'generate_qr_code',
                'spool_data': str(spool_data)[:100]  # Log first 100 chars to avoid huge logs
            })
            raise
    
    @staticmethod
    def read_barcode(image_path: str) -> Dict[str, Any]:
        """
        Read data from a barcode image.
        
        Note: This is a placeholder. In a real implementation, you would use
        a barcode scanning library like pyzbar, zxing, or a webcam interface.
        
        Args:
            image_path: Path to the barcode image
            
        Returns:
            Dict containing the parsed spool data
            
        Raises:
            NotImplementedError: This is a placeholder method
        """
        raise NotImplementedError("Barcode reading requires additional dependencies. "
                              "Consider using pyzbar or zxing for barcode scanning.")
    
    @staticmethod
    def read_qr_code(image_path: str) -> Dict[str, Any]:
        """
        Read data from a QR code image.
        
        Note: This is a placeholder. In a real implementation, you would use
        a QR code scanning library like pyzbar, zxing, or a webcam interface.
        
        Args:
            image_path: Path to the QR code image
            
        Returns:
            Dict containing the parsed spool data
            
        Raises:
            NotImplementedError: This is a placeholder method
        """
        try:
            import cv2
            from pyzbar.pyzbar import decode
            
            # Read the image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
                
            # Decode QR code
            decoded_objects = decode(img)
            if not decoded_objects:
                raise ValueError("No QR code found in the image")
                
            # Get the first QR code's data
            data = decoded_objects[0].data.decode('utf-8')
            
            # Parse the JSON data
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                # If it's not JSON, return as plain text
                return {'data': data}
                
        except ImportError:
            raise ImportError("QR code reading requires OpenCV and pyzbar. "
                           "Install with: pip install opencv-python pyzbar")
        except Exception as e:
            ErrorLogger.log_error(e, {'action': 'read_qr_code', 'image_path': image_path})
            raise


def generate_spool_label(spool_data: Dict[str, Any], output_format: str = 'barcode',
                        output_dir: str = 'labels') -> str:
    """
    Generate a printable label for a filament spool.
    
    Args:
        spool_data: Dictionary containing spool data
        output_format: 'barcode' or 'qrcode'
        output_dir: Directory to save the generated label
        
    Returns:
        str: Path to the generated label image
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a filename based on spool data
    spool_id = spool_data.get('id', 'unknown')
    material = spool_data.get('material', 'unknown').lower().replace(' ', '_')
    color = spool_data.get('color', 'unknown').lower().replace(' ', '_')
    filename = f"label_{spool_id}_{material}_{color}"
    
    # Generate the code
    spool_barcode = SpoolBarcode(output_dir)
    
    if output_format.lower() == 'qrcode':
        return spool_barcode.generate_qr_code(spool_data, filename)
    else:
        return spool_barcode.generate_barcode(spool_data, filename)
