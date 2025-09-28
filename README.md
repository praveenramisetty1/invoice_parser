# 🧾 Invoice Parser Microservice

A lightweight FastAPI-based microservice to parse medical distributor invoices in PDF format and extract structured data such as invoice number, date, amount, and item details. Supports vendor-specific templates via regex.

---

## 📚 Table of Contents

1. [Features](#-features)
2. [API Usage](#-api-usage)
3. [Template Format](#-template-format)
4. [Quick Start](#-quick-start)
5. [Testing](#-testing)
6. [Project Structure](#-project-structure)
7. [Dependencies](#-dependencies)
8. [License](#-license)

---

## ⚙️ Features

- ✅ Upload PDF invoices via `/parse-invoice/` API
- ✅ Extract text from:
  - Digital PDFs using `pypdf`
  - Scanned PDFs using OCR (`pdf2image` + `pytesseract`)
- ✅ Regex-based field extraction from vendor templates
- ✅ Auto-detection of vendor templates using `match` regex
- ✅ Fallback to `default.json` template
- ✅ JSON output with extracted invoice fields

---

## 🚀 API Usage

### `POST /parse-invoice/`

- Accepts: `multipart/form-data` with PDF file
- Returns: Extracted fields as JSON

### Example with `curl`

```bash
curl -X POST "http://localhost:8000/parse-invoice/" \
  -F "file=@sample_invoice.pdf"
