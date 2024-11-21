import os
import PyPDF2
from transformers import pipeline
from typing import List, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFTextProcessor:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.question_generator = pipeline("question-generation")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"The file {pdf_path} does not exist.")

        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text.strip()

    def summarize_text(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        """Generate a summary of the provided text."""
        if not text:
            raise ValueError("Cannot summarize empty text.")
        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

    def generate_questions(self, text: str) -> List[Dict[str, str]]:
        """Generate questions based on the provided text."""
        if not text:
            raise ValueError("Cannot generate questions from empty text.")
        return self.question_generator(text)

    def extract_topic_text(self, text: str, topic: str) -> str:
        """Extract text related to a specific topic."""
        topic_lower = topic.lower()
        lines = text.splitlines()
        extracted_lines = [line for line in lines if topic_lower in line.lower()]
        return "\n".join(extracted_lines).strip()

    def process_pdf(self, pdf_path: str, topics: List[str]) -> Dict[str, Dict[str, Any]]:
        """Process the PDF to extract summaries and questions for each topic."""
        logger.info(f"Processing PDF: {pdf_path}")
        extracted_text = self.extract_text_from_pdf(pdf_path)

        logger.info("Generating general summary...")
        results = {
            "general_summary": self.summarize_text(extracted_text),
            "topic_summaries": {}
        }

        for topic in topics:
            logger.info(f"Processing topic: {topic}")
            topic_text = self.extract_topic_text(extracted_text, topic)
            if topic_text:
                try:
                    topic_summary = self.summarize_text(topic_text)
                    questions = self.generate_questions(topic_summary)
                    results["topic_summaries"][topic] = {
                        "summary": topic_summary,
                        "questions": questions
                    }
                except ValueError as e:
                    logger.warning(f"Could not process topic '{topic}': {e}")
                    results["topic_summaries"][topic] = {
                        "summary": "",
                        "questions": []
                    }

        logger.info("PDF processing completed.")
        return results
