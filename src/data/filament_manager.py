import os
import xml.etree.ElementTree as ET
from datetime import datetime
import shutil
import logging
from typing import Dict, Any, Tuple, List, Set, Optional
import zipfile
import math
from collections import defaultdict
from functools import lru_cache
import threading

from ..config import FDM_DIR
from ..utils.error_logger import ErrorLogger

class SearchIndex:
    """
    Handles efficient text search across filament properties.
    
    This class provides full-text search capabilities over filament metadata.
    It indexes specific fields of filament data to enable fast text-based searching.
    
    Attributes:
        term_index: Dictionary mapping search terms to sets of filenames.
        fields: List of filament data fields to index for searching.
    """
    
    def __init__(self):
        self.term_index = defaultdict(set)  # term -> set of filenames
        self.fields = ['material', 'brand', 'color', 'name']
    
    def index_filament(self, filename: str, data: Dict[str, Any]) -> None:
        """
        Index a filament's data for searching.
        
        Extracts text from specified fields of the filament data and adds them
        to the search index.
        
        Args:
            filename: Name of the file containing the filament data.
            data: Dictionary containing the filament's data with fields to index.
        """
        for field in self.fields:
            if field in data and data[field]:
                text = str(data[field]).lower()
                # Split into words and index each one
                for word in text.split():
                    # Remove any non-alphanumeric characters
                    word = ''.join(c for c in word if c.isalnum())
                    if word:  # Only index non-empty words
                        self.term_index[word].add(filename)
    
    def search(self, query: str) -> Set[str]:
        """
        Search for filaments matching the query.
        
        Performs an AND search across all indexed terms in the query.
        
        Args:
            query: Search string containing one or more space-separated terms.
            
        Returns:
            Set of filenames that match all search terms.
        """
        terms = query.lower().split()
        if not terms:
            return set()
        
        # Start with all filenames for first term
        results = self.term_index.get(terms[0], set()).copy()
        
        # Intersect with results for other terms (AND search)
        for term in terms[1:]:
            term_results = self.term_index.get(term, set())
            if not term_results:  # If any term has no matches, return empty
                return set()
            results.intersection_update(term_results)
        
        return results


class FilamentManager:
    """
    Handles loading, parsing, and managing filament data with lazy loading and caching.
    
    This class is responsible for all filament data operations including:
    - Loading and parsing filament data from XML files
    - Caching frequently accessed data for performance
    - Searching and filtering filaments
    - Importing/exporting filament profiles
    
    Attributes:
        logger: Logger instance for recording operations and errors.
        filament_metadata: Dictionary mapping filenames to basic metadata.
        filament_cache: LRU cache of fully parsed filament data.
        search_index: SearchIndex instance for text search.
        cache_size: Maximum number of filaments to keep in memory.
    """

    def __init__(self, cache_size: int = 200):
        """
        Initialize the FilamentManager with an optional cache size.
        
        Args:
            cache_size: Maximum number of fully parsed filaments to cache in memory.
        """
        self.logger = logging.getLogger(__name__)
        self.filament_metadata: Dict[str, Dict[str, Any]] = {}  # filename -> basic metadata
        self.filament_cache: Dict[str, Dict[str, Any]] = {}      # filename -> full data
        self.search_index = SearchIndex()
        self.cache_size = cache_size
        self._lock = threading.RLock()  # For thread safety
        self._load_metadata()  # Fast initial load of just metadata

    def _load_metadata(self) -> Tuple[int, int]:
        """
        Load metadata for all filament files in the FDM directory.
        
        This method is called during initialization and loads only the metadata
        for faster startup. Full filament data is loaded on demand.
        
        Returns:
            Tuple containing (number of successfully loaded filaments,
                            number of corrupted files)
        """
        with self._lock:
            if not os.path.exists(FDM_DIR):
                os.makedirs(FDM_DIR, exist_ok=True)
                self.logger.warning(f"FDM directory created at: {FDM_DIR}. No profiles loaded.")
                return 0, 0

            self.filament_metadata = {}
            corrupted_files = []
            filenames = [f for f in os.listdir(FDM_DIR) 
                        if f.lower().endswith('.fdm_material') or f.lower().endswith('.xml')]
            
            self.logger.info(f"Found {len(filenames)} filament files in {FDM_DIR}.")

            for filename in filenames:
                self.logger.info(f"Processing file: {filename}")
                if not (filename.lower().endswith('.xml') or filename.lower().endswith('.fdm_material')):
                    self.logger.info(f"Skipping non-profile file: {filename}")
                    continue

                filepath = os.path.join(FDM_DIR, filename)
                self.logger.info(f"Attempting to parse: {filepath}")
                metadata = self._parse_metadata(filepath, filename)

                if metadata:
                    self.filament_metadata[filename] = metadata
                    # Index for search
                    self.search_index.index_filament(filename, metadata)
                else:
                    corrupted_files.append((filename, "Failed to parse metadata"))

            loaded_count = len(self.filament_metadata)
            corrupted_count = len(corrupted_files)
            self.logger.info(f"Loaded metadata for {loaded_count} filaments. Corrupted: {corrupted_count}.")
            return loaded_count, corrupted_count
    
    def _parse_metadata(self, filepath: str, filename: str) -> Optional[Dict[str, Any]]:
        """Parse just the metadata from a filament file.
        
        Args:
            filepath: Full path to the filament file
            filename: Just the filename (without path)
            
        Returns:
            Dictionary with metadata or None if parsing failed
        """
        try:
            # Initialize default metadata
            metadata = {
                'filename': filename,
                'path': filepath,
                'brand': '',
                'material': '',
                'color': '',
                'diameter': 1.75,  # Default diameter
                'last_modified': os.path.getmtime(filepath)
            }
            
            # First, try to parse as XML with error handling
            try:
                # Quick parse just the first part of the file for efficiency
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = ''
                    for _ in range(50):  # Only read first 50 lines for metadata
                        line = f.readline()
                        if not line:
                            break
                        content += line
                        if '</metadata>' in line:
                            break
                
                # Try to parse the XML content
                if not content.strip():
                    self.logger.warning(f"Empty file: {filename}")
                    return metadata  # Return minimal metadata for empty files
                
                # Parse just the metadata section with error handling
                try:
                    # Try to find the metadata section
                    metadata_start = content.find('<metadata>')
                    metadata_end = content.find('</metadata>')
                    
                    if metadata_start == -1 or metadata_end == -1:
                        self.logger.warning(f"No metadata section found in {filename}")
                        return metadata  # Return minimal metadata if no metadata section
                        
                    # Extract just the metadata section
                    metadata_xml = content[metadata_start:metadata_end + len('</metadata>')]
                    
                    # Parse the XML
                    root = ET.fromstring(metadata_xml)
                    
                    # Extract basic info from metadata
                    for child in root:
                        if child.tag == 'metadata' or child.tag == 'name':
                            for field in child:
                                if field.tag == 'brand':
                                    metadata['brand'] = field.text or ''
                                elif field.tag == 'material':
                                    metadata['material'] = field.text or ''
                                elif field.tag == 'color':
                                    metadata['color'] = field.text or ''
                                elif field.tag == 'diameter':
                                    try:
                                        metadata['diameter'] = float(field.text or '1.75')
                                    except (ValueError, TypeError):
                                        metadata['diameter'] = 1.75
                    
                    return metadata
                    
                except ET.ParseError as e:
                    self.logger.warning(f"XML parse error in {filename}: {str(e)}")
                    # Fall through to regex parsing
                
                # If we get here, XML parsing failed - try to extract with regex as fallback
                import re
                
                # Try to extract basic info with regex
                brand_match = re.search(r'<brand>(.*?)</brand>', content, re.IGNORECASE | re.DOTALL)
                if brand_match:
                    metadata['brand'] = brand_match.group(1).strip()
                    
                material_match = re.search(r'<material>(.*?)</material>', content, re.IGNORECASE | re.DOTALL)
                if material_match:
                    metadata['material'] = material_match.group(1).strip()
                    
                color_match = re.search(r'<color>(.*?)</color>', content, re.IGNORECASE | re.DOTALL)
                if color_match:
                    metadata['color'] = color_match.group(1).strip()
                    
                diameter_match = re.search(r'<diameter>(.*?)</diameter>', content, re.IGNORECASE | re.DOTALL)
                if diameter_match:
                    try:
                        metadata['diameter'] = float(diameter_match.group(1).strip())
                    except (ValueError, TypeError):
                        pass  # Keep default diameter
                
                return metadata
                
            except Exception as e:
                self.logger.warning(f"Error reading file {filename}: {str(e)}")
                return metadata  # Return minimal metadata on read errors
                
        except Exception as e:
            self.logger.error(f"Unexpected error parsing {filename}: {str(e)}", exc_info=True)
            return None  # Return None for critical errors
                
        except Exception as e:
            self.logger.error(f"Error parsing metadata from {filename}: {e}")
            return None

    def get_filament(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a filament's full data, loading it if not in cache.
        
        Implements lazy loading of filament data with LRU caching.
        
        Args:
            filename: Name of the filament file to retrieve.
            
        Returns:
            Dictionary containing the filament's data, or None if not found.
        """
        with self._lock:
            # Check if we have the full data in cache
            if filename in self.filament_cache:
                return self.filament_cache[filename]
            
            # Check if we have metadata for this file
            if filename not in self.filament_metadata:
                return None
                
            # Load the full data
            filepath = os.path.join(FDM_DIR, filename)
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()
                
                # Parse the full data
                data = self._parse_filament_data(root, filename, filepath)
                if data:
                    # Add to cache (with LRU eviction if needed)
                    if len(self.filament_cache) >= self.cache_size:
                        # Remove the oldest item (FIFO for simplicity)
                        self.filament_cache.pop(next(iter(self.filament_cache)))
                    self.filament_cache[filename] = data
                    return data
            except Exception as e:
                ErrorLogger.log_error(e, {"context": f"Error loading filament {filename}", "filepath": filepath})
            
            return None
    
    def get_all_filaments(self) -> Dict[str, Dict[str, Any]]:
        """
        Retrieve metadata for all available filaments.
        
        This is a fast operation as it only returns pre-loaded metadata.
        
        Returns:
            Dictionary mapping filenames to filament metadata dictionaries.
        """
        return self.filament_metadata.copy()
    
    def get_filament_metadata(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve metadata for a specific filament by filename.
        
        Args:
            filename: Name of the filament file.
            
        Returns:
            Metadata dictionary if found, None otherwise.
        """
        return self.filament_metadata.get(filename)
    
    def search_filaments(self, query: str) -> Dict[str, Dict[str, Any]]:
        """
        Search for filaments matching the given query string.
        
        Performs a case-insensitive search across indexed filament fields.
        
        Args:
            query: Search string to match against filament properties.
            
        Returns:
            Dictionary of {filename: metadata} for matching filaments.
            Returns all filaments if query is empty or whitespace.
        """
        if not query.strip():
            return self.get_all_filaments()
            
        matching_filenames = self.search_index.search(query)
        return {fname: self.filament_metadata[fname] for fname in matching_filenames 
                if fname in self.filament_metadata}
    
    def _parse_filament_data(self, root: ET.Element, filename: str, filepath: str) -> Dict[str, Any]:
        """
        Parse the full filament data from an XML element.
        
        Extracts detailed information including metadata and settings.
        
        Args:
            root: Root XML element of the filament data.
            filename: Name of the source file.
            filepath: Full path to the source file.
            
        Returns:
            Dictionary containing the parsed filament data.
        """
        data = {
            'filename': filename,
            'path': filepath,
            'brand': '',
            'material': '',
            'color': '',
            'diameter': 1.75,
            'settings': {}
        }
        
        def get_text(element, default=''):
            """
            Safely extract text from an XML element.
            
            Args:
                element: XML element to extract text from.
                default: Default value to return if element is None or has no text.
                
            Returns:
                The element's text content or the default value.
            """
            return element.text if element is not None and element.text else default
        
        # Parse metadata
        metadata = root.find('metadata')
        if metadata is not None:
            name = metadata.find('name')
            if name is not None:
                for name_part in name:
                    if name_part.tag == 'brand':
                        data['brand'] = get_text(name_part)
                    elif name_part.tag == 'material':
                        data['material'] = get_text(name_part)
                    elif name_part.tag == 'color':
                        data['color'] = get_text(name_part)
            
            diameter = metadata.find('diameter')
            if diameter is not None:
                try:
                    data['diameter'] = float(get_text(diameter, '1.75'))
                except (ValueError, TypeError):
                    data['diameter'] = 1.75
        
        # Parse settings
        settings = root.find('settings')
        if settings is not None:
            for setting in settings:
                if setting.tag and setting.text:
                    data['settings'][setting.tag] = setting.text
        
        return data

    def save_filament(self, data: Dict[str, Any], original_filename: str = None) -> None:
        """Saves a filament profile to an XML file."""
        with self._lock:
            try:
                root = ET.Element("Filament", {"xmlns": "http://www.prusa3d.com/filament/1.0"})

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

                # Determine filename if not provided
                if not original_filename:
                    brand = data.get('brand', 'unknown').replace(' ', '_').lower()
                    material = data.get('material', 'unknown').replace(' ', '_').lower()
                    color = data.get('color', 'unknown').replace(' ', '_').lower()
                    
                    # Create a base filename
                    base_name = f"{brand}_{material}_{color}"
                    
                    # Clean up the filename
                    filename = "".join(c if c.isalnum() or c in '_-.' else '_' for c in base_name)
                    filename = filename.strip('_') + ".xml.fdm_material"
                    
                    # Ensure the filename is unique
                    counter = 1
                    base = os.path.splitext(filename)[0]  # Remove any existing extension
                    while os.path.exists(os.path.join(FDM_DIR, filename)):
                        filename = f"{base}_{counter}.xml.fdm_material"
                        counter += 1
                else:
                    # Ensure the original filename has the correct extension
                    if not original_filename.endswith('.xml.fdm_material'):
                        base = os.path.splitext(original_filename)[0]
                        filename = f"{base}.xml.fdm_material"
                        
                        # If the new filename already exists, add a counter
                        counter = 1
                        while os.path.exists(os.path.join(FDM_DIR, filename)):
                            filename = f"{base}_{counter}.xml.fdm_material"
                            counter += 1
                    else:
                        filename = original_filename
                        
                    # If we're overwriting, remove from cache
                    if filename in self.filament_cache:
                        del self.filament_cache[filename]

                filepath = os.path.join(FDM_DIR, filename)

                # Write to file
                tree = ET.ElementTree(root)
                ET.indent(tree, space="  ", level=0) # for pretty printing
                tree.write(filepath, encoding="utf-8", xml_declaration=True)
                
                # Update metadata
                metadata = {
                    'filename': filename,
                    'path': filepath,
                    'brand': data.get('brand', ''),
                    'material': data.get('material', ''),
                    'color': data.get('color', ''),
                    'diameter': float(data.get('diameter', 1.75)),
                    'last_modified': os.path.getmtime(filepath)
                }
                self.filament_metadata[filename] = metadata
                self.search_index.index_filament(filename, metadata)
                
                self.logger.info(f"Successfully saved filament profile to {filepath}")

            except Exception as e:
                ErrorLogger.log_error(e, {"context": "Error saving filament profile"})
                # Optionally re-raise or handle it so the UI can be notified
                raise

    def delete_filament(self, filename: str) -> bool:
        """Deletes a filament profile from the filesystem."""
        with self._lock:
            filepath = os.path.join(FDM_DIR, filename)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    # Remove from metadata and cache
                    if filename in self.filament_metadata:
                        del self.filament_metadata[filename]
                    if filename in self.filament_cache:
                        del self.filament_cache[filename]
                    self.logger.info(f"Deleted filament file: {filepath}")
                    return True
                except Exception as e:
                    ErrorLogger.log_error(e, {"context": f"Error deleting filament {filename}", "filepath": filepath})
                    return False
            else:
                self.logger.warning(f"Attempted to delete non-existent file: {filepath}")
                return False

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
