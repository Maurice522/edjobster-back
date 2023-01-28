from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('apply/', views.ApplyApi.as_view(), name='apply'),
    path('apply-job/', views.ApplyJobApi.as_view(), name='apply-job'),
    path('applications/', views.ApplicationsApi.as_view(), name='applications'),
    path('candidate/', views.CandidatesApi.as_view(), name='candidate'),
    path('resume/', views.ApplicationsResumeApi.as_view(), name='resume'),
    path('resume-parse/', views.ApplicationsResumeParseApi.as_view(), name='resume-parse'),
    path('details/', views.CandidateDetailsApi.as_view(), name='details'),
    path('notes/', views.NoteApi.as_view(), name='notes'),
    path('create-candidate/', views.CreateCandidateUsingResume.as_view(), name='create-candidate'),
    path('create-candidate-web/', views.CreateCandidateUsingWebForm.as_view(), name='create-candidate-web'),
    path('update-candidate-pipeline-status/',views.UpdateCandidatePipelineStatus.as_view(), name='update-candidate-pipeline-status')
]

urlpatterns += static(settings.RESUME_URL, document_root=settings.RESUME_URL_ROOT)