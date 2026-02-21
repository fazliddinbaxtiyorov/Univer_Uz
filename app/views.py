from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import (
    FanlarForm, IELTSReadingForm, TestForm, FanTanlashForm,
    IELTSListeningForm, SATForm, Writing, TestFanForm, ContactForm
)
from .models import (
    IELTS_Reading, Milliy_Sertifikat, IELTSListeningQuestion,
    SATQuestion, Davlat_Univer, Xususiy_Univer, Xorijiy_Univer,
    ContactMessage, UserTestResult, ReadingTest, ListeningTest, Sat, TestAccess
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random, time
from .models import ReadingTest, IELTS_Reading, UserTestResult
from .forms import IELTSReadingForm

import random
import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

def check_test_access(user, test, category):
    profile = user.profile

    with transaction.atomic():
        access, created = TestAccess.objects.get_or_create(
            user=user,
            category=category,
            test_id=test.id
        )


        if profile.coins < test.price:
            return False, "not_enough_coins"
        profile.coins -= test.price
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

def support(request):
    return render(request, 'support.html')

def ielts(request):
    return render(request, 'ielts.html')

def fanlar_view(request):
    form = FanlarForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, "home.html", {"form": form})

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
    duration = 60
    return render(request, "ielts.html", {
        "tests": all_passages,
        "total_questions": total_questions,
        "duration": duration,
    })





@login_required
def ielts_reading_view(request, test_id=None):
    if test_id:
        reading_test = get_object_or_404(ReadingTest, pk=test_id)
    else:
        reading_test = ReadingTest.objects.first()

    if not reading_test:
        messages.error(request, "Reading testi mavjud emas!")
        return redirect("ielts_list")

    if request.method == "POST":
        allowed, status = check_test_access(
            request.user,
            reading_test,
            category="IELTS_READING"
        )
        if not allowed:
            messages.error(request, "Sizda yetarli coin yo‘q!")
            return redirect("buy_coins")

    all_passages = list(ReadingTest.objects.filter(category='READING'))
    if len(all_passages) > 10:
        all_passages = random.sample(all_passages, 10)

    all_questions = []
    passage_question_map = {}
    for p in all_passages:
        qs = list(p.questions.all())
        if len(qs) > 4:
            qs = random.sample(qs, 4)
        all_questions.extend(qs)
        passage_question_map[p.id] = qs

    if 'reading_start' not in request.session:
        request.session['reading_start'] = time.time()

    form = IELTSReadingForm(request.POST or None, questions=all_questions)

    if request.method == "POST" and form.is_valid():
        total = sum(
            2 for q in all_questions
            if form.cleaned_data.get(f'q_{q.id}') == q.togri_variant
        )

        start = request.session.pop('reading_start', time.time())
        spent = int(time.time() - start)
        minutes = spent // 60
        seconds = spent % 60

        percentage = round(total / (len(all_questions) * 2) * 100, 1)

        UserTestResult.objects.create(
            user=request.user,
            test_name=f"IELTS Reading - {reading_test.id}",
            score=percentage
        )

        results = [{
            "savol": q.savol,
            "user_answer": form.cleaned_data.get(f'q_{q.id}'),
            "correct": q.togri_variant,
            "question_id": q.id,  # ← qo'shildi
            "category": "IELTS"  # ← qo'shildi
        } for q in all_questions]

        return render(request, "result.html", {
            "results": results,
            "total": total,
            "percentage": percentage,
            "minutes": minutes,
            "seconds": seconds
        })

    # 10️⃣ Template uchun data
    test_data = []
    for p in all_passages:
        test_data.append({
            "passage_text": p.passage_text,
            "questions": [
                {"model": q, "field": form[f"q_{q.id}"]}
                for q in passage_question_map[p.id]
            ]
        })

    return render(request, "reading_test.html", {
        "test_data": test_data,
        "duration": 60,
        "user_coins": request.user.profile.coins,
        "status": "ready",
        "test_id": reading_test.id
    })


@login_required
def ielts_listening_view(request, test_id):
    test = get_object_or_404(ListeningTest, pk=test_id)

    questions = test.questions.all().order_by('part', 'id')

    form = IELTSListeningForm(request.POST or None, questions=questions)

    if request.method == "POST":
        allowed, status = check_test_access(
            request.user,
            test,
            category="IELTS_LISTENING"
        )

        if not allowed:
            if status == "not_enough_coins":
                messages.error(request, "Sizda yetarli coin yo‘q!")
            return redirect("buy_coins")

        if form.is_valid():
            total = sum(
                1 for q in questions
                if form.cleaned_data.get(f'q_{q.id}') == q.togri_variant
            )

            # Taymer mantiqi (Frontenddan kelgan vaqtni ishlatish ham mumkin)
            start_time = request.session.pop('listening_start', time.time())
            spent = int(time.time() - start_time)

            percentage = round((total / questions.count()) * 100, 1) if questions.count() > 0 else 0

            UserTestResult.objects.create(
                user=request.user,
                test_name=f"Listening - {test.title}",
                score=percentage
            )
            results = [{
                "savol": q.savol,
                "user_answer": form.cleaned_data.get(f'q_{q.id}'),
                "correct": q.togri_variant,
                "question_id": q.id,  # ← qo'shildi
                "category": "IELTS"  # ← qo'shildi
            } for q in questions]

            return render(request, "result.html", {
                "results": results,
                "total": total,
                "percentage": percentage,
                "minutes": spent // 60,
                "seconds": spent % 60
            })

    if 'listening_start' not in request.session:
        request.session['listening_start'] = time.time()

    return render(request, "listening_test.html", {
        "test": test,
        "form": form,
        "questions": questions,
    })


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

@login_required
def test_boshlash(request, fan):
    questions = Milliy_Sertifikat.objects.filter(fan=fan)[:50]
    if 'milliy_start' not in request.session:
        request.session['milliy_start'] = time.time()

    form = TestForm(request.POST or None, questions=questions)

    if request.method == "POST" and form.is_valid():
        total = sum(2 for q in questions if form.cleaned_data.get(f'q_{q.id}') == q.togri_variant)
        minutes, seconds = get_time_spent(request, 'milliy_start')
        del request.session['milliy_start']

        # Save result
        UserTestResult.objects.create(
            user=request.user,
            test_name=f"{fan} Test",
            score=round(total / (len(questions)*2) * 100, 1)
        )

        results = [{
            "savol": q.savol,
            "user_answer": form.cleaned_data.get(f'q_{q.id}'),
            "correct": q.togri_variant,
            "question_id": q.id,
            "category": "MILLIY"
        } for q in questions]

        return render(request, "result.html", {
            "results": results,
            "total": total,
            "minutes": minutes,
            "seconds": seconds,
            "percentage": round(total / (len(questions)*2) * 100, 1)
        })

    return render(request, "test_milliy.html", {"form": form})

def test_list_sat(request):
    tests = Sat.objects.all()
    return render(request, "sat.html", {"tests": tests})



@login_required
def sat_test_view(request, test_id):
    test_obj = get_object_or_404(Sat, pk=test_id)
    questions = test_obj.questions.all()

    form = SATForm(request.POST or None, questions=questions)

    if request.method == "POST":

        # 💰 Faqat POST da tekshiramiz
        allowed, status = check_test_access(
            request.user,
            test_obj,
            category="SAT"
        )

        if not allowed:
            if status == "not_enough_coins":
                messages.error(request, "Sizda yetarli coin yo‘q!")
                return redirect("buy_coins")
            else:
                messages.error(request, "Kirish huquqi yo‘q.")
                return redirect("sat_list")

        if 'sat_start' not in request.session:
            request.session['sat_start'] = time.time()

        if form.is_valid():
            total = sum(
                16.3 for q in questions
                if form.cleaned_data.get(f'q_{q.id}') == q.togri_variant
            )

            minutes, seconds = get_time_spent(request, 'sat_start')
            request.session.pop('sat_start', None)

            percentage = round(total / (len(questions) * 16.3) * 100, 1)

            UserTestResult.objects.create(
                user=request.user,
                test_name=f"SAT - {test_obj.title}",
                score=percentage
            )

        results = [{
            "savol": q.savol,
            "user_answer": form.cleaned_data.get(f'q_{q.id}'),
            "correct": q.togri_variant,
            "question_id": q.id,  # ← qo'shildi
            "category": "SAT"  # ← qo'shildi
        } for q in questions]

        return render(request, "result.html", {
            "results": results,  # shunaqa bo‘lishi kerak
            "total": total,
            "minutes": minutes,
            "seconds": seconds,
            "percentage": percentage
        })

    return render(request, "sat_test.html", {
        "form": form,
        "questions": questions,
        "test": test_obj,
        "user_coins": request.user.profile.coins
    })


def fan_tanlash(request):
    if request.method == "POST":
        form = FanTanlashForm(request.POST)
        if form.is_valid():
            fan = form.cleaned_data["fan"]
            return redirect("milliy", fan=fan)
    else:
        form = FanTanlashForm()
    return render(request, "fan_tanlash.html", {"form": form})


def univerlar(request):
    davlat = Davlat_Univer.objects.all()
    xususiy = Xususiy_Univer.objects.all()
    xorijiy = Xorijiy_Univer.objects.all()
    return render(request, 'univerlar.html', {'davlat': davlat, 'xususiy': xususiy, 'xorijiy': xorijiy})

@login_required
def dtm_select_view(request):

    # Eski test sessionlarini tozalash
    request.session.pop('selected_subjects', None)
    request.session.pop('start_time', None)

    if request.method == "POST":
        birinchi_fan = request.POST.get('birinchi_fan')
        ikkinchi_fan = request.POST.get('ikkinchi_fan')

        if birinchi_fan and ikkinchi_fan and birinchi_fan != ikkinchi_fan:

            tanlangan = [birinchi_fan, ikkinchi_fan]
            fanlar = [
                birinchi_fan,
                ikkinchi_fan,
                'Ona Tili' if 'Ona Tili' not in tanlangan else 'Ingliz Tili',
                'Matematika' if 'Matematika' not in tanlangan else 'Fizika',
                'Tarix'
            ]

            request.session['selected_subjects'] = fanlar
            request.session['start_time'] = time.time()

            return redirect('dtm_test')

        return render(request, 'select_subjects.html', {
            "xato": "Fanlar bir xil bo‘lishi mumkin emas!"
        })

    return render(request, 'select_subjects.html')

@login_required
def dtm_test_view(request):

    if 'selected_subjects' not in request.session:
        return redirect('selected_subjects')

    fanlar = request.session['selected_subjects']

    all_questions = []
    for step, fan in enumerate(fanlar, 1):
        questions = Milliy_Sertifikat.objects.filter(fan=fan)
        for q in questions:
            q.step = step
        all_questions.extend(questions)

    total_questions = len(all_questions)

    if request.method == "POST":
        form = TestFanForm(request.POST, questions=all_questions)

        if form.is_valid():
            total_score = 0

            for q in all_questions:
                user_javob = form.cleaned_data.get(f'q_{q.id}')

                if user_javob == q.togri_variant:
                    if q.step == 1:
                        total_score += 3.1
                    elif q.step == 2:
                        total_score += 2.1
                    else:
                        total_score += 1.1

            start_time = request.session.get('start_time', time.time())
            spent_seconds = int(time.time() - start_time)
            minutes = spent_seconds // 60
            seconds = spent_seconds % 60
            percentage = round(total_score / (total_questions * 3.1) * 100, 1)

            UserTestResult.objects.create(
                user=request.user,
                test_name="DTM Test",
                score=percentage
            )

            results = [{
                "savol": q.savol,
                "user_answer": form.cleaned_data.get(f'q_{q.id}'),
                "correct": q.togri_variant,
                "question_id": q.id,
                "category": "MILLIY"  # ← DTM ham Milliy_Sertifikat modelidan
            } for q in all_questions]

            request.session.flush()

            return render(request, 'result.html', {
                "results": results,
                "total": round(total_score, 1),
                "minutes": minutes,
                "seconds": seconds,
                "percentage": percentage
            })
    else:
        form = TestFanForm(questions=all_questions)

    return render(request, 'test_process.html', {
        'form': form,
        'all_questions': all_questions,
        'timer_seconds': 3600
    })



@login_required
def my_statistics(request):
    results = UserTestResult.objects.filter(user=request.user)
    tests_taken = results.count()
    average_score = results.aggregate(avg=Avg('score'))['avg'] or 0
    best_score = results.aggregate(max_score=Max('score'))['max_score'] or 0

    context = {
        'tests_taken': tests_taken,
        'average_score': round(average_score),
        'best_score': round(best_score)
    }

    return render(request, 'my_statistics.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import (
    IELTS_Reading, ReadingTest,
    IELTSListeningQuestion, ListeningTest,
    SATQuestion, Sat,
    Milliy_Sertifikat
)


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin, login_url='login')
def manage_tests(request):
    if request.method == "POST":
        action = request.POST.get("action")

        # --- 1. GURUH YARATISH (Narx va Is_Paid bilan) ---
        if action == "create_group":
            g_type = request.POST.get("group_category")
            title = request.POST.get("group_title")
            content = request.POST.get("passage_content", "")
            is_paid = request.POST.get("is_paid") == "on"
            price = request.POST.get("price", 25)

            try:
                if g_type == "READING":
                    ReadingTest.objects.create(passage_text=content, category='READING', is_paid=is_paid, price=price)
                elif g_type == "LISTENING":
                    ListeningTest.objects.create(title=title, category='LISTENING', is_paid=is_paid, price=price)
                elif g_type == "SAT":
                    Sat.objects.create(title=title, category='SAT', is_paid=is_paid, price=price)
                messages.success(request, f"Guruh yaratildi! (Pullik: {is_paid}, Narxi: {price})")
            except Exception as e:
                messages.error(request, f"Xatolik: {e}")

        # --- 2. SAVOL QO'SHISH ---
        elif action == "add_question":
            cat = request.POST.get("category")
            group_id = request.POST.get("test_group")
            savol_matni = request.POST.get("savol")

            try:
                data = {
                    "savol": savol_matni,
                    "variant_a": request.POST.get("variant_a"),
                    "variant_b": request.POST.get("variant_b"),
                    "variant_c": request.POST.get("variant_c"),
                    "variant_d": request.POST.get("variant_d"),
                    "togri_variant": request.POST.get("togri_variant"),
                    "question_image": request.FILES.get("question_image"),
                }

                if cat == "IELTS_READING":
                    IELTS_Reading.objects.create(test_group_id=group_id, **data,
                                                 image_a=request.FILES.get("image_a"),
                                                 image_b=request.FILES.get("image_b"),
                                                 image_c=request.FILES.get("image_c"),
                                                 image_d=request.FILES.get("image_d"))
                elif cat == "IELTS_LISTENING":
                    IELTSListeningQuestion.objects.create(test_group_id=group_id, **data,
                                                          audio=request.FILES.get("audio"),
                                                          part=request.POST.get("part", 1))
                elif cat == "SAT":
                    SATQuestion.objects.create(test_group_id=group_id, **data,
                                               image_a=request.FILES.get("image_a"),
                                               image_b=request.FILES.get("image_b"),
                                               image_c=request.FILES.get("image_c"),
                                               image_d=request.FILES.get("image_d"))
                elif cat == "MILL_NATIONAL":
                    Milliy_Sertifikat.objects.create(fan=request.POST.get("fan"), **data)

                messages.success(request, "Savol muvaffaqiyatli saqlandi!")
            except Exception as e:
                messages.error(request, f"Xatolik: {e}")

        return redirect("manage_tests")

    context = {
        "reading_tests": ReadingTest.objects.all().order_by('-id'),
        "listening_tests": ListeningTest.objects.all().order_by('-id'),
        "sat_tests": Sat.objects.all().order_by('-id'),
        "milliy_fan_choices": Milliy_Sertifikat.FAN_CHOICES,
    }
    return render(request, "manage_tests.html", context)
# ======================== Contact Form ========================
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

@login_required
def my_profile_view(request):
    user = request.user

    user_results = UserTestResult.objects.filter(user=user)

    total_tests_taken = user_results.count()

    if total_tests_taken > 0:
        average_score = round(sum(result.score for result in user_results) / total_tests_taken, 1)
        best_score = max(result.score for result in user_results)
    else:
        average_score = 0
        best_score = 0

    context = {
        'user': user.get_full_name() or user.username,
        'total_tests_taken': total_tests_taken,
        'average_score': average_score,
        'best_score': best_score,
        'user_results': user_results,
    }

    return render(request, 'profile.html', context)



def ielts_main_dashboard(request):
    category = request.GET.get('category', 'ALL').upper()
    if category == 'READING':
        tests = ReadingTest.objects.filter(category='READING')
    elif category == 'LISTENING':
        tests = ListeningTest.objects.filter(category='LISTENING')
    else:
        tests = ReadingTest.objects.all()

    return render(request, 'ielts.html', {
        'tests': tests,
        'current_category': category
    })


import re

from .models import WritingQuestion, WritingSubmission
from .forms import WritingSubmissionForm
from .utils import check_ielts_writing


def writing_tests(request):
    testlar = WritingQuestion.objects.all()
    print(f"BAZADA {testlar.count()} TA TEST BOR")

    return render(request, 'ielts.html', {
        'tests_writing': testlar,
        'current_category': 'WRITING'
    })


@login_required
def writing_detail(request, pk):
    question = get_object_or_404(WritingQuestion, pk=pk)

    if request.method == "POST":

        allowed, status = check_test_access(
            request.user,
            question,
            category="IELTS_LISTENING"
        )
    if request.method == 'POST':
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


@login_required
def student_analytics(request):
    user = request.user

    # Writing ma'lumotlari
    writing_subs = WritingSubmission.objects.filter(user=user).order_by('created_at')
    writing_avg = writing_subs.aggregate(Avg('band_score'))['band_score__avg'] or 0
    writing_max = writing_subs.aggregate(Max('band_score'))['band_score__max'] or 0

    # Umumiy test natijalari (Reading, Listening, SAT, DTM, Milliy)
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

    context = {
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
        'recent_results': results.order_by('-date_taken')[:10]
    }

    return render(request, 'analytics.html', context)


from django.shortcuts import render
from django.db.models import Avg, Max
from .models import UserTestResult
from django.contrib.auth.models import User

@login_required
def leaderboard(request):
    users = User.objects.all()

    leaderboard_data = []

    for user in users:
        results = UserTestResult.objects.filter(user=user)
        if results.exists():
            total_score = sum(r.score for r in results)
            tests_taken = results.count()
            avg_score = round(total_score / tests_taken, 1)
            best_score = results.aggregate(max_score=Max('score'))['max_score'] or 0
            leaderboard_data.append({
                'username': user.username,
                'avg_score': avg_score,
                'best_score': best_score,
                'tests_taken': tests_taken
            })
    leaderboard_data.sort(key=lambda x: x['avg_score'], reverse=True)

    return render(request, 'leaderboard.html', {
        'leaderboard': leaderboard_data
    })

from .hi import get_ai_explanation
from django.views.decorators.csrf import csrf_exempt
import json


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SATQuestion, IELTS_Reading, IELTSListeningQuestion, Milliy_Sertifikat
from .hi import get_ai_explanation
import json

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

        elif category == 'IELTS_LISTENING':
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
            # Default: IELTS Reading
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