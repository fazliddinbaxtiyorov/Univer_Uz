from django.shortcuts import render
from .forms import FanlarForm


# Create your views here.
def fanlar_view(request):
    form = FanlarForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, "index.html", {"form": form})
