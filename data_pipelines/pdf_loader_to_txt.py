import fitz

def pipe_2_pdf_to_txt(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip() 

