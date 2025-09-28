from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_sample_invoice(path="./app/test_files/sample_invoice.pdf"):
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(100, 750, "Invoice Number: INV-1001")
    c.drawString(100, 730, "Date: 2025-09-19")
    c.drawString(100, 710, "Bill To: John Doe")
    c.drawString(100, 690, "Item: Medical Supplies")
    c.drawString(100, 670, "Amount: $150.00")

    c.save()

if __name__ == "__main__":
    create_sample_invoice()