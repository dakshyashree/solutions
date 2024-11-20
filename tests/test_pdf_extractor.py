import unittest
import tempfile
from pdf_extractor import PDFExtractor

class TestPDFExtractor(unittest.TestCase):
    def setUp(self):
        """Set up the PDFExtractor instance for testing."""
        self.extractor = PDFExtractor()

    def test_extract_text_from_valid_pdf(self):
        """Test extracting text from a valid PDF file."""
        valid_pdf_content = b"%PDF-1.4\n1 0 obj\n<</Type /Catalog>>\nendobj\n"
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            temp_pdf.write(valid_pdf_content)
            temp_pdf.flush()
            extracted_text = self.extractor.extract_text(temp_pdf.name)
            self.assertIsInstance(extracted_text, str)
            self.assertGreater(len(extracted_text), 0, "Extracted text should not be empty.")

    def test_extract_text_from_invalid_pdf(self):
        """Test extracting text from an invalid PDF file."""
        invalid_pdf_content = b"This is not a PDF file."
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            temp_pdf.write(invalid_pdf_content)
            temp_pdf.flush()
            with self.assertRaises(ValueError):  # Replace with the specific exception you expect
                self.extractor.extract_text(temp_pdf.name)

    def test_extract_text_from_empty_pdf(self):
        """Test extracting text from an empty PDF file."""
        empty_pdf_content = b""
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            temp_pdf.write(empty_pdf_content)
            temp_pdf.flush()
            extracted_text = self.extractor.extract_text(temp_pdf.name)
            self.assertEqual(extracted_text, "", "Extracted text from an empty PDF should be empty.")

    def test_extract_text_from_non_pdf_file(self):
        """Test extracting text from a non-PDF file."""
        non_pdf_content = b"Just some text, not a PDF."
        with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
            temp_file.write(non_pdf_content)
            temp_file.flush()
            with self.assertRaises(ValueError):  # Replace with the specific exception you expect
                self.extractor.extract_text(temp_file.name)

    def test_extract_text_from_encrypted_pdf(self):
        """Test extracting text from an encrypted PDF file."""
        # Create a simulated encrypted PDF file
        encrypted_pdf_content = b"%PDF-1.4\n1 0 obj\n<</Encrypt>>\nendobj\n"
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            temp_pdf.write(encrypted_pdf_content)
            temp_pdf.flush()
            with self.assertRaises(PermissionError):  # Replace with the specific exception you expect
                self.extractor.extract_text(temp_pdf.name)


if __name__ == "__main__":
    unittest.main()
