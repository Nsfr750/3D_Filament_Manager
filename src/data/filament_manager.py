import os
import xml.etree.ElementTree as ET
from datetime import datetime
import shutil
import logging
import re
from typing import Dict, Any, Tuple
import zipfile
import math

from src.config import FDM_DIR
from src.utils.error_logger import ErrorLogger

class FilamentManager:
    """Handles loading, parsing, and managing filament data."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.filaments: Dict[str, Dict[str, Any]] = {}

    def load_filaments(self):
        """Load all filament profiles from XML files in the fdm directory."""
        self.logger.info(f"Starting to load filament profiles from {FDM_DIR}...")
        if not os.path.exists(FDM_DIR):
            os.makedirs(FDM_DIR, exist_ok=True)
            self.logger.warning(f"FDM directory created at: {FDM_DIR}. No profiles loaded.")
            return

        self.filaments = {}
        corrupted_files = []

        filenames = os.listdir(FDM_DIR)
        self.logger.info(f"Found {len(filenames)} files/dirs in {FDM_DIR}.")

        for filename in filenames:
            self.logger.info(f"Processing file: {filename}")
            if not (filename.lower().endswith('.xml') or filename.lower().endswith('.fdm_material')):
                self.logger.info(f"Skipping non-profile file: {filename}")
                continue

            filepath = os.path.join(FDM_DIR, filename)
            self.logger.info(f"Attempting to parse: {filepath}")
            success, result = self._parse_xml_file(filepath)

            if not success:
                corrupted_files.append((filename, result))
                self.logger.warning(f"Failed to parse {filename}: {result}")
                continue

            try:
                tree = result
                root = tree.getroot()
                name_elem = root.find('.//{*}name')
                brand = self._get_safe_text(name_elem, 'brand', 'Unknown')
                material = self._get_safe_text(name_elem, 'material', 'Unknown')
                color = self._get_safe_text(name_elem, 'color', 'Unknown')
                description = self._get_safe_text(root, 'description', '')

                props = root.find('.//{*}properties')
                diameter = self._get_safe_text(props, 'diameter', '1.75')
                density = self._get_safe_text(props, 'density', '1.24')

                usage = root.find('.//{*}usage')
                initial_quantity = self._get_safe_float(usage, 'initial_quantity', 1000.0)
                used_quantity = self._get_safe_float(usage, 'used_quantity', 0.0)
                cost_per_kg = self._get_safe_float(usage, 'cost_per_kg', 20.0)
                last_used = self._get_safe_text(usage, 'last_used', datetime.now().strftime("%Y-%m-%d %H:%M"))

                diameter_float = float(diameter)
                density_float = float(density)
                remaining_quantity = max(0.0, initial_quantity - used_quantity)
                cost_per_meter = self.calculate_cost_per_meter(diameter_float, density_float, cost_per_kg)

                self.filaments[filename] = {
                    'brand': brand, 'material': material, 'color': color,
                    'description': description, 'diameter': diameter, 'density': density,
                    'initial_quantity': initial_quantity, 'used_quantity': used_quantity,
                    'remaining_quantity': remaining_quantity, 'cost_per_kg': cost_per_kg,
                    'cost_per_meter': cost_per_meter, 'last_used': last_used,
                    'filename': filename, 'path': filepath, 'tree': tree
                }
                self.logger.info(f"Successfully processed and stored data for {filename}.")

            except Exception as e:
                ErrorLogger.log_error(e, {"context": f"Error processing {filename}"})
                corrupted_files.append((filename, str(e)))

        loaded_count = len(self.filaments)
        corrupted_count = len(corrupted_files)
        self.logger.info(f"Finished loading profiles. Total loaded: {loaded_count}. Corrupted: {corrupted_count}.")
        return loaded_count, corrupted_count

    def _get_safe_text(self, parent_element, tag_name, default=''):
        """Safely get text from a direct child of an XML element, ignoring namespace."""
        if parent_element is None:
            return default
        child = parent_element.find(f'{{*}}{tag_name}')
        if child is not None and child.text:
            return child.text.strip()
        return default

    def _get_safe_float(self, parent_element, tag_name, default=0.0):
        """Safely get a float from a direct child of an XML element, ignoring namespace."""
        text_value = self._get_safe_text(parent_element, tag_name)
        if not text_value:
            return default
        try:
            return float(text_value)
        except (ValueError, TypeError):
            return default

    def calculate_cost_per_meter(self, diameter: float, density: float, cost_per_kg: float) -> float:
        """Calculate the cost per meter of filament."""
        if cost_per_kg == 0:
            return 0.0
        radius_mm = diameter / 2
        radius_m = radius_mm / 1000
        volume_m3 = math.pi * (radius_m ** 2) * 1
        density_kg_m3 = density * 1000
        mass_kg = volume_m3 * density_kg_m3
        cost = mass_kg * cost_per_kg
        return cost

    def _parse_xml_file(self, filepath: str) -> Tuple[bool, Any]:
        try:
            tree = ET.parse(filepath)
            return True, tree
        except Exception as e:
            return False, str(e)

    def get_all_filaments(self) -> Dict[str, Dict[str, Any]]:
        return self.filaments

    def save_filament(self, data: Dict[str, Any], original_filename: str = None) -> None:
        """Saves a filament profile to an XML file."""
        try:
            root = ET.Element("Filament", xmlns="http://www.prusa3d.com/filament/1.0")

            # Helper to create sub-elements
            def create_sub_element(parent, tag, text):
                sub = ET.SubElement(parent, tag)
                sub.text = str(text)
                return sub

            # Name section
            name_elem = ET.SubElement(root, "name")
            create_sub_element(name_elem, "brand", data.get('brand', ''))
            create_sub_element(name_elem, "material", data.get('material', ''))
            create_sub_element(name_elem, "color", data.get('color', ''))

            # Description
            create_sub_element(root, "description", data.get('description', ''))

            # Properties
            props = ET.SubElement(root, "properties")
            create_sub_element(props, "diameter", data.get('diameter', ''))
            create_sub_element(props, "density", data.get('density', ''))

            # Usage
            usage = ET.SubElement(root, "usage")
            create_sub_element(usage, "initial_quantity", data.get('initial_quantity', ''))
            create_sub_element(usage, "used_quantity", data.get('used_quantity', ''))
            create_sub_element(usage, "cost_per_kg", data.get('cost_per_kg', ''))
            create_sub_element(usage, "last_used", datetime.now().strftime("%Y-%m-%d %H:%M"))

            # Settings
            if data.get('slicer_settings'):
                create_sub_element(root, "settings", data['slicer_settings'])

            # Determine filename
            if original_filename:
                filename = original_filename
            else:
                brand = re.sub(r'[^a-zA-Z0-9_]', '', data.get('brand', '')).lower()
                material = re.sub(r'[^a-zA-Z0-9_]', '', data.get('material', '')).lower()
                color = re.sub(r'[^a-zA-Z0-9_]', '', data.get('color', '')).lower()
                filename = f"{brand}_{material}_{color}.xml"
                
                # Ensure filename is unique
                counter = 1
                base_filename = filename
                while os.path.exists(os.path.join(FDM_DIR, filename)):
                    name, ext = os.path.splitext(base_filename)
                    filename = f"{name}_{counter}{ext}"
                    counter += 1

            filepath = os.path.join(FDM_DIR, filename)

            # Write to file
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ", level=0) # for pretty printing
            tree.write(filepath, encoding="utf-8", xml_declaration=True)
            
            self.logger.info(f"Successfully saved filament profile to {filepath}")

        except Exception as e:
            ErrorLogger.log_error(e, {"context": "Error saving filament profile"})
            # Optionally re-raise or handle it so the UI can be notified
            raise

    def delete_filament(self, filename: str):
        """Deletes a filament profile from the filesystem."""
        filepath = os.path.join(FDM_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            self.logger.info(f"Deleted filament file: {filepath}")
            if filename in self.filaments:
                del self.filaments[filename]
        else:
            self.logger.warning(f"Attempted to delete non-existent file: {filepath}")

    def export_to_zip(self, target_path: str):
        """Zips the contents of the FDM_DIR."""
        self.logger.info(f"Exporting filament profiles to {target_path}")
        if not os.path.exists(FDM_DIR) or not os.listdir(FDM_DIR):
            self.logger.warning("FDM directory is empty or does not exist. Nothing to export.")
            raise ValueError("No filament profiles to export.")
        
        with zipfile.ZipFile(target_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(FDM_DIR):
                for file in files:
                    if file.lower().endswith('.xml'):
                        filepath = os.path.join(root, file)
                        zipf.write(filepath, os.path.basename(filepath))
        self.logger.info("Export completed successfully.")

    def import_from_zip(self, source_path: str):
        """Extracts a zip file into the FDM_DIR, overwriting existing files."""
        self.logger.info(f"Importing filament profiles from {source_path}")
        if not os.path.exists(FDM_DIR):
            os.makedirs(FDM_DIR)
        
        with zipfile.ZipFile(source_path, 'r') as zipf:
            zipf.extractall(FDM_DIR)
        self.logger.info("Import completed successfully. Files extracted to FDM directory.")
