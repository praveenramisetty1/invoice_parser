import os
import json
import logging
import pytest
from fastapi.testclient import TestClient
from app.main import app, extract_fields, extract_text

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

client = TestClient(app)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@pytest.fixture
def load_template():
    def _loader(vendor=None):
        base = os.path.join(os.path.dirname(__file__), "../app/templates")
        vendor_name = vendor or "default"
        path = os.path.join(base, f"{vendor_name}.json")
        if not os.path.exists(path):
            path = os.path.join(base, "default.json")
            if not os.path.exists(path):
                raise FileNotFoundError("No template found")
            if vendor_name != "default":
                logger.warning(f"Template '{vendor_name}.json' not found, using default.json instead.")
        with open(path) as f:
            return json.load(f)
    return _loader

def test_load_template_apollo(load_template):
    template = load_template("apollo_pharma")
    assert "fields" in template
    assert "invoice_number" in template["fields"]

def test_extract_fields_basic(load_template):
    template = load_template()
    text = """
    Invoice Number: INV-1001
    Date: 2025-09-19
    Bill To: John Doe
    Item: Medical Supplies
    Amount: $150.00
    """
    logger.debug(f"Using template: {template}")
    result = extract_fields(text, template)
    assert result["invoice_number"] == "INV-1001"
    assert result["date"] == "2025-09-19"
    assert result["bill_to"] == "John Doe"
    assert result["item"] == "Medical Supplies"
    assert result["amount"] == "150.00"

def test_extract_fields_with_structured_template():
    text = """
    Invoice Number: INV-9999
    Date: 2025-09-21
    Bill To: XYZ Pharma
    Item: Ibuprofen 200mg
    Amount: $99.50
    """
    structured_template = {
        "fields": {
            "invoice_number": r"Invoice Number:\s*(\S+)",
            "date": r"Date:\s*([\d-]+)",
            "bill_to": r"Bill To:\s*(.+)",
            "item": r"Item:\s*(.+)",
            "amount": r"Amount:\s*\$?([\d.,]+)"
        }
    }
    result = extract_fields(text, structured_template)
    assert result["invoice_number"] == "INV-9999"
    assert result["date"] == "2025-09-21"
    assert result["bill_to"] == "XYZ Pharma"
    assert result["item"] == "Ibuprofen 200mg"
    assert result["amount"] == "99.50"

def test_extract_text_from_sample_pdf():
    pdf_path = os.path.join(BASE_DIR, "tests_data", "sample_invoice.pdf")
    with open(pdf_path, "rb") as f:
        contents = f.read()
    text = extract_text(contents)
    assert "Invoice Number" in text

def test_parse_invoice_endpoint():
    pdf_path = os.path.join(BASE_DIR, "tests_data", "sample_invoice.pdf")
    with open(pdf_path, "rb") as f:
        response = client.post(
            "/parse-invoice/",
            files={"file": ("sample_invoice.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "extracted" in data
    assert data["extracted"]["invoice_number"] is not None
