from rest_framework import serializers
from .models import Assesment, AssesmentCategory, AssesmentQuestion, Job

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

    owner_id = serializers.CharField(source='owner.accountId')
    state_id = serializers.IntegerField(source='state.id')
    state_name = serializers.CharField(source='state.name')
    country_id = serializers.IntegerField(source='country.id')
    country_name = serializers.CharField(source='country.name')

    class Meta:
        model = Job
        fields = ['id', 'title', 'owner_id', 'vacancies', 'department', 'type',
         'nature', 'exp_min', 'exp_max', 'salary_min', 'salary_max', 'salary_type', 'currency', 
         'city', 'state_id', 'state_name', 'country_id', 'country_name', 'created', 'updated', 'active']


class JobDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'