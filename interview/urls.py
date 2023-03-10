from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('schedule/', views.InterviewApi.as_view(), name='schedule'),
    path('details/', views.InterviewDetailsApi.as_view(), name='details'),
    path('interview-latest/', views.LatestInterviewDetailsApi.as_view(), name='interview-latest'),
]
