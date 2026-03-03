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
    name    = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Ismingiz'}))
    email   = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Mavzu'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Xabar', 'rows': 5}))


class FanTanlashForm(forms.Form):
    fan = forms.ChoiceField(choices=Milliy_Sertifikat.FAN_CHOICES)


class TestForm(forms.Form):
    """Milliy Sertifikat uchun — faqat ABCD"""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for q in questions:
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=[('A', q.variant_a), ('B', q.variant_b),
                             ('C', q.variant_c), ('D', q.variant_d)],
                    widget=forms.RadioSelect,
                    label=q.savol,
                    required=False
                )


class TestFanForm(forms.Form):
    """DTM uchun — faqat ABCD"""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for q in questions:
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=[('A', q.variant_a), ('B', q.variant_b),
                             ('C', q.variant_c), ('D', q.variant_d)],
                    widget=forms.RadioSelect,
                    label=q.savol,
                    required=False
                )


class IELTSReadingForm(forms.Form):
    """
    IELTS Reading:
      ABCD    — radio A/B/C/D
      TFNG    — radio TRUE/FALSE/NOT GIVEN
      YNNG    — radio YES/NO/NOT GIVEN
      MATCH   — select i..xii
      FILL    — text input
      FILLBOX — hidden input (JS to'ldiradi)
    """
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not questions:
            return

        for q in questions:

            # ── ABCD ──
            if q.question_type == 'ABCD':
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=[('A', q.variant_a or 'A'), ('B', q.variant_b or 'B'),
                             ('C', q.variant_c or 'C'), ('D', q.variant_d or 'D')],
                    widget=forms.RadioSelect,
                    label=q.savol,
                    required=False,
                )

            # ── TRUE / FALSE / NOT GIVEN ──
            elif q.question_type == 'TFNG':
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=[
                        ('TRUE',      'True'),
                        ('FALSE',     'False'),
                        ('NOT GIVEN', 'Not Given'),
                    ],
                    widget=forms.RadioSelect,
                    label=q.savol,
                    required=False,
                )

            # ── YES / NO / NOT GIVEN ──
            elif q.question_type == 'YNNG':
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=[
                        ('YES',       'Yes'),
                        ('NO',        'No'),
                        ('NOT GIVEN', 'Not Given'),
                    ],
                    widget=forms.RadioSelect,
                    label=q.savol,
                    required=False,
                )

            # ── MATCHING HEADINGS (i–xii dropdown) ──
            elif q.question_type == 'MATCH':
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=[
                        ('',     '— Select heading —'),
                        ('i',    'i'),   ('ii',   'ii'),
                        ('iii',  'iii'), ('iv',   'iv'),
                        ('v',    'v'),   ('vi',   'vi'),
                        ('vii',  'vii'), ('viii', 'viii'),
                        ('ix',   'ix'),  ('x',    'x'),
                        ('xi',   'xi'),  ('xii',  'xii'),
                    ],
                    widget=forms.Select,
                    label=q.savol,
                    required=False,
                )

            # ── FILL IN THE BLANK (erkin matn) ──
            elif q.question_type == 'FILL':
                self.fields[f'q_{q.id}'] = forms.CharField(
                    label=q.savol,
                    required=False,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Write your answer...',
                        'class': 'fill-input',
                        'autocomplete': 'off',
                    })
                )

            # ── FILL IN THE BLANK WITH WORD BOX ──
            # JS blank-slot orqali to'ldiradi → hidden input
            elif q.question_type == 'FILLBOX':
                self.fields[f'q_{q.id}'] = forms.CharField(
                    label=q.savol,
                    required=False,
                    widget=forms.HiddenInput(attrs={
                        'id': f'answer-{q.id}',
                        'class': 'fillbox-hidden',
                    })
                )


class IELTSListeningForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not questions:
            return
        for q in questions:
            if q.question_type == 'ABCD':
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=[('A', q.variant_a or 'A'), ('B', q.variant_b or 'B'),
                             ('C', q.variant_c or 'C'), ('D', q.variant_d or 'D')],
                    widget=forms.RadioSelect, label=q.savol, required=False,
                )
            elif q.question_type == 'MATCH':
                self.fields[f'q_{q.id}'] = forms.ChoiceField(
                    choices=[('A', q.variant_a or 'A'), ('B', q.variant_b or 'B'),
                             ('C', q.variant_c or 'C'), ('D', q.variant_d or 'D')],
                    widget=forms.RadioSelect, label=q.savol, required=False,
                )
            elif q.question_type in ('FILL', 'MAP'):
                self.fields[f'q_{q.id}'] = forms.CharField(
                    label=q.savol, required=False,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Javobingizni kiriting...',
                        'class': 'fill-input', 'autocomplete': 'off',
                    })
                )
            elif q.question_type == 'CHECK':
                # Mavjud variantlardan choices yasaymiz
                choices = []
                for letter, val in [('A',q.variant_a),('B',q.variant_b),('C',q.variant_c),
                                    ('D',q.variant_d),('E',q.variant_e),('F',q.variant_f),
                                    ('G',q.variant_g),('H',q.variant_h),('I',q.variant_i)]:
                    if val:
                        choices.append((letter, val))
                self.fields[f'q_{q.id}'] = forms.MultipleChoiceField(
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple,
                    label=q.savol,
                    required=False,
                )

class SATForm(forms.Form):
    """SAT uchun — ABCD"""
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not questions:
            return

        for q in questions:
            self.fields[f'q_{q.id}'] = forms.ChoiceField(
                choices=[('A', q.variant_a or 'A'), ('B', q.variant_b or 'B'),
                         ('C', q.variant_c or 'C'), ('D', q.variant_d or 'D')],
                widget=forms.RadioSelect,
                label=q.savol,
                required=False,
            )


class WritingSubmissionForm(forms.ModelForm):
    class Meta:
        model = WritingSubmission
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(attrs={
                'rows': 15,
                'placeholder': 'Javobingizni shu yerga yozing...',
                'class': 'writing-textarea',
            })
        }