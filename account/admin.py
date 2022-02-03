from django.contrib import admin

from .models import Account, Company
# Register your models here.

admin.site.register([Account, Company])
