from account import serializer
from account.models import Account, Company
import interview
from job.models import Job
from common.utils import isValidUuid, getErrorResponse
from settings.models import EmailTemplate, Location
from .models import Candidate, Interview
from .serializer import  InterviewDetailsSerializer, InterviewListSerializer
from common.encoder import decode
import json

def scheduleInterview(request):

    data = request.data

    print('data', request.data)

    job_id = data.get('job_id', None)
    candidate_id = data.get('candidate_id', None)
    title = data.get('title', None)
    type = data.get('type', None)
    date = data.get('date', None)
    time_start = data.get('time_start', None)
    time_end = data.get('time_end', None)
    location_id = data.get('location_id', None)
    interviewers = data.get('interviewers', None)
    email_temp_id = data.get('email_temp_id', None)
    email_sub = data.get('email_sub', None)
    email_msg = data.get('email_msg', None)
    interview_id = data.get('id', None)
    send_email = data.get('send_email', None)

    if not job_id:
        return getErrorResponse('Job id required')

    job = Job.getById(decode(job_id))
    if not job:
        return getErrorResponse('Invalid Job')

    if not candidate_id:
        return getErrorResponse('Candidate required')
    
    candidate = Candidate.getById(decode(candidate_id), job)
    if not candidate:
        return getErrorResponse('Candidate not found')

    if not title:
        return getErrorResponse('title required')

    if not type or type not in Interview.INTEVIEW_TYPE_LIST:
        return getErrorResponse('Invalid interview type')

    if not date:
        return getErrorResponse('Interview date required')

    if not time_start:
        return getErrorResponse('Interview start time required')

    if not time_end:
        return getErrorResponse('Interview end time required')

    location = None
    company = Company.getByUser(request.user)

    if type == Interview.IN_PERSON: 
        if not location_id:
            return getErrorResponse('Interview location is required for In person interview')
        location = Location.getById(location_id, company)
        if not location:
            return getErrorResponse('Location not found')

    accounts = []
    if interviewers:
        try:
            interviewers = json.loads(interviewers)
            for user_id in interviewers:
                user = Account.getByIdAndCompany(user_id, company)
                if user:
                    accounts.append(user.account_id)            
        except: 
            getErrorResponse('Invalid interviewers data')


    if not email_temp_id:
        return getErrorResponse('Email template required')

    email_template = EmailTemplate.getById(email_temp_id, company)
    if not email_template:
        return getErrorResponse('Email template not found')       
    
    if not email_sub:
        return getErrorResponse('Email subject required')  

    if not email_msg:
        return getErrorResponse('Email message required')           
     
    interview = None

    if interview_id:
        interview = Interview.getById(interview_id, job)
        if not interview:
            return getErrorResponse('Interview not found')
    else:
        interview = Interview()

    if request.FILES != None:
        print("files")
        print(request.FILES)
        if 'document' in request.FILES:
            document = request.FILES['document']
            interview.document = document    

    interview.title = title
    interview.job = job
    interview.candidate = candidate
    interview.date = date
    interview.time_start = time_start
    interview.time_end = time_end
    interview.email_temp = email_template
    interview.email_sub = email_sub
    interview.email_msg = email_msg
    interview.location = location
    interview.interviewers = accounts
    interview.company = company

    interview.save()

    return {
        'code': 200,
        'msg': 'Interview scueduled sucessfully!'
    }            

def getInterviews(request):

    company = Company.getByUser(request.user)
    job_id = request.GET.get('job_id')
    candidate_id = request.GET.get('candidate_id')

    interviews = []

    if job_id:
        job = Job.getByIdAndCompany(decode(job_id), company)
        if not job:
            return getErrorResponse('Job not found')
        interviews = Interview.getByJob(job)
    elif candidate_id:
        candidate = Candidate.getByIdAndCompany(decode(candidate_id), company)     
        if not candidate:
            return getErrorResponse('Candidate not found')   
        interviews = Interview.getByCandidate(candidate)            
    else:
        interviews = Interview.getByCompany(company)      

    print('interviews', interviews)
    serializer = InterviewListSerializer(interviews, many=True)

    return {
        'code': 200,
        'list': serializer.data
    }

def delteInterview(request):

    company = Company.getByUser(request.user)
    interview_id = request.GET.get('id')

    interview = Interview.getByIdAndCompany(interview_id, company)

    if interview:
        interview.delete()

        return {
            'code': 200,
            'msg': 'Interview deleted successfully'
        }
    
    return getErrorResponse('Interview not found')

def interviewDetails(request):

    company = Company.getByUser(request.user)
    interview_id = request.GET.get('id')

    interview = Interview.getByIdAndCompany(interview_id, company)

    if not interview:
        return getErrorResponse('Interview not found')

    serializer = InterviewDetailsSerializer(interview)

    return {
        'code': 200,
        'data': serializer.data
    }

