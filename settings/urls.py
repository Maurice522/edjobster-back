from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('location/', views.LocationsApi.as_view(), name='location'),
    path('department/', views.DepartmentApi.as_view(), name='department'),
    path('designation/', views.DesignationApi.as_view(), name='designation'),
    path('degree/', views.DegreeApi.as_view(), name='degree'),
    path('pipeline-stage/', views.PipelineStageApi.as_view(), name='pipeline-stage'),
    path('pipeline-details/', views.PipelineDetails.as_view(), name='pipeline-details'),
    path('pipeline/', views.PipelinesApi.as_view(), name='pipeline'),
    path('email-field/', views.EmailFieldApi.as_view(), name='email-field'),
    path('email-category/', views.EmailCategoryApi.as_view(), name='email-category'),
    path('email-template/', views.EmailTemplateApi.as_view(), name='email-template'),
]
