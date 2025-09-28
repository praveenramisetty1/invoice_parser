# 🧾 Invoice Parser Microservice

A lightweight FastAPI microservice for parsing nvoices (PDF) into structured JSON data using vendor-specific regex templates.

---

## 📚 Table of Contents

- [Features](#features)
- [API Usage](#api-usage)
- [Template Format](#template-format)
- [Quick Start](#quick-start)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [License](#license)

---

## ⚙️ Features

- Upload PDF invoices and extract structured invoice fields
- Supports digital PDFs and scanned PDFs (OCR fallback)
- Vendor-specific parsing templates with regex patterns
- Automatic template detection by matching vendor name in text
- Default template fallback
- JSON output with extracted invoice data

---

## 🚀 API Usage

- Upload a PDF invoice file via multipart form data (`file` parameter)
- Returns JSON with extracted invoice fields

### POST `/parse-invoice/`

- Upload a PDF invoice file via multipart form data (`file` parameter)
- Returns JSON with extracted invoice fields

### Example `curl` command

```bash
curl -X POST "http://localhost:8000/parse-invoice/" \
  -F "file=@sample_invoice.pdf"

- Responses
  {
    "filename": "sample_invoice.pdf",
    "extracted": {
      "invoice_number": "INV-1001",
      "date": "2025-09-19",
      "amount": "150.00"
    },
    "raw_text_snippet": "Invoice Number: INV-1001\nDate: 2025-09-19\n..."
  }
- Client Errors
400 Bad Request – If uploaded file is not a PDF:
{
  "error": "Only PDF files are supported."
}
- 422 Unprocessable Entity – If no text could be extracted from the PDF:
{
  "error": "Could not extract any text from PDF."
}
```
---

## 📑 Template Format
```
{
  "match": "Apollo Pharma|APPL",
  "fields": {
    "invoice_number": "Invoice Number:\\s*(\\S+)",
    "date": "Date:\\s*(\\d{4}-\\d{2}-\\d{2})",
    "amount": "Amount:\\s*\\$?([\\d,.]+)"
  }
}
```
- match: Optional regex to identify vendor from invoice text
- fields: Dictionary mapping field names to regex extraction patterns
- Use default.json as fallback template
---

## ⚡ Quick Start
1. Clone the repo
```
git clone <your-repo-url>
cd invoice_parser
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Run the FastAPI server
```
uvicorn app.main:app --reload

```
4. Open API docs in your browser
Navigate to http://localhost:8000/docs to test endpoints interactively.

---

## 🧪 Testing

```
pytest

```

---

## 🗂️ Project Structure

```
invoice_parser/
├── app/
│   ├── main.py              # FastAPI app and core logic
│   └── templates/           # Vendor-specific JSON templates
│       ├── default.json
│       └── apollo_pharma.json
├── tests/
│   └── test_parser.py       # Unit & integration tests
├── tests_data/              # Sample PDF files for testing
├── README.md
└── requirements.txt

```

---

## 📦 Dependencies

```
pip install -r requirements.txt
```

---

## 📄 License
MIT License © 2025 Praveen Ramisetty

---
