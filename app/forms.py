from django import forms
from .models import Students, DTM_Practise, Fanlar, IELTS_Reading, IELTS_listening


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


class IELTSReadingForm(forms.ModelForm):
    class Meta:
        model = IELTS_Reading
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in range(1, 11):
            self.fields[f'mc_answer_{i}'] = forms.ChoiceField(
                label=f'Savol {i} (A/B/C/D)',
                choices=[('A','A'),('B','B'),('C','C'),('D','D')],
                widget=forms.RadioSelect,
                required=True
            )


        for i in range(11, 21):
            self.fields[f'text_answer_{i}'] = forms.CharField(
                label=f'Savol {i} (Text)',
                widget=forms.TextInput(attrs={'class':'form-control'}),
                required=True
            )


        for i in range(21, 31):
            self.fields[f'heading_{i}'] = forms.CharField(
                label=f'Sarlavha {i-20}',
                widget=forms.TextInput(attrs={'class':'form-control'}),
                required=True
            )


class IELTSListeningForm(forms.ModelForm):
    class Meta:
        model = IELTS_listening
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(1, 41):
            self.fields[f'answer_{i}'] = forms.ChoiceField(
                label=f'Savol {i}',
                choices=[('A','A'),('B','B'),('C','C'),('D','D')],
                widget=forms.RadioSelect,
                required=True
            )
