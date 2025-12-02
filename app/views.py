from django.shortcuts import render, get_object_or_404
from .forms import FanlarForm, IELTSReadingForm
from .models import IELTS_Reading

# Create your views here.
def fanlar_view(request):
    form = FanlarForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, "index.html", {"form": form})


def reading_test(request):
    if request.method == 'POST':
        form = IELTSReadingForm(request.POST)
        if form.is_valid():
            # 10 ta A/B/C/D
            mc_data = {str(i): form.cleaned_data[f'mc_answer_{i}'] for i in range(1,11)}
            # 10 ta text
            text_data = {str(i): form.cleaned_data[f'text_answer_{i}'] for i in range(11,21)}
            # 10 ta heading
            heading_data = {str(i): form.cleaned_data[f'heading_{i}'] for i in range(21,31)}

            IELTS_Reading.objects.create(
                multiple_choice_answers=mc_data,
                text_answers=text_data,
                headings=heading_data
            )
    else:
        form = IELTSReadingForm()
    return render(request, 'reading_test.html', {'form': form})


def listening_test(request):
    if request.method == 'POST':
        form = IELTSReadingForm(request.POST)
        if form.is_valid():
            data = {str(i): form.cleaned_data[f'answer_{i}'] for i in range(1, 31)}
            IELTS_Reading.objects.create(answers=data)
    else:
        form = IELTSReadingForm()
    return render(request, 'listening_test.html', {'form': form})
