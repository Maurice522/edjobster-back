from rest_framework import serializers
from .models import Location, Department, Designation, Degree, Pipeline, PipelineField, PipelineStage, EmailCategory, EmailTemplate, EmailFields


class LocationSerializer(serializers.ModelSerializer):
    city_id = serializers.IntegerField(source='city.id')
    city_name = serializers.CharField(source='city.name')
    state_id = serializers.IntegerField(source='state.id')
    state_name = serializers.CharField(source='state.name')
    country_id = serializers.IntegerField(source='country.id')
    country_name = serializers.CharField(source='country.name')

    class Meta:
        model = Location
        fields = ['id',  'name', 'address', 'pincode', 'loc_lat', 'loc_lon', 'city_id', 'city_name', 'state_id', 'state_name',
                  'country_id', 'country_name']


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'name']

class DesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = ['id', 'name']



class DegreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Degree
        fields = ['id', 'name']



class PipelineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pipeline
        fields = ['id', 'name', 'fields', 'created' , 'updated']



class PipelineFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = PipelineField
        fields = ['id', 'name']



class PipelineStageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PipelineStage
        fields = ['id', 'name']

class EmailFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailCategory
        fields = ['id', 'name', 'value']

class EmailCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailCategory
        fields = ['id', 'name']



class EmailTemplateSerializer(serializers.ModelSerializer):

    category_id = serializers.IntegerField(source='category.id')
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = EmailTemplate
        fields = ['id', 'name', 'subject', 'message', 'type', 'category_id', 'category_name', 'attachment', 'created' , 'updated']

                                                 