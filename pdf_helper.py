from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(resume_text):
    """
    Generate a PDF file from resume text and return as bytes
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    x_margin = 40
    y_position = height - 40

    for line in resume_text.split("\n"):
        if y_position < 40:
            c.showPage()
            y_position = height - 40

        c.drawString(x_margin, y_position, line)
        y_position -= 14

    c.save()
    buffer.seek(0)

    return buffer
