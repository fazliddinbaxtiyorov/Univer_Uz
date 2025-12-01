from django import forms
from .models import Students, DTM_Practise, Fanlar


class DTMForm(forms.ModelForm):
    class Meta:
        model = DTM_Practise
        fields = '__all__'


class FanlarForm(forms.ModelForm):
    class Meta:
        model = Fanlar
        fields = '__all__'


class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = '__all__'
