from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('common/', include('common.urls')),
    path('settings/', include('settings.urls')),
]
