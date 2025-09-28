from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import logging
import re
import io
import json
import os
import glob
from pypdf import PdfReader
from pdf2image import convert_from_bytes
from PIL import Image, ImageFilter, ImageOps
import pytesseract

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_templates():
    templates = {}
    for filepath in glob.glob(os.path.join(BASE_DIR, "templates", "*.json")):
        try:
            with open(filepath) as f:
                content = f.read().strip()
                if not content:
                    # Empty file: load as empty dict or skip
                    logger.warning(f"Template file is empty: {filepath}, loading as empty template.")
                    template = {}
                else:
                    template = json.loads(content)
                key = os.path.splitext(os.path.basename(filepath))[0]
                templates[key] = template
        except json.JSONDecodeError as e:
            logger.error(f"Failed to load JSON from {filepath}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading template {filepath}: {e}")
    return templates


def identify_template(text: str, templates: dict):
    for name, template in templates.items():
        pattern = template.get("match")
        if pattern and re.search(pattern, text, re.IGNORECASE):
            return template
    return templates.get("default")

def extract_fields(text: str, template: dict) -> dict:
    field_patterns = template.get("fields", template)
    results = {}
    for field, pattern in field_patterns.items():
        try:
            match = re.search(pattern, text, re.IGNORECASE)
            results[field] = match.group(1).strip() if match else None
        except Exception as e:
            logger.error(f"[extract_fields] Error extracting '{field}': {e}")
            results[field] = None
    return results

def preprocess_image(image):
    image = image.convert("L")
    image = ImageOps.invert(image).point(lambda x: 0 if x < 150 else 255, '1')
    image = image.filter(ImageFilter.SHARPEN)
    return image

def extract_text(contents: bytes):
    text = ""
    try:
        reader = PdfReader(io.BytesIO(contents))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        logger.debug(f"pypdf error: {e}")

    if not text.strip():
        logger.info("Falling back to OCR...")
        images = convert_from_bytes(contents)
        for image in images:
            processed_image = preprocess_image(image)
            text += pytesseract.image_to_string(processed_image)

    return text

@app.post("/parse-invoice/")
async def parse_invoice(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()
    text = extract_text(contents)

    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract any text from PDF.")

    templates = load_templates()
    template = identify_template(text, templates)
    if not template:
        raise HTTPException(status_code=422, detail="No matching template found and no default template available.")

    parsed_data = extract_fields(text, template)

    return {
        "filename": file.filename,
        "extracted": parsed_data,
        "raw_text_snippet": text[:500]
    }
