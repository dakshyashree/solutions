import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import logging

from app.text_extraction import extract_text_from_pdf
from app.summarization import summarize_text
from app.question_generation import generate_high_quality_questions
from app.utils import create_directory, save_to_file

# Configure logging
logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s: %(message)s")


class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Summarizer and Question Generator")
        self.pdf_path = None

        # Create logs directory if it doesn't exist
        create_directory("logs")
        create_directory("output")

        self.setup_ui()

    def setup_ui(self):
        # Buttons
        self.select_button = tk.Button(self.root, text="Select PDF", command=self.select_pdf)
        self.select_button.pack(pady=10)

        self.generate_button = tk.Button(
            self.root, text="Generate Summary and Questions",
            command=lambda: threading.Thread(target=self.process_pdf).start()
        )
        self.generate_button.pack(pady=10)

        # Output box
        self.output_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=30)
        self.output_box.pack(pady=10)

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not self.pdf_path:
            messagebox.showwarning("No File Selected", "Please select a valid PDF file.")
        else:
            messagebox.showinfo("File Selected", "PDF file has been selected.")

    def process_pdf(self):
        if not self.pdf_path:
            messagebox.showwarning("No File Selected", "Please select a PDF file first.")
            return

        try:
            # Extract, summarize, and generate questions
            extracted_text = extract_text_from_pdf(self.pdf_path)
            summary = summarize_text(extracted_text)
            questions = generate_high_quality_questions(summary)

            # Save results to a file
            output_content = f"Summary:\n{summary}\n\nQuestions:\n" + "\n".join(questions)
            save_to_file(content=output_content, file_path="output/summary_and_questions.txt")

            # Display results
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, f"Concise Summary:\n\n{summary}\n\n")
            self.output_box.insert(tk.END, "Generated Questions:\n\n")
            for question in questions:
                self.output_box.insert(tk.END, f"- {question}\n")

            messagebox.showinfo("Processing Complete",
                                "Summary and questions have been saved to output/summary_and_questions.txt")
            logging.info("Processing completed successfully.")
        except Exception as e:
            logging.error(f"Error during processing: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)
    root.mainloop()