from transformers import pipeline
from typing import List, Dict


class QAModel:
    def __init__(self, model_name: str = "deepset/roberta-base-squad2"):
        """Initialize the QA model."""
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def answer_question(self, question: str, context: str) -> Dict[str, str]:
        """Generate an answer to a question based on the provided context."""
        if not question or not context:
            raise ValueError("Question and context must not be empty.")

        result = self.qa_pipeline(question=question, context=context)
        return {
            "question": question,
            "answer": result['answer'],
            "score": result['score']
        }

    def answer_questions(self, questions: List[str], context: str) -> List[Dict[str, str]]:
        """Generate answers for a list of questions based on the provided context."""
        answers = []
        for question in questions:
            answer = self.answer_question(question, context)
            answers.append(answer)
        return answers


if __name__ == "__main__":
    # Example usage
    context = "The capital of France is Paris. It is known for its art, fashion, and culture."
    questions = [
        "What is the capital of France?",
        "What is Paris known for?"
    ]

    qa_model = QAModel()
    try:
        answers = qa_model.answer_questions(questions, context)
        for answer in answers:
            print(f"Q: {answer['question']}\nA: {answer['answer']} (Score: {answer['score']:.2f})\n")
    except Exception as e:
        print(f"An error occurred: {e}")