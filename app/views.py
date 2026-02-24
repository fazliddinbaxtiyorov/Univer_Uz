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
from django.db.models import Avg, Max
from django.contrib.auth.models import User
import random, time, re, json
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test

from .models import WritingQuestion, WritingSubmission
from .forms import WritingSubmissionForm
from .utils import check_ielts_writing
from .hi import get_ai_explanation


# ======================== HELPERS ========================

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
    return render(request, "ielts.html", {
        "tests": all_passages,
        "total_questions": total_questions,
        "duration": 60,
    })


def test_list_sat(request):
    tests = Sat.objects.all()
    return render(request, "sat.html", {"tests": tests})


def fan_tanlash(request):
    """Milliy Sertifikat — fan tanlash + test card ko'rsatish"""
    selected_fan = request.GET.get('fan', '')

    # Har bir fan uchun savol soni
    fans_with_count = []
    for code, name in Milliy_Sertifikat.FAN_CHOICES:
        count = Milliy_Sertifikat.objects.filter(fan=code).count()
        fans_with_count.append({
            'code': code,
            'name': name,
            'count': count,
        })

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
        total = sum(
            2 for q in all_questions
            if answers_match(form.cleaned_data.get(f'q_{q.id}'), q.togri_variant)
        )
        start = request.session.pop('reading_start', time.time())
        spent = int(time.time() - start)
        percentage = round(total / (len(all_questions) * 2) * 100, 1) if all_questions else 0

        UserTestResult.objects.create(
            user=request.user,
            test_name="IELTS Reading",
            score=percentage
        )

        results = [{
            "savol": q.savol,
            "question_type": q.question_type,
            "user_answer": form.cleaned_data.get(f'q_{q.id}'),
            "correct": q.togri_variant,
            "is_correct": answers_match(form.cleaned_data.get(f'q_{q.id}'), q.togri_variant),
            "question_id": q.id,
            "category": "IELTS"
        } for q in all_questions]

        return render(request, "result.html", {
            "results": results,
            "total": total,
            "percentage": percentage,
            "minutes": spent // 60,
            "seconds": spent % 60
        })

    # Part bo'yicha guruhlash
    parts_dict = {}
    for q in all_questions:
        parts_dict.setdefault(q.part, []).append(q)

    test_data = []
    for part_num in sorted(parts_dict.keys()):
        qs = parts_dict[part_num]
        test_data.append({
            "part": part_num,
            "part_label": f"Part {part_num}",
            "passage_text": reading_test.passage_text,
            "passage_title": reading_test.passage_title,
            "questions": [
                {"model": q, "field": form[f"q_{q.id}"]}
                for q in qs
            ]
        })

    return render(request, "reading_test.html", {
        "test_data": test_data,
        "total_steps": len(test_data),
        "duration": 60,
        "reading_test": reading_test,
        "user_coins": request.user.profile.coins,
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
            if status == "not_enough_coins":
                messages.error(request, "Sizda yetarli coin yo'q!")
            return redirect("buy_coins")

        if form.is_valid():
            total = sum(
                1 for q in questions
                if answers_match(form.cleaned_data.get(f'q_{q.id}'), q.togri_variant)
            )
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
                "question_type": q.question_type,
                "user_answer": form.cleaned_data.get(f'q_{q.id}'),
                "correct": q.togri_variant,
                "is_correct": answers_match(form.cleaned_data.get(f'q_{q.id}'), q.togri_variant),
                "question_id": q.id,
                "category": "IELTS_LISTENING"
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

    parts = {}
    for q in questions:
        parts.setdefault(q.part, []).append(q)

    return render(request, "listening_test.html", {
        "test": test,
        "form": form,
        "questions": questions,
        "parts": parts,
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

    # Sessiyada saqlangan savollar bormi?
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
            tanlangan = [birinchi_fan, ikkinchi_fan]

            # Majburiy fanlar — tanlangan fanlar bilan takrorlanmasin
            majburiy = []
            for fan in ['Ona Tili', 'Matematika', 'Tarix']:
                if fan not in tanlangan:
                    majburiy.append(fan)
                else:
                    # Alternativlar
                    for alt in ['Ingliz Tili', 'Fizika', 'Kimyo', 'Biologiya']:
                        if alt not in tanlangan and alt not in majburiy:
                            majburiy.append(alt)
                            break

            fanlar = tanlangan + majburiy[:3]
            request.session['selected_subjects'] = fanlar
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

    fanlar = request.session['selected_subjects']

    all_questions = []
    for step, fan in enumerate(fanlar, 1):
        qs = list(Milliy_Sertifikat.objects.filter(fan=fan))
        if len(qs) > 30:
            qs = random.sample(qs, 30)
        for q in qs:
            q.step = step
            q.fan_nomi = fan
        all_questions.extend(qs)

        # ✅ SHU QATORNI QO'SHING — barcha savollarni aralashtirib yuborish
    random.shuffle(all_questions)

    total_questions = len(all_questions)

    if request.method == "POST":
        total_score = 0
        for q in all_questions:
            user_javob = request.POST.get(f'q_{q.id}')
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
        percentage = round(total_score / (total_questions * 3.1) * 100, 1) if total_questions else 0

        UserTestResult.objects.create(
            user=request.user,
            test_name="DTM Test",
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
            "fan": q.fan,
            "step": q.step
        } for q in all_questions]

        request.session.flush()

        return render(request, 'result.html', {
            "results": results,
            "total": round(total_score, 1),
            "total_questions": total_questions,
            "minutes": minutes,
            "seconds": seconds,
            "percentage": percentage,
            "test_type": "DTM Test",
            "fanlar": fanlar
        })

    # Fan bo'yicha guruhlash — template uchun
    fanlar_data = []
    fan_groups = {}
    for q in all_questions:
        fan_groups.setdefault(q.fan, []).append(q)

    for step, fan in enumerate(fanlar, 1):
        qs = fan_groups.get(fan, [])
        fanlar_data.append({
            'fan': fan,
            'step': step,
            'questions': qs,
            'ball': 3.1 if step == 1 else (2.1 if step == 2 else 1.1)
        })

    return render(request, 'test_process.html', {
        'all_questions': all_questions,
        'fanlar_data': fanlar_data,
        'timer_seconds': 3600,
        'fanlar': fanlar,
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
            if status == "not_enough_coins":
                messages.error(request, "Sizda yetarli coin yo'q!")
                return redirect("buy_coins")
            else:
                messages.error(request, "Kirish huquqi yo'q.")
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
            percentage = round(total / (len(questions) * 16.3) * 100, 1) if questions else 0

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
                "minutes": minutes,
                "seconds": seconds,
                "percentage": percentage,
                "test_type": f"SAT - {test_obj.title}"
            })

    return render(request, "sat_test.html", {
        "form": form,
        "questions": questions,
        "test": test_obj,
        "user_coins": request.user.profile.coins
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
    user_results = UserTestResult.objects.filter(user=user)
    total_tests_taken = user_results.count()

    if total_tests_taken > 0:
        average_score = round(sum(r.score for r in user_results) / total_tests_taken, 1)
        best_score = max(r.score for r in user_results)
    else:
        average_score = 0
        best_score = 0

    return render(request, 'profile.html', {
        'user': user.get_full_name() or user.username,
        'total_tests_taken': total_tests_taken,
        'average_score': average_score,
        'best_score': best_score,
        'user_results': user_results,
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
    return render(request, 'leaderboard.html', {'leaderboard': leaderboard_data})


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


# ======================== MANAGE TESTS (ADMIN) ========================

def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin, login_url='login')
def manage_tests(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create_group":
            g_type = request.POST.get("group_category")
            title = request.POST.get("group_title")
            content = request.POST.get("passage_content", "")
            is_paid = request.POST.get("is_paid") == "on"
            price = request.POST.get("price", 25)

            try:
                if g_type == "READING":
                    ReadingTest.objects.create(
                        passage_text=content, category='READING',
                        is_paid=is_paid, price=price
                    )
                elif g_type == "LISTENING":
                    ListeningTest.objects.create(
                        title=title, category='LISTENING',
                        is_paid=is_paid, price=price
                    )
                elif g_type == "SAT":
                    Sat.objects.create(
                        title=title, category='SAT',
                        is_paid=is_paid, price=price
                    )
                messages.success(request, f"Guruh yaratildi!")
            except Exception as e:
                messages.error(request, f"Xatolik: {e}")

        elif action == "add_question":
            cat = request.POST.get("category")
            group_id = request.POST.get("test_group")
            savol_matni = request.POST.get("savol")

            try:
                if cat == "IELTS_READING":
                    IELTS_Reading.objects.create(
                        test_group_id=group_id,
                        savol=savol_matni,
                        question_type=request.POST.get("question_type", "ABCD"),
                        part=request.POST.get("part", 1),
                        variant_a=request.POST.get("variant_a", ""),
                        variant_b=request.POST.get("variant_b", ""),
                        variant_c=request.POST.get("variant_c", ""),
                        variant_d=request.POST.get("variant_d", ""),
                        togri_variant=request.POST.get("togri_variant"),
                        question_image=request.FILES.get("question_image"),
                        image_a=request.FILES.get("image_a"),
                        image_b=request.FILES.get("image_b"),
                        image_c=request.FILES.get("image_c"),
                        image_d=request.FILES.get("image_d"),
                    )
                elif cat == "IELTS_LISTENING":
                    IELTSListeningQuestion.objects.create(
                        test_group_id=group_id,
                        savol=savol_matni,
                        question_type=request.POST.get("question_type", "ABCD"),
                        variant_a=request.POST.get("variant_a", ""),
                        variant_b=request.POST.get("variant_b", ""),
                        variant_c=request.POST.get("variant_c", ""),
                        variant_d=request.POST.get("variant_d", ""),
                        togri_variant=request.POST.get("togri_variant"),
                        audio=request.FILES.get("audio"),
                        map_image=request.FILES.get("map_image"),
                        part=request.POST.get("part", 1),
                    )
                elif cat == "SAT":
                    SATQuestion.objects.create(
                        test_group_id=group_id,
                        savol=savol_matni,
                        variant_a=request.POST.get("variant_a", ""),
                        variant_b=request.POST.get("variant_b", ""),
                        variant_c=request.POST.get("variant_c", ""),
                        variant_d=request.POST.get("variant_d", ""),
                        togri_variant=request.POST.get("togri_variant"),
                        question_image=request.FILES.get("question_image"),
                        image_a=request.FILES.get("image_a"),
                        image_b=request.FILES.get("image_b"),
                        image_c=request.FILES.get("image_c"),
                        image_d=request.FILES.get("image_d"),
                    )
                elif cat == "MILL_NATIONAL":
                    Milliy_Sertifikat.objects.create(
                        fan=request.POST.get("fan"),
                        savol=savol_matni,
                        variant_a=request.POST.get("variant_a", ""),
                        variant_b=request.POST.get("variant_b", ""),
                        variant_c=request.POST.get("variant_c", ""),
                        variant_d=request.POST.get("variant_d", ""),
                        togri_variant=request.POST.get("togri_variant"),
                        savol_rasm=request.FILES.get("savol_rasm"),
                        image_a=request.FILES.get("image_a"),
                        image_b=request.FILES.get("image_b"),
                        image_c=request.FILES.get("image_c"),
                        image_d=request.FILES.get("image_d"),
                    )

                messages.success(request, "Savol muvaffaqiyatli saqlandi!")
            except Exception as e:
                messages.error(request, f"Xatolik: {e}")

        return redirect("manage_tests")

    return render(request, "manage_tests.html", {
        "reading_tests": ReadingTest.objects.all().order_by('-id'),
        "listening_tests": ListeningTest.objects.all().order_by('-id'),
        "sat_tests": Sat.objects.all().order_by('-id'),
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