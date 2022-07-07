from django.db import models

# Create your models here.

from employer.models import User

class CandidateProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="candidate")
    profile_pic=models.ImageField(upload_to="cadprofile")
    resume=models.FileField(upload_to="cvs",null=True)
    qualification=models.CharField(max_length=120)
    experience=models.PositiveIntegerField(default=0)
    skills=models.CharField(max_length=120)


