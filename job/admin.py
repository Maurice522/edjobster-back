from django.contrib import admin

# Register your models here.
from .models import Job, Assesment, AssesmentQuestion, AssesmentCategory, JobNotes
my_modules = [Job, Assesment, AssesmentQuestion, AssesmentCategory, JobNotes]

class JobAdmin(admin.ModelAdmin):
    list_display=('id','company','vacancies')
    list_filter=('id',)
admin.site.register(Job,JobAdmin)

class AssessmentAdmin(admin.ModelAdmin):
    list_display=('id','company','category','name')
    list_filter=('id',)
admin.site.register(Assesment,AssessmentAdmin)

class AssesmentQuestionAdmin(admin.ModelAdmin):
    list_display=('id','created','type')
    list_filter=('id',)
admin.site.register(AssesmentQuestion,AssesmentQuestionAdmin)

class AssesmentCategoryAdmin(admin.ModelAdmin):
    list_display=('id','company','name')
    list_filter=('id',)
admin.site.register(AssesmentCategory,AssesmentCategoryAdmin)

class JobNotesAdmin(admin.ModelAdmin):
    list_display=('id','added_by')
    list_filter=('id',)
admin.site.register(JobNotes,JobNotesAdmin)
