from email.policy import default
from django.db import models
from common.models import Country, State, NoteType
from django.db.models import Q
from job.models import Job, Account
from django.contrib.postgres.fields import JSONField

from settings.models import Webform

class Candidate(models.Model):

    SINGLE = 'Single'
    MARRIED = 'Married'

    MARITAL_STATUS_LIST = [SINGLE, MARRIED]

    MARITAL_STATUS = [
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
    ]

    MALE = 'Male'
    FEMALE = 'Female'

    GENDER_LIST = [MALE, FEMALE]

    GENDER_OPTIONS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    SSC = 'SSC'
    HSC = 'HSC'
    DIPLOMA = 'DIPLOMA'
    GRADUATION = 'UG'
    POST_GRADUATION = 'PG'

    QUALIFICATION_LIST = [SSC, HSC, DIPLOMA, GRADUATION, POST_GRADUATION]

    QUALIFICATIONS = [
        (SSC, 'SSC'),
        (HSC, 'HSC'),
        (DIPLOMA, 'DIPLOMA'),
        (GRADUATION, 'UG'),
        (POST_GRADUATION, 'PG'),
    ]

    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, default=None, null=True, verbose_name='Job', on_delete=models.SET_NULL)
    webform = models.ForeignKey(Webform, default=None, null=True, verbose_name='webform', on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    email_alt = models.CharField(max_length=100, null=True, blank=True)
    marital_status = models.CharField(max_length=10,  null=True, blank=True, choices=MARITAL_STATUS, default=SINGLE)
    gender = models.CharField(max_length=6,  null=True, blank=True, choices=GENDER_OPTIONS, default=MALE)
    date_of_birth = models.DateField(default=None, null=True, blank=True)
    age = models.IntegerField(default=0)
    last_applied = models.DateTimeField(default=None, null=True, blank=True)

    street = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    # state = models.CharField(max_length=10, null=True, blank=True)
    # country = models.CharField(max_length=50, null=True, blank=True)
    state = models.ForeignKey(State, default=None, null=True, verbose_name='State', on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, default=None, null=True, verbose_name='Country', on_delete=models.SET_NULL)
  
    exp_years = models.IntegerField(null=True,blank=True)
    exp_months = models.IntegerField(null=True,blank=True)

    # Addition of admission_date and graduation_date
    admission_date = models.DateField(default=None,null=True, blank=True)
    graduation_date = models.DateField(default=None,null=True, blank=True)

    # qualification = models.CharField(max_length=10, choices=QUALIFICATIONS, default=GRADUATION)
    qualification = models.CharField(max_length=10, choices=QUALIFICATIONS, default=GRADUATION, blank = True, null = True)
    cur_job = models.CharField(max_length=100, null=True, blank=True)
    cur_employer = models.CharField(max_length=100, null=True, blank=True)
    pipeline_stage_status = models.CharField(max_length=100, null=True, blank=True)
    pipeline_stage = models.CharField(max_length=100, null=True, blank=True)
    certifications = models.TextField(null=True, blank=True)
    fun_area = models.TextField(null=True, blank=True)
    subjects = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

    resume = models.FileField(upload_to='media/resume/', default=None, null=True, blank=True)  
    resume_parse_data = JSONField(null=True, default=None)

    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.job)+' '+str(self.email)[:30]

    class Meta:
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'

    @staticmethod
    def getById(id):
        if Candidate.objects.filter(id=id).exists():
            return Candidate.objects.get(id=id)
        return None

    @staticmethod
    def getByIdAndCompany(id, company):
        if Candidate.objects.filter(id=id).exists():
            candidate = Candidate.objects.get(id=id)
            if candidate.job.company.id == company.id:
                return candidate
        return None

    @staticmethod
    def getByCompany(company):
        return Candidate.objects.filter(job__company=company)

    @staticmethod
    def getByJob(job):
        return Candidate.objects.filter(job=job)

    @staticmethod
    def getByEmail(job, email):
        return Candidate.objects.filter(job=job).filter(email=email)

    @staticmethod
    def getByPhone(job, mobile):
        return Candidate.objects.filter(job=job).filter(mobile=mobile)

class CandidateExperience(models.Model):

    id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(Candidate, null=True, verbose_name='candidate', on_delete=models.CASCADE)
    employer = models.CharField(max_length=100, null=True, blank=True)
    jobProfile = models.CharField(max_length=100, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(max_length=30, null=True, blank=True)
    end_date = models.DateField(max_length=30, null=True, blank=True)
    jobDescription = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.employer)+' exp'

class CandidateQualification(models.Model):

    id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(Candidate, null=True, verbose_name='candidate', on_delete=models.CASCADE)
    institute_name = models.TextField(max_length=300, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(max_length=30, null=True, blank=True)
    end_date = models.DateField(max_length=30, null=True, blank=True)
    grade = models.CharField(max_length=30, null=True, blank=True)
    gradeType = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.id)+' '+str(self.candidate)


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(
        Candidate, default=None, null=False, verbose_name='Candidate', on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        Account, default=None, null=True, verbose_name='Added by', on_delete=models.SET_NULL)
    type = models.ForeignKey(
        NoteType, default=None, null=True, verbose_name='Type', on_delete=models.SET_NULL)
    note = models.TextField(max_length=1000, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.candidate)+' '+str(self.added_by)[:20]

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    @staticmethod
    def getById(id, candidate):
        if Note.objects.filter(id=id, candidate=candidate).exists():
            return Note.objects.get(id=id)
        return None

    @staticmethod
    def getForCandidate(candidate):
        return Note.objects.filter(candidate=candidate)

    @staticmethod
    def getByIdAndCompany(id, company):
        if Note.objects.filter(id=id).exists():
            note = Note.objects.get(id=id)
            if note.candidate.job.company.id == company.id:
                return note
        return None

    @staticmethod
    def getAll():
        return Note.objects.all()

        

class ResumeFiles(models.Model):
    id = models.AutoField(primary_key=True)
    resume = models.FileField(upload_to='media/temp/', default=None, null=True, blank=True)  
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.candidate)+' '+str(self.added_by)[:20]

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'