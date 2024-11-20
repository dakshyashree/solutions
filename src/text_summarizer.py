from transformers import pipeline
from typing import List, Dict
class TextSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """Initialize the TextSummarizer with a specified model."""
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize_text(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        """Generate a summary of the provided text."""
        if not text:
            raise ValueError("Input text must not be empty.")

        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

    def summarize_texts(self, texts: List[str], max_length: int = 130, min_length: int = 30) -> List[str]:
        """Generate summaries for a list of texts."""
        summaries = []
        for text in texts:
            summary = self.summarize_text(text, max_length, min_length)
            summaries.append(summary)
        return summaries


if __name__ == "__main__":
    # Example usage
    sample_text = (
        "The capital of France is Paris. It is known for its art, fashion, and culture. "
        "Paris is home to the Eiffel Tower, one of the most recognizable structures in the world. "
        "The city is also famous for its cafes, museums, and historical landmarks."
    )

    summarizer = TextSummarizer()
    try:
        summary = summarizer.summarize_text(sample_text)
        print("Original Text:")
        print(sample_text)
        print("\nSummary:")
        print(summary)
    except Exception as e:
        print(f"An error occurred: {e}")