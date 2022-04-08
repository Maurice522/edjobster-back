from django.urls import path
from .import views

urlpatterns = [
    path('apply/', views.ApplyApi.as_view(), name='apply'),
    path('applications/', views.ApplicationsApi.as_view(), name='applications'),
    path('resume/', views.ApplicationsResumeApi.as_view(), name='resume'),
    path('details/', views.CandidateDetailsApi.as_view(), name='details'),
    path('notes/', views.NoteApi.as_view(), name='notes'),
]
