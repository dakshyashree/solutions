import unittest
from pdf_extractor import PDFExtractor

class TestPDFExtractor(unittest.TestCase):
    def setUp(self):
        """Set up the PDFExtractor instance for testing."""
        self.extractor = PDFExtractor()

    def test_extract_text_from_valid_pdf(self):
        """Test extracting text from a valid PDF file."""
        # Assuming you have a sample PDF file for testing
        sample_pdf_path = "sample.pdf"  # Replace with the path to your test PDF
        extracted_text = self.extractor.extract_text(sample_pdf_path)
        self.assertIsInstance(extracted_text, str)
        self.assertGreater(len(extracted_text), 0, "Extracted text should not be empty.")

    def test_extract_text_from_invalid_pdf(self):
        """Test extracting text from an invalid PDF file."""
        invalid_pdf_path = "invalid.pdf"  # Replace with a path to an invalid PDF
        with self.assertRaises(Exception):
            self.extractor.extract_text(invalid_pdf_path)

    def test_extract_text_from_empty_pdf(self):
        """Test extracting text from an empty PDF file."""
        empty_pdf_path = "empty.pdf"  # Replace with a path to an empty PDF
        extracted_text = self.extractor.extract_text(empty_pdf_path)
        self.assertEqual(extracted_text, "", "Extracted text from an empty PDF should be empty.")

    def test_extract_text_from_non_pdf_file(self):
        """Test extracting text from a non-PDF file."""
        non_pdf_path = "sample.txt"  # Replace with a path to a non-PDF file
        with self.assertRaises(Exception):
            self.extractor.extract_text(non_pdf_path)

if __name__ == "__main__":
    unittest.main()