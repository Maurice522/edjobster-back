from rest_framework import serializers
from .models import Interview


class InterviewListSerializer(serializers.ModelSerializer):

    candidate_id = serializers.IntegerField(source='candidate.id')
    candidate_name = serializers.CharField(source='candidate.name')
    job_id = serializers.IntegerField(source='job.id')
    job_title = serializers.CharField(source='job.title')

    class Meta:
        model = Interview
        fields = ['id', 'title', 'type', 'date', 'time_start', 'time_end', 
                  'job_id', 'job_title', 'candidate_id', 'candidate_name']


class InterviewDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interview
        fields = '__all__'