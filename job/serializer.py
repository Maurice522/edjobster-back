from rest_framework import serializers
from .models import Assesment, AssesmentCategory, AssesmentQuestion, Job
from common.encoder import encode
from settings.serializer import DepartmentSerializer, Department

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
                return {
                    'id': department.id,
                    'name': department.name                
                }
        return None

class JobDetailsSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return encode(obj.id)
        
    class Meta:
        model = Job
        fields = '__all__'