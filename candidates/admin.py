from django.contrib import admin

# Register your models here.
from .models import Candidate , CandidateExperience , CandidateQualification
my_modules = [Candidate, CandidateExperience, CandidateQualification]

admin.site.register(my_modules)