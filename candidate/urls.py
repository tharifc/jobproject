from django.urls import path
from candidate import views

urlpatterns=[
  path('home',views.CandidateHomeView.as_view(),name='candidate-home'),
  path('add/profile',views.CandidateProfileView.as_view(),name='cand-view-profile'),
  path('edit/profile',views.CandidateProfileEditView.as_view(),name='candidate-edit-profile'),
  path('detail/profile',views.CandidateProfileDetailView.as_view(),name='candidate-detail-profile'),
  path('job-list',views.CandidateJobListView.as_view(),name="candidate-job-list"),
  path('job-detail/<int:id>',views.CandidateJobDetailView.as_view(),name="candidate-detail-job"),
  path('job/apply-now/<int:id>',views.apply_now,name="applynow"),
  path('all/applications',views.ApplicationListView.as_view(),name="candidate-applications")

]