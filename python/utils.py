#!/usr/bin/env python3
"""
Common utility functions for OSCAL catalog and mapping generation.
"""

import json
from typing import Dict, List

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is not installed.")
    print("Please install it with: pip install pdfplumber")
    exit(1)


def check_pdfplumber():
    """Check if pdfplumber is installed."""
    try:
        import pdfplumber
        return True
    except ImportError:
        print("Error: pdfplumber is not installed.")
        print("Please install it with: pip install pdfplumber")
        return False


def get_trestle_oscal_version() -> str:
    """
    Get the OSCAL version used by compliance-trestle.
    
    Returns:
        OSCAL version string (e.g., "1.1.2")
    """
    try:
        from trestle.oscal import OSCAL_VERSION
        return OSCAL_VERSION
    except ImportError:
        # Fallback to a default version if trestle is not available
        return "1.1.2"


def load_catalog(catalog_path: str) -> Dict:
    """Load an OSCAL catalog from JSON file."""
    with open(catalog_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict, output_path: str) -> None:
    """Save data to JSON file with proper formatting."""
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def extract_table_from_pdf(pdf_path: str, skip_header_check: str = 'AI RMF') -> List[List[str]]:
    """
    Extract tables from PDF using pdfplumber.
    
    Args:
        pdf_path: Path to the PDF file
        skip_header_check: String to identify header rows to skip
    
    Returns:
        List of table rows, where each row is a list of cell values
    """
    all_rows = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            
            if not tables:
                continue
            
            for table in tables:
                for row in table:
                    if not row or len(row) < 4:
                        continue
                    
                    # Skip header rows
                    if row[0] and skip_header_check in str(row[0]):
                        continue
                    
                    # Skip ISO/IEC header rows
                    if row[2] and ('ISO/IEC' in str(row[2]) or str(row[2]).strip() == 'ISO/IEC FDIS 42001'):
                        continue
                    
                    all_rows.append(row)
    
    return all_rows


def find_control_or_group_in_catalog(catalog: Dict, id_ref: str) -> bool:
    """
    Check if a control or group exists in the catalog.
    
    Args:
        catalog: OSCAL catalog dictionary
        id_ref: Control or group ID to search for
    
    Returns:
        True if found, False otherwise
    """
    groups = catalog.get('catalog', {}).get('groups', [])
    
    def check_groups(groups_list: List[Dict]) -> bool:
        for group in groups_list:
            # Check if this group matches
            if group.get('id') == id_ref:
                return True
            
            # Check controls in this group
            controls = group.get('controls', [])
            for control in controls:
                if control.get('id') == id_ref:
                    return True
            
            # Check nested groups recursively
            nested_groups = group.get('groups', [])
            if nested_groups and check_groups(nested_groups):
                return True
        
        return False
    
    return check_groups(groups)


def get_all_controls_in_group(catalog: Dict, group_id: str) -> List[str]:
    """
    Get all control IDs within a specific group.
    
    Args:
        catalog: OSCAL catalog dictionary
        group_id: Group ID to search for
    
    Returns:
        List of control IDs in the group
    """
    groups = catalog.get('catalog', {}).get('groups', [])
    control_ids = []
    
    def search_groups(groups_list: List[Dict]) -> bool:
        for group in groups_list:
            if group.get('id') == group_id:
                # Found the group, get all its controls
                controls = group.get('controls', [])
                for control in controls:
                    control_ids.append(control.get('id'))
                return True
            
            # Check nested groups
            nested_groups = group.get('groups', [])
            if nested_groups and search_groups(nested_groups):
                return True
        
        return False
    
    search_groups(groups)
    return control_ids


def deduplicate_list_of_dicts(items: List[Dict], key: str) -> List[Dict]:
    """
    Remove duplicates from a list of dictionaries based on a key.
    
    Args:
        items: List of dictionaries
        key: Key to use for deduplication
    
    Returns:
        List with duplicates removed
    """
    seen = {}
    unique_items = []
    
    for item in items:
        item_key = item.get(key)
        if item_key and item_key not in seen:
            seen[item_key] = item
            unique_items.append(item)
    
    return unique_items


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and newlines.
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    return ' '.join(text.split())

# Made with Bob
