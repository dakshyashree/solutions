import streamlit as st
import pdfplumber
from transformers import pipeline
import re


# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


# Step 2: Summarize the extracted text in smaller chunks
def summarize_text(text, max_chunk_length=1000):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Split the text into chunks if it's too long
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]

    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=47, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    # Combine the summaries into one final summary
    return " ".join(summaries)


# Clean text function to remove unwanted characters and formatting issues
def clean_text(text):
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # Remove unwanted newlines or characters that might affect rendering
    text = re.sub(r'\n+', ' ', text)

    return text.strip()


# Streamlit UI
st.title("PDF Summarization and Q&A Tool")

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(uploaded_file)

        if not text:
            st.error("No text extracted from the PDF.")
        else:
            # Clean the extracted text
            clean_text_data = clean_text(text)

            # Summarize the cleaned text
            summary = summarize_text(clean_text_data)

            if len(summary.strip()) == 0:
                st.error("Summary is empty. Unable to generate a meaningful summary.")
            else:
                # Display the summary
                st.subheader("Summary:")
                st.markdown(summary)

                # Load the question-answering pipeline
                question_answering_pipeline = pipeline("question-answering")

                # User input for questions
                st.subheader("Ask a question about the summary:")
                user_question = st.text_area("Type your question here...", height=100)

                # Submit button for processing the question
                if st.button("Get Answer"):
                    if user_question:
                        # Generate answer based on the user question and the summary
                        answer = question_answering_pipeline(question=user_question, context=summary)["answer"]

                        # Display the answer
                        st.subheader("Answer:")
                        st.write(answer)
                    else:
                        st.warning("Please enter a question before clicking the button.")

    except Exception as e:
        st.error(f"An error occurred: {e}")