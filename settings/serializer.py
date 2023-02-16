from rest_framework import serializers
from .models import Contacts, Location, Department, Designation, Degree, Pipeline, PipelineStage, EmailCategory, EmailTemplate, EmailFields, Webform, Testimonials


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
                  'country_id', 'country_name', 'phone', 'email']


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

class PipelineStageSerializer(serializers.ModelSerializer):    
    class Meta:
        model = PipelineStage
        fields = "__all__"

    def get_pipeline(self, obj):
        if obj.pipeline:
            return PipelineSerializer(obj.pipeline).data
        return None 

class TestimonialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = "__all__"

    def get_testimonials(self, obj):
        if obj.testimonials:
            return TestimonialsSerializer(obj.testimonials).data
        return None 

class PipelineSerializer(serializers.ModelSerializer):
    stages = PipelineStageSerializer(many=True, read_only=True)
    class Meta:
        model = Pipeline
        fields = ['id', 'name', 'company','stages']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        stages = []
        for i in range(1, 8):
            stages.append(PipelineStageSerializer(getattr(instance, f"stage{i}")).data)
        representation['stages'] = stages
        return representation

class PipelineStagListSerializer(serializers.ModelSerializer):
    pipeline = serializers.SerializerMethodField()
    class Meta:
        model = PipelineStage
        fields = ['id', 'name', 'pipeline', 'status']
    def get_pipeline(self, obj):
        if obj.pipeline:
            return PipelineSerializer(obj.pipeline).data
        return None 

class EmailFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailFields
        fields = ['name', 'value']

class EmailCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailCategory
        fields = ['id', 'name']



class EmailTemplateSerializer(serializers.ModelSerializer):

    category_id = serializers.IntegerField(source='category.id')
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = EmailTemplate
        fields = ['id', 'subject', 'message', 'type', 'category_id', 'category_name', 'attachment', 'created' , 'updated']


class WebformListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Webform
        fields = ['id', 'name', 'created', 'updated']

                                                                  
class WebformDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Webform
        fields = ['id', 'name', 'form', 'created', 'updated']

class ContactsDataSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    class Meta:
        model = Contacts
        fields = ['id', 'name', 'email', 'mobile', 'company_name']

    def get_company_name(self, obj):
        if obj.company:
            return obj.company.name
        return None 