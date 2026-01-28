import docx

def extract_text_docx(path):
    doc = docx.Document(path)
    return " ".join([para.text for para in doc.paragraphs if para.text.strip()])