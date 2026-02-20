from .utils import explain_wrong_answer


def get_ai_explanation(test_type, passage, question, correct_answer, user_answer):
    """
    Views.py dan chaqiriladi.
    test_type: 'SAT', 'IELTS Reading', 'IELTS Listening'
    """
    return explain_wrong_answer(
        test_type=test_type,
        passage=passage,
        question=question,
        correct_answer=correct_answer,
        user_answer=user_answer
    )