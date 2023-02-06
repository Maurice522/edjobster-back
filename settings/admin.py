from django.contrib import admin

# Register your models here.
from .models import Location, Degree, Department, Designation, EmailCategory, EmailTemplate, Pipeline, PipelineStage, EmailFields , Webform
my_modules = [Location, Degree, Designation, EmailCategory, EmailTemplate, EmailFields , Webform]

class PipelineAdmin(admin.ModelAdmin):
    list_display=('id',)
    list_filter=('id',)

admin.site.register(Department, PipelineAdmin)
admin.site.register(Pipeline, PipelineAdmin)
admin.site.register(PipelineStage, PipelineAdmin)
# admin.site.register(Location, PipelineAdmin)

admin.site.register(my_modules)