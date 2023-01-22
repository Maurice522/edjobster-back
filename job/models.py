from django.db import models
from account.models import Account, Company
from django.contrib.postgres.fields import ArrayField
from common.models import Country, State, City
from common.utils import generateFileName
from settings.models import Department, Pipeline, Webform

class AssesmentCategory(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, default=None, null=False, verbose_name='Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.company.name)+' '+str(self.name)[:20]

    class Meta:
        verbose_name = 'Assesment Category'
        verbose_name_plural = 'Assesment Categories'

    @staticmethod
    def getById(id, company):
        if AssesmentCategory.objects.filter(company=company, id=id).exists():
            return AssesmentCategory.objects.get(id=id)
        return None
    
    @staticmethod
    def getByName(name, company):
        return AssesmentCategory.objects.filter(company=company, name=name).exists()
           

    @staticmethod
    def getForCompany(company):
        return AssesmentCategory.objects.filter(company=company)

    @staticmethod
    def getAll():
        return AssesmentCategory.objects.all()

class Assesment(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, default=None, null=False, verbose_name='Company', on_delete=models.CASCADE)
    category = models.ForeignKey(AssesmentCategory, default=None, null=False, verbose_name='Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    created_by =  models.ForeignKey(Account, default=None, null=True, verbose_name='Created By', on_delete=models.SET_NULL)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.company.name)+' '+str(self.name)[:20]

    class Meta:
        verbose_name = 'Assesment'
        verbose_name_plural = 'Assesments'

    @staticmethod
    def getById(id, company):
        if Assesment.objects.filter(company=company, id=id).exists():
            return Assesment.objects.get(id=id)
        return None
    
    @staticmethod
    def getByAssessmentId(id):
        if Assesment.objects.filter(id=id).exists():
            return Assesment.objects.get(id=id)
        return None
    
    @staticmethod
    def getByName(name, company):
        return Assesment.objects.filter(company=company, name=name).exists()

    @staticmethod
    def getByNameAndCategory(name, category):
        return Assesment.objects.filter(category=category, name=name).exists()           

    @staticmethod
    def getForCompany(company):
        return Assesment.objects.filter(company=company)

    @staticmethod
    def getAll():
        return Assesment.objects.all()

class AssesmentQuestion(models.Model):
    
    RADIO = 'R'
    CHECK = 'C'
    SELECT = 'S'
    TEXT = 'T'

    TYPES = [RADIO, CHECK, SELECT, TEXT]

    TYPE = [
        (RADIO, 'Radio'),
        (CHECK, 'Check'),
        (SELECT, 'Select'),
        (TEXT, 'Text'),
    ] 

    id = models.AutoField(primary_key=True)
    assesment =  models.ForeignKey(Assesment, default=False, null=False, verbose_name='Assesment', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE, default=RADIO)
    question = models.TextField(max_length=500, null=False, blank=False)
    options = ArrayField(models.CharField(max_length=100), blank=True)
    answer = models.CharField(max_length=100)
    marks = models.IntegerField(default=1)
    text = models.TextField(max_length=1000, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.assesment.company.name)+' '+str(self.question)[:40]

    class Meta:
        verbose_name = 'AssesmentQuestion'
        verbose_name_plural = 'AssesmentQuestions'

    @staticmethod
    def getById(id, assesment):
        if AssesmentQuestion.objects.filter(assesment=assesment, id=id).exists():
            return AssesmentQuestion.objects.get(id=id)
        return None

    @staticmethod
    def getByCompany(id, company):
        if AssesmentQuestion.objects.filter(id=id).exists():
            question = AssesmentQuestion.objects.get(id=id)
            if question.assesment.company.id == company.id:
                return question
        return None        

    @staticmethod
    def getAll():
        return AssesmentQuestion.objects.all()

    @staticmethod
    def getForAssesment(assesment):
        return AssesmentQuestion.objects.filter(assesment=assesment)



class Job(models.Model):
    
    REMOTE = 'R'
    PHYSICAL = 'P'
    NATURES = [REMOTE, PHYSICAL]
    NATURE = [
        (PHYSICAL, 'Physical'),
        (REMOTE, 'Remote')
    ]

    FULL_TIME = 'F'
    PART_TIME = 'P'
    TYPES = [FULL_TIME, PART_TIME]
    TYPE = [
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time')
    ]

    DAILY = 'D'
    WEEKLY = 'W'
    MONTHY = 'M'
    YEARLY = 'Y'

    PAY_TYPES = [DAILY, WEEKLY, MONTHY, YEARLY]
    PAY_TYPE = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHY, 'Monthly'),
        (YEARLY, 'Yearly'),
    ]

    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, default=None, null=True, verbose_name='Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    vacancies = models.IntegerField(default=1, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    # department = models.ForeignKey(Department, default=None, null=True, verbose_name='Assesment', on_delete=models.SET_NULL)
    # owner = models.ForeignKey(Account, related_name='Owner', default=None, null=True, verbose_name='Owner', on_delete=models.SET_NULL)
    owner = models.CharField(max_length=50, null=True, blank=True)
    # assesment = models.ForeignKey(Assesment, default=None, null=True, verbose_name='Assesment', on_delete=models.SET_NULL)
    assesment =  models.CharField(max_length=50, null=True, blank=True)
    members = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    type = models.CharField(max_length=1, choices=TYPE, default=FULL_TIME)
    nature = models.CharField(max_length=1, choices=NATURE, default=PHYSICAL)
    educations = ArrayField(models.IntegerField(default=0), null=True, default=None, blank=True)
    speciality = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(max_length=3000, null=True, blank=True)
    exp_min = models.IntegerField(default=0)
    exp_max = models.IntegerField(default=0)
    salary_min = models.CharField(max_length=50, null=True, blank=True, default='')
    salary_max = models.CharField(max_length=50, null=True, blank=True, default='')
    salary_type = models.CharField(max_length=1, choices=PAY_TYPE, default=MONTHY)
    currency = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    # state = models.ForeignKey(State, default=None, null=True, verbose_name='State', on_delete=models.SET_NULL)
    state =  models.CharField(max_length=50, null=True, blank=True)
    # country = models.ForeignKey(Country, default=None, null=True, verbose_name='Country', on_delete=models.SET_NULL)
    country =  models.CharField(max_length=50, null=True, blank=True)
    # created_by =  models.ForeignKey(Account, related_name='createdby', default=None, null=True, verbose_name='Created By', on_delete=models.SET_NULL)
    created_by =  models.CharField(max_length=50, null=True, blank=True)
    document = models.FileField(upload_to='media/jobs/', default=None, null=True, blank=True)  
    job_boards = ArrayField(models.CharField(max_length=50), blank=True)
    pipeline = models.IntegerField(default=0, null=True, blank=True)
    # pipeline = models.ForeignKey(Pipeline,related_name='webform_id',null=True,on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    webform = models.ForeignKey(Webform,related_name='webform_id',null=True,on_delete=models.CASCADE)
    # webform_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.company)+' '+str(self.title)[:20]

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    @staticmethod
    def getById(id):
        if Job.objects.filter(id=id).exists():
            return Job.objects.get(id=id)
        return None

    @staticmethod
    def getByIdAndCompany(id, company):
        if Job.objects.filter(company=company, id=id).exists():
            return Job.objects.get(id=id)
        return None

    @staticmethod
    def getAll():
        return Job.objects.all()

    @staticmethod
    def getForCompany(company):
        return Job.objects.filter(company=company)



