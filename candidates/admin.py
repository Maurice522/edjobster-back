from django.contrib import admin

# Register your models here.
from .models import Candidate , CandidateExperience , CandidateQualification, ApplicantWebForm
my_modules = [Candidate, CandidateExperience, CandidateQualification, ApplicantWebForm]
#Registering Candidate on admin panel
class CandidateAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','id','job','created',)
    list_filter=('id',)
admin.site.register(Candidate,CandidateAdmin)

class ApplicantWebFormAdmin(admin.ModelAdmin):
    list_display=('id',)
    list_filter=('id',)
admin.site.register(ApplicantWebForm,ApplicantWebFormAdmin)

#register candidate according to experience
class CandidateExperienceAdmin(admin.ModelAdmin):
    list_display=('id','candidate','employer','jobProfile')
    list_filter=('id',)
admin.site.register(CandidateExperience,CandidateExperienceAdmin)

class CandidateQualificationAdmin(admin.ModelAdmin):
    list_display=('id','candidate','institute_name','grade')
    list_filter=('id',)
admin.site.register(CandidateQualification,CandidateQualificationAdmin)