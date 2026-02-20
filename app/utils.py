import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY topilmadi! .env faylni tekshiring.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-latest")

def check_ielts_writing(task_type, question, answer):
    prompt = f"""
You are an IELTS examiner. Evaluate this {task_type}.
Question: {question}
Candidate Answer: {answer}

Format your response exactly like this:
Overall Band: [Score between 0-9]
Feedback: [Detailed feedback about the writing]
Suggestions: [3 specific tips to improve]
"""

    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ check_ielts_writing xato ({attempt+1}/3): {type(e).__name__}: {e}")
            if "429" in str(e) or "quota" in str(e).lower():
                print("Rate limit! 10 soniya kutilmoqda...")
                time.sleep(10)
                continue
            return f"Xatolik yuz berdi: {e}"

    return "Limitlar tufayli javob olib bo'lmadi. Birozdan keyin urinib ko'ring."


def explain_wrong_answer(test_type, passage, question, correct_answer, user_answer):
    """
    Xato javob uchun AI tushuntirish beradi.

    Parametrlar:
        test_type     : 'IELTS Reading', 'IELTS Listening', 'SAT', 'Milliy Sertifikat'
        passage       : Matn yoki kontekst
        question      : Savol matni
        correct_answer: To'g'ri variant (A/B/C/D)
        user_answer   : Foydalanuvchi tanlagan variant
    """

    prompt = f"""
You are a friendly and expert {test_type} tutor helping a student understand their mistake.

Context/Passage:
{passage}

Question:
{question}

The student answered: {user_answer}
The correct answer is: {correct_answer}

Please explain in a clear, simple and encouraging way (in Uzbek language):
1. Nima uchun "{user_answer}" javobi noto'g'ri
2. Nima uchun "{correct_answer}" javobi to'g'ri
3. Matndan qaysi qism bu javobni tasdiqlaydi
4. Kelajakda bunday xatoni qilmaslik uchun 1 ta maslahat

Maksimum 150 so'z ishlatib, oddiy va tushunarli tilda yozing.
"""

    for attempt in range(3):
        try:
            print(f"🤖 Gemini so'rov yuborilmoqda... (urinish {attempt+1}/3)")
            response = model.generate_content(prompt)
            print("✅ Gemini javob berdi!")
            return response.text
        except Exception as e:
            print(f"❌ explain_wrong_answer xato ({attempt+1}/3): {type(e).__name__}: {e}")
            if "429" in str(e) or "quota" in str(e).lower():
                print("Rate limit! 10 soniya kutilmoqda...")
                time.sleep(10)
                continue
            elif "invalid" in str(e).lower() or "api_key" in str(e).lower():
                return "❌ API kalit noto'g'ri yoki muddati o'tgan. GEMINI_API_KEY ni tekshiring."
            return f"❌ Xatolik: {e}"

    return "⚠️ Hozirda Gemini API band. Bir oz kutib qayta urinib ko'ring."