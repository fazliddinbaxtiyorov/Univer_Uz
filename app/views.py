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



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import random, time
from .models import ReadingTest, IELTS_Reading, UserTestResult
from .forms import IELTSReadingForm

import random
import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import random
import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def ielts_reading_view(request, test_id=None):
    """
    IELTS Reading test view
    - test_id berilsa o'sha test ishlatiladi
    - yo'q bo'lsa, birinchi test ishlatiladi
    """
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
            "correct": q.togri_variant
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
    questions = test.questions.all()
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

        if 'listening_start' not in request.session:
            request.session['listening_start'] = time.time()

        if form.is_valid():
            total = sum(
                1 for q in questions
                if form.cleaned_data.get(f'q_{q.id}') == q.togri_variant
            )

            start_time = request.session.pop('listening_start', time.time())
            spent = int(time.time() - start_time)

            percentage = round((total / questions.count()) * 100, 1)
            UserTestResult.objects.create(
                user=request.user,
                test_name=test.title,
                score=percentage
            )

            results = [{
                "savol": q.savol,
                "user_answer": form.cleaned_data.get(f'q_{q.id}'),
                "correct": q.togri_variant
            } for q in questions]
            return render(request, "result.html", {
                "results": results,
                "total": total,
                "percentage": percentage,
                "minutes": spent // 60,
                "seconds": spent % 60
            })

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
            "correct": q.togri_variant
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
                test_name=test_obj.title,
                score=percentage
            )

        results = [{
            "savol": q.savol,
            "user_answer": form.cleaned_data.get(f'q_{q.id}'),
            "correct": q.togri_variant
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


def davlat_univer(request):
    davlat = Davlat_Univer.objects.all()
    return render(request, 'davlat_univer.html', {'davlat': davlat})


def xususiy_univer(request):
    xususiy = Xususiy_Univer.objects.all()
    return render(request, 'xususiy.html', {'xususiy': xususiy})


def xorijiy_univer(request):
    xorijiy = Xorijiy_Univer.objects.all()
    return render(request, 'leaderboard.html', {'xorijiy': xorijiy})


@login_required
def dtm_test_view(request):
    if 'start_time' not in request.session:
        request.session['start_time'] = time.time()

    if 'selected_subjects' not in request.session:
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
                return redirect('dtm_test')
            else:
                return render(request, 'select_subjects.html', {
                    'xato': 'Ikkala fan ham tanlanishi va bir xil bo\'lmasligi kerak!'
                })
        return render(request, 'select_subjects.html')

    fanlar = request.session['selected_subjects']

    all_questions = []
    for step, fan in enumerate(fanlar, 1):
        questions = Milliy_Sertifikat.objects.filter(fan=fan)
        for q in questions:
            q.step = step
        all_questions.extend(questions)

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
            end_time = time.time()
            spent_seconds = int(end_time - start_time)
            minutes = spent_seconds // 60
            seconds = spent_seconds % 60

            # Save DTM result
            UserTestResult.objects.create(
                user=request.user,
                test_name="DTM Test",
                score=round(total_score / (len(all_questions)*3.1) * 100, 1)
            )

            results = [{
                "savol": q.savol,
                "user_answer": form.cleaned_data.get(f'q_{q.id}'),
                "correct": q.togri_variant
            } for q in all_questions]

            request.session.flush()
            return render(request, 'result.html', {
                "results": results,
                'total': round(total_score, 1),
                'minutes': minutes,
                'seconds': seconds,
                "percentage": round(total_score / (len(all_questions) * 3.1) * 100, 1)
            })
    else:
        form = TestFanForm(questions=all_questions)

    return render(request, 'test_process.html', {
        'form': form,
        'all_questions': all_questions,
        'timer_seconds': 3600
    })


# ======================== User Statistics ========================
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


# ======================== Manage Tests (Admin) ========================
def manage_tests(request):
    milliy_fan_choices = Milliy_Sertifikat.FAN_CHOICES

    if request.method == "POST":
        category = request.POST.get("category")
        savol = request.POST.get("savol")
        variant_a = request.POST.get("variant_a")
        variant_b = request.POST.get("variant_b")
        variant_c = request.POST.get("variant_c")
        variant_d = request.POST.get("variant_d")
        togri_variant = request.POST.get("togri_variant")
        audio_file = request.FILES.get("audio")
        fan = request.POST.get("fan")  # Milliy Sertifikat uchun

        if category == "IELTS_READING":
            IELTS_Reading.objects.create(
                savol=savol,
                variant_a=variant_a,
                variant_b=variant_b,
                variant_c=variant_c,
                variant_d=variant_d,
                togri_variant=togri_variant
            )
            messages.success(request, "IELTS Reading question added successfully.")

        elif category == "IELTS_LISTENING":
            IELTSListeningQuestion.objects.create(
                savol=savol,
                variant_a=variant_a,
                variant_b=variant_b,
                variant_c=variant_c,
                variant_d=variant_d,
                togri_variant=togri_variant,
                audio=audio_file
            )
            messages.success(request, "IELTS Listening question added successfully.")

        elif category == "SAT":
            SATQuestion.objects.create(
                savol=savol,
                variant_a=variant_a,
                variant_b=variant_b,
                variant_c=variant_c,
                variant_d=variant_d,
                togri_variant=togri_variant
            )
            messages.success(request, "SAT question added successfully.")

        elif category == "MILL_NATIONAL":
            if not fan:
                messages.error(request, "Please select a fan for Milliy Sertifikat!")
                return redirect("manage_tests")
            Milliy_Sertifikat.objects.create(
                fan=fan,
                savol=savol,
                variant_a=variant_a,
                variant_b=variant_b,
                variant_c=variant_c,
                variant_d=variant_d,
                togri_variant=togri_variant
            )
            messages.success(request, f"{fan} faniga Milliy Sertifikat savol qo‘shildi!")

        return redirect("manage_tests")

    all_tests = list(IELTS_Reading.objects.all()) + \
                list(IELTSListeningQuestion.objects.all()) + \
                list(SATQuestion.objects.all()) + \
                list(Milliy_Sertifikat.objects.all())

    context = {
        "all_tests": all_tests,
        "milliy_fan_choices": milliy_fan_choices
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


def student_analytics(request):
    submissions = WritingSubmission.objects.filter(user=request.user).order_by('-created_at')

    avg_score = submissions.aggregate(Avg('band_score'))['band_score__avg']
    max_score = submissions.aggregate(Max('band_score'))['band_score__max']

    context = {
        'submissions': submissions,
        'avg_score': round(avg_score, 1) if avg_score else 0,
        'max_score': max_score
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
