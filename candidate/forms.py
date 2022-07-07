from django import forms
from candidate.models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
    class Meta:
            model = CandidateProfile
            exclude = ("user",)
            widgets = {
                "qualification": forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
                "experience": forms.TextInput(attrs={'class': "form-control rounded-pill"}),
                "skills": forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
                'resume': forms.FileInput(attrs={'class': 'form-control rounded-pill'}),
                'profile_pic': forms.FileInput(attrs={'class': 'form-control rounded-pill'})

            }


class CandidateProfileEditForm(forms.ModelForm):
    first_name=forms.CharField(max_length=120)
    last_name=forms.CharField(max_length=120)
    phone=forms.CharField(max_length=12)
    email=forms.EmailField()
    class Meta:
        model=CandidateProfile
        fields=[
            'first_name',
            'last_name',
            'phone',
            'email',
            'qualification',
            'experience',
            'skills',
            'profile_pic',
            'resume'

        ]




