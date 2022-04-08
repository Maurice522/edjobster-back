from account.models import Account
from candidates.models import Candidate
from rest_framework import serializers
from .models import Interview
from job.serializer import JobListSerializer
from candidates.serializer import CandidateListSerializer
from account.serializer import AccountSerializer


class InterviewListSerializer(serializers.ModelSerializer):

    job = serializers.SerializerMethodField()
    candidate = serializers.SerializerMethodField()

    class Meta:
        model = Interview
        fields = ['id', 'title', 'type', 'date', 'time_start', 'time_end', 
                  'job', 'candidate']

    def get_job(self, obj):
        if obj.job:
            return {
                'id': obj.job.id,
                'title': obj.job.title,
            }
        return None      

    def get_candidate(self, obj):
        if obj.candidate:
            return {
                'id': obj.candidate.id,
                'first_name': obj.candidate.first_name,
                'middle_name': obj.candidate.middle_name,
                'last_name': obj.candidate.last_name,
                'email': obj.candidate.email,
                'mobile': obj.candidate.mobile,
                'exp_years': obj.candidate.exp_years,
                'exp_months': obj.candidate.exp_months,
            }
        return None     

class InterviewDetailsSerializer(serializers.ModelSerializer):

    job = serializers.SerializerMethodField()
    candidate = serializers.SerializerMethodField()
    interviewers = serializers.SerializerMethodField()

    def get_job(self, obj):
        if obj.job:
            return JobListSerializer(obj.job).data
        return None      

    def get_candidate(self, obj):
        if obj.candidate:
            return CandidateListSerializer(obj.candidate).data
        return None               

    def get_interviewers(self, obj):
        if obj.interviewers:
            interviewers = []
            for user in obj.interviewers:
                account = Account.getById(user)
                if account:
                    interviewers.append(AccountSerializer(account).data)
            return interviewers
        return None    

    class Meta:
        model = Interview
        fields = '__all__'