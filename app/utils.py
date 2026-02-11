import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")


def check_ielts_writing(task_type, question, answer):
    prompt = f"""
    You are an IELTS examiner. Evaluate this {task_type}.
    Question: {question}
    Candidate Answer: {answer}

    Format:
    Overall Band: [Score]
    Feedback: [Detailed feedback]
    Suggestions: [3 tips]
    """

    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                print(f"Limit band, {attempt + 1}-urinish. 10 soniya kutilyapti...")
                time.sleep(10)
                continue
            return f"Xatolik: {e}"

    return "Limitlar tufayli javob olib bo'lmadi. Birozdan keyin urinib ko'ring."


# Ishlatib ko'ramiz
if __name__ == "__main__":
    result = check_ielts_writing("Task 2", "Is AI good?", "I think AI is helpful.")
    print(result)