from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('job/', views.JobApi.as_view(), name='job'),
    path('job-details/', views.JobDetailsApi.as_view(), name='job-details'),
    path('assesment/', views.AssesmentApi.as_view(), name='assesment'),
    path('assesment-question/', views.AssesmentQuestionApi.as_view(), name='assesment-question'),
    path('assesment-category/', views.AssesmentCategoryApi.as_view(), name='assesment-category'),
    path('board/', views.BoardApi.as_view(), name='board'),
]
