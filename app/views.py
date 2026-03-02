from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import (
    FanlarForm, IELTSReadingForm, TestForm, FanTanlashForm,
    IELTSListeningForm, SATForm, Writing, TestFanForm, ContactForm
)
from .models import (
    IELTS_Reading, Milliy_Sertifikat, IELTSListeningQuestion,
    SATQuestion, Davlat_Univer, Xususiy_Univer, Xorijiy_Univer,
    ContactMessage, UserTestResult, ReadingTest, ListeningTest, Sat, TestAccess, DTM_Majburiy

)
from user.models import Friendship
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Q
from django.contrib.auth.models import User
import random, time, re, json
from datetime import date, timedelta
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test

from .models import WritingQuestion, WritingSubmission
from .forms import WritingSubmissionForm
from .utils import check_ielts_writing
from .hi import get_ai_explanation
from .models import News


# ======================== CONSTANTS ========================

VILOYATLAR = [
    'Toshkent', 'Samarqand', 'Buxoro', 'Andijon', "Farg'ona",
    'Namangan', 'Xorazm', 'Qashqadaryo', 'Surxondaryo',
    'Jizzax', 'Sirdaryo', 'Navoiy', "Qoraqalpog'iston"
]


# ======================== HELPERS ========================

def score_to_band(correct_count, total=40):
    """IELTS rasmiy band score jadvali"""
    if total != 40:
        correct_count = round(correct_count * 40 / total)
    table = {
        40: 9.0, 39: 8.5, 38: 8.5, 37: 8.0, 36: 8.0,
        35: 7.5, 34: 7.0, 33: 7.0, 32: 6.5, 31: 6.5,
        30: 6.0, 29: 6.0, 28: 5.5, 27: 5.5, 26: 5.0,
        25: 5.0, 24: 4.5, 23: 4.5, 22: 4.0, 21: 4.0,
        20: 4.0, 19: 3.5, 18: 3.5, 17: 3.0, 16: 3.0,
    }
    return table.get(correct_count, 0)


def update_streak(user):
    """Har kuni test yechsa streak oshadi"""
    profile = user.profile
    today = date.today()
    if profile.last_test_date == today:
        return
    if profile.last_test_date == today - timedelta(days=1):
        profile.streak_days += 1
    else:
        profile.streak_days = 1
    profile.last_test_date = today
    profile.save()


def get_discounted_price(user, original_price):
    """5 kun streak bo'lsa 25% chegirma"""
    if user.profile.streak_days >= 5:
        return int(original_price * 0.75)
    return original_price


def coins_back_if_perfect(user, percentage):
    """100% to'g'ri javob bersa 20 coin qaytarish"""
    if percentage == 100.0:
        profile = user.profile
        profile.coins += 20
        profile.save()
        return True
    return False


def check_sat_master(user, percentage):
    """5 ketma-ket 100% → SAT Master 🏆"""
    profile = user.profile
    if percentage == 100.0:
        profile.consecutive_perfect += 1
        if profile.consecutive_perfect >= 5:
            profile.badge = 'SAT Master 🏆'
    else:
        profile.consecutive_perfect = 0
    profile.save()
    return profile.badge == 'SAT Master 🏆'


def check_test_access(user, test, category):
    profile = user.profile
    update_streak(user)
    actual_price = get_discounted_price(user, test.price)

    with transaction.atomic():
        access, created = TestAccess.objects.get_or_create(
            user=user,
            category=category,
            test_id=test.id
        )
        if not created and access.paid:
            return True, "already_paid"
        if profile.coins < actual_price:
            return False, "not_enough_coins"
        profile.coins -= actual_price
        profile.save()
        access.paid = True
        access.save()
    return True, "paid_now"


def get_time_spent(request, session_key):
    start_time = request.session.get(session_key)
    end_time = time.time()
    spent_seconds = int(end_time - start_time)
    minutes = spent_seconds // 60
    seconds = spent_seconds % 60
    return minutes, seconds


def answers_match(user_answer, correct_answer):
    if not user_answer:
        return False
    return user_answer.strip().lower() == correct_answer.strip().lower()


# ======================== ODDIY VIEWLAR ========================

def support(request):
    return render(request, 'support.html')


def ielts(request):
    return render(request, 'ielts.html')


def fanlar_view(request):
    form = FanlarForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, "home.html", {"form": form, 'news_items': News.objects.filter(is_active=True).order_by('-created_at')[:6]})


def writing(request):
    form = Writing(request.POST)
    if form.is_valid():
        form.save()
    return render(request, "writing.html", {"form": form})


def test_list_listening(request):
    tests = ListeningTest.objects.all()
    return render(request, "ielts.html", {
        "tests_listening": tests,
        "current_category": "LISTENING"
    })


def test_list_view(request):
    all_passages = ReadingTest.objects.filter(category='READING').order_by('id')[:10]
    total_questions = sum(p.questions.count() for p in all_passages)
    return render(request, "ielts.html", {
        "tests": all_passages,
        "total_questions": total_questions,
        "duration": 60,
    })


def test_list_sat(request):
    tests = Sat.objects.all()
    return render(request, "sat.html", {"tests": tests})


def fan_tanlash(request):
    selected_fan = request.GET.get('fan', '')
    fans_with_count = []
    for code, name in Milliy_Sertifikat.FAN_CHOICES:
        count = Milliy_Sertifikat.objects.filter(fan=code).count()
        fans_with_count.append({'code': code, 'name': name, 'count': count})
    return render(request, "fan_tanlash.html", {
        "fans_with_count": fans_with_count,
        "selected_fan": selected_fan,
    })


def univerlar(request):
    davlat = Davlat_Univer.objects.all()
    xususiy = Xususiy_Univer.objects.all()
    xorijiy = Xorijiy_Univer.objects.all()
    return render(request, 'univerlar.html', {
        'davlat': davlat,
        'xususiy': xususiy,
        'xorijiy': xorijiy
    })


def contact_view(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],
        )
        return redirect('support')
    return render(request, 'support.html')


# ======================== IELTS DASHBOARD ========================

def ielts_main_dashboard(request):
    category = request.GET.get('category', 'ALL').upper()
    context = {
        'current_category': category,
        'tests': ReadingTest.objects.filter(category='READING') if category in ('ALL', 'READING') else [],
        'tests_listening': ListeningTest.objects.filter(category='LISTENING') if category in ('ALL', 'LISTENING') else [],
        'tests_writing': WritingQuestion.objects.all() if category in ('ALL', 'WRITING') else [],
    }
    return render(request, 'ielts.html', context)


def writing_tests(request):
    testlar = WritingQuestion.objects.all()
    return render(request, 'ielts.html', {
        'tests_writing': testlar,
        'current_category': 'WRITING'
    })


# ======================== IELTS READING ========================

@login_required
def ielts_reading_view(request, test_id=None):
    if test_id:
        reading_test = get_object_or_404(ReadingTest, pk=test_id)
    else:
        reading_test = ReadingTest.objects.first()

    if not reading_test:
        messages.error(request, "Reading testi mavjud emas!")
        return redirect("ielts_main_dashboard")

    if request.method == "POST":
        allowed, status = check_test_access(
            request.user, reading_test, category="IELTS_READING"
        )
        if not allowed:
            messages.error(request, "Sizda yetarli coin yo'q!")
            return redirect("buy_coins")

    all_questions = list(reading_test.questions.all().order_by('part', 'id'))

    if 'reading_start' not in request.session:
        request.session['reading_start'] = time.time()

    form = IELTSReadingForm(request.POST or None, questions=all_questions)

    if request.method == "POST" and form.is_valid():
        correct_count = sum(
            1 for q in all_questions
            if answers_match(form.cleaned_data.get(f'q_{q.id}'), q.togri_variant)
        )
        total = correct_count * 2
        start = request.session.pop('reading_start', time.time())
        spent = int(time.time() - start)
        percentage = round(correct_count / len(all_questions) * 100, 1) if all_questions else 0

        band_score = score_to_band(correct_count, total=len(all_questions))
        coins_returned = coins_back_if_perfect(request.user, percentage)

        UserTestResult.objects.create(
            user=request.user,
            test_name="IELTS Reading",
            score=percentage
        )

        # answers_match funksiyasi allaqachon bor, YNNG ham shu orqali ishlaydi
        # faqat result.html da question_type ni ko'rsatish uchun results ga qo'shing:
        results = [{
            "savol": q.savol,
            "question_type": q.question_type,  # ← bor
            "user_answer": form.cleaned_data.get(f'q_{q.id}'),
            "correct": q.togri_variant,
            "is_correct": answers_match(form.cleaned_data.get(f'q_{q.id}'), q.togri_variant),
            "question_id": q.id,
            "category": "IELTS"
        } for q in all_questions]

        return render(request, "result.html", {
            "results": results,
            "total": total,
            "correct_count": correct_count,
            "total_questions": len(all_questions),
            "percentage": percentage,
            "band_score": band_score,
            "coins_returned": coins_returned,
            "minutes": spent // 60,
            "seconds": spent % 60,
            "test_type": "IELTS Reading",
        })

    parts_dict = {}
    for q in all_questions:
        parts_dict.setdefault(q.part, []).append(q)

    test_data = []
    for part_num in sorted(parts_dict.keys()):
        qs = parts_dict[part_num]
        title, text = reading_test.get_passage(part_num)  # ← YANGI
        test_data.append({
            "part": part_num,
            "part_label": f"Part {part_num}",
            "passage_title": title,  # ← YANGI
            "passage_text": text,  # ← har part o'z matni
            "questions": [{"model": q, "field": form[f"q_{q.id}"]} for q in qs]
        })

    return render(request, "reading_test.html", {
        "test_data": test_data,
        "total_steps": len(test_data),
        "duration": 60,
        "reading_test": reading_test,
        "user_coins": request.user.profile.coins,
        "streak_days": request.user.profile.streak_days,
        "has_discount": request.user.profile.streak_days >= 5,
        "test_id": reading_test.id
    })


# ======================== IELTS LISTENING ========================

@login_required
def ielts_listening_view(request, test_id):
    test = get_object_or_404(ListeningTest, pk=test_id)
    questions = test.questions.all().order_by('part', 'id')
    form = IELTSListeningForm(request.POST or None, questions=questions)

    if request.method == "POST":
        allowed, status = check_test_access(request.user, test, category="IELTS_LISTENING")
        if not allowed:
            messages.error(request, "Sizda yetarli coin yo'q!")
            return redirect("buy_coins")

        if form.is_valid():
            correct_count = sum(
                1 for q in questions
                if answers_match(form.cleaned_data.get(f'q_{q.id}'), q.togri_variant)
            )
            start_time = request.session.pop('listening_start', time.time())
            spent = int(time.time() - start_time)
            q_count = questions.count()
            percentage = round((correct_count / q_count) * 100, 1) if q_count > 0 else 0

            band_score = score_to_band(correct_count, total=q_count)
            coins_returned = coins_back_if_perfect(request.user, percentage)

            UserTestResult.objects.create(
                user=request.user,
                test_name=f"Listening - {test.title}",
                score=percentage
            )

            results = [{
                "savol": q.savol,
                "question_type": q.question_type,
                "user_answer": form.cleaned_data.get(f'q_{q.id}'),
                "correct": q.togri_variant,
                "is_correct": answers_match(form.cleaned_data.get(f'q_{q.id}'), q.togri_variant),
                "question_id": q.id,
                "category": "IELTS_LISTENING"
            } for q in questions]

            return render(request, "result.html", {
                "results": results,
                "total": correct_count,
                "correct_count": correct_count,
                "total_questions": q_count,
                "percentage": percentage,
                "band_score": band_score,
                "coins_returned": coins_returned,
                "minutes": spent // 60,
                "seconds": spent % 60,
                "test_type": f"IELTS Listening - {test.title}",
            })

    if 'listening_start' not in request.session:
        request.session['listening_start'] = time.time()

    parts = {}
    for q in questions:
        parts.setdefault(q.part, []).append(q)

    return render(request, "listening_test.html", {
        "test": test,
        "form": form,
        "questions": questions,
        "parts": parts,
        "user_coins": request.user.profile.coins,
        "streak_days": request.user.profile.streak_days,
        "has_discount": request.user.profile.streak_days >= 5,
    })


# ======================== MILLIY SERTIFIKAT ========================

@login_required
def test_boshlash(request, fan):
    # FAN o'zgargan bo'lsa sessiyani tozalash
    session_fan = request.session.get('milliy_fan')
    if session_fan != fan:
        request.session.pop('milliy_start', None)
        request.session.pop('milliy_questions_ids', None)
        request.session['milliy_fan'] = fan

    saved_ids = request.session.get('milliy_questions_ids', [])

    if saved_ids:
        questions = list(Milliy_Sertifikat.objects.filter(id__in=saved_ids, fan=fan))
    else:
        all_questions = list(Milliy_Sertifikat.objects.filter(fan=fan))
        if not all_questions:
            messages.error(request, f"{fan} fani bo'yicha hozircha savollar mavjud emas!")
            return redirect("fan_tanlash")

        if len(all_questions) > 40:
            questions = random.sample(all_questions, 40)
        else:
            questions = all_questions

        request.session['milliy_start'] = time.time()
        request.session['milliy_questions_ids'] = [q.id for q in questions]

    if not questions:
        messages.error(request, f"{fan} fani bo'yicha savollar topilmadi!")
        return redirect("fan_tanlash")

    if request.method == "POST":
        total = 0
        for q in questions:
            user_javob = request.POST.get(f'q_{q.id}')
            if user_javob == q.togri_variant:
                total += 2

        minutes, seconds = get_time_spent(request, 'milliy_start')

        request.session.pop('milliy_start', None)
        request.session.pop('milliy_questions_ids', None)
        request.session.pop('milliy_fan', None)

        percentage = round((total / (len(questions) * 2)) * 100, 1) if questions else 0
        coins_returned = coins_back_if_perfect(request.user, percentage)

        UserTestResult.objects.create(
            user=request.user,
            test_name=f"{fan} Test (Milliy)",
            score=percentage
        )

        results = [{
            "savol": q.savol,
            "savol_rasm": q.savol_rasm.url if q.savol_rasm else None,
            "variant_a": q.variant_a,
            "variant_b": q.variant_b,
            "variant_c": q.variant_c,
            "variant_d": q.variant_d,
            "image_a": q.image_a.url if q.image_a else None,
            "image_b": q.image_b.url if q.image_b else None,
            "image_c": q.image_c.url if q.image_c else None,
            "image_d": q.image_d.url if q.image_d else None,
            "user_answer": request.POST.get(f'q_{q.id}'),
            "correct": q.togri_variant,
            "is_correct": request.POST.get(f'q_{q.id}') == q.togri_variant,
            "question_id": q.id,
            "category": "MILLIY",
            "fan": fan
        } for q in questions]

        return render(request, "result.html", {
            "results": results,
            "total": total,
            "correct_count": total // 2,
            "total_questions": len(questions),
            "minutes": minutes,
            "seconds": seconds,
            "percentage": percentage,
            "coins_returned": coins_returned,
            "fan_nomi": fan,
            "test_type": "Milliy Sertifikat"
        })

    random.shuffle(questions)

    return render(request, "test_milliy.html", {
        "questions": questions,
        "fan_nomi": fan,
        "total_questions": len(questions),
        "timer_seconds": 90 * 60
    })


# ======================== DTM ========================

@login_required
def dtm_select_view(request):
    request.session.pop('selected_subjects', None)
    request.session.pop('start_time', None)

    if request.method == "POST":
        birinchi_fan = request.POST.get('birinchi_fan')
        ikkinchi_fan = request.POST.get('ikkinchi_fan')

        if birinchi_fan and ikkinchi_fan and birinchi_fan != ikkinchi_fan:
            request.session['selected_subjects'] = [birinchi_fan, ikkinchi_fan]
            request.session['start_time'] = time.time()
            return redirect('dtm_test')

        return render(request, 'select_subjects.html', {
            "xato": "Fanlar bir xil bo'lishi mumkin emas!",
            "fan_choices": Milliy_Sertifikat.FAN_CHOICES
        })

    return render(request, 'select_subjects.html', {
        "fan_choices": Milliy_Sertifikat.FAN_CHOICES
    })


@login_required
def dtm_test_view(request):
    if 'selected_subjects' not in request.session:
        return redirect('dtm_select')

    tanlangan = request.session['selected_subjects']
    majburiy_fanlar = ['Ona Tili', 'Matematika', 'Tarix']

    all_questions = []
    for step, fan in enumerate(tanlangan, 1):
        qs = list(Milliy_Sertifikat.objects.filter(fan=fan))
        if len(qs) > 40:
            qs = random.sample(qs, 30)
        for q in qs:
            q.step = step
            q.fan_nomi = fan
            q.ball_per_q = 3.1 if step == 1 else 2.1
            q.model_name = 'milliy'
        all_questions.extend(qs)

    # Majburiy — DTM_Majburiy dan
    for step, fan in enumerate(majburiy_fanlar, 3):
        qs = list(DTM_Majburiy.objects.filter(fan=fan))
        if len(qs) > 10:
            qs = random.sample(qs, 30)
        for q in qs:
            q.step = step
            q.fan_nomi = fan
            q.ball_per_q = 1.1
            q.model_name = 'majburiy'
        all_questions.extend(qs)

    total_questions = len(all_questions)

    if request.method == "POST":
        total_score = 0
        for q in all_questions:
            user_javob = request.POST.get(f'q_{q.model_name}_{q.id}')
            if user_javob == q.togri_variant:
                total_score += q.ball_per_q

        start_time = request.session.get('start_time', time.time())
        spent_seconds = int(time.time() - start_time)

        max_ball = 0
        for step, _ in enumerate(tanlangan, 1):
            max_ball += 30 * (3.1 if step == 1 else 2.1)
        max_ball += 30 * 1.1 * len(majburiy_fanlar)

        percentage = round(total_score / max_ball * 100, 1) if max_ball else 0

        coins_returned = coins_back_if_perfect(request.user, percentage)
        UserTestResult.objects.create(user=request.user, test_name="DTM Test", score=percentage)

        results = [{
            "savol": q.savol,
            "savol_rasm": q.savol_rasm.url if q.savol_rasm else None,
            "variant_a": q.variant_a,
            "variant_b": q.variant_b,
            "variant_c": q.variant_c,
            "variant_d": q.variant_d,
            "image_a": q.image_a.url if q.image_a else None,
            "image_b": q.image_b.url if q.image_b else None,
            "image_c": q.image_c.url if q.image_c else None,
            "image_d": q.image_d.url if q.image_d else None,
            "user_answer": request.POST.get(f'q_{q.model_name}_{q.id}'),
            "correct": q.togri_variant,
            "is_correct": request.POST.get(f'q_{q.model_name}_{q.id}') == q.togri_variant,
            "fan": q.fan,
            "step": q.step,
            "ball": q.ball_per_q,
        } for q in all_questions]

        request.session.flush()

        return render(request, 'result.html', {
            "results": results,
            "total": round(total_score, 1),
            "total_questions": total_questions,
            "minutes": spent_seconds // 60,
            "seconds": spent_seconds % 60,
            "percentage": percentage,
            "coins_returned": coins_returned,
            "test_type": "DTM Test",
            "max_ball": round(max_ball, 1),
        })

    fanlar_data = []

    for step, fan in enumerate(tanlangan, 1):
        qs = [q for q in all_questions if q.fan_nomi == fan and q.model_name == 'milliy']
        fanlar_data.append({
            'fan': fan, 'step': step, 'questions': qs,
            'ball': 3.1 if step == 1 else 2.1,
            'turi': 'Ixtisoslik fani',
        })

    for step, fan in enumerate(majburiy_fanlar, 3):
        qs = [q for q in all_questions if q.fan_nomi == fan and q.model_name == 'majburiy']
        fanlar_data.append({
            'fan': fan, 'step': step, 'questions': qs,
            'ball': 1.1,
            'turi': 'Majburiy fan',
        })

    return render(request, 'test_process.html', {
        'fanlar_data': fanlar_data,
        'total_questions': total_questions,
    })
# ======================== SAT ========================

@login_required
def sat_test_view(request, test_id):
    test_obj = get_object_or_404(Sat, pk=test_id)
    questions = test_obj.questions.all()
    form = SATForm(request.POST or None, questions=questions)

    if request.method == "POST":
        allowed, status = check_test_access(request.user, test_obj, category="SAT")
        if not allowed:
            messages.error(request, "Sizda yetarli coin yo'q!")
            return redirect("buy_coins")

        if 'sat_start' not in request.session:
            request.session['sat_start'] = time.time()

        if form.is_valid():
            correct_count = sum(
                1 for q in questions
                if form.cleaned_data.get(f'q_{q.id}') == q.togri_variant
            )
            total = round(correct_count * 16.3, 1)
            minutes, seconds = get_time_spent(request, 'sat_start')
            request.session.pop('sat_start', None)
            q_count = questions.count()
            percentage = round(correct_count / q_count * 100, 1) if q_count else 0

            coins_returned = coins_back_if_perfect(request.user, percentage)
            sat_master_achieved = check_sat_master(request.user, percentage)

            UserTestResult.objects.create(
                user=request.user,
                test_name=f"SAT - {test_obj.title}",
                score=percentage
            )

            results = [{
                "savol": q.savol,
                "user_answer": form.cleaned_data.get(f'q_{q.id}'),
                "correct": q.togri_variant,
                "is_correct": form.cleaned_data.get(f'q_{q.id}') == q.togri_variant,
                "question_id": q.id,
                "category": "SAT"
            } for q in questions]

            return render(request, "result.html", {
                "results": results,
                "total": total,
                "correct_count": correct_count,
                "total_questions": q_count,
                "minutes": minutes,
                "seconds": seconds,
                "duration": test_obj.duration,
                "percentage": percentage,
                "coins_returned": coins_returned,
                "sat_master_achieved": sat_master_achieved,
                "consecutive_perfect": request.user.profile.consecutive_perfect,
                "test_type": f"SAT - {test_obj.title}"
            })

    return render(request, "sat_test.html", {
        "form": form,
        "questions": questions,
        "test": test_obj,
        "user_coins": request.user.profile.coins,
        "streak_days": request.user.profile.streak_days,
        "has_discount": request.user.profile.streak_days >= 5,
        "duration": test_obj.duration
    })


# ======================== BUY COINS ========================

@login_required
def buy_coins(request):
    if request.method == "POST":
        amount = int(request.POST.get('amount'))
        profile = request.user.profile
        profile.coins += amount
        profile.save()
        messages.success(request, f"Muvaffaqiyatli xarid! Hisobingizga {amount} coin qo'shildi.")
        return redirect('profile')
    return render(request, 'buy_coins.html')


# ======================== PROFIL VA STATISTIKA ========================

@login_required
def my_profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == "POST" and request.POST.get('action') == 'update_viloyat':
        profile.viloyat = request.POST.get('viloyat', '')
        profile.save()
        messages.success(request, "Viloyat muvaffaqiyatli saqlandi!")
        return redirect('profile')

    user_results = UserTestResult.objects.filter(user=user).order_by('-date_taken')
    total_tests_taken = user_results.count()

    show_analysis = total_tests_taken >= 15
    tests_until_analysis = max(0, 15 - total_tests_taken)

    average_score = 0
    best_score = 0
    recent_avg = 0
    trend = ""

    if total_tests_taken > 0:
        scores = [r.score for r in user_results]
        average_score = round(sum(scores) / total_tests_taken, 1)
        best_score = max(scores)

        if show_analysis:
            recent_scores = [r.score for r in user_results[:15]]
            recent_avg = round(sum(recent_scores) / len(recent_scores), 1)
            trend = "📈 Yaxshilanmoqda" if recent_avg >= average_score else "📉 Kamaymoqda"

    pending_requests = Friendship.objects.filter(to_user=user, accepted=False)

    return render(request, 'profile.html', {
        'user': user.get_full_name() or user.username,
        'profile': profile,
        'total_tests_taken': total_tests_taken,
        'average_score': average_score,
        'best_score': best_score,
        'user_results': user_results[:20],
        'show_analysis': show_analysis,
        'tests_until_analysis': tests_until_analysis,
        'recent_avg': recent_avg,
        'trend': trend,
        'streak_days': profile.streak_days,
        'has_discount': profile.streak_days >= 5,
        'badge': profile.badge,
        'consecutive_perfect': profile.consecutive_perfect,
        'viloyatlar': VILOYATLAR,
        'selected_viloyat': profile.viloyat,
        'pending_requests': pending_requests,
        'pending_count': pending_requests.count(),
    })


@login_required
def my_statistics(request):
    results = UserTestResult.objects.filter(user=request.user)
    tests_taken = results.count()
    average_score = results.aggregate(avg=Avg('score'))['avg'] or 0
    best_score = results.aggregate(max_score=Max('score'))['max_score'] or 0

    return render(request, 'my_statistics.html', {
        'tests_taken': tests_taken,
        'average_score': round(average_score),
        'best_score': round(best_score)
    })


# ======================== LEADERBOARD ========================

@login_required
def leaderboard(request):
    selected_viloyat = request.GET.get('viloyat', '')
    users = User.objects.select_related('profile').all()

    leaderboard_data = []
    for user in users:
        if not hasattr(user, 'profile'):
            continue
        if selected_viloyat and user.profile.viloyat != selected_viloyat:
            continue

        results = UserTestResult.objects.filter(user=user)
        if not results.exists():
            continue

        total_score = sum(r.score for r in results)
        tests_taken = results.count()
        avg_score = round(total_score / tests_taken, 1)
        best_score = results.aggregate(max_score=Max('score'))['max_score'] or 0
        leaderboard_points = int(total_score / 10)

        leaderboard_data.append({
            'username': user.username,
            'avg_score': avg_score,
            'best_score': best_score,
            'tests_taken': tests_taken,
            'leaderboard_points': leaderboard_points,
            'viloyat': user.profile.viloyat or '—',
            'badge': user.profile.badge,
            'streak_days': user.profile.streak_days,
        })

    leaderboard_data.sort(key=lambda x: x['leaderboard_points'], reverse=True)

    return render(request, 'leaderboard.html', {
        'leaderboard': leaderboard_data,
        'viloyatlar': VILOYATLAR,
        'selected_viloyat': selected_viloyat,
    })


# ======================== ANALYTICS ========================

@login_required
def student_analytics(request):
    user = request.user
    writing_subs = WritingSubmission.objects.filter(user=user).order_by('created_at')
    writing_avg = writing_subs.aggregate(Avg('band_score'))['band_score__avg'] or 0
    writing_max = writing_subs.aggregate(Max('band_score'))['band_score__max'] or 0
    results = UserTestResult.objects.filter(user=user).order_by('date_taken')

    def get_category_data(category_name):
        data = results.filter(test_name__icontains=category_name)
        return {
            'avg': round(data.aggregate(Avg('score'))['score__avg'] or 0, 1),
            'max': data.aggregate(Max('score'))['score__max'] or 0,
            'count': data.count(),
            'scores': list(data.values_list('score', flat=True)),
            'dates': [d.strftime('%d %b') for d in data.values_list('date_taken', flat=True)]
        }

    return render(request, 'analytics.html', {
        'writing': {
            'avg': round(writing_avg, 1),
            'max': writing_max,
            'count': writing_subs.count(),
            'scores': list(writing_subs.values_list('band_score', flat=True)),
            'dates': [d.strftime('%d %b') for d in writing_subs.values_list('created_at', flat=True)]
        },
        'reading': get_category_data('Reading'),
        'listening': get_category_data('Listening'),
        'sat': get_category_data('SAT'),
        'dtm': get_category_data('DTM'),
        'milliy': get_category_data('Milliy'),  # ← QO'SHILDI
        'recent_results': results.order_by('-date_taken')[:10]
    })


# ======================== WRITING ========================

@login_required
def writing_detail(request, pk):
    question = get_object_or_404(WritingQuestion, pk=pk)

    if request.method == 'POST':
        allowed, status = check_test_access(request.user, question, category="IELTS_WRITING")
        if not allowed:
            messages.error(request, "Sizda yetarli coin yo'q!")
            return redirect("buy_coins")

        form = WritingSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.question = question

            ai_result = check_ielts_writing(
                question.task_type,
                question.question_text,
                submission.answer
            )

            match = re.search(r'Overall Band:\s*([\d\.]+)', ai_result)
            if match:
                submission.band_score = float(match.group(1))

            submission.feedback = ai_result
            submission.save()
            return redirect('writing_result', submission.id)
    else:
        form = WritingSubmissionForm()

    return render(request, 'detail.html', {
        'question': question,
        'form': form,
        'status': 'ready'
    })


@login_required
def writing_result(request, pk):
    submission = get_object_or_404(WritingSubmission, pk=pk)
    return render(request, 'writing_result.html', {'submission': submission})


# ======================== DO'STLIK ========================

@login_required
def friend_profile(request, username):
    friend = get_object_or_404(User, username=username)

    if friend == request.user:
        return redirect('profile')

    is_friend = Friendship.objects.filter(
        Q(from_user=request.user, to_user=friend) |
        Q(from_user=friend, to_user=request.user),
        accepted=True
    ).exists()

    pending_sent = Friendship.objects.filter(
        from_user=request.user, to_user=friend, accepted=False
    ).exists()

    pending_received = Friendship.objects.filter(
        from_user=friend, to_user=request.user, accepted=False
    ).exists()

    friend_results = []
    friend_avg = 0
    friend_best = 0

    if is_friend:
        friend_results = UserTestResult.objects.filter(user=friend).order_by('-date_taken')[:10]
        agg = friend_results.aggregate(avg=Avg('score'), best=Max('score'))
        friend_avg = round(agg['avg'] or 0, 1)
        friend_best = agg['best'] or 0

    return render(request, 'friend_profile.html', {
        'friend': friend,
        'friend_profile': getattr(friend, 'profile', None),
        'is_friend': is_friend,
        'pending_sent': pending_sent,
        'pending_received': pending_received,
        'friend_results': friend_results,
        'friend_avg': friend_avg,
        'friend_best': friend_best,
    })


@login_required
def add_friend(request, username):
    to_user = get_object_or_404(User, username=username)
    if to_user != request.user:
        obj, created = Friendship.objects.get_or_create(
            from_user=request.user,
            to_user=to_user,
            defaults={'accepted': False}
        )
        if created:
            messages.success(request, f"Do'stlik so'rovi {username} ga yuborildi! 📨")
        else:
            messages.info(request, "So'rov allaqachon yuborilgan.")
    return redirect('friend_profile', username=username)


@login_required
def accept_friend(request, username):
    from_user = get_object_or_404(User, username=username)
    friendship = get_object_or_404(
        Friendship, from_user=from_user, to_user=request.user
    )
    friendship.accepted = True
    friendship.save()
    messages.success(request, f"{username} endi do'stingiz! 🎉")
    return redirect('friend_profile', username=username)


@login_required
def reject_friend(request, username):
    from_user = get_object_or_404(User, username=username)
    Friendship.objects.filter(
        from_user=from_user, to_user=request.user
    ).delete()
    messages.info(request, "So'rov rad etildi.")
    return redirect('my_friends')


@login_required
def my_friends(request):
    friends_qs = Friendship.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
        accepted=True
    ).select_related('from_user', 'to_user')

    friends_list = []
    for f in friends_qs:
        friend_user = f.to_user if f.from_user == request.user else f.from_user
        results = UserTestResult.objects.filter(user=friend_user)
        avg = round(results.aggregate(avg=Avg('score'))['avg'] or 0, 1)
        friends_list.append({
            'user': friend_user,
            'profile': getattr(friend_user, 'profile', None),
            'avg_score': avg,
            'tests_taken': results.count(),
        })

    pending_requests = Friendship.objects.filter(
        to_user=request.user, accepted=False
    ).select_related('from_user')

    return render(request, 'friends.html', {
        'friends_list': friends_list,
        'pending_requests': pending_requests,
    })


# ======================== MANAGE TESTS (ADMIN) ========================

def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin, login_url='login')
def manage_tests(request):
    if request.method == "POST":
        action = request.POST.get("action")

        # ── GURUH YARATISH ────────────────────────────────────────────────────
        if action == "create_group":
            g_type   = request.POST.get("group_category")
            title    = request.POST.get("group_title", "")
            is_paid  = request.POST.get("is_paid") == "on"
            price    = request.POST.get("price", 25)

            try:
                if g_type == "READING":
                    ReadingTest.objects.create(
                        # Part 1
                        passage_title   = request.POST.get("passage_title_1", ""),
                        passage_text    = request.POST.get("passage_text_1", ""),
                        # Part 2
                        passage_title_2 = request.POST.get("passage_title_2", ""),
                        passage_text_2  = request.POST.get("passage_text_2", ""),
                        # Part 3
                        passage_title_3 = request.POST.get("passage_title_3", ""),
                        passage_text_3  = request.POST.get("passage_text_3", ""),
                        category = 'READING',
                        is_paid  = is_paid,
                        price    = price,
                    )
                elif g_type == "LISTENING":
                    ListeningTest.objects.create(
                        title    = title,
                        category = 'LISTENING',
                        is_paid  = is_paid,
                        price    = price,
                    )
                elif g_type == "SAT":
                    Sat.objects.create(
                        title    = title,
                        category = 'SAT',
                        is_paid  = is_paid,
                        price    = price,
                    )
                messages.success(request, "✅ Guruh muvaffaqiyatli yaratildi!")
            except Exception as e:
                messages.error(request, f"Xatolik: {e}")

        # ── SAVOL QO'SHISH ────────────────────────────────────────────────────
        elif action == "add_question":
            cat        = request.POST.get("category")
            group_id   = request.POST.get("test_group")
            savol_matni = request.POST.get("savol")

            try:
                if cat == "IELTS_READING":
                    IELTS_Reading.objects.create(
                        test_group_id  = group_id,
                        savol          = savol_matni,
                        question_type  = request.POST.get("question_type", "ABCD"),
                        part           = request.POST.get("part", 1),
                        variant_a      = request.POST.get("variant_a", ""),
                        variant_b      = request.POST.get("variant_b", ""),
                        variant_c      = request.POST.get("variant_c", ""),
                        variant_d      = request.POST.get("variant_d", ""),
                        togri_variant  = request.POST.get("togri_variant", ""),
                        question_image = request.FILES.get("question_image"),
                        image_a        = request.FILES.get("image_a"),
                        image_b        = request.FILES.get("image_b"),
                        image_c        = request.FILES.get("image_c"),
                        image_d        = request.FILES.get("image_d"),
                    )
                elif cat == "IELTS_LISTENING":
                    IELTSListeningQuestion.objects.create(
                        test_group_id = group_id,
                        savol         = savol_matni,
                        question_type = request.POST.get("question_type", "ABCD"),
                        variant_a     = request.POST.get("variant_a", ""),
                        variant_b     = request.POST.get("variant_b", ""),
                        variant_c     = request.POST.get("variant_c", ""),
                        variant_d     = request.POST.get("variant_d", ""),
                        togri_variant = request.POST.get("togri_variant", ""),
                        audio         = request.FILES.get("audio"),
                        map_image     = request.FILES.get("map_image"),
                        part          = request.POST.get("part", 1),
                    )
                elif cat == "SAT":
                    SATQuestion.objects.create(
                        test_group_id  = group_id,
                        savol          = savol_matni,
                        variant_a      = request.POST.get("variant_a", ""),
                        variant_b      = request.POST.get("variant_b", ""),
                        variant_c      = request.POST.get("variant_c", ""),
                        variant_d      = request.POST.get("variant_d", ""),
                        togri_variant  = request.POST.get("togri_variant", ""),
                        question_image = request.FILES.get("question_image"),
                        image_a        = request.FILES.get("image_a"),
                        image_b        = request.FILES.get("image_b"),
                        image_c        = request.FILES.get("image_c"),
                        image_d        = request.FILES.get("image_d"),
                    )
                elif cat == "MILL_NATIONAL":
                    Milliy_Sertifikat.objects.create(
                        fan           = request.POST.get("fan"),
                        savol         = savol_matni,
                        variant_a     = request.POST.get("variant_a", ""),
                        variant_b     = request.POST.get("variant_b", ""),
                        variant_c     = request.POST.get("variant_c", ""),
                        variant_d     = request.POST.get("variant_d", ""),
                        togri_variant = request.POST.get("togri_variant", ""),
                        savol_rasm    = request.FILES.get("savol_rasm"),
                        image_a       = request.FILES.get("image_a"),
                        image_b       = request.FILES.get("image_b"),
                        image_c       = request.FILES.get("image_c"),
                        image_d       = request.FILES.get("image_d"),
                    )
                messages.success(request, "✅ Savol muvaffaqiyatli saqlandi!")
            except Exception as e:
                messages.error(request, f"Xatolik: {e}")

        return redirect("manage_tests")

    # ── GET ───────────────────────────────────────────────────────────────────
    return render(request, "manage_tests.html", {
        "reading_tests":      ReadingTest.objects.all().order_by('-id'),
        "listening_tests":    ListeningTest.objects.all().order_by('-id'),
        "sat_tests":          Sat.objects.all().order_by('-id'),
        "milliy_fan_choices": Milliy_Sertifikat.FAN_CHOICES,
    })




# ======================== AI EXPLANATION ========================

@csrf_exempt
def explain_error_view(request, submission_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            data = request.POST
    else:
        data = request.GET

    category = data.get('category', 'IELTS')
    user_answer = data.get('user_answer', '')

    try:
        if category == 'SAT':
            q_obj = SATQuestion.objects.get(id=submission_id)
            passage = q_obj.test_group.description
            question_text = q_obj.savol
            correct_answer = q_obj.togri_variant
            test_type = "SAT"
        elif category in ('IELTS_LISTENING', 'IELTS'):
            q_obj = IELTSListeningQuestion.objects.get(id=submission_id)
            passage = f"Part {q_obj.part} listening question."
            question_text = q_obj.savol
            correct_answer = q_obj.togri_variant
            test_type = "IELTS Listening"
        elif category == 'MILLIY':
            q_obj = Milliy_Sertifikat.objects.get(id=submission_id)
            passage = f"Fan: {q_obj.fan}"
            question_text = q_obj.savol
            correct_answer = q_obj.togri_variant
            test_type = "Milliy Sertifikat"
        else:
            q_obj = IELTS_Reading.objects.get(id=submission_id)
            passage = q_obj.test_group.passage_text
            question_text = q_obj.savol
            correct_answer = q_obj.togri_variant
            test_type = "IELTS Reading"

        explanation = get_ai_explanation(
            test_type=test_type,
            passage=passage,
            question=question_text,
            correct_answer=correct_answer,
            user_answer=user_answer
        )
        return JsonResponse({'explanation': explanation})

    except Exception as e:
        return JsonResponse({'explanation': f"Savol topilmadi: {str(e)}"}, status=200)