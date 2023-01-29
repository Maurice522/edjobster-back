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
    path('pipeline-detalis/<int:id>/', views.PipelinesDetailApi.as_view(), name='pipeline_details'),
    path('pipeline-stage-delete/<int:id>/', views.PipelineStageDelete.as_view(), name='pipeline-stage-delete'),
    path('pipeline-update-stage/<int:id>/', views.PipelineStageUpdate.as_view(), name='pipeline_details'),
    path('pipeline-detalis-by-company/<int:id>/', views.PipelinesDetailCompanyApi.as_view(), name='pipeline-update-stage'),
    path('pipeline/', views.PipelinesApi.as_view(), name='pipeline'),
    path('email-field/', views.EmailFieldApi.as_view(), name='email-field'),
    path('email-category/', views.EmailCategoryApi.as_view(), name='email-category'),
    path('email-template/', views.EmailTemplateApi.as_view(), name='email-template'),
    path('webform/', views.WebformApi.as_view(), name='webform'),
    path('webform-fields/', views.WebformFieldsApi.as_view(), name='webform-fields'),
]
