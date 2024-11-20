import os
import PyPDF2
from transformers import pipeline
from typing import List, Dict


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
                text += page.extract_text() or ""
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

        questions = self.question_generator(text)
        return questions

    def process_pdf(self, pdf_path: str, topics: List[str]) -> Dict[str, Dict[str, List[str]]]:
        """Process the PDF to extract summaries and questions for each topic."""
        extracted_text = self.extract_text_from_pdf(pdf_path)

        results = {
            "general_summary": self.summarize_text(extracted_text),
            "topic_summaries": {}
        }

        for topic in topics:
            topic_text = self.extract_topic_text(extracted_text, topic)  # Implement this method
            if topic_text:
                topic_summary = self.summarize_text(topic_text)
                questions = self.generate_questions(topic_summary)
                results["topic_summaries"][topic] = {
                    "summary": topic_summary,
                    "questions": questions
                }

        return results

    def extract_topic_text(self, text: str, topic: str) -> str:
        """Extract text related to a specific topic. This is a placeholder for actual implementation."""
        # Implement logic to extract text for the given topic
        # For example, you could use keyword matching or NLP techniques to find relevant sections
        return text  # Placeholder: return the entire text for now


if __name__ == "__main__":
    pdf_path = "your_pdf_file.pdf"  # Specify your PDF file path
    topics = ["Topic 1", "Topic 2"]  # Replace with actual topics

    processor = PDFTextProcessor()
    try:
        results = processor.process_pdf(pdf_path, topics)

        print("General Summary:")
        print(results["general_summary"])

        for topic, data in results["topic_summaries"].items():
            print(f"\nSummary for {topic}:")
            print(data["summary"])
            print(f"Questions for {topic}:")
            for question in data["questions"]:
                print(question['question'])
    except Exception as e:
        print(f"An error occurred: {e}")