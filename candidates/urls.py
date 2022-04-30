from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('apply/', views.ApplyApi.as_view(), name='apply'),
    path('applications/', views.ApplicationsApi.as_view(), name='applications'),
    path('resume/', views.ApplicationsResumeApi.as_view(), name='resume'),
    path('resume-parse/', views.ApplicationsResumeParseApi.as_view(), name='resume-parse'),
    path('details/', views.CandidateDetailsApi.as_view(), name='details'),
    path('notes/', views.NoteApi.as_view(), name='notes'),
]

urlpatterns += static(settings.RESUME_URL, document_root=settings.RESUME_URL_ROOT)