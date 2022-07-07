from django.shortcuts import render, redirect
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView, FormView, TemplateView
from django.urls import reverse_lazy
# Create your views here.
from employer.forms import JObForm
from employer.models import Jobs, CompanyProfile
from django.contrib.auth import authenticate, login, logout

from employer.forms import SignUpForm, LoginForm, CompanyprofileForm
# from django.contrib.auth.models import User
from employer.models import User, Applications
from django.contrib import messages
from django.utils.decorators import method_decorator
from employer.decorators import signin_required


@method_decorator(signin_required, name='dispatch')
class EmployerHomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "emp_home.html")


@method_decorator(signin_required, name='dispatch')
class AddJobView(CreateView):
    model = Jobs
    form_class = JObForm
    template_name = "emp-addjob.html"
    success_url = reverse_lazy("all-jobs")

    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)

    # def get(self,request):
    #     form=JObForm()
    #     return render(request,"emp-addjob.html",{"form":form})
    # def post(self,request):
    #     form=JObForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return render(request,"emp_home.html")
    #     else:
    #         return render(request, "emp-addjob.html", {"form": form})


@method_decorator(signin_required, name='dispatch')
class ListJobView(ListView):
    model = Jobs
    context_object_name = "jobs"
    template_name = "emp-listjob.html"

    def get_queryset(self):
        return Jobs.objects.filter(company=self.request.user)

    # def get(self,request):
    #     qs=Jobs.objects.filter(company=request.user)
    #     return render(request,"emp-listjob.html",{"jobs":qs})


@method_decorator(signin_required, name='dispatch')
class JobdetailView(DetailView):
    model = Jobs
    context_object_name = "job"
    template_name = "emp-jobdetail.html"
    pk_url_kwarg = "id"
    # def get(self,request,id):
    #     qs=Jobs.objects.get(id=id)
    #     return render(request,"emp-jobdetail.html",{"job":qs})


@method_decorator(signin_required, name='dispatch')
class JobEditView(UpdateView):
    model = Jobs
    form_class = JObForm
    template_name = "emp-jobedit.html"
    success_url = reverse_lazy("all-jobs")
    pk_url_kwarg = "id"
    # def get(self,request,id):
    #     qs=Jobs.objects.get(id=id)
    #     form=JObForm(instance=qs)
    #     return render(request,"emp-jobedit.html",{"form":form})
    #
    # def post(self,request,id):
    #     qs = Jobs.objects.get(id=id)
    #     form=JObForm(request.POST,instance=qs)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("all-jobs",{"form":form})


@method_decorator(signin_required, name='dispatch')
class JobDeleteview(DeleteView):
    template_name = "jobdelete.html"
    success_url = reverse_lazy("all-jobs")
    model = Jobs
    pk_url_kwarg = "id"

    # def get(self, request, id):
    #     qs = Jobs.objects.get(id=id)
    #     qs.delete()
    #     return redirect("all-jobs")


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "usersignup.html"

    success_url = reverse_lazy("signin")



class SigninView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            user = authenticate(request, username=uname, password=pwd)
            if user:
                login(request, user)
                if request.user.role == "employer":
                    return redirect("all-jobs")
                elif request.user.role == "candidate":
                    return render(request, "candidate-homeview.html")

                return redirect("all-jobs")
            else:
                return render(request, "login.html", {"form": form})


@signin_required
def signout_view(request, *args, **kwargs):
    logout(request)
    return redirect("signin")


@method_decorator(signin_required, name='dispatch')
class ChangepasswordView(TemplateView):
    template_name = "passwordchange.html"

    def post(self, request, *args, **kwargs):
        pwd = request.POST.get("pwd")
        uname = request.user
        user = authenticate(request, username=uname, password=pwd)
        if user:
            return redirect("reset-password")
        else:
            return render(request, self.template_name)


@method_decorator(signin_required, name='dispatch')
class PasswordRestView(TemplateView):
    template_name = "passwordreset.html"

    def post(self, request, *args, **kwargs):
        pwd1 = request.POST.get("pwd1")
        pwd2 = request.POST.get("pwd2")
        if pwd1 != pwd2:
            return render(request, self.template_name, {"msg": "invalid password"})
        else:
            u = User.objects.get(username=request.user)
            u.set_password(pwd1)
            u.save()
            return redirect("signin")


@method_decorator(signin_required, name='dispatch')
class CompanyProfileView(CreateView):
    model = CompanyProfile
    form_class = CompanyprofileForm
    template_name = "emp-addprofile.html"
    success_url = reverse_lazy("emp-home")

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


@method_decorator(signin_required, name='dispatch')
class EmpProfileView(TemplateView):
    template_name = "emp-viewprofile.html"


@method_decorator(signin_required, name='dispatch')
class EmpProfileEditView(UpdateView):
    model = CompanyProfile
    form_class = CompanyprofileForm
    template_name = "emp-editprofile.html"
    success_url = reverse_lazy("emp-viewprofile")
    pk_url_kwarg = "id"


@method_decorator(signin_required, name='dispatch')
class EmployeeListApplications(ListView):
    model = Applications
    context_object_name = "applications"
    template_name = "emp-applicationlist.html"

    def get_queryset(self):
        return Applications.objects.filter(job=self.kwargs.get("id")).exclude(status="cancelled")


@method_decorator(signin_required, name='dispatch')
class DetailApplicationsView(DetailView):
    model = Applications
    context_object_name = "applications"
    template_name = "emp-application-detail.html"
    pk_url_kwarg = "id"
