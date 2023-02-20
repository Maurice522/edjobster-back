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
    path('notes/<int:pk>', views.DetailNoteApi.as_view(), name='notes-details'),
    path('notes-update/<int:pk>', views.NotesUpdateApi.as_view(), name='notes-update'),
    path('create-candidate/', views.CreateCandidateUsingResume.as_view(), name='create-candidate'),
    path('create-candidate-web/', views.CreateCandidateUsingWebForm.as_view(), name='create-candidate-web'),
    path('candidate-stats/', views.CandidateStats.as_view(), name='candidate-stats'),
    path('update-candidate-pipeline-status/',views.UpdateCandidatePipelineStatus.as_view(), name='update-candidate-pipeline-status'),

    path('applicant-get/<str:lookup_field>/<str:lookup_value>/', views.ApplicationWebFormByJobApi.as_view(), name='applicant-get'),
    path('applicant-update/<int:pk>', views.ApplicationWebFormUpdateApi.as_view(), name='applicant-update'),
    path('applicant-delete/<int:pk>', views.ApplicationWebFormDeleteApi.as_view(), name='applicant-delete'),
    path('applicant/', views.ApplicationWebFormCreateApi.as_view(), name='applicant-create'),

    path('update-candidate-status/', views.UpdateCandidateStatusApi.as_view(), name='update-candidate-status'),
    path('assign-job/',  views.AssignJob.as_view(), name='assign-job'),
]

urlpatterns += static(settings.RESUME_URL, document_root=settings.RESUME_URL_ROOT)