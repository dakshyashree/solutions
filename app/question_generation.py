from transformers import pipeline


def generate_high_quality_questions(
        summary_text: str, num_questions: int = 3
) -> list:
    """
    Generates high-quality questions based on the summarized text.

    Args:
        summary_text (str): The summarized text.
        num_questions (int): Number of questions to generate.

    Returns:
        list: A list of generated questions.
    """
    question_generator = pipeline("text2text-generation", model="valhalla/t5-base-qa-qg-hl", device=-1)

    # Process summary in manageable pieces for better generation
    max_question_length = 300
    chunks = [summary_text[i:i + max_question_length] for i in range(0, len(summary_text), max_question_length)]

    questions = []
    for chunk in chunks:
        prompt = f"Generate distinct questions based on the following:\n\n{chunk}\n\n"
        try:
            question_output = question_generator(
                prompt, max_length=100, num_return_sequences=min(num_questions, 1), num_beams=3
            )
            for output in question_output:
                question_text = output["generated_text"].strip()
                if question_text.endswith("?") and question_text not in questions:
                    questions.append(question_text)
            if len(questions) >= num_questions:
                break
        except Exception as e:
            print(f"Error generating questions for chunk: {e}")

    return questions[:num_questions] if questions else ["No questions generated."]