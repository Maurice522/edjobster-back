from django.contrib import admin

# Register your models here.
from .models import Location, Degree, Department, Designation, EmailCategory, EmailTemplate, Pipeline, PipelineStage
my_modules = [Location, Degree, Department, Designation, EmailCategory, EmailTemplate, Pipeline, PipelineStage]

admin.site.register(my_modules)
