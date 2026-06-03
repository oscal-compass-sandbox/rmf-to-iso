.PHONY: help venv install-tools iso-catalog validate-catalog mapping validate-mapping all clean

VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
TRESTLE = $(VENV_DIR)/bin/trestle
CATALOG_PATH = trestle.ws/catalogs/iso_iec_42001_1.0.0/catalog.json
MAPPING_PATH = trestle.ws/mapping-collections/nist_ai_rmf_to_iso_42001/mapping-collection.json

help:
	@echo "Available targets:"
	@echo "  venv             - Create Python virtual environment"
	@echo "  install-tools    - Install required Python packages (pdfplumber, compliance-trestle)"
	@echo "  iso-catalog      - Extract ISO controls and create OSCAL catalog"
	@echo "  validate-catalog - Validate OSCAL catalog using compliance-trestle"
	@echo "  mapping          - Create OSCAL mapping collection from RMF to ISO"
	@echo "  validate-mapping - Validate OSCAL mapping collection using compliance-trestle"
	@echo "  all              - Run complete workflow (catalog + mapping + validation)"
	@echo "  clean            - Remove generated files and virtual environment"

venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)/"
	@echo "Activate it with: source $(VENV_DIR)/bin/activate"

install-tools: venv
	@echo "Installing required tools..."
	$(PIP) install --upgrade pip
	$(PIP) install pdfplumber compliance-trestle
	@echo "Tools installed successfully"

iso-catalog:
	@echo "Extracting ISO/IEC 42001 controls and creating OSCAL catalog..."
	python3 python/create_iso_catalog.py
	@echo "Done! Catalog created at: $(CATALOG_PATH)"

validate-catalog: install-tools
	@echo "Validating OSCAL catalog with compliance-trestle..."
	@if [ ! -f "$(CATALOG_PATH)" ]; then \
		echo "Error: Catalog not found at $(CATALOG_PATH)"; \
		echo "Run 'make iso-catalog' first"; \
		exit 1; \
	fi
	cd trestle.ws && ../$(TRESTLE) validate -f catalogs/iso_iec_42001_1.0.0/catalog.json
	@echo "✓ Catalog validation successful"

mapping:
	@echo "Creating OSCAL mapping collection from NIST AI RMF to ISO/IEC 42001..."
	python3 python/create_rmf_to_iso_mapping.py
	@echo "Done! Mapping collection created at: $(MAPPING_PATH)"

validate-mapping: install-tools
	@echo "Validating OSCAL mapping collection with compliance-trestle..."
	@if [ ! -f "$(MAPPING_PATH)" ]; then \
		echo "Error: Mapping collection not found at $(MAPPING_PATH)"; \
		echo "Run 'make mapping' first"; \
		exit 1; \
	fi
	cd trestle.ws && ../$(TRESTLE) validate -f mapping-collections/nist_ai_rmf_to_iso_42001/mapping-collection.json
	@echo "✓ Mapping collection validation successful"

all: iso-catalog validate-catalog mapping validate-mapping
	@echo ""
	@echo "=========================================="
	@echo "✓ Complete workflow finished successfully"
	@echo "=========================================="
	@echo "Generated files:"
	@echo "  - $(CATALOG_PATH)"
	@echo "  - $(MAPPING_PATH)"

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)
	rm -f crosswalk_text.txt crosswalk_layout.txt
	rm -rf trestle.ws/catalogs/iso_iec_42001_1.0.0
	rm -rf trestle.ws/mapping-collections/nist_ai_rmf_to_iso_42001
	@echo "Cleanup complete"
	@echo "Note: README.md is preserved (contains mapping report)"

# Made with Bob
