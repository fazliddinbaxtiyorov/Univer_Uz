from django import forms
from .models import Students, DTM_Practise, Fanlar, IELTS_Reading, IELTSListeningQuestion, Milliy_Sertifikat


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


# ===== IELTS Reading =====
class IELTSReadingForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)

        for q in questions:
            items = q.variantlar.split()  # "A 3 B 4 C 5 D 6" → ['A','3','B','4','C','5','D','6']
            choices = [(items[i], f"{items[i]} {items[i+1]}") for i in range(0, len(items), 2)]

            self.fields[f'q_{q.id}'] = forms.ChoiceField(
                label=q.savol,
                choices=choices,
                widget=forms.RadioSelect
            )


# ===== IELTS Listening =====
from django import forms

class IELTSListeningForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)

        for q in questions:
            items = q.variantlar.split()  # "A 3 B 4 C 5 D 6" → ['A','3','B','4','C','5','D','6']
            choices = []

            # Xatolikdan saqlanish: agar noto‘liq yozilgan bo‘lsa
            for i in range(0, len(items), 2):
                if i+1 < len(items):
                    choices.append((items[i], f"{items[i]} {items[i+1]}"))

            self.fields[f'q_{q.id}'] = forms.ChoiceField(
                label=q.savol,
                choices=choices,
                widget=forms.RadioSelect
            )



class TestForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)

        for q in questions:
            # q.togri_javob = "A 3 B 4 C 5 D 6"
            # Split qilib variantlar va matnli javoblar hosil qilamiz
            items = q.togri_javob.split()  # ['A','3','B','4','C','5','D','6']

            choices = [
                (items[i], f"{items[i]} {items[i+1]}")  # ('A','A 3')
                for i in range(0, len(items), 2)
            ]

            self.fields[f"q_{q.id}"] = forms.ChoiceField(
                label=q.savol,
                choices=choices,
                widget=forms.RadioSelect
            )


class FanTanlashForm(forms.Form):
    fan = forms.ChoiceField(choices=Milliy_Sertifikat.Fan_CHOICES)
