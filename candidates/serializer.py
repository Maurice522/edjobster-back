from account.serializer import AccountSerializer
from rest_framework import serializers
from .models import Candidate, Note
from common.encoder import encode
from common.serializer import NoteTypeSerializer
from django.conf import settings

class CandidateListSerializer(serializers.ModelSerializer):

    state_id = serializers.IntegerField(source='state.id')
    state_name = serializers.CharField(source='state.name')
    country_id = serializers.IntegerField(source='country.id')
    country_name = serializers.CharField(source='country.name')
    webform_id = serializers.SerializerMethodField()

    job_id = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    job_title = serializers.CharField(source='job.title')

    class Meta:
        model = Candidate
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'phone', 'mobile', 'email', 'email_alt',
                  'city', 'pincode', 'state_id', 'state_name', 'country_id', 'country_name',
                  'job_id', 'job_title', 'webform_id']

    def get_job_id(self, obj):
        return encode(obj.job.id)
    
    def get_id(self, obj):
        return encode(obj.id)  

    def get_webform_id(self, obj):
        if obj.webform:
            return obj.webform.id
        return None     

class CandidateDetailsSerializer(serializers.ModelSerializer):

    resume = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = '__all__'

    def get_resume(self, obj):
        if obj.resume:
            return settings.RESUME_FILE_URL+obj.resume.name[13:]
        return None              

class NoteSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()
    added_by = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'type', 'added_by', 'note', 'created', 'updated']

    def get_type(self, obj):
        if obj.type:
            return NoteTypeSerializer(obj.type).data
        return None           

    def get_added_by(self, obj):
        if obj.added_by:
            return AccountSerializer(obj.added_by).data
        return None    