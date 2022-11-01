from collections import namedtuple
import email
from math import degrees
import re
from unicodedata import category
from venv import create
from account import serializer
from account.models import Account, Company, TokenEmailVerification, TokenResetPassword
import candidates
import job
from job.models import Job
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import authenticate
from common.utils import isValidUuid, getErrorResponse
from common.models import Country, NoteType, State, City
import json
from settings.models import Degree, Department, Pipeline, Webform
from .models import Candidate, CandidateExperience, CandidateQualification, Note, ResumeFiles
from .serializer import CandidateExperienceSerializer, CandidateListSerializer, CandidateDetailsSerializer, CandidateQualificationSerializer, NoteSerializer
from common.encoder import decode
from django.utils.dateparse import parse_date
from common.utils import parseDate
from datetime import date, datetime    
from django.conf import settings
import requests
from django.core.paginator import Paginator
from django.db import transaction

PAGE_SIZE = 30

def applyJob(request):

    data = request.data

    print('data', request.data)

    first_name = data.get('first_name', None)
    middle_name = data.get('middle_name', None)
    last_name = data.get('last_name', None)
    job_id = data.get('job_id', None)
    phone = data.get('phone', None)
    mobile = data.get('mobile', None)
    email = data.get('email', None)
    email_alt = data.get('email_alt', None)
    marital_status = data.get('marital_status', None)
    date_of_birth = data.get('date_of_birth', None)
    last_applied = data.get('last_applied', None)

    street = data.get('street', None)
    pincode = data.get('pincode', None)
    city = data.get('city', None)
    state_id = data.get('state_id', None)

    exp_years = data.get('exp_years', 0)
    exp_months = data.get('exp_months', 0)
    qualification = data.get('qualification', None)
    cur_job = data.get('cur_job', None)
    cur_employer = data.get('cur_employer', None)
    certifications = data.get('certifications', None)
    fun_area = data.get('fun_area', None)
    subjects = data.get('subjects', None)
    skills = data.get('skills', None)

    if not job_id:
        return getErrorResponse('Job id required')

    job = Job.getById(int(job_id))
    if not job:
        return getErrorResponse('Invalid Job')

    if not first_name:
        return getErrorResponse('First name required')
    if not last_name:
        return getErrorResponse('Last name required')
    # if not mobile:
    #     return getErrorResponse('mobile required')
    # if not email:
    #     return getErrorResponse('email required')
    # if not date_of_birth:
    #     return getErrorResponse('Date of birth required')

    # dob = parseDate(date_of_birth)
    # if not dob:
    #     return getErrorResponse('Invalid date of birth')
    
    # age = ((date.today() - dob).days) / 365
    # print('Age', age)

    # if age < 18:
    #     return getErrorResponse("You are under age!")

    # if not marital_status:
    #     return getErrorResponse('Marital status required')

    # if marital_status not in Candidate.MARITAL_STATUS_LIST:
    #     return getErrorResponse('Invalid marital status')

    # if not street:
    #     return getErrorResponse('Street required')          
    # if not pincode:
    #     return getErrorResponse('pincode required')  
     
    # if int(pincode) != pincode and len(str(pincode)) != 6:
    #     return getErrorResponse('invalid pincode')   
    # if not city:
    #     return getErrorResponse('city required')          
    # if not state_id:
    #     return getErrorResponse('state required')     

    # state = State.getById(state_id)       
    # if not state:
    #     return getErrorResponse('invalid state')     

    # if not exp_years :
    #     return getErrorResponse('Experience year required')     

    # if not qualification:
    #     return getErrorResponse('qualification required')    

    # if qualification not in Candidate.QUALIFICATION_LIST:
    #     return getErrorResponse('Invalid Qualification')    

    candidate = Candidate()
        
    if request.FILES != None:
        print("files")
        print(request.FILES)
        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            candidate.resume = resume

    candidate.first_name = first_name
    candidate.last_name = last_name
    candidate.middle_name = middle_name
    candidate.email = email
    candidate.email_alt = email_alt
    candidate.phone = phone
    candidate.mobile = mobile
    candidate.marital_status = marital_status
    # candidate.date_of_birth = dob
    # candidate.age = age
    candidate.last_applied = last_applied
    candidate.street = street
    candidate.last_applied = last_applied
    candidate.street = street
    candidate.pincode = pincode
    candidate.city = city
    candidate.state = state_id
    # candidate.country = ''
    candidate.exp_years = exp_years
    candidate.exp_months = exp_months
    candidate.qualification = qualification            
    candidate.cur_job = cur_job            
    candidate.cur_employer = cur_employer            
    candidate.certifications = certifications            
    candidate.fun_area = fun_area            
    candidate.subjects = subjects            
    candidate.skills = skills
    candidate.job = job

    candidate.save()

    return {
        'code': 200,
        'msg': 'Job application submitted successfully!',
        'data': CandidateDetailsSerializer(candidate).data,
    }            

def getApplications(request):

    company = Company.getByUser(request.user)
    job_id = request.GET.get('job')
    if not job_id:
        return getErrorResponse('Job id required')

    job = Job.getByIdAndCompany(decode(job_id), company)        
    if not job:
        return getErrorResponse('Job not found')

    page_no = request.GET.get('page', 1)  

    try:
        page_no = int(page_no)
    except Exception as e:
        print(e)
        page_no = 1
    
    candidates = Candidate.getByJob(job=job)

    candidates = Paginator(candidates, PAGE_SIZE)

    pages = candidates.num_pages

    if pages >= page_no:
        p1 = candidates.page(page_no)
        lst = p1.object_list
        serializer = CandidateListSerializer(lst, many=True)

        return {
            'code': 200,
            'list': serializer.data,
            'current_page': page_no,
            'total_pages': pages
        }        
    else:
        return getErrorResponse('Page not available')

def deleteApplication(request):
    candidate_id = request.GET.get('id')
    if not candidate_id:
        return getErrorResponse('Invalid request')

    company = Company.getByUser(request.user)

    candidate = Candidate.getByIdAndCompany(decode(candidate_id), company)

    if candidate:
        candidate.delete()

        return {
            'code': 200,
            'msg': 'Candidate deleted successfully'
        }
    
    return getErrorResponse('Candidate not found')

def candidateDetails(request):
    candidate_id = request.GET.get('id')
    if not candidate_id:
        return getErrorResponse('Invalid request')

    company = Company.getByUser(request.user)

    candidate = Candidate.getByIdAndCompany(decode(candidate_id), company)

    if not candidate:
        return getErrorResponse('Candidate not found')

    serializer = CandidateDetailsSerializer(candidate)

    return {
        'code': 200,
        'data': serializer.data
    }


def updateApplication(request):

    data = request.data

    candidate_id = data.get('id', None)
    first_name = data.get('first_name', None)
    middle_name = data.get('first_name', None)
    last_name = data.get('first_name', None)
    job_id = data.get('job_id', None)
    phone = data.get('first_name', None)
    mobile = data.get('first_name', None)
    email = data.get('first_name', None)
    email_alt = data.get('first_name', None)
    marital_status = data.get('first_name', None)
    date_of_birth = data.get('first_name', None)
    last_applied = data.get('first_name', None)

    street = data.get('first_name', None)
    pincode = data.get('first_name', None)
    city = data.get('city', None)
    state_id = data.get('first_name', None)

    exp_years = data.get('exp_years', None)
    exp_months = data.get('exp_months', 0)
    qualification = data.get('qualification', None)
    cur_job = data.get('cur_job', None)
    cur_employer = data.get('cur_employer', None)
    certifications = data.get('certifications', None)
    fun_area = data.get('fun_area', None)
    subjects = data.get('subjects', None)
    skills = data.get('skills', None)

    if not candidate_id:
        return getErrorResponse('Invalid request')

    company = Company.getByUser(request.user)
    candidate = Candidate.getByIdAndCompany(decode(candidate_id), company)
    
    if not candidate:
        return getErrorResponse('candidate not found')

    if not job_id:
        return getErrorResponse('Job id required')

    job = Job.getById(decode(job_id))
    if not job:
        return getErrorResponse('Invalid Job')

    if not first_name:
        return getErrorResponse('First name required')
    if not last_name:
        return getErrorResponse('Last name required')
    if not date_of_birth:
        return getErrorResponse('Date of birth required')
    if not marital_status:
        return getErrorResponse('Marital status required')
    if not street:
        return getErrorResponse('Street required')          
    if not pincode:
        return getErrorResponse('pincode required')  
     
    if int(pincode) != pincode and len(str(pincode)) != 6:
        return getErrorResponse('invalid pincode')   
    if not city:
        return getErrorResponse('city required')          
    if not state_id:
        return getErrorResponse('state required')     

    state = State.getById(state_id)       
    if not state:
        return getErrorResponse('invalid state')     

    if int(exp_years) != exp_years:
        return getErrorResponse('Experience year required')     

    if exp_months:
        if exp_months != int(exp_months):
            return getErrorResponse('invalid experience months')   

    if not qualification:
        return getErrorResponse('qualification required')    

    if candidate.email != email:
        candidate = Candidate.getByEmail(job=job, email=email)
        if candidate:
            return getErrorResponse("Email already exists for other candidate")
    if candidate.mobile != mobile:
        candidate = Candidate.getByPhone(job=job, mobile=mobile)
        if candidate:
            return getErrorResponse("Mobile already exists for other candidate")

    if request.FILES != None:
        print("files")
        print(request.FILES)
        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            candidate.resume = resume    

    candidate.first_name = first_name            
    candidate.last_name = last_name            
    candidate.middle_name = middle_name            
    candidate.email = email            
    candidate.email_alt = email_alt            
    candidate.phone = phone            
    candidate.mobile = mobile            
    candidate.marital_status = marital_status            
    candidate.date_of_birth = date_of_birth            
    candidate.last_applied = last_applied            
    candidate.street = street            
    candidate.last_applied = last_applied            
    candidate.street = street            
    candidate.pincode = pincode            
    candidate.city = city            
    candidate.state = state            
    candidate.country = state.country          
    candidate.exp_years = exp_years            
    candidate.exp_months = exp_months            
    candidate.qualification = qualification            
    candidate.cur_job = cur_job            
    candidate.cur_employer = cur_employer            
    candidate.certifications = certifications            
    candidate.fun_area = fun_area            
    candidate.subjects = subjects            
    candidate.skills = skills

    candidate.save()

    return {
        'code': 200,
        'msg': 'Job application submitted sucessfully!'
    }                

def updateResume(request):

    data = request.data

    candidate_id = data.get('id', None)

    if not candidate_id:
        return getErrorResponse('Invalid request')

    company = Company.getByUser(request.user)
    candidate = Candidate.getByIdAndCompany(decode(candidate_id), company)
    
    if not candidate:
        return getErrorResponse('candidate not found')

    print("files")
    print(request.FILES)

    if request.FILES != None:
 
        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            candidate.resume = resume    
            candidate.save()
            data = parseResume(request, candidate)
            if data.get('code') == 200:
                candidate.resume_parse_data = data.get('data')

            candidate.save()

            return {
                'code': 200,
                'msg': 'Resume updated!'
            }         
    return getErrorResponse('Resume required!')                       

def parseResume(request, candidate=None):

    if request.FILES != None:
        print("files")
        print(request.FILES)
        if 'resume' in request.FILES:
            file = request.FILES['resume']

            url = ''
            if candidate == None:
                resume = ResumeFiles()
                resume.resume = file
                resume.save()
                url = settings.RESUME_TEMP_FILE_URL+resume.resume.name[11:]
            else:
                url = settings.RESUME_FILE_URL+candidate.resume.name[13:]

            parse = {
                "url": url,
                "userkey": settings.RESUME_PARSE_KEY,
                "version": settings.RESUME_PARSE_VERSION,
                "subuserid": settings.RESUME_PARSE_USER,
            }
            response = requests.post(settings.RESUME_PARSE_URL, data=json.dumps(parse))

            if response.status_code == 200:
                res = response.json()
                if 'error' in res:
                    error = res.get('error')
                    return getErrorResponse(str(error.get('errorcode'))+": "+error.get('errormsg'))

                return {
                    'code': 200,
                    'data': res
                } 
            return getErrorResponse('Failed to parse resume')

    return getErrorResponse('Resume required!')          

def getAllNotes(request):
    candidate_id = request.GET.get('candidate')
    if not candidate_id:
        return getErrorResponse('Invalid request')

    company = Company.getByUser(request.user)

    candidate = Candidate.getByIdAndCompany(decode(candidate_id), company)

    if not candidate:
        return getErrorResponse('Candidate not found')

    return {
        'code': 200,
        'notes': getNotesForCandidate(candidate)
    }

def getNotesForCandidate(candidate):
    notes = Note.getForCandidate(candidate)
    serializer = NoteSerializer(notes, many=True)  
    return serializer.data  

def saveNote(request):

    data = request.data

    candidate_id = data.get('candidate')
    if not candidate_id:
        return getErrorResponse('Invalid request')

    company = Company.getByUser(request.user)

    candidate = Candidate.getByIdAndCompany(decode(candidate_id), company)

    if not candidate:
        return getErrorResponse('Candidate not found')    

    type_id = data.get('type', None)
    if not type_id:
        return getErrorResponse('Note type required')

    type = NoteType.getById(type_id)

    if not type:
        return getErrorResponse('Invalid note type')        

    text = data.get('note', None)        
    if not text:
        return getErrorResponse('Note text required')    

    id = data.get('id', None)
    if id:
        note = Note.getById(id, candidate)
        if not note:
            return getErrorResponse('Note not found')
    else:
        note = Note()

    note.type = type
    note.added_by = request.user
    note.note = text
    note.candidate = candidate
    note.save()

    return {
        'code': 200,
        'msg': 'Note added successfully',
        'notes': getNotesForCandidate(candidate)
    }

def deleteNote(request):
    note_id = request.GET.get('id')
    if not note_id:
        return getErrorResponse('Invalid request')

    company = Company.getByUser(request.user)

    note = Note.getByIdAndCompany(note_id, company)

    if note:
        candidate = note.candidate
        note.delete()

        return {
            'code': 200,
            'msg': 'Note deleted successfully',
            'notes': getNotesForCandidate(candidate)
        }
    
    return getErrorResponse('Note not found')


def applyWebformJob(request):

    data = request.data

    print('data', request.data)

    webform_id = data.get('webform_id', None)

    if not webform_id: 
        return getErrorResponse('Webform id required!')

    job_id = data.get('job_id', None)
    if not job_id: 
        return getErrorResponse('Job id required!')


    job = Job.getById(decode(job_id))
    if not job:
        return getErrorResponse('Invalid Job')

    webform = Webform.getById(webform_id, job.company)
    if not webform:
        return getErrorResponse('Invalid Webform')

    first_name = data.get('first_name', None)

    middle_name = data.get('middle_name', None)
    last_name = data.get('last_name', None)
    phone = data.get('phone', None)
    mobile = data.get('mobile', None)
    email = data.get('email', None)
    email_alt = data.get('email_alt', None)
    marital_status = data.get('marital_status', None)
    date_of_birth = data.get('date_of_birth', None)
    last_applied = data.get('last_applied', None)

    street = data.get('street', None)
    pincode = data.get('pincode', None)
    city = data.get('city', None)
    state_id = data.get('state_id', None)

    exp_years = data.get('exp_years', None)
    exp_months = data.get('exp_months', 0)
    qualification = data.get('qualification', None)
    cur_job = data.get('cur_job', None)
    cur_employer = data.get('cur_employer', None)
    certifications = data.get('certifications', None)
    fun_area = data.get('fun_area', None)
    subjects = data.get('subjects', None)
    skills = data.get('skills', None)
    gender = data.get('gender', None)
    age = data.get('age', 0)

    if not webform.form:
        return getErrorResponse('Invalid Webform')

    for item in webform.form:
        print('item', item.get('value', None))
        value = item.get('value', None)
        type = item.get('type', None)
        if value:
            if type == 'file':
                if request.FILES == None or value not in request.FILES:           
                    return getErrorResponse(item.get('name', None)+' is required')
            elif not data.get(value, None):
                return getErrorResponse(item.get('name', None)+' is required')
            
            if 'marital_status' == value:
                if marital_status not in Candidate.MARITAL_STATUS_LIST:
                    return getErrorResponse('Invalid marital status')   
            if 'dob' == value:             
                dob = parseDate(date_of_birth)
                if not dob:
                    return getErrorResponse('Invalid date of birth')
                
                age = ((date.today() - dob).days) / 365
                print('Age', age)

                if age < 18:
                    return getErrorResponse("You are under age!")
            if 'pincode' == value:
                if int(pincode) != pincode and len(str(pincode)) != 6:
                    return getErrorResponse('invalid pincode')   
            if 'qualification' == value:
                if qualification not in Candidate.QUALIFICATION_LIST:
                    return getErrorResponse('Invalid Qualification')   
            if 'gender' == value:
                if gender not in Candidate.GENDER_LIST:
                    return getErrorResponse('Invalid Gender')   
            if 'age' == value:
                if int(age) != age and (int(age) < 18 or int(age) > 75):
                    return getErrorResponse('invalid age')       
            if 'state' == value:
                state = State.getById(state_id)       
                if not state:
                    return getErrorResponse('invalid state')                                                          
    
    if not age:
        if date_of_birth:
            age = ((date.today() - date_of_birth).days) / 365
            print('Age', age)

    candidate = Candidate()
        
    if request.FILES != None:
        print("files")
        print(request.FILES)
        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            candidate.resume = resume    

    candidate.first_name = first_name            
    candidate.last_name = last_name            
    candidate.middle_name = middle_name            
    candidate.email = email            
    candidate.email_alt = email_alt            
    candidate.phone = phone            
    candidate.mobile = mobile            
    candidate.marital_status = marital_status            
    candidate.date_of_birth = date_of_birth            
    candidate.age = age            
    candidate.last_applied = last_applied            
    candidate.street = street            
    candidate.last_applied = last_applied            
    candidate.street = street            
    candidate.pincode = pincode            
    candidate.city = city 

    if state:           
        candidate.state = state            
        candidate.country = state.country          
    
    candidate.exp_years = exp_years            
    candidate.exp_months = exp_months            
    candidate.qualification = qualification            
    candidate.cur_job = cur_job            
    candidate.cur_employer = cur_employer            
    candidate.certifications = certifications            
    candidate.fun_area = fun_area            
    candidate.subjects = subjects            
    candidate.skills = skills
    candidate.job = job
    candidate.webform = webform

    candidate.save()
    print("Candidate created")

    return {
        'code': 200,
        'msg': 'Job application submitted sucessfully!',
        'data': CandidateDetailsSerializer(candidate)
    }            


def getCandidates(request):

    company = Company.getByUser(request.user)
    if not company:
        return getErrorResponse('Company required')

    page_no = request.GET.get('page', 1)  

    try:
        page_no = int(page_no)
    except Exception as e:
        print(e)
        page_no = 1
    
    candidates = Candidate.getByCompany(company=company)
    all_candidates = [candidate for candidate in candidates if candidate.job.company.id == company.id]

    candidates = Paginator(all_candidates, PAGE_SIZE)

    pages = candidates.num_pages

    if pages >= page_no:
        p1 = candidates.page(page_no)
        lst = p1.object_list
        serializer = CandidateListSerializer(lst, many=True)

        return {
            'code': 200,
            'list': serializer.data,
            'current_page': page_no,
            'total_pages': pages
        }        
    else:
        return getErrorResponse('Given page not available')


def createCandidate(request):

    company = Company.getByUser(request.user)
    if not company:
        return getErrorResponse('Company required')

    job_id = request.data.get("job_id")
    job = Job.getByIdAndCompany(decode(job_id), company)
    if not job:
        return getErrorResponse('job_id is missing or incorrect')

    webform_id = request.data.get("webform_id", None)
    form_filled = request.data.get("form_filled", None)

    print(webform_id)
    print(form_filled)
    if webform_id != None:
        if form_filled != None:
            empty_webform = Webform.getById(webform_id, company)
            filled_webform = Webform()
            filled_webform.company = company
            filled_webform.form = form_filled

        else:    
            return getErrorResponse('Please provide filled form data')

    if request.FILES['resume']:#TO-DO imporve if check
        resume = request.FILES['resume']
        url = settings.RESUME_FILE_URL+resume.name
        # url = 'https://196034-584727-raikfcquaxqncofqfm.stackpathdns.com/wp-content/uploads/2022/02/Stockholm-Resume-Template-Simple.pdf'

        apiParserBody = {
            "url": url,
            "userkey": settings.RESUME_PARSE_KEY,
            "version": settings.RESUME_PARSE_VERSION,
            "subuserid": settings.RESUME_PARSE_USER,
        }
        response = requests.post(settings.RESUME_PARSE_URL, data=json.dumps(apiParserBody))
        
        if response.status_code == 200:
                res = response.json()
                if 'error' in res:
                    error = res.get('error')
                    print("Resume parsing API didn't return a valid response")
                    return getErrorResponse(str(error.get('errorcode'))+": "+error.get('errormsg'))
                else:
                    if getCandidateFromResumeJson(res)['code'] == 200:
                        candidate = getCandidateFromResumeJson(res)['candidate']
                    else:
                        return {
                            'code': 400,
                            'msg': 'Something went wrong while parsing data from JSON'
                        }
                    candidate.job = job
                    candidate.resume = resume
                    candidate.resume_parse_data = res
                    candidateExperiences = getCandidateExperiencesFromResumeJson(res)
                    try:
                        with transaction.atomic():
                            filled_webform.save()
                            candidate.webform = filled_webform
                            candidateExperiences = getCandidateExperiencesFromResumeJson(res)
                            candidateQualifications = getCandidateQualificationsFromResumeJson(res)
                            candidate.save()

                            for candidateExperience in candidateExperiences:
                                candidateExperience.candidate = candidate
                                candidateExperience.save()
                            
                            for candidateQualification in candidateQualifications:
                                candidateQualification.candidate = candidate
                                candidateQualification.save()
                            
                            candidateSerialized = CandidateDetailsSerializer(candidate)
                            candidateExperiencesSerialized = CandidateExperienceSerializer(candidateExperiences,many = True)
                            candidateQualificationsSerialized = CandidateQualificationSerializer(candidateQualifications,many = True)
                            return {
                                'code': 200,
                                'msg': 'Candidate created successfully',
                                'candidate': candidateSerialized.data,
                                'candidateExp':  candidateExperiencesSerialized.data,
                                'candidateQual': candidateQualificationsSerialized.data
                            }

                    except Exception as e:
                        print("some error occurred while saving the candidate")
                        print(e)
                        return getErrorResponse('Failed to parse resume and create candidate')

        return getErrorResponse("Resume parsing API didn't return a valid response")
    return getErrorResponse('Resume required!')

def getCandidateFromResumeJson(res):
    try:
        candidate = Candidate()
        if res["ResumeParserData"]["Name"]:
            candidate.first_name = res["ResumeParserData"]["Name"]["FirstName"]
            candidate.middle_name = res["ResumeParserData"]["Name"]["MiddleName"]
            candidate.last_name = res["ResumeParserData"]["Name"]["LastName"]

        if len(res["ResumeParserData"]["PhoneNumber"]) > 0:
            candidate.phone = res["ResumeParserData"]["PhoneNumber"][0]["FormattedNumber"]
        
        if len(res["ResumeParserData"]["PhoneNumber"]) > 1:
            candidate.mobile = res["ResumeParserData"]["PhoneNumber"][1]["FormattedNumber"]

        if len(res["ResumeParserData"]["Email"]) > 0:
            candidate.email = res["ResumeParserData"]["Email"][0]["EmailAddress"]
        
        if len(res["ResumeParserData"]["Email"]) > 1:
            candidate.email_alt = res["ResumeParserData"]["Email"][1]["EmailAddress"]

        if res["ResumeParserData"]["MaritalStatus"]:
            candidate.marital_status = res["ResumeParserData"]["MaritalStatus"]

        if res["ResumeParserData"]["Gender"]:
            candidate.gender = res["ResumeParserData"]["Gender"]

        if res["ResumeParserData"]["DateOfBirth"]:
            candidate.date_of_birth = datetime.strptime(res["ResumeParserData"]["DateOfBirth"], "%d/%m/%Y").strftime("%Y-%m-%d")

        if len(res["ResumeParserData"]["Address"]) > 0:
            candidate.street = res["ResumeParserData"]["Address"][0]["Street"]
            candidate.pincode = res["ResumeParserData"]["Address"][0]["ZipCode"]
            candidate.city = res["ResumeParserData"]["Address"][0]["City"]
            candidate.state = res["ResumeParserData"]["Address"][0]["State"]
            candidate.country = res["ResumeParserData"]["Address"][0]["Country"]

        if res["ResumeParserData"]["WorkedPeriod"]:
            candidate.exp_years = int ( float(res["ResumeParserData"]["WorkedPeriod"]["TotalExperienceInYear"] ) )
            candidate.exp_months = res["ResumeParserData"]["WorkedPeriod"]["TotalExperienceInMonths"]

        if res["ResumeParserData"]["Summary"]:
            candidate.cur_job = res["ResumeParserData"]["Summary"]

        if res["ResumeParserData"]["JobProfile"]:
            candidate.cur_job = res["ResumeParserData"]["JobProfile"]

        if res["ResumeParserData"]["CurrentEmployer"]:
            candidate.cur_employer = res["ResumeParserData"]["CurrentEmployer"]

        if res["ResumeParserData"]["Certification"]:
            candidate.certifications = res["ResumeParserData"]["Certification"]
        
        if res["ResumeParserData"]["Hobbies"]:
            candidate.fun_area = res["ResumeParserData"]["Hobbies"]
        
        if res["ResumeParserData"]["SkillKeywords"]:
            candidate.skills = res["ResumeParserData"]["SkillKeywords"]
        
        return {
            'code': 200,
            'candidate' : candidate
        }

    except Exception as e:
        print("Exception occured while parsing data from JSON")
        print(e)
        return {
            'code': 400,
            'msg': 'Something went wrong while parsing data from JSON'
        }
    


def getCandidateExperiencesFromResumeJson(res):

    if res["ResumeParserData"]["SegregatedExperience"]:
        candidateExperiences = []
        for experience in res["ResumeParserData"]["SegregatedExperience"]:
            candidateExperience = CandidateExperience()
            if experience["Employer"]["EmployerName"]:
                candidateExperience.employer = experience["Employer"]["EmployerName"]
            if experience["JobProfile"]:
                if experience["JobProfile"]["Title"]:
                    candidateExperience.jobProfile = experience["JobProfile"]["Title"]
                if experience["JobProfile"]["RelatedSkills"]:
                    candidateExperience.skills = getSkillsFromRelatedSkillsArray(experience["JobProfile"]["RelatedSkills"])
            if experience["Location"]:
                candidateExperience.city = experience["Location"]["City"]
                candidateExperience.state = experience["Location"]["State"]
                candidateExperience.country = experience["Location"]["Country"]
            if experience["StartDate"]:
                candidateExperience.start_date = datetime.strptime(experience["StartDate"], "%d/%m/%Y").strftime("%Y-%m-%d")
            if experience["EndDate"]:
                candidateExperience.end_date = datetime.strptime(experience["EndDate"], "%d/%m/%Y").strftime("%Y-%m-%d")
            if experience["JobDescription"]:
                candidateExperience.jobDescription = experience["JobDescription"]
            candidateExperiences.append(candidateExperience)
        
        return candidateExperiences
        
            

def getSkillsFromRelatedSkillsArray(relatedSkills):

    if relatedSkills:
        skillString = ''
        for skill in relatedSkills:
            skillString = skillString + skill["Skill"] + ', '
        return skillString


def getCandidateQualificationsFromResumeJson(res):

    if res["ResumeParserData"]["SegregatedQualification"]:
        qualifications = []
        for qualification in res["ResumeParserData"]["SegregatedQualification"]:
            candidateQualification = CandidateQualification()
            if qualification["Institution"]["Name"]:
                candidateQualification.institue_name = qualification["Institution"]["Name"]
            if qualification["Degree"]:
                candidateQualification.degree = qualification["Degree"]["DegreeName"]
            if qualification["Institution"]["Location"]:
                candidateQualification.city = qualification["Institution"]["Location"]["City"]
                candidateQualification.state = qualification["Institution"]["Location"]["State"]
                candidateQualification.country = qualification["Institution"]["Location"]["Country"]
            if qualification["StartDate"]:
                candidateQualification.start_date = datetime.strptime(qualification["StartDate"], "%d/%m/%Y").strftime("%Y-%m-%d")
            if qualification["EndDate"]:
                candidateQualification.end_date = datetime.strptime(qualification["StartDate"], "%d/%m/%Y").strftime("%Y-%m-%d")
            if qualification["Aggregate"]:
                candidateQualification.grade = str (qualification["Aggregate"]["Value"])
                candidateQualification.gradeType = qualification["Aggregate"]["MeasureType"]
            qualifications.append(candidateQualification)
        return qualifications
                      

def parseResume(request, candidate=None):

    if request.FILES != None:
        print("files")
        print(request.FILES)
        if 'resume' in request.FILES:
            file = request.FILES['resume']

            url = ''
            if candidate == None:
                resume = ResumeFiles()
                resume.resume = file
                resume.save()
                url = settings.RESUME_TEMP_FILE_URL+resume.resume.name[11:]
            else:
                url = settings.RESUME_FILE_URL+candidate.resume.name[13:]

            parse = {
                "url": url,
                "userkey": settings.RESUME_PARSE_KEY,
                "version": settings.RESUME_PARSE_VERSION,
                "subuserid": settings.RESUME_PARSE_USER,
            }
            response = requests.post(settings.RESUME_PARSE_URL, data=json.dumps(parse))

            if response.status_code == 200:
                res = response.json()
                if 'error' in res:
                    error = res.get('error')
                    return getErrorResponse(str(error.get('errorcode'))+": "+error.get('errormsg'))

                return {
                    'code': 200,
                    'data': res
                } 
            return getErrorResponse('Failed to parse resume')

    return getErrorResponse('Resume required!') 