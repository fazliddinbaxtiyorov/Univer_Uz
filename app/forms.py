# forms.py
from django import forms
from .models import (
    Fanlar, IELTS_writing, WritingSubmission, Milliy_Sertifikat
)


class FanlarForm(forms.ModelForm):
    class Meta:
        model = Fanlar
        fields = '__all__'


class Writing(forms.ModelForm):
    class Meta:
        model = IELTS_writing
        fields = '__all__'


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Ismingiz'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Mavzu'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Xabar', 'rows': 5}))


class FanTanlashForm(forms.Form):
    fan = forms.ChoiceField(choices=Milliy_Sertifikat.FAN_CHOICES)


class TestForm(forms.Form):
    """Milliy Sertifikat uchun - faqat ABCD"""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for q in questions:
                choices = [
                    ('A', q.variant_a),
                    ('B', q.variant_b),
                    ('C', q.variant_c),
                    ('D', q.variant_d),
                ]
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect,
                    label=q.savol,
                    required=False
                )


class TestFanForm(forms.Form):
    """DTM uchun - faqat ABCD"""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for q in questions:
                choices = [
                    ('A', q.variant_a),
                    ('B', q.variant_b),
                    ('C', q.variant_c),
                    ('D', q.variant_d),
                ]
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect,
                    label=q.savol,
                    required=False
                )


class IELTSReadingForm(forms.Form):
    """IELTS Reading: ABCD, TFNG, MATCH, FILL"""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for q in questions:
                if q.question_type == 'ABCD':
                    choices = [
                        ('A', q.variant_a or 'A'),
                        ('B', q.variant_b or 'B'),
                        ('C', q.variant_c or 'C'),
                        ('D', q.variant_d or 'D'),
                    ]
                    self.fields[f'q_{q.id}'] = forms.ChoiceField(
                        choices=choices,
                        widget=forms.RadioSelect,
                        label=q.savol,
                        required=False
                    )

                elif q.question_type == 'TFNG':
                    choices = [
                        ('TRUE', 'True'),
                        ('FALSE', 'False'),
                        ('NOT GIVEN', 'Not Given'),
                    ]
                    self.fields[f'q_{q.id}'] = forms.ChoiceField(
                        choices=choices,
                        widget=forms.RadioSelect,
                        label=q.savol,
                        required=False
                    )

                elif q.question_type == 'MATCH':
                    choices = [
                        ('A', q.variant_a or 'A'),
                        ('B', q.variant_b or 'B'),
                        ('C', q.variant_c or 'C'),
                        ('D', q.variant_d or 'D'),
                    ]
                    self.fields[f'q_{q.id}'] = forms.ChoiceField(
                        choices=choices,
                        widget=forms.RadioSelect,
                        label=q.savol,
                        required=False
                    )

                elif q.question_type == 'FILL':
                    self.fields[f'q_{q.id}'] = forms.CharField(
                        label=q.savol,
                        required=False,
                        widget=forms.TextInput(attrs={
                            'placeholder': 'Javobingizni kiriting...',
                            'class': 'fill-input',
                            'autocomplete': 'off',
                        })
                    )


class IELTSListeningForm(forms.Form):
    """IELTS Listening: ABCD, FILL, MATCH, MAP"""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for q in questions:
                if q.question_type == 'ABCD':
                    choices = [
                        ('A', q.variant_a or 'A'),
                        ('B', q.variant_b or 'B'),
                        ('C', q.variant_c or 'C'),
                        ('D', q.variant_d or 'D'),
                    ]
                    self.fields[f'q_{q.id}'] = forms.ChoiceField(
                        choices=choices,
                        widget=forms.RadioSelect,
                        label=q.savol,
                        required=False
                    )

                elif q.question_type == 'MATCH':
                    choices = [
                        ('A', q.variant_a or 'A'),
                        ('B', q.variant_b or 'B'),
                        ('C', q.variant_c or 'C'),
                        ('D', q.variant_d or 'D'),
                    ]
                    self.fields[f'q_{q.id}'] = forms.ChoiceField(
                        choices=choices,
                        widget=forms.RadioSelect,
                        label=q.savol,
                        required=False
                    )

                elif q.question_type in ('FILL', 'MAP'):
                    self.fields[f'q_{q.id}'] = forms.CharField(
                        label=q.savol,
                        required=False,
                        widget=forms.TextInput(attrs={
                            'placeholder': 'Javobingizni kiriting...',
                            'class': 'fill-input',
                            'autocomplete': 'off',
                        })
                    )


class SATForm(forms.Form):
    """SAT uchun - faqat ABCD"""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for q in questions:
                choices = [
                    ('A', q.variant_a or 'A'),
                    ('B', q.variant_b or 'B'),
                    ('C', q.variant_c or 'C'),
                    ('D', q.variant_d or 'D'),
                ]
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect,
                    label=q.savol,
                    required=False
                )


class WritingSubmissionForm(forms.ModelForm):
    class Meta:
        model = WritingSubmission
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(attrs={
                'rows': 15,
                'placeholder': 'Javobingizni shu yerga yozing...',
                'class': 'writing-textarea'
            })
        }