import re
import string
from typing import List, Optional

class TextCleaner:
    def __init__(self, retain_case: bool = False, retain_hyphen: bool = False):
        """Initialize the TextCleaner with optional parameters."""
        self.retain_case = retain_case
        self.retain_hyphen = retain_hyphen

    def remove_special_characters(self, text: str) -> str:
        """Remove special characters from the text."""
        allowed_characters = r'A-Za-z0-9\s'
        if self.retain_hyphen:
            allowed_characters += r'-'
        return re.sub(f'[^{allowed_characters}]+', '', text)

    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in the text."""
        return re.sub(r'\s+', ' ', text).strip()

    def remove_punctuation(self, text: str) -> str:
        """Remove punctuation from the text."""
        if self.retain_hyphen:
            punctuations = string.punctuation.replace("-", "")
        else:
            punctuations = string.punctuation
        return text.translate(str.maketrans('', '', punctuations))

    def clean_text(self, text: str) -> str:
        """Clean the text by applying various cleaning methods."""
        if not text:
            raise ValueError("Input text must not be empty.")

        text = self.remove_special_characters(text)
        text = self.normalize_whitespace(text)
        text = self.remove_punctuation(text)
        if not self.retain_case:
            text = text.lower()  # Convert to lowercase for uniformity
        return text

    def clean_texts(self, texts: List[str]) -> List[str]:
        """Clean a list of texts."""
        return [self.clean_text(text) for text in texts]


