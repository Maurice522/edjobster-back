from email.policy import default
from django.db import models
from common.models import Country, State, NoteType
from django.db.models import Q
from job.models import Job, Account
from django.contrib.postgres.fields import JSONField

class Candidate(models.Model):

    SINGLE = 'S'
    MARRIED = 'M'

    MARITAL_STATUS_LIST = [SINGLE, MARRIED]

    MARITAL_STATUS = [
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
    ]

    SSC = 'SSC'
    HSC = 'HSC'
    DIPLOMA = 'DIP'
    GRADUATION = 'UG'
    POST_GRADUATION = 'PG'

    QUALIFICATION_LIST = [SSC, HSC, DIPLOMA, GRADUATION, POST_GRADUATION]

    QUALIFICATIONS = [
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
    ]

    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, default=None, null=False, verbose_name='Job', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    email_alt = models.CharField(max_length=100, null=True, blank=True)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS, default=SINGLE)
    date_of_birth = models.DateField(default=None, null=True, blank=True)
    age = models.IntegerField(default=0)
    last_applied = models.DateTimeField(default=None, null=True, blank=True)

    street = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.ForeignKey(State, default=None, null=True, verbose_name='State', on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, default=None, null=True, verbose_name='Country', on_delete=models.SET_NULL)
  
    exp_years = models.IntegerField(default=0)
    exp_months = models.IntegerField(default=0)
    qualification = models.CharField(max_length=3, choices=QUALIFICATIONS, default=GRADUATION)
    cur_job = models.CharField(max_length=50, null=True, blank=True)
    cur_employer = models.CharField(max_length=50, null=True, blank=True)
    certifications = models.CharField(max_length=50, null=True, blank=True)
    fun_area = models.CharField(max_length=50, null=True, blank=True)
    subjects = models.CharField(max_length=50, null=True, blank=True)
    skills = models.CharField(max_length=250, null=True, blank=True)

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
    def getById(id, job):
        if Candidate.objects.filter(job=job, id=id).exists():
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
    def getByJob(job):
        return Candidate.objects.filter(job=job)

    @staticmethod
    def getByEmail(job, email):
        return Candidate.objects.filter(job=job).filter(email=email)

    @staticmethod
    def getByPhone(job, mobile):
        return Candidate.objects.filter(job=job).filter(mobile=mobile)


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