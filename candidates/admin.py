from django.contrib import admin

# Register your models here.
from .models import Candidate
my_modules = [Candidate]

admin.site.register(my_modules)