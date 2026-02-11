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

        if not questions:
            return

        for q in questions:

            # 🔹 Variantlar savol turiga qarab
            if q.question_type == 'TFNG':
                choices = [
                    ('A', 'True'),
                    ('B', 'False'),
                    ('C', 'Not Given'),
                ]
            else:  # ABCD
                choices = []

                if q.variant_a:
                    choices.append(('A', q.variant_a))
                if q.variant_b:
                    choices.append(('B', q.variant_b))
                if q.variant_c:
                    choices.append(('C', q.variant_c))
                if q.variant_d:
                    choices.append(('D', q.variant_d))

            # 🔹 Field yaratish
            self.fields[f"q_{q.id}"] = forms.ChoiceField(
                label=q.savol,
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
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


# forms.py
from django import forms
from .models import WritingSubmission

class WritingSubmissionForm(forms.ModelForm):
    class Meta:
        model = WritingSubmission
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(attrs={
                'rows': 14,
                'placeholder': 'Write your IELTS answer here...'
            })
        }
