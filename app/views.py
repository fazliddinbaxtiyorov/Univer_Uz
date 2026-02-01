from django.shortcuts import render, get_object_or_404, redirect
from .forms import (
    FanlarForm, IELTSReadingForm, TestForm, FanTanlashForm,
    IELTSListeningForm, SATForm, Writing, TestFanForm, ContactForm
)
from .models import (
    IELTS_Reading, Milliy_Sertifikat, IELTSListeningQuestion,
    SATQuestion, Davlat_Univer, Xususiy_Univer, Xorijiy_Univer,
    ContactMessage, UserTestResult
)
from django.db.models import Q, Avg, Max
from django.contrib import messages
import time
from django.contrib.auth.decorators import login_required


# ======================== Helper ========================
def get_time_spent(request, session_key):
    start_time = request.session.get(session_key)
    end_time = time.time()
    spent_seconds = int(end_time - start_time)
    minutes = spent_seconds // 60
    seconds = spent_seconds % 60
    return minutes, seconds


# ======================== Static Pages ========================
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


# ======================== IELTS ========================
@login_required
def ielts_reading_view(request):
    questions = IELTS_Reading.objects.all()[:10]
    if 'ielts_reading_start' not in request.session:
        request.session['ielts_reading_start'] = time.time()

    form = IELTSReadingForm(request.POST or None, questions=questions)

    if request.method == "POST" and form.is_valid():
        total = sum(2 for q in questions if form.cleaned_data.get(f'q_{q.id}') == q.togri_variant)
        minutes, seconds = get_time_spent(request, 'ielts_reading_start')
        del request.session['ielts_reading_start']

        # Save result
        UserTestResult.objects.create(
            user=request.user,
            test_name="IELTS Reading",
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

    return render(request, "reading_test.html", {"form": form, "questions": questions})


@login_required
def ielts_listening_view(request):
    questions = IELTSListeningQuestion.objects.all()[:20]
    if 'listening_start' not in request.session:
        request.session['listening_start'] = time.time()

    form = IELTSListeningForm(request.POST or None, questions=questions)

    if request.method == "POST" and form.is_valid():
        total = sum(2 for q in questions if form.cleaned_data.get(f'q_{q.id}') == q.togri_variant)
        minutes, seconds = get_time_spent(request, 'listening_start')
        del request.session['listening_start']

        # Save result
        UserTestResult.objects.create(
            user=request.user,
            test_name="IELTS Listening",
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

    return render(request, "listening_test.html", {"form": form, "questions": questions})


# ======================== Milliy Sertifikat / DTM ========================
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


# ======================== SAT ========================
@login_required
def sat_test_view(request):
    questions = SATQuestion.objects.all()[:20]
    if 'sat_start' not in request.session:
        request.session['sat_start'] = time.time()

    form = SATForm(request.POST or None, questions=questions)

    if request.method == "POST" and form.is_valid():
        total = sum(16.3 for q in questions if form.cleaned_data.get(f'q_{q.id}') == q.togri_variant)
        minutes, seconds = get_time_spent(request, 'sat_start')
        del request.session['sat_start']

        # Save result
        UserTestResult.objects.create(
            user=request.user,
            test_name="SAT Test",
            score=round(total / (len(questions)*16.3) * 100, 1)
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
            "percentage": round(total / (len(questions)*16.3) * 100, 1)
        })

    return render(request, "sat_test.html", {"form": form})


# ======================== Fan tanlash ========================
def fan_tanlash(request):
    if request.method == "POST":
        form = FanTanlashForm(request.POST)
        if form.is_valid():
            fan = form.cleaned_data["fan"]
            return redirect("milliy", fan=fan)
    else:
        form = FanTanlashForm()
    return render(request, "fan_tanlash.html", {"form": form})


# ======================== Universities ========================
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
    return render(request, 'xorijiy.html', {'xorijiy': xorijiy})


# ======================== DTM Stepwise Test ========================
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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserTestResult

@login_required
def my_profile_view(request):
    user = request.user

    # Foydalanuvchining barcha test natijalari
    user_results = UserTestResult.objects.filter(user=user)

    total_tests_taken = user_results.count()

    # O'rtacha ball va eng yuqori ball
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
        'user_results': user_results,  # agar kerak bo'lsa test nomlari va ballarini ko‘rsatish uchun
    }

    return render(request, 'profile.html', context)
