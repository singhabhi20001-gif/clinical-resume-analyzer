from docx import Document
from io import BytesIO

def generate_docx(resume_text):
    """
    Generate a DOCX file from resume text and return as bytes
    """
    doc = Document()

    for line in resume_text.split("\n"):
        doc.add_paragraph(line)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer
