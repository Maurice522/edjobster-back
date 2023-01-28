from django.contrib import admin

# Register your models here.
from .models import Location, Degree, Department, Designation, EmailCategory, EmailTemplate, Pipeline, PipelineStage, EmailFields , Webform
my_modules = [Location, Degree, Department, Designation, EmailCategory, EmailTemplate, Pipeline, PipelineStage, EmailFields , Webform]

admin.site.register(my_modules)