import re
import string
from typing import List

class TextCleaner:
    def __init__(self):
        """Initialize the TextCleaner."""
        pass

    def remove_special_characters(self, text: str) -> str:
        """Remove special characters from the text."""
        return re.sub(r'[^A-Za-z0-9\s]+', '', text)

    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in the text."""
        return re.sub(r'\s+', ' ', text).strip()

    def remove_punctuation(self, text: str) -> str:
        """Remove punctuation from the text."""
        return text.translate(str.maketrans('', '', string.punctuation))

    def clean_text(self, text: str) -> str:
        """Clean the text by applying various cleaning methods."""
        if not text:
            raise ValueError("Input text must not be empty.")

        text = self.remove_special_characters(text)
        text = self.normalize_whitespace(text)
        text = self.remove_punctuation(text)
        return text.lower()  # Convert to lowercase for uniformity

    def clean_texts(self, texts: List[str]) -> List[str]:
        """Clean a list of texts."""
        return [self.clean_text(text) for text in texts]


if __name__ == "__main__":
    # Example usage
    sample_text = "Hello, World! This is a sample text with special characters: @#$%^&*() and punctuation!!!"

    cleaner = TextCleaner()
    try:
        cleaned_text = cleaner.clean_text(sample_text)
        print("Original Text:")
        print(sample_text)
        print("\nCleaned Text:")
        print(cleaned_text)
    except Exception as e:
        print(f"An error occurred: {e}")