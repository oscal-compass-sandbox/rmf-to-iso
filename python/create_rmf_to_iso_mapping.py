#!/usr/bin/env python3
"""
Create OSCAL mapping collection from NIST AI RMF to ISO/IEC 42001
using the crosswalk PDF and existing catalogs.
"""

import json
from datetime import datetime, timezone
from typing import List, Dict, Any
import uuid

from utils import (
    check_pdfplumber,
    extract_table_from_pdf,
    load_catalog,
    save_json,
    find_control_or_group_in_catalog,
    get_all_controls_in_group,
    clean_text,
    get_trestle_oscal_version
)

if not check_pdfplumber():
    exit(1)


def extract_mappings_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extract RMF to ISO mappings from PDF.
    The PDF has 4 columns:
    1. RMF ID (e.g., "Govern 1.1")
    2. RMF Description
    3. ISO Control Number (e.g., "4.1", "B.2.2")
    4. ISO Control Name
    
    Note: Blank cells in columns 1-2 inherit values from the previous row.
    """
    mappings = []
    rows = extract_table_from_pdf(pdf_path)
    
    # Track the current RMF ID and description for blank row handling
    current_rmf_id = None
    current_rmf_desc = None
    
    for row in rows:
        rmf_id, rmf_desc, iso_id, iso_name = row[0], row[1], row[2], row[3]
        
        # Update current RMF ID if present
        if rmf_id and rmf_id.strip():
            current_rmf_id = clean_text(rmf_id)
            current_rmf_desc = clean_text(rmf_desc) if rmf_desc else ""
        
        # Only process rows with ISO data
        if iso_id and iso_id.strip() and current_rmf_id:
            mappings.append({
                'rmf_id': current_rmf_id,
                'rmf_description': current_rmf_desc,
                'iso_id': clean_text(iso_id),
                'iso_name': clean_text(iso_name) if iso_name else ""
            })
    
    return mappings


def convert_rmf_id_to_control_id(rmf_id: str) -> str:
    """
    Convert RMF ID to OSCAL control ID format.
    Examples:
    - "Govern 1.1" -> "GV-1.1"
    - "Map 1.1" -> "MP-1.1"
    - "Measure 1.1" -> "MS-1.1"
    - "Manage 1.1" -> "MG-1.1"
    """
    # Map function names to abbreviations
    function_map = {
        'govern': 'GV',
        'map': 'MP',
        'measure': 'MS',
        'manage': 'MG'
    }
    
    parts = rmf_id.split()
    if len(parts) >= 2:
        function = parts[0].lower()
        number = parts[1]
        
        if function in function_map:
            return f"{function_map[function]}-{number}"
    
    # Fallback: return as-is with cleanup
    return rmf_id.replace(' ', '-').upper()


def convert_iso_id_to_control_id(iso_id: str) -> str:
    """
    Convert ISO control number to OSCAL control ID format.
    Examples:
    - "4.1" -> "iso-iec-42001_4-1"
    - "B.2.2" -> "iso-iec-42001_B-2-2"
    """
    return f"iso-iec-42001_{iso_id.replace('.', '-')}"


def group_mappings_by_rmf_control(mappings: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group mappings by RMF control ID, preserving order from PDF.
    Returns an OrderedDict to maintain the sequence.
    """
    from collections import OrderedDict
    grouped = OrderedDict()
    
    for mapping in mappings:
        rmf_id = mapping['rmf_id']
        if rmf_id not in grouped:
            grouped[rmf_id] = []
        grouped[rmf_id].append(mapping)
    
    return grouped

def create_markdown_report(
    mappings: List[Dict],
    mapping_collection: Dict,
    rmf_catalog: Dict,
    output_path: str
):
    """Create a Markdown report of the mapping."""
    from collections import OrderedDict
    
    # Group mappings by RMF ID
    grouped = OrderedDict()
    for mapping in mappings:
        rmf_id = mapping['rmf_id']
        if rmf_id not in grouped:
            grouped[rmf_id] = {
                'description': mapping['rmf_description'],
                'iso_controls': []
            }
        grouped[rmf_id]['iso_controls'].append({
            'id': mapping['iso_id'],
            'name': mapping['iso_name']
        })
    
    # Get all RMF group IDs from catalog
    catalog_groups = set()
    for group in rmf_catalog['catalog']['groups']:
        if 'groups' in group:
            for subgroup in group['groups']:
                catalog_groups.add(subgroup['id'])
    
    # Find missing controls
    missing_rmf = []
    for rmf_id in grouped.keys():
        control_id = convert_rmf_id_to_control_id(rmf_id)
        if control_id not in catalog_groups:
            missing_rmf.append({
                'original': rmf_id,
                'converted': control_id,
                'description': grouped[rmf_id]['description'],
                'iso_count': len(grouped[rmf_id]['iso_controls'])
            })
    
    # Get maps from collection
    maps = mapping_collection['mapping-collection']['mappings'][0]['maps']
    
    # Create report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# NIST AI RMF to ISO/IEC 42001 Mapping Report\n\n")
        
        # Summary
        f.write("## Summary\n\n")
        f.write(f"- **Total RMF controls in PDF**: {len(grouped)}\n")
        f.write(f"- **Total RMF→ISO mappings in PDF**: {len(mappings)}\n")
        f.write(f"- **Mapping entries created**: {len(maps)}\n")
        f.write(f"- **Missing RMF controls**: {len(missing_rmf)}\n\n")
        
        # Missing controls
        if missing_rmf:
            f.write("## Missing RMF Controls\n\n")
            f.write("The following RMF controls are referenced in the PDF crosswalk but not found in the NIST AI RMF Generative AI Profile catalog:\n\n")
            f.write("| Original ID | Control ID | Description | ISO Mappings |\n")
            f.write("|-------------|------------|-------------|-------------|\n")
            for ctrl in missing_rmf:
                desc = ctrl['description'][:50] + "..." if len(ctrl['description']) > 50 else ctrl['description']
                f.write(f"| {ctrl['original']} | {ctrl['converted']} | {desc} | {ctrl['iso_count']} |\n")
            f.write("\n")
            f.write("**Note**: These controls are from the full NIST AI RMF framework. The catalog used is specifically for the Generative AI Profile, which is a subset.\n\n")
        
        # Complete mapping table
        f.write("## Complete Mapping Table\n\n")
        f.write("| RMF ID | RMF Group | ISO Controls | Status |\n")
        f.write("|--------|-----------|--------------|--------|\n")
        
        for rmf_id in grouped.keys():
            control_id = convert_rmf_id_to_control_id(rmf_id)
            iso_ids = ", ".join([ctrl['id'] for ctrl in grouped[rmf_id]['iso_controls']])
            status = "✓ Mapped" if control_id in catalog_groups else "⚠ Missing from catalog"
            f.write(f"| {rmf_id} | {control_id} | {iso_ids} | {status} |\n")
        
        f.write("\n---\n")
        f.write("*Report generated by create_rmf_to_iso_mapping.py*\n")


def create_mapping_collection(
    mappings: List[Dict],
    rmf_catalog: Dict,
    iso_catalog: Dict,
    version: str = "1.0.0"
) -> Dict:
    """Create an OSCAL mapping collection."""
    
    # Group mappings by RMF control
    grouped_mappings = group_mappings_by_rmf_control(mappings)
    
    # Get catalog UUIDs
    rmf_uuid = rmf_catalog.get('catalog', {}).get('uuid', str(uuid.uuid4()))
    iso_uuid = iso_catalog.get('catalog', {}).get('uuid', str(uuid.uuid4()))
    
    # Create maps for each RMF control
    maps = []
    unmapped_iso_controls = set()
    
    for rmf_id, rmf_mappings in grouped_mappings.items():
        # Convert RMF ID to group ID (e.g., "Govern 1.1" -> "GV-1.1")
        rmf_group_id = convert_rmf_id_to_control_id(rmf_id)
        
        # Verify RMF group exists
        if not find_control_or_group_in_catalog(rmf_catalog, rmf_group_id):
            print(f"Warning: RMF group {rmf_group_id} not found in catalog")
            continue
        
        # Create source pointing to the RMF control itself
        sources = [{
            'type': 'control',
            'id-ref': rmf_group_id
        }]
        
        # Create targets for all ISO controls mapped to this RMF group
        targets = []
        for mapping in rmf_mappings:
            iso_control_id = convert_iso_id_to_control_id(mapping['iso_id'])
            
            # Verify ISO control exists
            if not find_control_or_group_in_catalog(iso_catalog, iso_control_id):
                print(f"Warning: ISO control {iso_control_id} not found in catalog")
                continue
            
            targets.append({
                'type': 'control',
                'id-ref': iso_control_id
            })
        
        if targets:
            # Create ONE map entry per RMF group
            map_entry = {
                'uuid': str(uuid.uuid4()),
                'relationship': 'intersects-with',
                'sources': sources,
                'targets': targets
            }
            maps.append(map_entry)
    
    # Create the mapping collection
    mapping_collection = {
        'mapping-collection': {
            'uuid': str(uuid.uuid4()),
            'metadata': {
                'title': 'NIST AI RMF Generative AI Profile to ISO/IEC 42001:2023 Mapping',
                'last-modified': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00'),
                'version': version,
                'oscal-version': get_trestle_oscal_version()
            },
            'provenance': {
                'method': 'manual',
                'matching-rationale': 'semantic',
                'status': 'complete',
                'mapping-description': 'Mapping collection from NIST AI Risk Management Framework Generative AI Profile to ISO/IEC 42001:2023 AI Management System based on the official NIST crosswalk document.'
            },
            'mappings': [
                {
                    'uuid': str(uuid.uuid4()),
                    'source-resource': {
                        'type': 'catalog',
                        'href': 'catalogs/nist_ai_rmf_gen_ai_1.0.0/catalog.json',
                        'props': [
                            {
                                'name': 'catalog_uuid',
                                'value': rmf_uuid,
                                'ns': 'https://nist.gov/oscal/ns'
                            }
                        ]
                    },
                    'target-resource': {
                        'type': 'catalog',
                        'href': 'catalogs/iso_iec_42001_1.0.0/catalog.json',
                        'props': [
                            {
                                'name': 'catalog_uuid',
                                'value': iso_uuid,
                                'ns': 'https://nist.gov/oscal/ns'
                            }
                        ]
                    },
                    'maps': maps,
                    'target-gap-summary': {
                        'uuid': str(uuid.uuid4()),
                        'unmapped-controls': [
                            {
                                'with-ids': list(unmapped_iso_controls)
                            }
                        ]
                    }
                }
            ]
        }
    }
    
    return mapping_collection


def main():
    """Main execution function."""
    # File paths
    pdf_path = 'data/NIST_AI_RMF_to_ISO_IEC_42001_Crosswalk.pdf'
    rmf_catalog_path = 'trestle.ws/catalogs/nist_ai_rmf_gen_ai_1.0.0/catalog.json'
    iso_catalog_path = 'trestle.ws/catalogs/iso_iec_42001_1.0.0/catalog.json'
    output_path = 'trestle.ws/mapping-collections/nist_ai_rmf_to_iso_42001/mapping-collection.json'
    
    print("=" * 70)
    print("NIST AI RMF to ISO/IEC 42001 Mapping Collection Generator")
    print("=" * 70)
    
    # Extract mappings from PDF
    print("\n1. Extracting mappings from PDF...")
    mappings = extract_mappings_from_pdf(pdf_path)
    print(f"   Found {len(mappings)} mapping entries")
    
    # Load catalogs
    print("\n2. Loading catalogs...")
    print(f"   Loading RMF catalog: {rmf_catalog_path}")
    rmf_catalog = load_catalog(rmf_catalog_path)
    print(f"   Loading ISO catalog: {iso_catalog_path}")
    iso_catalog = load_catalog(iso_catalog_path)
    
    # Show sample mappings
    print("\n3. Sample mappings extracted:")
    for i, mapping in enumerate(mappings[:5], 1):
        print(f"   {i}. {mapping['rmf_id']} -> {mapping['iso_id']}")
    if len(mappings) > 5:
        print(f"   ... and {len(mappings) - 5} more")
    
    # Create mapping collection
    print("\n4. Creating OSCAL mapping collection...")
    mapping_collection = create_mapping_collection(
        mappings,
        rmf_catalog,
        iso_catalog,
        version="1.0.0"
    )
    
    # Count maps created
    maps_count = len(mapping_collection['mapping-collection']['mappings'][0]['maps'])
    print(f"   Created {maps_count} mapping entries")
    
    # Write output
    print(f"\n5. Writing mapping collection to {output_path}...")
    save_json(mapping_collection, output_path)
    
    # Create report
    report_path = 'README.md'
    print(f"\n6. Creating mapping report at {report_path}...")
    create_markdown_report(mappings, mapping_collection, rmf_catalog, report_path)
    
    print("\n" + "=" * 70)
    print("✓ Successfully created OSCAL mapping collection")
    print(f"  Output: {output_path}")
    print(f"  Report: {report_path}")
    print(f"  Total mappings: {maps_count}")
    print("=" * 70)


if __name__ == '__main__':
    main()

# Made with Bob