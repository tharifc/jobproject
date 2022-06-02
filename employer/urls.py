from django.urls import path
from employer import views

urlpatterns = [
    path('home',views.EmployerHomeView.as_view(),name='emp-home'),
    path('jobs/add',views.AddJobView.as_view(),name='emp-addjob'),
    path('jobs/all',views.ListJobView.as_view(),name='all-jobs'),
    path('jobs/detail/<int:id>',views.JobdetailView.as_view(),name="job-details"),
    path('jobs/change/<int:id>',views.JobEditView.as_view(),name="job-edit"),
    path('job/remove/<int:id>',views.JobDeleteview.as_view(),name="job-delete"),
    path('users/accounts/signup',views.SignUpView.as_view(),name="signup"),
    path('users/accounts/login',views.SigninView.as_view(),name="signin"),
    path('users/accounts/logout',views.signout_view,name="signout"),
    path('password/change',views.ChangepasswordView.as_view(),name="change-password"),
    path('accounts/password/reset',views.PasswordRestView.as_view(),name="reset-password")
]