#!/usr/bin/env python3
"""
Extract ISO/IEC 42001 controls from NIST AI RMF crosswalk PDF
and create an OSCAL catalog using pdfplumber for proper table extraction.
"""

import json
from datetime import datetime, timezone
from typing import List, Dict
import uuid

from utils import (
    check_pdfplumber,
    extract_table_from_pdf,
    deduplicate_list_of_dicts,
    clean_text,
    save_json,
    get_trestle_oscal_version
)

if not check_pdfplumber():
    exit(1)


def extract_controls_from_pdf(pdf_path: str) -> List[Dict[str, str]]:
    """
    Extract ISO controls from PDF using pdfplumber to properly parse the table.
    The PDF has 4 columns:
    1. RMF ID (e.g., "Govern 1.1")
    2. RMF Description
    3. ISO Control Number (e.g., "4.1", "B.2.2")
    4. ISO Control Name
    """
    controls = []
    rows = extract_table_from_pdf(pdf_path)
    
    for row in rows:
        col1, col2, col3, col4 = row[0], row[1], row[2], row[3]
        
        # Extract ISO control if column 3 has data
        if col3 and col3.strip():
            control_num = col3.strip()
            control_name = col4.strip() if col4 else ""
            
            # Clean control name: remove newlines and extra whitespace
            clean_title = clean_text(control_name)
            
            controls.append({
                'id': control_num,
                'title': clean_title
            })
    
    return controls


def deduplicate_controls(controls: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Remove duplicate controls, keeping unique control IDs."""
    return deduplicate_list_of_dicts(controls, 'id')


def sort_control_id(control_id: str) -> tuple:
    """
    Create a sort key for control IDs.
    Returns tuple: (is_letter_prefixed, letter_prefix, major, minor, fix)
    This ensures numeric controls (4.x, 5.x) come before letter-prefixed (B.x)
    and within each type, they're sorted numerically.
    """
    if control_id.startswith('B.'):
        # Letter-prefixed control: B.2.3 -> (True, 'B', 2, 3, 0)
        parts = control_id[2:].split('.')  # Remove 'B.' prefix
        major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
        minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        fix = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        return (True, 'B', major, minor, fix)
    else:
        # Numeric control: 4.1 -> (False, '', 4, 1, 0)
        parts = control_id.split('.')
        major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
        minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        fix = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        return (False, '', major, minor, fix)


def organize_controls_by_section(controls: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Organize controls by their top-level section number."""
    sections = {}
    
    for control in controls:
        # Extract top-level section (e.g., "4" from "4.1", "B.2" from "B.2.2")
        control_id = control['id']
        if control_id.startswith('B.'):
            # For Annex B controls, use "B.X" as section
            parts = control_id.split('.')
            if len(parts) >= 2:
                section = 'B.' + parts[1]
            else:
                section = 'B'
        else:
            # For main body controls, use first number
            section = control_id.split('.')[0]
        
        if section not in sections:
            sections[section] = []
        sections[section].append(control)
    
    # Sort controls within each section
    for section_id in sections:
        sections[section_id].sort(key=lambda x: sort_control_id(x['id']))
    
    return sections


def create_oscal_catalog(controls: List[Dict[str, str]], version: str = "1.0.0") -> Dict:
    """Create an OSCAL catalog from the extracted ISO controls."""
    
    # Organize controls by section
    sections = organize_controls_by_section(controls)
    
    # Section titles mapping
    section_titles = {
        '4': 'Context of the Organization',
        '5': 'Leadership',
        '6': 'Planning',
        '7': 'Support',
        '8': 'Operation',
        '9': 'Performance Evaluation',
        '10': 'Improvement',
        'B.2': 'AI Policy',
        'B.3': 'AI Roles and Responsibilities',
        'B.4': 'AI Resources',
        'B.5': 'AI System Impact Assessment',
        'B.6': 'AI System Development and Deployment',
        'B.7': 'Data for AI Systems',
        'B.8': 'Information for Interested Parties',
        'B.9': 'Use of AI Systems',
        'B.10': 'Relationships with Interested Parties'
    }
    
    # Create groups for each section, sorted properly
    groups = []
    for section_id in sorted(sections.keys(), key=lambda x: sort_control_id(x)):
        section_controls = sections[section_id]
        
        # Create OSCAL controls for this section
        oscal_controls = []
        for ctrl in section_controls:
            oscal_control = {
                'id': f"iso-iec-42001_{ctrl['id'].replace('.', '-')}",
                'title': ctrl['title'],
                'parts': [
                    {
                        'id': f"iso-iec-42001_{ctrl['id'].replace('.', '-')}_smt",
                        'name': 'statement',
                        'prose': ctrl['title']
                    }
                ]
            }
            
            oscal_controls.append(oscal_control)
        
        # Create group
        group = {
            'id': f"iso-iec-42001_{section_id.replace('.', '-')}",
            'title': section_titles.get(section_id, f"Section {section_id}"),
            'controls': oscal_controls
        }
        groups.append(group)
    
    # Create the catalog
    catalog = {
        'catalog': {
            'uuid': str(uuid.uuid4()),
            'metadata': {
                'title': 'ISO/IEC 42001:2023 AI Management System',
                'last-modified': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00'),
                'version': version,
                'oscal-version': get_trestle_oscal_version(),
                'remarks': 'This catalog was generated from the NIST AI RMF to ISO/IEC 42001 crosswalk document.'
            },
            'groups': groups
        }
    }
    
    return catalog


def main():
    """Main execution function."""
    pdf_path = 'data/NIST_AI_RMF_to_ISO_IEC_42001_Crosswalk.pdf'
    output_path = 'trestle.ws/catalogs/iso_iec_42001_1.0.0/catalog.json'
    
    print("Extracting controls from PDF using pdfplumber...")
    controls = extract_controls_from_pdf(pdf_path)
    
    print(f"Found {len(controls)} control references")
    
    print("Deduplicating controls...")
    unique_controls = deduplicate_controls(controls)
    
    print(f"Unique controls: {len(unique_controls)}")
    
    # List all unique controls found
    print("\nControls found:")
    for ctrl in sorted(unique_controls, key=lambda x: (not x['id'].startswith('B'), x['id'])):
        title_preview = ctrl['title'][:60] + '...' if len(ctrl['title']) > 60 else ctrl['title']
        print(f"  {ctrl['id']}: {title_preview}")
    
    print("\nCreating OSCAL catalog...")
    catalog = create_oscal_catalog(unique_controls, version="1.0.0")
    
    print(f"Writing catalog to {output_path}...")
    save_json(catalog, output_path)
    
    print(f"✓ Successfully created OSCAL catalog with {len(unique_controls)} controls")
    print(f"  Output: {output_path}")
    
    # Print summary
    sections = organize_controls_by_section(unique_controls)
    print("\nControls by section:")
    for section_id in sorted(sections.keys(), key=lambda x: (not x.startswith('B'), x)):
        print(f"  {section_id}: {len(sections[section_id])} controls")


if __name__ == '__main__':
    main()

# Made with Bob
