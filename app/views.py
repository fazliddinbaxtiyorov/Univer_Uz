from django.shortcuts import render, get_object_or_404, redirect
from .forms import FanlarForm, IELTSReadingForm, TestForm, FanTanlashForm, IELTSListeningForm, SATForm, Writing, TestFanForm
from .models import IELTS_Reading, Milliy_Sertifikat, IELTSListeningQuestion, SATQuestion, Davlat_Univer, Xususiy_Univer, Xorijiy_Univer
from django.db.models import Q


# Create your views here.
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
            return redirect("milliy", fan=fan)
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




def dtm_test_view(request):
    if 'selected_subjects' not in request.session:
        if request.method == "POST":
            birinchi_fan = request.POST.get('birinchi_fan')
            ikkinchi_fan = request.POST.get('ikkinchi_fan')

            if birinchi_fan and ikkinchi_fan and birinchi_fan != ikkinchi_fan:
                tanlangan = [birinchi_fan, ikkinchi_fan]
                fanlar = {
                    '1': birinchi_fan,
                    '2': ikkinchi_fan,
                    '3': 'Ona Tili' if 'Ona Tili' not in tanlangan else 'Ingliz Tili',
                    '4': 'Matematika' if 'Matematika' not in tanlangan else 'Fizika',
                    '5': 'Tarix'
                }

                request.session['selected_subjects'] = fanlar
                request.session['current_step'] = 1
                request.session['total_score'] = 0.0
                return redirect('dtm_test')
            else:
                return render(request, 'select_subjects.html', {'xato': 'Ikkala fan ham tanlanishi va bir xil bo\'lmasligi kerak!'})

        return render(request, 'select_subjects.html')

    step = request.session.get('current_step', 1)
    subjects = request.session['selected_subjects']

    if step > 5:
        score = request.session.get('total_score', 0)
        request.session.flush()
        return render(request, 'result.html', {'score': round(score, 1)})

    current_subject = subjects[str(step)]
    ball = 3.1 if step == 1 else 2.1 if step == 2 else 1.1
    questions = Milliy_Sertifikat.objects.filter(fan=current_subject)

    form = TestFanForm(questions=questions)

    if request.method == "POST":
        form = TestFanForm(request.POST, questions=questions)
        if form.is_valid():
            togri_javoblar = 0
            for q in questions:
                user_javob = form.cleaned_data.get(f'q_{q.id}')
                if user_javob == q.togri_variant:
                    togri_javoblar += 1

            request.session['total_score'] += togri_javoblar * ball
            request.session['current_step'] += 1
            return redirect('dtm_test')

    return render(request, 'test_process.html', {
        'subject': current_subject,
        'questions': questions,
        'step': step,
        'ball': ball,
        'form': form
    })
