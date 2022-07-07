from django import forms
from employer.models import Jobs,CompanyProfile
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from employer.models import User
class JObForm(forms.ModelForm):
    class Meta:
        model=Jobs
        exclude=("company","created_date","active_status")
        widgets={
            "last_date":forms.DateInput(attrs={"class":"form-control ","type":"date"}),
            "job_title": forms.TextInput(attrs={'class':'form-control rounded-pill ',"placeholder":"job-title"}),
            "experience": forms.TextInput(attrs={'class': "form-control rounded-pill","placeholder":"0"}),
            "location": forms.TextInput(attrs={'class': 'form-control rounded-pill',"placeholder":"location"}),
            'salary': forms.TextInput(attrs={'class': 'form-control rounded-pill',"placeholder":"0"}),

        }


class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2","role","phone"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())

class CompanyprofileForm(forms.ModelForm):
    class Meta:
        model=CompanyProfile
        exclude=("user",)