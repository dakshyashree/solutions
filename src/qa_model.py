from transformers import pipeline
from typing import List, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QAModel:
    def __init__(self, model_name: str = "deepset/roberta-base-squad2"):
        """Initialize the QA model with a specified model name."""
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def answer_question(self, question: str, context: str, score_threshold: float = 0.0) -> Dict[str, Any]:
        """Generate an answer to a single question based on the provided context."""
        if not question or not context:
            raise ValueError("Question and context must not be empty.")

        result = self.qa_pipeline(question=question, context=context)
        if result['score'] < score_threshold:
            return {
                "question": question,
                "answer": "Confidence score too low.",
                "score": result['score']
            }

        return {
            "question": question,
            "answer": result['answer'],
            "score": result['score']
        }

    def answer_questions(self, questions: List[str], context: str, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        """Generate answers for a list of questions based on the provided context."""
        if not questions or not context:
            raise ValueError("Questions and context must not be empty.")

        answers = []
        for question in questions:
            try:
                answer = self.answer_question(question, context, score_threshold)
                answers.append(answer)
            except Exception as e:
                logger.error(f"Error processing question '{question}': {e}")
                answers.append({
                    "question": question,
                    "answer": "Error in answering the question.",
                    "score": 0.0,
                    "error": str(e)
                })
        return answers

