from transformers import pipeline
from app.utils import split_text_into_chunks


def summarize_text(
        text: str, max_chunk_length: int = 700, max_summary_length: int = 50
) -> str:
    """
    Summarizes the given text into concise chunks.

    Args:
        text (str): The text to summarize.
        max_chunk_length (int): Maximum length of input text chunks.
        max_summary_length (int): Maximum length of the summary.

    Returns:
        str: The summarized text.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Split text into manageable chunks
    chunks = split_text_into_chunks(text, max_chunk_length)

    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=max_summary_length, min_length=25, do_sample=False)
        summaries.append(summary[0]["summary_text"])

    return " ".join(summaries)