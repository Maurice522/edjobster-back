from django.db import models
from account.models import Company, Account
from django.contrib.postgres.fields import ArrayField
from common.models import Country, State, City, NoteType
from settings.models import Location, Designation, EmailTemplate
import uuid
from common.utils import generateFileName


class Candidate(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    company = models.ForeignKey(
        Company, default=None, null=False, verbose_name='Company', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)
    alt_email = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=False, blank=False)
    alt_mobile = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=250, null=False, blank=False)
    country = models.ForeignKey(
        Country, default=None, null=True, verbose_name='Country', on_delete=models.SET_NULL)
    state = models.ForeignKey(
        State, default=None, null=True, verbose_name='state', on_delete=models.SET_NULL)
    city = models.ForeignKey(
        City, default=None, null=True, verbose_name='pincode', on_delete=models.SET_NULL)
    pincode = models.CharField(max_length=6, null=False, blank=False)
    details = models.JSONField(null=True)
    skills = ArrayField(models.CharField(
        max_length=20, blank=True), default=None, null=True)
    experiance = models.CharField(max_length=20, null=True, blank=True)
    summary = models.TextField(max_length=1000, null=True, blank=True)
    overview = models.TextField(max_length=1000, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.company)+' '+str(self.first_name)[:20]+' '+str(self.last_name)[:20]

    class Meta:
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'

    @staticmethod
    def getById(id):
        if Candidate.objects.filter(id=id).exists():
            return Candidate.objects.get(id=id)
        return None

    @staticmethod
    def getForCompany(company):
        return Candidate.objects.filter(company=company).exists()

    @staticmethod
    def getAll():
        return Candidate.objects.all()


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
    def getById(id):
        if Note.objects.filter(id=id).exists():
            return Note.objects.get(id=id)
        return None

    @staticmethod
    def getForCompany(company):
        return Note.objects.filter(company=company).exists()

    @staticmethod
    def getAll():
        return Note.objects.all()


class Interview(models.Model):

    ON_SITE = 'S'
    ON_PHONE = 'P'
    ON_VIDEO = 'V'

    TYPE = [
        (ON_SITE, 'S'),
        (ON_PHONE, 'P'),
        (ON_VIDEO, 'V'),
    ]

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    candidate = models.ForeignKey(
        Candidate, default=None, null=False, verbose_name='Candidate', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE, default=ON_SITE)
    created_by = models.ForeignKey(
        Account, default=None, null=True, verbose_name='Added by', on_delete=models.SET_NULL)
    title = models.CharField(max_length=250, null=False, blank=False)
    time_start = models.DateTimeField(null=False, blank=False)
    time_end = models.DateTimeField(null=False, blank=False)
    location = models.ForeignKey(
        Location, default=None, null=True, verbose_name='Location', on_delete=models.SET_NULL)
    job = models.ForeignKey(
        Designation, default=None, null=True, verbose_name='Designation', on_delete=models.SET_NULL)
    email_template = models.ForeignKey(
        EmailTemplate, default=None, null=True, verbose_name='EmailTemplate', on_delete=models.SET_NULL)
    subject = models.TextField(max_length=500, null=False, blank=False)
    message = models.TextField(max_length=5000, null=False, blank=False)
    attachment = models.FileField(
        upload_to=generateFileName, default=None, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.candidate)+' '+str(self.title)[:20]

    class Meta:
        verbose_name = 'Interview'
        verbose_name_plural = 'Interviews'

    @staticmethod
    def getById(id):
        if Interview.objects.filter(id=id).exists():
            return Interview.objects.get(id=id)
        return None

    @staticmethod
    def getForCompany(company):
        return Interview.objects.filter(company=company).exists()

    @staticmethod
    def getAll():
        return Interview.objects.all()
