from django.shortcuts import render,redirect
from django.views.generic import View,ListView,CreateView,DetailView,UpdateView,DeleteView,FormView,TemplateView
from django.urls import reverse_lazy
# Create your views here.
from employer.forms import JObForm
from employer.models import Jobs
from django.contrib.auth import authenticate,login,logout

from employer.forms import SignUpForm,LoginForm
from django.contrib.auth.models import User


class EmployerHomeView(View):
    def get(self,request):
        return render(request,"emp_home.html")

class AddJobView(CreateView):
    model=Jobs
    form_class = JObForm
    template_name = "emp-addjob.html"
    success_url = reverse_lazy("all-jobs")

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



class ListJobView(ListView):
    model=Jobs
    context_object_name = "jobs"
    template_name = "emp-listjob.html"

    # def get(self,request):
    #     qs=Jobs.objects.all()
    #     return render(request,"emp-listjob.html",{"jobs":qs})
    #

class JobdetailView(DetailView):
    model=Jobs
    context_object_name = "job"
    template_name = "emp-jobdetail.html"
    pk_url_kwarg = "id"
    # def get(self,request,id):
    #     qs=Jobs.objects.get(id=id)
    #     return render(request,"emp-jobdetail.html",{"job":qs})

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
class JobDeleteview(DeleteView):
    template_name = "jobdelete.html"
    success_url = reverse_lazy("all-jobs")
    model=Jobs
    pk_url_kwarg = "id"

    # def get(self, request, id):
    #     qs = Jobs.objects.get(id=id)
    #     qs.delete()
    #     return redirect("all-jobs")

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "usersignup.html"

    success_url = reverse_lazy("all-jobs")

class SigninView(FormView):
    form_class = LoginForm
    template_name = "login.html"


    def post(self, request, *args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)

                return redirect("all-jobs")
            else:
                return  render(request,"login.html",{"form":form})



def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")


class ChangepasswordView(TemplateView):
    template_name = "passwordchange.html"
    def post(self,request,*args,**kwargs):
        pwd=request.POST.get("pwd")
        uname=request.user
        user=authenticate(request,username=uname,password=pwd)
        if user:
            return redirect("reset-password")
        else:
            return render(request,self.template_name)

class PasswordRestView(TemplateView):
    template_name = "passwordreset.html"
    def post(self,request,*args,**kwargs):
        pwd1=request.POST.get("pwd1")
        pwd2=request.POST.get("pwd2")
        if pwd1 != pwd2:
            return render(request,self.template_name,{"msg":"invalid password"})
        else:
            u=User.objects.get(username=request.user)
            u.set_password(pwd1)
            u.save()
            return redirect("signin")




