from django import forms
from .models import Students, DTM_Practise, Fanlar


class DTMForm(forms.ModelForm):
    class Meta:
        model = DTM_Practise
        fields = '__all__'


class FanlarForm(forms.ModelForm):
    class Meta:
        model = Fanlar
        fields = ['birinchi_fan', 'ikkinchi_fan']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        birinchi = self.initial.get("birinchi_fan") or self.data.get("birinchi_fan")

        if birinchi:
            self.fields['ikkinchi_fan'].choices = [
                (k, v) for k, v in self.fields['ikkinchi_fan'].choices if k != birinchi
            ]


class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = '__all__'

