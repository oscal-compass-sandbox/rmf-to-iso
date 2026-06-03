# NIST AI RMF to ISO/IEC 42001 Mapping Report

## Summary

- **Total RMF controls in PDF**: 72
- **Total RMF→ISO mappings in PDF**: 281
- **Mapping entries created**: 49
- **Missing RMF controls**: 23

## Missing RMF Controls

The following RMF controls are referenced in the PDF crosswalk but not found in the NIST AI RMF Generative AI Profile catalog:

| Original ID | Control ID | Description | ISO Mappings |
|-------------|------------|-------------|-------------|
| Govern 1.4 | GV-1.4 | The risk management process and its outcomes are e... | 3 |
| Govern 2.2 | GV-2.2 | The organization’s personnel and partners receive ... | 1 |
| Govern 2.3 | GV-2.3 | Executive leadership of the organization takes res... | 5 |
| Govern 3.1 | GV-3.1 | Decision-making related to mapping, measuring, and... | 2 |
| Govern 5.2 | GV-5.2 | Mechanisms are established to enable the team that... | 6 |
| Map 1.3 | MP-1.3 | The organization’s mission and relevant goals for ... | 6 |
| Map 1.4 | MP-1.4 | The business value or context of business use has ... | 6 |
| Map 1.5 | MP-1.5 | Organizational risk tolerances are determined and ... | 1 |
| Map 1.6 | MP-1.6 | System requirements (e.g., “the system shall respe... | 3 |
| Map 3.1 | MP-3.1 | Potential benefits of intended AI system functiona... | 4 |
| Map 3.2 | MP-3.2 | Potential costs, including non- monetary costs, wh... | 7 |
| Map 3.3 | MP-3.3 | Targeted application scope is specified and docume... | 5 |
| Map 3.5 | MP-3.5 | Processes for human oversight are defined, assesse... | 3 |
| Map 4.2 | MP-4.2 | Internal risk controls for components of the AI sy... | 3 |
| Measure 1.2 | MS-1.2 | Appropriateness of AI metrics and effectiveness of... | 4 |
| Measure 2.1 | MS-2.1 | Test sets, metrics, and details about the tools us... | 4 |
| Measure 2.4 | MS-2.4 | The functionality and behavior of the AI system an... | 3 |
| Measure 4.1 | MS-4.1 | Measurement approaches for identifying AI risks ar... | 4 |
| Measure 4.3 | MS-4.3 | Measurable performance improvements or declines ba... | 3 |
| Manage 1.1 | MG-1.1 | A determination is made as to whether the AI syste... | 6 |
| Manage 1.2 | MG-1.2 | Treatment of documented AI risks is prioritized ba... | 4 |
| Manage 1.4 | MG-1.4 | Negative residual risks (defined as the sum of all... | 4 |
| Manage 2.1 | MG-2.1 | Resources required to manage AI risks are taken in... | 2 |

**Note**: These controls are from the full NIST AI RMF framework. The catalog used is specifically for the Generative AI Profile, which is a subset.

## Complete Mapping Table

| RMF ID | RMF Group | ISO Controls | Status |
|--------|-----------|--------------|--------|
| Govern 1.1 | GV-1.1 | 4.1, 6.2, B.2.2, B.2.4 | ✓ Mapped |
| Govern 1.2 | GV-1.2 | B.9.3, B.6.1.2, B.6.1.3, B.10.3, B.2.2, 4.4, 5.2 | ✓ Mapped |
| Govern 1.3 | GV-1.3 | 6.1.2, 6.1.1, 6.1.3 | ✓ Mapped |
| Govern 1.4 | GV-1.4 | 6.1.2, 6.1.3, 8.3 | ⚠ Missing from catalog |
| Govern 1.5 | GV-1.5 | 8.2, 8.3, 8.4 | ✓ Mapped |
| Govern 1.6 | GV-1.6 | B.4.5, B.4.3, B.4.4, B.4.6, B.4.2 | ✓ Mapped |
| Govern 1.7 | GV-1.7 | B.6.2.6 | ✓ Mapped |
| Govern 2.1 | GV-2.1 | 9.1, 5.3, 7.1, 7..2, 7.3, 7.4, B.3.2 | ✓ Mapped |
| Govern 2.2 | GV-2.2 | 7.2 | ⚠ Missing from catalog |
| Govern 2.3 | GV-2.3 | 5.1, 9.3.1, 9.3.2, 9.3.3, 5.2 | ⚠ Missing from catalog |
| Govern 3.1 | GV-3.1 | B.4.6, B.5.4 | ⚠ Missing from catalog |
| Govern 3.2 | GV-3.2 | B.6.1.3, B.9.3, B.4.6, B.5.3, 7.2, B.3.2 | ✓ Mapped |
| Govern 4.1 | GV-4.1 | B.5.2, B.6.1.2, B.6.1.3, B.9.2, B.9.3, B.10.3, B.5.4 | ✓ Mapped |
| Govern 4.2 | GV-4.2 | B.5.4, B.8.5, 7.4, 6.1.4, B.5.5 | ✓ Mapped |
| Govern 4.3 | GV-4.3 | B.6.2.4, B.6.2.6, B.6.2.7, B.8.2, B.8.3, B.8.4, B.8.5, B.6.1.2, B.6.1.3 | ✓ Mapped |
| Govern 5.1 | GV-5.1 | B.10.4, B.5.3, B.5.4, B.8.3 | ✓ Mapped |
| Govern 5.2 | GV-5.2 | B.8.3, B.10.4, B.5.4, B.5.5, B.6.1.3, B.6.2.6 | ⚠ Missing from catalog |
| Govern 6.1 | GV-6.1 | B.10.2, B.10.3 | ✓ Mapped |
| Govern 6.2 | GV-6.2 | B.10.2, B.10.3 | ✓ Mapped |
| Map 1.1 | MP-1.1 | 6.1.4, B.5.2, B.5.3, B.5.4, B.5.5 | ✓ Mapped |
| Map 1.2 | MP-1.2 | B.4.6, 7.2 | ✓ Mapped |
| Map 1.3 | MP-1.3 | 4.1, 5.2, 6.2, 7.5.3, 7.3, 7.4 | ⚠ Missing from catalog |
| Map 1.4 | MP-1.4 | 5.1, 4.1, B.2.2, B.5.2, B.9.4, B.6.2.2 | ⚠ Missing from catalog |
| Map 1.5 | MP-1.5 | 6.1.1 | ⚠ Missing from catalog |
| Map 1.6 | MP-1.6 | B.6.2.2, B.5.4, B.5.5 | ⚠ Missing from catalog |
| Map 2.1 | MP-2.1 | B.6.2.3, B.4.2, B.4.3, B.4.4, B.4.5, B.4.6 | ✓ Mapped |
| Map 2.2 | MP-2.2 | B.6.2.7, B.9.3, B.8.2 | ✓ Mapped |
| Map 2.3 | MP-2.3 | B.6.1.3, B.6.2.7, B.7.2, B.7.3, B.7.4, B.7.5, B.7.6, B.6.2.4 | ✓ Mapped |
| Map 3.1 | MP-3.1 | B.5.2, B.5.3, B.5.4, B.5.5 | ⚠ Missing from catalog |
| Map 3.2 | MP-3.2 | B.5.2, B.5.3, B.5.4, B.5.5, 8.2, 8.3, 8.4 | ⚠ Missing from catalog |
| Map 3.3 | MP-3.3 | 4.3, B.5.2, B.5.3, B.5.4, B.5.5 | ⚠ Missing from catalog |
| Map 3.4 | MP-3.4 | 7.2, B.4.6 | ✓ Mapped |
| Map 3.5 | MP-3.5 | B.6.1.3, B.6.2.7, B.8.2 | ⚠ Missing from catalog |
| Map 4.1 | MP-4.1 | 4.1, B.2.2, B.9.2, B.9.4 | ✓ Mapped |
| Map 4.2 | MP-4.2 | B.6.2.7, B.8.2, B.10.3 | ⚠ Missing from catalog |
| Map 5.1 | MP-5.1 | 6.1.2, B.5.2 | ✓ Mapped |
| Map 5.2 | MP-5.2 | B.6.1.3, B.6.2.6, B.8.3 | ✓ Mapped |
| Measure 1.1 | MS-1.1 | 6.1.1, 6.1.2 | ✓ Mapped |
| Measure 1.2 | MS-1.2 | B.6.2.4, B.5.4, B.5.2, B.5.5 | ⚠ Missing from catalog |
| Measure 1.3 | MS-1.3 | 6.1.2, 9.2.2, B.5.2, B.5.4, B.5.5 | ✓ Mapped |
| Measure 2.1 | MS-2.1 | B.8.4, B.6.2.4, B.6.2.7, B.4.2 | ⚠ Missing from catalog |
| Measure 2.2 | MS-2.2 | B.6.2.4 | ✓ Mapped |
| Measure 2.3 | MS-2.3 | B.7.4, B.6.2.6 | ✓ Mapped |
| Measure 2.4 | MS-2.4 | 9.1, B.6.2.6, B.6.2.8 | ⚠ Missing from catalog |
| Measure 2.5 | MS-2.5 | B.6.2.4, B.6.2.5, B.6.2.7, B.8.2 | ✓ Mapped |
| Measure 2.6 | MS-2.6 | B.6.2.8, B.6.2.6, B.6.2.4, 8.2 | ✓ Mapped |
| Measure 2.7 | MS-2.7 | B.7.2, B.3.2, B.2.3, B.5.2, B.6.1.2, B.6.2.3, B.9.3 | ✓ Mapped |
| Measure 2.8 | MS-2.8 | B.7.2, B.5.4, B.5.5, B.6.1.2, B.9.3, 6.1.2 | ✓ Mapped |
| Measure 2.9 | MS-2.9 | B.7.5, B.6.2.5, B.6.2.7, B.8.2 | ✓ Mapped |
| Measure 2.10 | MS-2.10 | B.5.2, B.7.2, B.7.3, B.2.3 | ✓ Mapped |
| Measure 2.11 | MS-2.11 | B.5.5, B.5.4 | ✓ Mapped |
| Measure 2.12 | MS-2.12 | B.5.5, B.4.5 | ✓ Mapped |
| Measure 2.13 | MS-2.13 | B.6.2.4, B.6.2.6 | ✓ Mapped |
| Measure 3.1 | MS-3.1 | 8.2, 4.4, 8.4 | ✓ Mapped |
| Measure 3.2 | MS-3.2 | B.6.2.8, B.6.2.6, 10.1 | ✓ Mapped |
| Measure 3.3 | MS-3.3 | B.8.2, B.8.4, B.8.3 | ✓ Mapped |
| Measure 4.1 | MS-4.1 | B.6.2.4, B.5.4, B.5.5, 9.1 | ⚠ Missing from catalog |
| Measure 4.2 | MS-4.2 | 9.1, B.8.2, 9.2.1, B.8.3 | ✓ Mapped |
| Measure 4.3 | MS-4.3 | 9.3.1, B.6.2.6, B.6.2.7 | ⚠ Missing from catalog |
| Manage 1.1 | MG-1.1 | B.9.3, B.9.2, B.9.4, B.6.1.3, B.6.2.4, B.6.2.4 | ⚠ Missing from catalog |
| Manage 1.2 | MG-1.2 | 9.3.3, 6.1.2, 6.1.3, 6.1.4 | ⚠ Missing from catalog |
| Manage 1.3 | MG-1.3 | 6.1.1, 6.1.2, 6.1.3, 6.1.4 | ✓ Mapped |
| Manage 1.4 | MG-1.4 | B.5.3, B.5.4, B.6.2.7, B.8.2 | ⚠ Missing from catalog |
| Manage 2.1 | MG-2.1 | B.4.2, 7.1 | ⚠ Missing from catalog |
| Manage 2.2 | MG-2.2 | B.3.3, B.6.1.2, B.6.1.3, B.6.2.4, B.6.2.6, B.7.2, 7.1, 10.1 | ✓ Mapped |
| Manage 2.3 | MG-2.3 | 10.2, 6.1.1, 6.1.2, 6.1.3 | ✓ Mapped |
| Manage 2.4 | MG-2.4 | B.9.4, B.8.2, B.6.2.7, B.6.1.3 | ✓ Mapped |
| Manage 3.1 | MG-3.1 | B.10.3, B.10.2 | ✓ Mapped |
| Manage 3.2 | MG-3.2 | B.4.4, B.6.2.6 | ✓ Mapped |
| Manage 4.1 | MG-4.1 | 9.2.1, B.6.2.6, B.8.3, B.10.4 | ✓ Mapped |
| Manage 4.2 | MG-4.2 | 9.3.3, B.6.2.4, B.6.2.6 | ✓ Mapped |
| Manage 4.3 | MG-4.3 | 9.3.2, B.8.5, B.6.2.6 | ✓ Mapped |

---
*Report generated by create_rmf_to_iso_mapping.py*
