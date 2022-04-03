from django.contrib import admin

# Register your models here.
from .models import Job, Assesment, AssesmentQuestion, AssesmentCategory
my_modules = [Job, Assesment, AssesmentQuestion, AssesmentCategory]

admin.site.register(my_modules)