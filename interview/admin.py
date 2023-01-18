from django.contrib import admin
from .models import Interview
# Register your models here.
class InterviewAdmin(admin.ModelAdmin):
    list_display=('id','job','candidate','company')
    list_filter=('id',)
admin.site.register(Interview,InterviewAdmin)