from os import access
from account.models import Account
from common.models import Country, State
from rest_framework import serializers
from .models import Assesment, AssesmentCategory, AssesmentQuestion, Job
from common.encoder import encode
from settings.serializer import DepartmentSerializer, DegreeSerializer, PipelineSerializer
from settings.models import Degree, Department, Pipeline
from account.serializer import AccountSerializer
from common.serializer import CitySerializer, StateSerializer, CountrySerializer
from django.conf import settings

class AssesmentSerializer(serializers.ModelSerializer):
    categpry_id = serializers.IntegerField(source='category.id')
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Assesment
        fields = ['id',  'name', 'categpry_id', 'category_name', 'created', 'updated']


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



class JobListSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    owner_id = serializers.CharField(source='owner.account_id')
    state_id = serializers.IntegerField(source='state.id')
    state_name = serializers.CharField(source='state.name')
    country_id = serializers.IntegerField(source='country.id')
    country_name = serializers.CharField(source='country.name')
    department = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'title', 'owner_id', 'vacancies', 'department', 'type',
         'nature', 'exp_min', 'exp_max', 'salary_min', 'salary_max', 'salary_type', 'currency', 
         'city', 'state_id', 'state_name', 'country_id', 'country_name', 'created', 'updated', 'active']

    def get_id(self, obj):
        return encode(obj.id)

    def get_department(self, obj):
        if obj.department:
            department = Department.getById(obj.department, obj.company)
            if department:
                return department.name
        return None

class JobDetailsSerializer(serializers.ModelSerializer):

    department = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    assesment = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    document = serializers.SerializerMethodField()
    pipeline = serializers.SerializerMethodField()
    educations = serializers.SerializerMethodField()

    def get_id(self, obj):
        return encode(obj.id)
        
    class Meta:
        model = Job
        fields = [
             'id', 'title', 'vacancies', 'department', 'owner', 'assesment', 'members', 'type', 'nature', 'educations', 'speciality', 'description',
             'exp_min', 'exp_max', 'salary_min', 'salary_max', 'salary_type', 'currency', 'city', 'state', 'country', 'created_by', 'document', 
             'job_boards', 'pipeline', 'active', 'updated', 'created']

    def get_department(self, obj):
        if obj.department:
            department = Department.getById(obj.department, obj.company)
            if department:
                return DepartmentSerializer(department).data
        return None   

    def get_educations(self, obj):
        if obj.educations:
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
            return AssesmentSerializer(obj.assesment).data
        return None            

    def get_document(self, obj):
        if obj.document:
            return settings.JOB_DOC_FILE_URL+obj.document.name[11:]
        return None           

    def get_state(self, obj):
        if obj.state:
            return StateSerializer(obj.state).data
        return None  

    def get_country(self, obj):
        if obj.country:
            return CountrySerializer(obj.country).data
        return None          

    def get_pipeline(self, obj):
        if obj.pipeline:
            pipeline = Pipeline.getById(obj.pipeline, obj.company)
            if pipeline:
                return PipelineSerializer(pipeline).data
        return None          