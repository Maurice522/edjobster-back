from django.db import models
from django.contrib.postgres.fields import ArrayField
from common.models import Country, State
from django.db.models import Q
from job.models import Job
from settings.models import Location, EmailTemplate

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
    marital_status = models.CharField(max_length=3, choices=MARITAL_STATUS, default=SINGLE)
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
    qualification = models.CharField(max_length=1, choices=QUALIFICATIONS, default=GRADUATION)
    cur_job = models.CharField(max_length=50, null=True, blank=True)
    cur_employer = models.CharField(max_length=50, null=True, blank=True)
    certifications = models.CharField(max_length=50, null=True, blank=True)
    fun_area = models.CharField(max_length=50, null=True, blank=True)
    subjects = models.CharField(max_length=50, null=True, blank=True)
    skills = models.CharField(max_length=250, null=True, blank=True)

    resume = models.FileField(upload_to='media/resume/', default=None, null=True, blank=True)  

    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.job.title)[20]+' '+str(self.email)[:30]

    class Meta:
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'

    @staticmethod
    def getById(id, job):
        if Candidate.objects.filter(job=job, id=id).exists():
            return Candidate.objects.get(id=id)
        return None
    
    @staticmethod
    def getByJob(job):
        return Candidate.objects.filter(job=job)

    @staticmethod
    def getByEmail(job, email):
        return Candidate.objects.filter(job=job).filter(Q(email=email) | Q(email_alt=email))

    @staticmethod
    def getByPhone(job, phone):
        return Candidate.objects.filter(job=job).filter(Q(mobile=phone) | Q(phone=phone))


class Interview(models.Model):

    IN_PERSON = 'IP'
    PHONE_CALL = 'PC'
    VIDEO_CALL = 'VC'

    INTEVIEW_TYPE_LIST = [IN_PERSON, PHONE_CALL, VIDEO_CALL]

    INTEVIEW_TYPES = [
        (IN_PERSON, 'In Person'),
        (PHONE_CALL, 'Telephonic'),
        (VIDEO_CALL, 'Video'),
    ]

    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, default=None, null=False, verbose_name='Job', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, default=None, null=False, verbose_name='Candidate', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=2, choices=INTEVIEW_TYPES, default=IN_PERSON)
    date = models.DateField(default=None, null=True, blank=True)
    time_start = models.TimeField(default=None, null=True, blank=True)
    time_end = models.TimeField(default=None, null=True, blank=True)
    location = models.ForeignKey(Location, default=None, null=False, verbose_name='Location', on_delete=models.CASCADE)
    interviewers = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    email_temp = models.ForeignKey(EmailTemplate, default=None, null=False, verbose_name='Email Template', on_delete=models.CASCADE)
    email_sub = models.CharField(max_length=250, null=True, blank=True)
    email_msg = models.TextField(max_length=5000, null=True, blank=True)
    document = models.FileField(upload_to='media/interview/', default=None, null=True, blank=True)  
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.job.title)[20]+' '+str(self.title)[:20]

    class Meta:
        verbose_name = 'Interview'
        verbose_name_plural = 'Interviews'

    @staticmethod
    def getById(id, job):
        if Interview.objects.filter(job=job, id=id).exists():
            return Interview.objects.get(id=id)
        return None
    
    @staticmethod
    def getByJob(job):
        return Interview.objects.filter(job=job)

    @staticmethod
    def getByCandidate(candidate):
        return Candidate.objects.filter(candidate=candidate)

