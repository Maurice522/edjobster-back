from rest_framework import serializers
from .models import Assesment, AssesmentCategory, AssesmentQuestion, Job

class Assesment(serializers.ModelSerializer):
    categpry_id = serializers.IntegerField(source='categpry.id')
    category_name = serializers.CharField(source='categpry.name')

    class Meta:
        model = Assesment
        fields = ['id',  'name', 'categpry_id', 'category_name', 'created', 'updated']


class AssesmentCategory(serializers.ModelSerializer):

    class Meta:
        model = AssesmentCategory
        fields = ['id', 'name']

class AssesmentQuestion(serializers.ModelSerializer):

    class Meta:
        model = AssesmentQuestion
        fields = ['id', 'type', 'question', 'options', ]



class JobList(serializers.ModelSerializer):

    owner_id = serializers.IntegerField(source='owner.id')
    owner_name = serializers.CharField(source='owner.name')
    state_id = serializers.IntegerField(source='state.id')
    state_name = serializers.CharField(source='state.name')
    country_id = serializers.IntegerField(source='country.id')
    country_name = serializers.CharField(source='country.name')

    class Meta:
        model = Job
        fields = ['id', 'title', 'owner_id', 'owner_name', 'vacancies', 'department', 'type',
         'nature', 'exp_min', 'exp_max', 'salary_min', 'salary_max', 'salary_type', 'currency', 
         'city', 'state_id', 'state_name', 'country_id', 'country_name', 'created', 'updated', 'active']


