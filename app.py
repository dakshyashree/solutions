import streamlit as st
from src.pdf_extractor import PDFTextProcessor
from src.text_summarizer import TextSummarizer
from src.text_cleaner import TextCleaner

def main():
    # Set the title and description of the app
    st.title("PDF Summarization App")
    st.markdown("""
        This application allows users to upload PDF files and receive a summarized version of the content.
        Simply upload a PDF file, and the app will extract the text, clean it, and provide a summary.
    """)

    # File uploader for PDF files
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Display a progress spinner while processing the PDF
        with st.spinner("Processing your PDF..."):
            try:
                # Create an instance of PDFTextProcessor
                processor = PDFTextProcessor()

                # Extract text from PDF
                raw_text = processor.extract_text_from_pdf(uploaded_file)

                # Check if raw_text is empty
                if not raw_text.strip():
                    st.error("The PDF file does not contain any readable text.")
                    return

                # Clean the extracted text
                cleaned_text = TextCleaner.clean_text(raw_text)  # Assuming clean_text is a static method

                # Check if cleaned_text is empty
                if not cleaned_text.strip():
                    st.error("The cleaned text is empty. Please check the PDF content.")
                    return

                # Summarize the cleaned text
                summary = TextSummarizer.summarize_text(cleaned_text)  # Assuming summarize_text is a static method

                # Check if summary is empty
                if not summary.strip():
                    st.error("The summary is empty. Please check the cleaning and summarization process.")
                    return

                # Display the original text and summary
                st.subheader("Original Text")
                st.write(cleaned_text)

                st.subheader("Summary")
                st.write(summary)

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()