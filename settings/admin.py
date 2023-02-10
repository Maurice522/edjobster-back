from django.contrib import admin

# Register your models here.
from .models import Contacts, Location, Degree, Department, Designation, EmailCategory, EmailTemplate, Pipeline, PipelineStage, EmailFields , Webform
my_modules = [Location, Degree, Designation, EmailCategory, EmailTemplate, EmailFields , Webform]

class PipelineAdmin(admin.ModelAdmin):
    list_display=('id',)
    list_filter=('id',)

class ContactsAdmin(admin.ModelAdmin):
    list_display=('id','name', 'mobile', 'email', 'company_name')
    list_filter=('id',)
    def company_name(self, contacts):
        return contacts.company.name


admin.site.register(Department, PipelineAdmin)
admin.site.register(Pipeline, PipelineAdmin)
admin.site.register(PipelineStage, PipelineAdmin)
admin.site.register(Contacts, ContactsAdmin)

admin.site.register(my_modules)