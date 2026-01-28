import sys
from utils.extract_docx import extract_text_docx
from utils.extract_pdf import extract_text_pdf
from utils.extract_pptx import extract_text_pptx
from utils.extract_txt import extract_text_txt
from summarizer.summarizer import summarize_text

def get_text_from_file(path):
    if path.endswith(".docx"):
        return extract_text_docx(path)
    elif path.endswith(".pdf"):
        return extract_text_pdf(path)
    elif path.endswith(".pptx"):
        return extract_text_pptx(path)
    elif path.endswith(".txt"):
        return extract_text_txt(path)
    else:
        raise ValueError("Unsupported file format")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    text = get_text_from_file(file_path)
    summary = summarize_text(text)
    print("\n--- Document Summary ---\n")
    print(summary)