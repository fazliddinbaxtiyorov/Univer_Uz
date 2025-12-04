from django.shortcuts import render, get_object_or_404, redirect
from .forms import FanlarForm, IELTSReadingForm, TestForm, FanTanlashForm, IELTSListeningForm, SATForm, Writing
from .models import IELTS_Reading, Milliy_Sertifikat, IELTSListeningQuestion, SATQuestion, Davlat_Univer, Xususiy_Univer, Xorijiy_Univer
from django.db.models import Q


# Create your views here.
def ielts(request):
    return render(request, 'ielts.html')


def fanlar_view(request):
    form = FanlarForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, "index.html", {"form": form})


def writing(request):
    form = Writing(request.POST)
    if form.is_valid():
        form.save()
    return render(request, "writing.html", {"form": form})


def ielts_reading_view(request):
    questions = IELTS_Reading.objects.all()[:10]  # masalan 10 ta savol

    if request.method == "POST":
        form = IELTSReadingForm(request.POST, questions=questions)
        if form.is_valid():
            total = 0
            results = []

            for q in questions:
                user_answer = form.cleaned_data.get(f'q_{q.id}')
                correct = q.togri_variant

                if user_answer == correct:
                    total += 2  # har to‘g‘ri javob = 2 ball

                results.append({
                    "savol": q.savol,
                    "user_answer": user_answer,
                    "correct": correct
                })

            return render(request, "ielts_reading_result.html", {"results": results, "total": total})

    else:
        form = IELTSReadingForm(questions=questions)

    return render(request, "reading_test.html", {"form": form})


# ===== Listening =====
def ielts_listening_view(request):
    questions = IELTSListeningQuestion.objects.all()[:20]  # 20 ta savol

    if request.method == "POST":
        form = IELTSListeningForm(request.POST, questions=questions)
        if form.is_valid():
            total = 0
            results = []

            for q in questions:
                user_answer = form.cleaned_data.get(f'q_{q.id}')
                correct = q.togri_variant
                if user_answer == correct:
                    total += 2

                results.append({
                    "savol": q.savol,
                    "user_answer": user_answer,
                    "correct": correct
                })

            return render(request, "ielts_listening_result.html", {"results": results, "total": total})
    else:
        form = IELTSListeningForm(questions=questions)

    return render(request, "listening_test.html", {"form": form, "questions": questions})


def fan_tanlash(request):
    if request.method == "POST":
        form = FanTanlashForm(request.POST)
        if form.is_valid():
            fan = form.cleaned_data["fan"]
            return redirect("test_boshlash", fan=fan)
    else:
        form = FanTanlashForm()

    return render(request, "fan_tanlash.html", {"form": form})


def test_boshlash(request, fan):
    questions = Milliy_Sertifikat.objects.filter(fan=fan)[:50]

    if request.method == "POST":
        form = TestForm(request.POST, questions=questions)

        if form.is_valid():
            total = 0

            for q in questions:
                user_answer = form.cleaned_data.get(f"q_{q.id}")

                if user_answer == q.togri_variant:
                    total += 2

            return render(request, "test_natija.html", {"ball": total})

    else:
        form = TestForm(questions=questions)

    return render(request, "test_milliy.html", {"form": form})


def sat_test_view(request):
    questions = SATQuestion.objects.all()[:20]

    if request.method == "POST":
        form = SATForm(request.POST, questions=questions)

        if form.is_valid():
            total = 0
            results = []

            for q in questions:
                user_answer = form.cleaned_data.get(f"q_{q.id}")
                correct = q.togri_variant

                if user_answer == correct:
                    total += 16.3

                results.append({
                    "savol": q.savol,
                    "user_answer": user_answer,
                    "correct": correct
                })

            return render(request, "sat_result.html", {
                "results": results,
                "total": total
            })

    else:
        form = SATForm(questions=questions)

    return render(request, "sat_test.html", {"form": form})


def univerlar(request):
    davlat = Davlat_Univer.objects.all()
    xususiy = Xususiy_Univer.objects.all()
    xorijiy= Xorijiy_Univer.objects.all()
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


def search(request):
    query = request.GET.get('q')
    davlat_search = Davlat_Univer.objects.filter(Q(title__icontains=query))
    xususiy_search = Xususiy_Univer.objects.filter(Q(title__icontains=query))
    xorijiy_search = Xorijiy_Univer.objects.filter(Q(title__icontains=query))
