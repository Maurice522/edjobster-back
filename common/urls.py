from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('data/', views.DataApi.as_view(), name='data'),
    path('countires/', views.CountryApi.as_view(), name='countires'),
    path('states/', views.StatesApi.as_view(), name='states'),
    path('cities/', views.CitiesApi.as_view(), name='cities'),
    path('note-types/', views.NotesApi.as_view(), name='note-types'),
]
