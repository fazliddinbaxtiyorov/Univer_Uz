from django import forms
from .models import DTM_Practise, Fanlar, IELTS_Reading, IELTSListeningQuestion, Milliy_Sertifikat, IELTS_writing


class DTMForm(forms.ModelForm):
    class Meta:
        model = DTM_Practise
        fields = '__all__'


class TestFanForm(forms.Form):
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


class IELTSReadingForm(forms.Form):
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


class IELTSListeningForm(forms.Form):
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


class TestForm(forms.Form):
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


class FanTanlashForm(forms.Form):
    fan = forms.ChoiceField(choices=Milliy_Sertifikat.FAN_CHOICES)


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

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
