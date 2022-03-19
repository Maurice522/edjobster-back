from django.contrib import admin

from .models import Account, Company, TokenEmailVerification
# Register your models here.

admin.site.register([Account, TokenEmailVerification, Company])
