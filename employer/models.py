from django.db import models


# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    options=(

        ("employer","employer"),
        ("candidate","candidate")
    )

    role=models.CharField(max_length=120,choices=options,default="candidate")
    phone=models.CharField(max_length=12,null=True)
    date_of_birth=models.DateField(null=True)



class Jobs(models.Model):
    job_title=models.CharField(max_length=150)
    company=models.ForeignKey(User,on_delete=models.CASCADE,related_name="company")
    location=models.CharField(max_length=130)
    salary=models.PositiveIntegerField(null=True)
    experience=models.PositiveIntegerField(default=0)
    created_data=models.DateField(auto_now_add=True)
    last_date=models.DateField(null=True)
    active_status=models.BooleanField(default=True)

    def __str__(self):
        return self.job_title

class CompanyProfile(models.Model):
    company_name=models.CharField(max_length=120)
    location=models.CharField(max_length=120)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="employer")
    logo=models.ImageField(upload_to="companyprofile",null=True)
    description=models.CharField(max_length=120)
    services=models.CharField(max_length=1200)


class Applications(models.Model):
    applicant=models.ForeignKey(User,on_delete=models.CASCADE,related_name="applicant")
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE)
    options=(
        ("applied","applied"),
        ("accepted","accepted"),
        ("rejected","rejected"),
        ("pending","pending"),
        ("cancelled","cancelled")

    )


    status=models.CharField(max_length=120,choices=options,default="applied")
    date=models.DateTimeField(auto_now_add=True)


    # class Meta:
    #     unique_together=("applicant","job")