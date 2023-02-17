import email
from django.db import models
from account.models import Company
from django.contrib.postgres.fields import ArrayField
from common.models import Country, State, City
from common.utils import generateFileName
from django.contrib.postgres.fields import JSONField


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(
        Company, default=None, null=False, verbose_name='Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(
        Country, default=None, null=True, verbose_name='Country', on_delete=models.SET_NULL)
    state = models.ForeignKey(
        State, default=None, null=True, verbose_name='State', on_delete=models.SET_NULL)
    city = models.ForeignKey(
        City, default=None, null=True, verbose_name='City', on_delete=models.SET_NULL)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    loc_lat = models.CharField(max_length=20, null=True, blank=True)
    loc_lon = models.CharField(max_length=20, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.company)+' '+str(self.name)[:20]

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    @staticmethod
    def getById(id, company):
        if Location.objects.filter(company=company, id=id).exists():
            return Location.objects.get(id=id)
        return None

    @staticmethod
    def getForCompany(company):
        return Location.objects.filter(company=company)

    @staticmethod
    def getAll():
        return Location.objects.all()


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(
        Company, default=None, null=False, verbose_name='Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.company)+' '+str(self.name)[:20]

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    @staticmethod
    def getByDid(id):
        if Department.objects.filter(id=id).exists():
            return Department.objects.get(id=id)
        return None
    

    @staticmethod
    def getById(id, company):
        if Department.objects.filter(company=company, id=id).exists():
            return Department.objects.get(id=id)
        return None
    
    @staticmethod
    def getByName(name, company):
        return Department.objects.filter(company=company, name=name).exists()
           

    @staticmethod
    def getForCompany(company):
        return Department.objects.filter(company=company)

    @staticmethod
    def getAll():
        return Department.objects.all()


class Designation(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(
        Company, default=None, null=True, verbose_name='Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.company)+' '+str(self.name)[:20]

    class Meta:
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'

    @staticmethod
    def getByDid(id):
        if Designation.objects.filter(id=id).exists():
            return Designation.objects.get(id=id)
        return None

    @staticmethod
    def getById(id, company):
        if Designation.objects.filter(company=company, id=id).exists():
            return Designation.objects.get(id=id)
        return None

    @staticmethod
    def getByName(name, company):
        return Designation.objects.filter(company=company, name=name).exists()

    @staticmethod
    def getAll():
        return Designation.objects.all()

    @staticmethod
    def getForCompany(company):
        return Designation.objects.filter(company=company)


class Degree(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(
        Company, default=None, null=True, verbose_name='Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.company)+' '+str(self.name)[:20]

    class Meta:
        verbose_name = 'Degree'
        verbose_name_plural = 'Degrees'

    @staticmethod
    def getById(id, company):
        if Degree.objects.filter(id=id, company=company).exists():
            return Degree.objects.get(id=id)
        return None

    @staticmethod
    def getByIds(ids, company):
        # Old code for multiple degrees
        # return Degree.objects.filter(company=company, id__in=ids)
        # New code for single degree as of now
        return Degree.objects.filter(company=company, id=ids)

    @staticmethod
    def getByName(name, company):
        return Degree.objects.filter(company=company, name=name).exists()

    @staticmethod
    def getAll():
        return Degree.objects.all()

    @staticmethod
    def getForCompany(company):
        return Degree.objects.filter(company=company)


# Pipeline
class PipelineStage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    status = ArrayField(models.CharField(max_length=50), blank=True, default=list) 
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)[:20]

    class Meta:
        verbose_name = 'PipelineStage'
        verbose_name_plural = 'PipelineStages'

    @staticmethod
    def getById(id):
        if PipelineStage.objects.filter(id=id).exists():
            return PipelineStage.objects.get(id=id)
        return None

    @staticmethod
    def getByName(name, company):
        return Department.objects.filter(company=company, name=name).exists()

    @staticmethod
    def getAll():
        return PipelineStage.objects.all()

    @staticmethod
    def getForCompany(company):
        return PipelineStage.objects.filter(company=company)

class Pipeline(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(
        Company, default=None, null=True, verbose_name='Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True,)
    created = models.DateTimeField(auto_now_add=True)
    
    stage1 = models.ForeignKey(PipelineStage, blank=True, null=True, verbose_name='Pipeline Stage 1', related_name='pipeline_stages_1', on_delete=models.CASCADE)
    stage2 = models.ForeignKey(PipelineStage, blank=True, null=True, verbose_name='Pipeline Stage 2', related_name='pipeline_stages_2', on_delete=models.CASCADE)
    stage3 = models.ForeignKey(PipelineStage, blank=True, null=True, verbose_name='Pipeline Stage 3', related_name='pipeline_stages_3', on_delete=models.CASCADE)
    stage4 = models.ForeignKey(PipelineStage, blank=True, null=True, verbose_name='Pipeline Stage 4', related_name='pipeline_stages_4', on_delete=models.CASCADE)
    stage5 = models.ForeignKey(PipelineStage, blank=True, null=True, verbose_name='Pipeline Stage 5', related_name='pipeline_stages_5', on_delete=models.CASCADE)
    stage6 = models.ForeignKey(PipelineStage, blank=True, null=True, verbose_name='Pipeline Stage 6', related_name='pipeline_stages_6', on_delete=models.CASCADE)
    stage7 = models.ForeignKey(PipelineStage, blank=True, null=True, verbose_name='Pipeline Stage 7', related_name='pipeline_stages_7', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.company)+' '+str(self.name)[:20]

    class Meta:
        verbose_name = 'Pipeline'
        verbose_name_plural = 'Pipelines'

    @staticmethod
    def getByName(name, company):
        return Department.objects.filter(company=company, name=name).exists()

    @staticmethod
    def getById(id, company):
        if Pipeline.objects.filter(company=company, id=id).exists():
            return Pipeline.objects.get(id=id)
        return None

    @staticmethod
    def getAll():
        return Pipeline.objects.all()

    @staticmethod
    def getForCompany(company):
        return Pipeline.objects.filter(company=company)

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Pipeline)
def create_pipeline_stages(sender, instance, created, **kwargs):
    if created:
        stage_list = ["Associated-Screeening", "Applied", "Shortlisted", "Interview", "Offered", "Hired", "Onboarded"]
        i = 1
        for stage in stage_list:
            stage_instance = PipelineStage.objects.create(name=stage)
            print(stage_instance)
            cmd =  f"instance.stage{i} = stage_instance"
            exec(cmd)
            i+=1
            instance.save()    

# Email
class EmailCategory(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(
        Company, default=None, null=False, verbose_name='Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.company)+' '+str(self.name)[:20]

    class Meta:
        verbose_name = 'EmailCategory'
        verbose_name_plural = 'EmailCategories'

    @staticmethod
    def getById(id, company):
        if EmailCategory.objects.filter(company=company, id=id).exists():
            return EmailCategory.objects.get(id=id)
        return None

    @staticmethod
    def getByName(name, company):
        return EmailCategory.objects.filter(company=company, name=name).exists()

    @staticmethod
    def getForCompany(company):
        return EmailCategory.objects.filter(company=company)

    @staticmethod
    def getAll():
        return EmailCategory.objects.all()


class EmailTemplate(models.Model):

    CANDIDATE = 'C'
    INTERNAL = 'I'
    EMAIL_TYPES = [CANDIDATE, INTERNAL]
    TYPE = [
        (CANDIDATE, 'Candidate'),
        (INTERNAL, 'Internal')
    ]

    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(
        Company, null=False, verbose_name='Company', on_delete=models.CASCADE)
    category = models.ForeignKey(
        EmailCategory, null=False, verbose_name='Category', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE, default=CANDIDATE)
    subject = models.TextField(max_length=500, null=False, blank=False)
    message = models.TextField(max_length=5000, null=False, blank=False)
    attachment = models.FileField(
        upload_to=generateFileName, default=None, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.company)+' '+str(self.subject)

    class Meta:
        verbose_name = 'EmailTemplate'
        verbose_name_plural = 'EmailTemplates'

    @staticmethod
    def getById(id, company):
        if EmailTemplate.objects.filter(company=company, id=id).exists():
            return EmailTemplate.objects.get(id=id)
        return None

    @staticmethod
    def getByName(subject, company):
        return EmailTemplate.objects.filter(company=company, subject=subject).exists()

    @staticmethod
    def getForCompany(company):
        return EmailTemplate.objects.filter(company=company)

    @staticmethod
    def getAll():
        return EmailTemplate.objects.all()


class EmailFields(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)+' '+str(self.value)[:20]

    class Meta:
        verbose_name = 'EmailField'
        verbose_name_plural = 'EmailFields'

    @staticmethod
    def getByName(name, company):
        return EmailFields.objects.filter(company=company, name=name).exists()

    @staticmethod
    def getById(id):
        if EmailFields.objects.filter(id=id).exists():
            return EmailFields.objects.get(id=id)
        return None

    @staticmethod
    def getForCompany(company):
        return EmailFields.objects.filter(company=company)

    @staticmethod
    def getAll():
        return EmailFields.objects.all()        



class Webform(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, default=None, null=True, verbose_name='Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    form = JSONField(null=True, default=None)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = 'Webform'
        verbose_name_plural = 'Webforms'

    @staticmethod
    def getByName(name, company):
        return Webform.objects.filter(company=company, name=name).exists()

    @staticmethod
    def getById(id, company):
        if Webform.objects.filter(id=id, company=company).exists():
            return Webform.objects.get(id=id)
        return None
    
    @staticmethod
    def getByWebformId(id):
        if Webform.objects.filter(id=id).exists():
            return Webform.objects.get(id=id)
        return None

    @staticmethod
    def getForCompany(company):
        return Webform.objects.filter(company=company)

    @staticmethod
    def getAll():
        return Webform.objects.all()    


class Contacts(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, default=None, null=True, verbose_name='Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    @staticmethod
    def getByName(name, company):
        return Contacts.objects.filter(company=company, name=name).exists()

    @staticmethod
    def getById(id, company):
        if Contacts.objects.filter(id=id, company=company).exists():
            return Contacts.objects.get(id=id)
        return None
    
    @staticmethod
    def getByContactId(id):
        if Contacts.objects.filter(id=id).exists():
            return Contacts.objects.get(id=id)
        return None

    @staticmethod
    def getByEmailId(email, company):
        return Contacts.objects.filter(company=company, email=email).exists()

    @staticmethod
    def getByMobile(mobile, company):
        return Contacts.objects.filter(company=company, mobile=mobile).exists()     

    @staticmethod
    def getForCompany(company):
        return Contacts.objects.filter(company=company)

    @staticmethod
    def getAll():
        return Contacts.objects.all()         
    
class Testimonials(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True,blank=True)
    designation = models.CharField(max_length=100,null=True,blank=True)
    testimonials = models.TextField(max_length=2000, null=True, blank=True)
    Profile_picture = models.ImageField(upload_to='media/users/photos', default=None, null=True, blank=True)

    def __str__(self):
        return  f"{str(self.company)} {str(self.name)}"

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
