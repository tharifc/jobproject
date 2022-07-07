from django.shortcuts import render

# Create your views here.
from candidate.forms import CandidateProfileForm
from candidate.models import CandidateProfile
from candidate.forms import CandidateProfileEditForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, FormView, UpdateView,DetailView,ListView
from django.shortcuts import redirect

from employer.models import User,Jobs,Applications
from django.contrib import messages
from employer.decorators import signin_required

class CandidateHomeView(TemplateView):
    template_name = "candidate-homeview.html"


class CandidateProfileView(CreateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = "candidate-profile.html"
    success_url = reverse_lazy('candidate-home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)




class CandidateProfileDetailView(TemplateView):
    template_name = "candidate-view-profile.html"


class CandidateProfileEditView(FormView):
    model = CandidateProfile
    template_name = "cand-edit.html"
    form_class = CandidateProfileEditForm

    def get(self, request, *args, **kwargs):
        print(request.user.candidate.qualification)


        profile = CandidateProfile.objects.get(user=request.user)
        form = CandidateProfileEditForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': request.user.phone,
            'email': request.user.email
        })
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        profile = CandidateProfile.objects.get(user=request.user)

        form = self.form_class(instance=profile, data=request.POST, files=request.files)
        if form.is_valid():
            first_name = form.cleaned_data.pop("first_name")
            last_name = form.cleaned_data.pop("last_name")
            phone = form.cleaned_data.pop("phone")
            email = form.cleaned_data.pop("email")
            form.save()
            user=User.objects.get(id=request.user.id)
            user.email=email
            user.phone=phone
            user.first_name=first_name
            user.last_name=last_name
            user.save()

            return redirect('cand-home')
        else:
            return render(request,self.template_name,{"forms":form})



class CandidateJobListView(ListView):
    model = Jobs
    context_object_name = "jobs"
    template_name = "candidate-joblist.html"

    def get_queryset(self):
        return self.model.objects.all().order_by("-created_data")


class CandidateJobDetailView(DetailView):
    model = Jobs
    context_object_name = "job"
    template_name = "candidate-job-detail.html"
    pk_url_kwarg = "id"


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        is_applied=Applications.objects.filter(applicant=self.request.user,job=self.object)
        context["is_applied"]=is_applied
        return context

def apply_now(request, *args, **kwargs):
        user = request.user
        job_id = kwargs.get("id")
        job = Jobs.objects.get(id=job_id)
        Applications.objects.create(applicant=user,
                                    job=job, )
        messages.success(request, "your application has been posted successfully")
        return redirect('candidate-home')

class ApplicationListView(ListView):
    model = Applications
    template_name = "candidate-applications.html"
    context_object_name = "applications"

    def get_queryset(self):
        return Applications.objects.filter(applicant=self.request.user)

