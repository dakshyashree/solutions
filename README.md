This application provides an intuitive and efficient solution for summarizing PDF documents and generating meaningful questions for study or review purposes. Built using Streamlit, it offers a user-friendly interface to streamline text extraction, summarization, and question generation. Key features include:

PDF Text Extraction: Extracts text from uploaded PDF files using the pdfplumber library, ensuring accurate retrieval of content even from multi-page documents.

Text Summarization: Summarizes lengthy texts into concise and coherent summaries using a pre-trained BART model (facebook/bart-large-cnn), making it easier to grasp the main ideas. Users can control the chunk size for processing through an adjustable slider.

Dynamic Question Generation: Utilizes a pre-trained T5 model (t5-base) to create insightful questions based on the summarized text. The questions are context-aware and cover various aspects such as reasoning (why), methods (how), and comprehension.

Interactive Q&A: Enables users to ask specific questions about the summarized content. The app leverages a question-answering pipeline to provide accurate answers derived directly from the context of the summary.

Customization and Feedback:

Allows users to select chunk sizes for summarization to balance detail and brevity.
Displays generated questions and provides an expander to review all questions conveniently.
Offers fallback mechanisms to ensure meaningful outputs even in cases of sparse data.
Streamlined Workflow:

Upload a PDF file via the app.
Extract, clean, and summarize the document content automatically.
Generate and review questions or interactively ask your own for tailored insights.
Usage:

Navigate to the project directory and locate the app.py file.
Run the application with the command:
streamlit run app.py
Open the local host link displayed in the terminal to access the app via your web browser.
This tool is ideal for students, educators, and professionals seeking to summarize complex documents and generate meaningful study material or questions. With its combination of AI-powered pipelines and an interactive interface, it provides a seamless and efficient experience.
