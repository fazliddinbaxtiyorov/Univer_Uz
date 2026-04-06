# utils.py
import os
import time
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv()

api_key = os.getenv("CEREBRAS_API_KEY")
if not api_key:
    print("❌ CEREBRAS_API_KEY topilmadi! .env faylni tekshiring.")

client = Cerebras(api_key=api_key)
MODEL_NAME = "llama-3.1-8b"


def ask_cerebras(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful and accurate AI tutor."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_completion_tokens=600,
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ Cerebras xato ({attempt+1}/{max_retries}): {type(e).__name__}: {e}")
            error_text = str(e).lower()

            if "rate" in error_text or "429" in error_text:
                print("⏳ Rate limit. 5 soniya kutmoqda...")
                time.sleep(5)
                continue

            if any(k in error_text for k in ("auth", "api key", "401", "403")):
                return "❌ API key noto'g'ri yoki access yo'q. CEREBRAS_API_KEY ni tekshiring."

            if attempt < max_retries - 1:
                time.sleep(3)
                continue

            return f"❌ Xatolik yuz berdi: {e}"

    return "⚠️ Hozircha javob olib bo'lmadi. Keyinroq qayta urinib ko'ring."


def check_ielts_writing(task_type, question, answer):
    prompt = f"""
You are an IELTS examiner. Evaluate this {task_type}.

Question:
{question}

Candidate Answer:
{answer}

Format your response exactly like this:
Overall Band: [Score between 0-9]
Feedback: [Detailed feedback about the writing]
Suggestions:
1. [Specific tip]
2. [Specific tip]
3. [Specific tip]
"""
    return ask_cerebras(prompt)


def explain_wrong_answer(test_type, passage, question, correct_answer, user_answer, all_variants=None):
    # Til aniqlash
    is_english = any(t in test_type for t in ("IELTS", "SAT"))

    # Rasmli variant borligini tekshirish
    has_image_variants = any(
        '[Rasm variant' in v or '[Image variant' in v
        for v in (all_variants or {}).values()
        if v
    )

    # Savol rasmli ekanligini tekshirish
    has_question_image = '[Bu savolda rasm mavjud' in question or '[This question has an image' in question

    # Variantlarni formatlash
    variants_block = ""
    if all_variants:
        lines = [f"  {k}) {v}" for k, v in all_variants.items() if v]
        if lines:
            label = "Answer choices:" if is_english else "Javob variantlari:"
            variants_block = label + "\n" + "\n".join(lines) + "\n"

    # Rasm eslatmasi
    image_note = ""
    if has_image_variants or has_question_image:
        if is_english:
            image_note = (
                "\nNote: This question or some answer choices contain images. "
                "Since you cannot see the images, base your explanation only on "
                "the correct answer letter and general subject knowledge.\n"
            )
        else:
            image_note = (
                "\nEslatma: Bu savol yoki ba'zi variantlar rasm ko'rinishida. "
                "Rasmlarni ko'ra olmaganing uchun faqat to'g'ri javob harfi "
                "va mavzu bo'yicha umumiy bilim asosida tushuntir.\n"
            )

    # Passage / kontekst bloki
    is_reading_or_listening = any(t in test_type for t in ("Reading", "Listening"))

    if is_reading_or_listening and passage:
        if is_english:
            context_block = f"Text / Audio context:\n{passage}\n"
            rule_hint = "3. Point to the specific part of the text/audio that confirms the correct answer."
        else:
            context_block = f"Matn / Audio kontekst:\n{passage}\n"
            rule_hint = "3. Matnning qaysi qismi to'g'ri javobni tasdiqlaydi — shu joyni ko'rsat."
    else:
        if is_english:
            context_block = f"Subject / Topic: {passage}\n" if passage else ""
            rule_hint = "3. Briefly explain the key rule, formula, or concept related to this topic."
        else:
            context_block = f"Fan / Mavzu: {passage}\n" if passage else ""
            rule_hint = "3. Bu mavzu bo'yicha asosiy qoida, formula yoki tushunchani qisqacha tushuntir."

    # Prompt tuzish
    if is_english:
        prompt = f"""
You are a friendly and expert {test_type} tutor helping a student understand their mistake.

{context_block}
Question:
{question}

{variants_block}{image_note}
Student's answer : {user_answer if user_answer else '(no answer given)'}
Correct answer   : {correct_answer}

Please explain clearly and encouragingly IN ENGLISH:
1. Why "{user_answer}" is wrong — short and specific reason.
2. Why "{correct_answer}" is correct — explain with evidence.
{rule_hint}
4. One practical tip to avoid this mistake next time.

Maximum 200 words. Use simple, clear language.
"""
    else:
        prompt = f"""
Sen {test_type} bo'yicha tajribali va do'stona ustazsan. O'quvchiga xatosini tushuntir.

{context_block}
Savol:
{question}

{variants_block}{image_note}
O'quvchi tanladi : {user_answer if user_answer else '(javob berilmadi)'}
To'g'ri javob    : {correct_answer}

Quyidagi tartibda O'ZBEK TILIDA tushuntir:
1. Nima uchun "{user_answer}" noto'g'ri — qisqa va aniq sabab.
2. Nima uchun "{correct_answer}" to'g'ri — dalil bilan izohlat.
{rule_hint}
4. Keyingi safar xuddi shunday savolda qanday fikrlash kerak — 1 ta amaliy maslahat.

Maksimum 200 so'z. Oddiy, tushunarli til ishlat.
"""

    return ask_cerebras(prompt)