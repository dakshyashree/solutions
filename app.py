import streamlit as st
from src.pdf_extractor import extract_text_from_pdf
from src.text_summarizer import summarize_text
from src.text_cleaner import clean_text


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
                # Extract text from PDF
                raw_text = extract_text_from_pdf(uploaded_file)

                if not raw_text.strip():
                    st.error("The PDF file does not contain any readable text.")
                    return

                # Clean the extracted text
                cleaned_text = clean_text(raw_text)

                # Summarize the cleaned text
                summary = summarize_text(cleaned_text)

                # Display the original text and summary
                st.subheader("Original Text")
                st.write(cleaned_text)

                st.subheader("Summary")
                st.write(summary)

            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()