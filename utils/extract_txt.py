def extract_text_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()