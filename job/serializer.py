from dataclasses import fields
from os import access
from account.models import Account, Company
from common.models import Country, State
from rest_framework import serializers
from .models import Assesment, AssesmentCategory, AssesmentQuestion, Job, JobNotes
from common.encoder import encode
from settings.serializer import DepartmentSerializer, DegreeSerializer, LocationSerializer, PipelineSerializer, WebformDataSerializer
from settings.models import Degree, Department, Location, Pipeline, Webform
from account.serializer import AccountSerializer
from common.serializer import CitySerializer, StateSerializer, CountrySerializer
from django.conf import settings

class AssesmentSerializer(serializers.ModelSerializer):
    # category = serializers.CharField()

    class Meta:
        model = Assesment
        fields ='__all__'


class AssesmentCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = AssesmentCategory
        fields = ['id', 'name']

class AssesmentQuestionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssesmentQuestion
        fields = ['id', 'type', 'question', 'options', 'marks', 'created', 'updated' ]

class AssesmentQuestionDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssesmentQuestion
        fields = ['id', 'type', 'question', 'options', 'marks', 'answer', 'created', 'updated' ]        


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class JobListSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()
    # state_name = serializers.CharField(source='state')
    # country_name = serializers.CharField(source='country')
    location = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'title', 'owner_id', 'vacancies', 'department', 'type',
         'nature', 'exp_min', 'exp_max', 'salary_min', 'salary_max', 'salary_type', 'currency', 'location', 
         'created', 'updated', 'active', 'webform_id']

    def get_id(self, obj):
        return encode(obj.id)

    def get_owner_id(self, obj):
        if obj.owner:
            return obj.owner
        return None

    def get_department(self, obj):
        if obj.department:
            department = Department.getById(obj.department, obj.company)
            if department:
                return department.name
        return None

    def get_location(self, obj):
        if obj.location:
            return LocationSerializer(obj.location).data
        return None

class JobDetailsSerializer(serializers.ModelSerializer):

    department = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    assesment = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    # # state = serializers.SerializerMethodField()
    # # country = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    document = serializers.SerializerMethodField()
    pipeline = serializers.SerializerMethodField()
    educations = serializers.SerializerMethodField()
    webform = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id
        
    class Meta:
        model = Job
        fields = [
             'id', 'title', 'vacancies', 'department', 'owner', 'assesment', 'members', 'type', 'nature', 'educations', 'speciality', 'description',
             'exp_min', 'exp_max', 'salary_min', 'salary_max', 'salary_type', 'currency', 'location', 'created_by', 'document', 
             'job_boards', 'pipeline', 'active', 'updated', 'created', 'webform']

    def get_department(self, obj):
        if obj.department:
            print(f"The department is {obj.department}, of company {obj.company}")
            department = Department.getById(obj.department, obj.company)
            if department:
                return DepartmentSerializer(department).data
        return None   

    def get_educations(self, obj):
        if obj.educations:
            print(f"The Education is {obj.educations}, of company {obj.company}")
            educations = Degree.getByIds(obj.educations, obj.company)
            if educations:
                return DegreeSerializer(educations, many=True).data
        return []                     

    def get_owner(self, obj):
        if obj.owner:
            return AccountSerializer(obj.owner).data
        return None    

    def get_members(self, obj):
        if obj.members:
            members = []
            for memberId in obj.members:
                account = Account.getById(memberId)
                if account:
                    members.append(AccountSerializer(account).data)
            return members
        return None  

    def get_assesment(self, obj):
        if obj.assesment:
            assess = Assesment.getByAssessmentId(obj.assesment)
            return AssesmentSerializer(assess).data
        return None            

    def get_document(self, obj):
        if obj.document:
            return settings.JOB_DOC_FILE_URL+obj.document.name[11:]
        return None           

    # def get_state(self, obj):
    #     if obj.state:
    #         return StateSerializer(obj.state).data
    #     return None  

    # def get_country(self, obj):
    #     if obj.country:
    #         return CountrySerializer(obj.country).data
    #     return None          

    def get_pipeline(self, obj):
        if obj.pipeline:
            print(f"One of the member is {obj.pipeline}")
            pipeline = Pipeline.getById(obj.pipeline, obj.company)
            if pipeline:
                return PipelineSerializer(pipeline).data
        return None  

    def get_webform(self, obj):
        if obj.webform:
            print(f"Webform is {obj.webform}")
            return WebformDataSerializer(obj.webform).data
        return None        

    def get_location(self, obj):
        if obj.location:
            print(f"Location is {obj.location}")
            return LocationSerializer(obj.location).data
        return None

class JobNotesSerializer(serializers.ModelSerializer):
    job_id = serializers.CharField(source='job.id')
    added_by = serializers.SerializerMethodField()

    class Meta:
        model = JobNotes
        fields = ['id', 'job_id', 'added_by', 'note', 'created', 'updated']       

    def get_added_by(self, obj):
        if obj.added_by:
            return AccountSerializer(obj.added_by).data
        return None    