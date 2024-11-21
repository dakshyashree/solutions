from transformers import pipeline
from typing import List, Dict

class TextSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """Initialize the TextSummarizer with a specified model."""
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize_text(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        """Generate a summary of the provided text."""
        if not text.strip():
            raise ValueError("Input text must not be empty.")
        if len(text) < min_length:
            raise ValueError("Input text is too short for summarization.")

        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

    def summarize_texts(self, texts: List[str], max_length: int = 130, min_length: int = 30) -> List[str]:
        """Generate summaries for a list of texts."""
        summaries = []
        for text in texts:
            try:
                if len(text.strip()) >= min_length:
                    summary = self.summarize_text(text, max_length, min_length)
                    summaries.append(summary)
                else:
                    summaries.append("Text is too short for summarization.")
            except Exception as e:
                summaries.append(f"Error summarizing text: {e}")
        return summaries

