from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q
from account.models import Company
from job.models import Job
from settings.models import Location, EmailTemplate
from candidates.models import Candidate

# Create your models here.
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
    company = models.ForeignKey(Company, default=None, null=False, verbose_name='Company', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, default=None, null=False, verbose_name='Candidate', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=2, choices=INTEVIEW_TYPES, default=IN_PERSON)
    date = models.DateField(default=None, null=True, blank=True)
    time_start = models.TimeField(default=None, null=True, blank=True)
    time_end = models.TimeField(default=None, null=True, blank=True)
    location = models.ForeignKey(Location, default=None, null=True, verbose_name='Location', on_delete=models.SET_NULL)
    interviewers = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    email_temp = models.ForeignKey(EmailTemplate, default=None, null=True, verbose_name='Email Template', on_delete=models.SET_NULL)
    email_sub = models.CharField(max_length=250, null=True, blank=True)
    email_msg = models.TextField(max_length=5000, null=True, blank=True)
    document = models.FileField(upload_to='media/interview/', default=None, null=True, blank=True)  
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.job.title)[:20]+' '+str(self.title)[:20]

    class Meta:
        verbose_name = 'Interview'
        verbose_name_plural = 'Interviews'

    @staticmethod
    def getById(id, job):
        if Interview.objects.filter(job=job, id=id).exists():
            return Interview.objects.get(id=id)
        return None
    
    @staticmethod
    def getByIdAndCompany(id, company):
        if Interview.objects.filter(company=company, id=id).exists():
            return Interview.objects.get(id=id)
        return None

    @staticmethod
    def getByJob(job):
        return Interview.objects.filter(job=job)

    @staticmethod
    def getByCandidate(candidate):
        return Interview.objects.filter(candidate=candidate)

    @staticmethod
    def getByCompany(company):
        return Interview.objects.filter(company=company)