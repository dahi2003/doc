from transformers import pipeline

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_len=200, min_len=50):
    if len(text) > 1000:  # Chunk long text
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        summaries = [summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text'] for chunk in chunks]
        return " ".join(summaries)
    else:
        return summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']