from django import forms
from .models import Students, DTM_Practise, Fanlar, IELTS_Reading, IELTSListeningQuestion, Milliy_Sertifikat, IELTS_writing


class DTMForm(forms.ModelForm):
    class Meta:
        model = DTM_Practise
        fields = '__all__'


class TestFanForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for q in questions:
                items = q.togri_javob.split()
                choices = []
                for i in range(0, len(items), 2):
                    if i + 1 < len(items):
                        key = items[i]
                        value = f"{items[i]} {items[i + 1]}"  # A salom
                        choices.append((key, value))

                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    label=q.savol[:50],
                    choices=choices[:4],
                    widget=forms.RadioSelect
                )

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


class IELTSListeningForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)

        for q in questions:
            items = q.variantlar.split()
            choices = []

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
            items = q.togri_javob.split()

            choices = [
                (items[i], f"{items[i]} {items[i+1]}")
                for i in range(0, len(items), 2)
            ]

            self.fields[f"q_{q.id}"] = forms.ChoiceField(
                label=q.savol,
                choices=choices,
                widget=forms.RadioSelect
            )


class FanTanlashForm(forms.Form):
    fan = forms.ChoiceField(choices=Milliy_Sertifikat.Fan_CHOICES)


class SATForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)

        if questions:
            for q in questions:
                self.fields[f"q_{q.id}"] = forms.ChoiceField(
                    label=q.savol,
                    choices=[
                        ("A", q.variant_a),
                        ("B", q.variant_b),
                        ("C", q.variant_c),
                        ("D", q.variant_d)
                    ],
                    widget=forms.RadioSelect,
                    required=True
                )


class Writing(forms.ModelForm):
    class Meta:
        model = IELTS_writing
        fields = '__all__'
