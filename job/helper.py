from collections import namedtuple
import email
from math import degrees
import re
from unicodedata import category
from venv import create
from account import serializer
from account.models import Account, Company, TokenEmailVerification, TokenResetPassword
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import authenticate
from common.encoder import decode
from common.utils import isValidUuid, getErrorResponse
from common.models import Country, State, City
import json

from settings.models import Degree, Department, Pipeline
from .models import AssesmentCategory, Assesment, AssesmentQuestion, Job
from .serializer import AssesmentSerializer, AssesmentCategorySerializer, AssesmentQuestionListSerializer, AssesmentQuestionDetailsSerializer, JobListSerializer, JobDetailsSerializer


#ASSESMENT
def getAssesmentCategories(request):

    company = Company.getByUser(request.user)
    assesments = AssesmentCategory.getForCompany(company=company)

    serializer = AssesmentCategorySerializer(assesments, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def saveAssesmentCategory(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    name = data.get('name', None)   

    if not name:
        return getErrorResponse('Category name required')

    id = data.get('id', None)

    if id:
        category = AssesmentCategory.getById(id, company)
        if not category:
            return getErrorResponse( 'Assesment category not found')

        if category.name != name and AssesmentCategory.getByName(name=name, company=company):
            return getErrorResponse('Assesment category with name '+name+' already exists.')
    else:
        if AssesmentCategory.getByName(name=name, company=company):
            return getErrorResponse('Assesment category with name '+name+' already exists.')

        category = AssesmentCategory()   
        category.company = company
    
    category.name = name
    category.save()

    return getAssesmentCategories(request)

def deleteAssesmentCategory(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        category = AssesmentCategory.getById(id, company)
        if not category:
            return getErrorResponse('Assesment category not found')

        category.delete()
        return {
            'code': 200,
            'msg': 'Assesment category deleted succesfully!',
            'data': getAssesmentCategories(request)['data']
        }

    return getErrorResponse('Invalid request')

def getAssesments(request):

    company = Company.getByUser(request.user)
    assesments = Assesment.getForCompany(company=company)

    serializer = AssesmentSerializer(assesments, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def saveAssesment(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    name = data.get('name', None)   
    cat_id = data.get('category', None)   

    if not name or not cat_id:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }
    print(cat_id, company)

    category = AssesmentCategory.getById(cat_id, company)
    if not category:
        return getErrorResponse( 'Assesment category not found')

    id = data.get('id', None)

    if id:
        assesment = Assesment.getById(id, company)
        if not assesment:
            return getErrorResponse('Assesment not found')

        if assesment.name != name and Assesment.getByNameAndCategory(name=name, category=category):
            return getErrorResponse('Assesment with name '+name+' already exists.')
    else:
        if Assesment.getByNameAndCategory(name=name, category=category):
            return getErrorResponse('Assesment with name '+name+' already exists.')

        assesment = Assesment()   
        assesment.company = company

    assesment.name = name
    assesment.category = category
    assesment.save()

    return getAssesments(request)

def deleteAssesment(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        assesment = Assesment.getById(id, company)
        if not assesment:
            return getErrorResponse('Assesment not found')

        assesment.delete()
        return {
            'code': 200,
            'msg': 'Assesment deleted succesfully!',
            'data': getAssesments(request)['data']
        }

    return getErrorResponse('Invalid request') 


def getAssesmentDetails(request):

    company = Company.getByUser(request.user)
    id = request.GET.get('id')

    assesment = Assesment.getById(id=id, company=company)
    if not assesment:
        return getErrorResponse('Assesment not found')

    questions = AssesmentQuestion.getForAssesment(assesment=assesment)

    assesmentSerializer = AssesmentSerializer(assesment, many=False)
    questionSerializer = AssesmentQuestionDetailsSerializer(questions, many=True)

    return {
        'code': 200,
        'assesment': assesmentSerializer.data,
        'questions': questionSerializer.data
    }    

def getAssesmentQuestions(assesment):
    questions = AssesmentQuestion.getForAssesment(assesment=assesment)
    questionSerializer = AssesmentQuestionDetailsSerializer(questions, many=True)
    return {
        'code': 200,
        'questions': questionSerializer.data
    }  


def saveAssesmentQuestion(request):

    company = Company.getByUser(request.user)
    id = request.GET.get('id')

    assesment = Assesment.getById(id=id, company=company)
    if not assesment:
        return getErrorResponse( 'Assesment not found')
    
    data = request.data    
    type = data.get('type', None)   
    question_text = data.get('question', None)   

    if not question_text:
        return getErrorResponse('question required')
    
    if not type or type not in AssesmentQuestion.TYPES:
        return getErrorResponse('Invalid type')

    id = data.get('id', None)
        
    if id:
        question = AssesmentQuestion.getById(id, assesment)
        if not question:
            return getErrorResponse('Assesment question not found')
    else:
        question = AssesmentQuestion()   
        question.assesment = assesment

    if not type or not question or type not in AssesmentQuestion.TYPES:
        return getErrorResponse('Invalid request')

    if type == AssesmentQuestion.RADIO or type == AssesmentQuestion.SELECT:
        marks = data.get('marks', None)   
        answer = data.get('answer', None)   
        options = data.get('options', None)

        if not marks:
            return getErrorResponse('marks required')

        if not answer:
            return getErrorResponse('answer required')

        if not options or not isinstance(options, list):
            return getErrorResponse('options required')

        question.marks = marks
        question.answer = answer
        question.options = options
    
    elif type == AssesmentQuestion.CHECK:
        options = data.get('options', None)

        if not options or not isinstance(options, list):
            return getErrorResponse('options required')

        question.options = options  
    else:
        question.marks = 0
        question.answer = ""
        question.options = []

    question.type = type
    question.question = question_text
    question.save()

    return getAssesmentQuestions(assesment=assesment)

def deleteAssesmentQuestion(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        question = AssesmentQuestion.getByCompany(id, company)
        if not question:
            return getErrorResponse('Question not found')

        assesment = question.assesment
        question.delete()
        return {
            'code': 200,
            'msg': 'question deleted succesfully!',
            'data': getAssesmentQuestions(assesment)['questions']
        }

    return getErrorResponse('Invalid request')

#JOBS
def getJobs(request):

    company = Company.getByUser(request.user)
    jobs = Job.getForCompany(company=company)
    serializer = JobListSerializer(jobs, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def getJobDetails(request):

    company = Company.getByUser(request.user)
    id = request.GET.get('id', None)

    if not id:
        return getErrorResponse('Invalid request')

    job = Job.getByIdAndCompany(decode(id), company)
    if not job:
        return getErrorResponse('Job not found')

    serializer = JobDetailsSerializer(job, many=False)
    data = serializer.data

    data['owner_id'] = job.owner.accountId 
    data['owner'] = job.owner.first_name+' '+job.owner.last_name 
    data['state_id'] = job.state.id
    data['state'] = job.state.name 
    data['country_id'] = job.country.id
    data['country'] = job.country.name 
    data['created_by'] = job.created_by.first_name+' '+job.created_by.last_name 
    if job.document:
        data['document'] = job.document.name 
    data['job_boards'] = job.job_boards 

    members = []
    for member in job.members:
        account = Account.getById(member, company)
        if account:
            members.append(
                {
                    'id': member,
                    'name': account.first_name+' '+account.last_name
                }
            )

    data['members'] = members 
    pipeline = Pipeline.getById(job.pipeline, company)
    if pipeline:
        data['pipeline_id'] = pipeline.id 
        data['pipeline'] = pipeline.name 

    return {
        'code': 200,
        'data': data
    }
    
def saveJob(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    

    id = data.get('id', None)

    if id:
        job = Job.getByIdAndCompany(decode(id), company)
        if not category:
            return getErrorResponse( 'Job not found')
    else:
        job = Job()   
        job.company = company
    
    data = request.data    
    
    print(data)

    title = data.get('title', None)   
    vacancies = data.get('vacancies', None)   
    department_id = data.get('department', None)   
    owner_id = data.get('owner', None)   
    assesment_id = data.get('assesment', None)   
    member_ids = data.get('members', None)   
    type = data.get('type', None)   
    nature = data.get('nature', None)   
    education = data.get('education', None)   
    speciality = data.get('speciality', None)   
    description = data.get('description', None)   
    exp_min = data.get('exp_min', None)   
    exp_max = data.get('exp_max', None)   
    salary_min = data.get('salary_min', None)   
    salary_max = data.get('salary_max', None)   
    salary_type = data.get('salary_type', None)   
    currency = data.get('currency', None)   
    city = data.get('city', None)   
    state_id = data.get('state', None)   
    job_board_ids = data.get('job_boards', None)   
    pipeline_id = data.get('pipeline', None)   
    active = data.get('active', None)   
    
    if not title:
        return getErrorResponse('Job title required')
    if not vacancies or int(vacancies) != vacancies:
        return getErrorResponse('Vacancies required')
    if not department_id:
        return getErrorResponse('Department required')
    
    department = Department.getById(department_id, company)
    if not department:
        return getErrorResponse('Department not found')
    
    if not owner_id:
        return getErrorResponse('Owner required')
    
    owner = Account.getById(owner_id)
    if not owner:
        return getErrorResponse('Owner not found')    

    assesment = None
    if assesment_id:
        assesment = Assesment.getById(assesment_id, company)
        if not assesment:
            return getErrorResponse('Assesment not found')

    jobMembers = []
    if member_ids:
        if not isinstance(member_ids, list):
            return getErrorResponse('Invalid members')
        for member in member_ids:
            user = Account.getById(member)
            if user:
                jobMembers.append(user.accountId)
    
    if not type or not type in Job.TYPES:
        return getErrorResponse('invalid job type')

    if not nature or not nature in Job.NATURES:
        return getErrorResponse('invalid job nature')

    if not education or not isinstance(education, list):
        return getErrorResponse('Invalid education list')
    
    degrees = []
    for e in education:
        d = Degree.getById(e, company)
        if d:
            degrees.append(d.name)

    if not speciality:
        return getErrorResponse('Speciality required')

    if not description:
        return getErrorResponse('Job description required')
    
    if int(exp_min) != exp_min:
        return getErrorResponse('Minimum experience required')
    
    if int(exp_max) != exp_max:
        return getErrorResponse('Maximum experience required')

    if not salary_min:
        return getErrorResponse('Minimum salary required')

    if not salary_max:
        return getErrorResponse('Maximum salary required')
    
    if not salary_type or not salary_type in Job.PAY_TYPES:
        return getErrorResponse('invalid Pay type')

    if not currency:
        return getErrorResponse('Currency required')

    if not city:
        return getErrorResponse('City required')    

    if not state_id:
        return getErrorResponse('State required')

    state = State.getById(state_id)
    if not state:
        return getErrorResponse('State not found')     

    #ADD JOB BOARDS ONCE READY
    if not pipeline_id:
        return getErrorResponse('Pipeline required')

    pipeline = Pipeline.getById(pipeline_id, company)
    if not pipeline:
        return getErrorResponse('Pipeline not found')          

    if not active or int(active) not in [0 , 1]:
        return getErrorResponse('Active status required') 

    if active == 1:
        active = True
    else:
        active = False

    job.title = title
    job.vacancies = vacancies
    job.department = department.id
    job.owner = owner
    job.assesment = assesment
    members = []
    for member in members:
        members.append(member.id)
    
    job.members = members
    job.type = type
    job.nature = nature
    job.education = degrees
    job.description = description
    job.speciality = speciality
    job.exp_min = exp_min
    job.exp_max = exp_max
    job.salary_min = salary_min
    job.salary_max = salary_max
    job.salary_type = salary_type
    job.currency = currency
    job.city = city
    job.state = state
    job.country = state.country
    job.created_by = request.user
    job.pipeline = pipeline.id
    job.active = active
    job.job_boards = job_board_ids

    if request.FILES != None:
        print("files")
        print(request.FILES)
        if 'document' in request.FILES:
            document = request.FILES['document']
            job.document = document    

    job.save()

    return {
        'code': 200,
        'msg': 'Job saved successfully'
    }

def deleteJob(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        job = Job.getByIdAndCompany(decode(id), company)
        if not job:
            return getErrorResponse('Job not found')

        job.delete()
        return {
            'code': 200,
            'msg': 'Job deleted succesfully!',
            'data': getJobs(request)['data']
        }

    return getErrorResponse('Invalid request')    