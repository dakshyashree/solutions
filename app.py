import streamlit as st
import pdfplumber
from transformers import pipeline
import re


# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text
    return text


# Step 2: Summarize the extracted text in smaller chunks
def summarize_text(text, max_chunk_length=1000):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Split the text into chunks if it's too long
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]

    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
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


# Enhanced question generation function
# Enhanced question generation function
def generate_questions(summary):
    question_generator = pipeline("text2text-generation", model="t5-base")
    questions = []

    # Split the summary into sentences
    sentences = re.split(r'(?<=\w[.!?])\s', summary)  # Split sentences accurately

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue  # Skip empty sentences

        generated_questions = []

        # Define specific prompts to ensure meaningful questions
        prompts = [
            f"Turn this statement into a question: {sentence}",
            f"Ask a 'why' question about: {sentence}",
            f"Ask a 'how' question about: {sentence}",
            f"Create a question based on: {sentence}"
        ]

        # Try generating questions for each prompt
        for prompt in prompts:
            try:
                question = question_generator(prompt, max_length=50, num_beams=5, early_stopping=True)[0]['generated_text']
                # Validate and add unique questions
                if question and question not in generated_questions:
                    generated_questions.append(question.strip())
            except Exception:
                continue  # Skip errors during generation

        # Use fallback questions if nothing valid is generated
        if not generated_questions:
            fallback_questions = [
                f"What is the main idea of: '{sentence}'?",
                f"Why might this be important: '{sentence}'?",
                f"How does this relate to the context?"
            ]
            generated_questions.extend(fallback_questions)

        # Append unique questions to the final list
        for question in generated_questions:
            if question not in questions:
                questions.append(question)

    return questions



# Streamlit UI
st.title("PDF Summarization and Q&A Tool")

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    try:
        # Extract text from PDF
        with st.spinner("Extracting text from the PDF..."):
            text = extract_text_from_pdf(uploaded_file)

        if not text:
            st.error("No text extracted from the PDF. The file may contain non-selectable text.")
        else:
            # Clean the extracted text
            clean_text_data = clean_text(text)

            # Let the user choose the maximum chunk length for summarization
            max_chunk_length = st.slider("Select max chunk length for summarization:", 500, 2000, 1000, 100)

            with st.spinner("Summarizing the extracted text..."):
                # Summarize the cleaned text
                summary = summarize_text(clean_text_data, max_chunk_length)

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
                        with st.spinner("Processing your question..."):
                            answer = question_answering_pipeline(question=user_question, context=summary)["answer"]

                        # Display the answer
                        st.subheader("Answer:")
                        st.write(answer)
                    else:
                        st.warning("Please enter a question before clicking the button.")

                # Generate and display questions based on the summary
                st.subheader("Questions based on the summary:")
                questions = generate_questions(summary)
                if questions:
                    with st.expander("View all generated questions"):
                        for i, question in enumerate(questions, 1):
                            st.markdown(f"**{i}. {question}**")
                else:
                    st.write("No questions could be generated. Please ensure the summary contains enough detail.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
