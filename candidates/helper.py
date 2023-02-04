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
from common.utils import isValidUuid, getErrorResponse, getDomainFromEmail
from common.models import Country, NoteType, State, City
import json
from settings.models import Degree, Department, Pipeline, Webform
from .models import Candidate, CandidateExperience, CandidateQualification, Note, ResumeFiles, ApplicantWebForm
from .serializer import CandidateExperienceSerializer, CandidateListSerializer, CandidateDetailsSerializer, CandidateQualificationSerializer, NoteSerializer
from common.encoder import decode
from django.utils.dateparse import parse_date
from common.utils import parseDate
from datetime import date, datetime    
from django.conf import settings
import requests
from django.core.paginator import Paginator
from django.db import transaction
from django.core.files.storage import FileSystemStorage

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

    job = Job.getByIdAndCompany((job_id), company)        
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

    candidate = Candidate.getByIdAndCompany(candidate_id, company)

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

    candidate = Candidate.getById(candidate_id)

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


    # company = request.data.get('company')
    # company = Company.getById(company)

    company = Company.getByUser(request.user)
    candidate = Candidate.getByIdAndCompany(candidate_id, company)
    
    if not candidate:
        return getErrorResponse('candidate not found')

    if not job_id:
        return getErrorResponse('Job id required')

    job = Job.getById(job_id)
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
     
    if len(pincode) != 6:
        print(pincode, len(pincode))
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
    if Candidate.getByPhone(job=job, mobile=mobile):
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
    print(candidate, 'candidate here')
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
    candidate = Candidate.getByIdAndCompany(candidate_id, company)
    
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
 
    company = Company.getByUser(request.user)
    # company = request.GET.get('company')
    # company = Company.getById(company)
    
    if not candidate_id:
        return getErrorResponse('Invalid request')

    candidate = Candidate.getByIdAndCompany(candidate_id, company)

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
    # company = data.get('company', None)
    # company = Company.getById(company)

    candidate = Candidate.getByIdAndCompany(candidate_id, company)

    if not candidate:
        return getErrorResponse('Candidate not found')    

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


    job = Job.getById(job_id)
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

    # company = request.data.get('company')
    # company = Company.getById(company)
    company = Company.getByUser(request.user)
    print(company)
    
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
    job = Job.getByIdAndCompany(job_id, company)
    if not job:
        return getErrorResponse('job_id is missing or incorrect')
    
    email = request.data.get("email")
    if email is None or len(str(email).strip())==0:
        return getErrorResponse("Please provide candidate email")

    if Candidate.objects.filter(email=email).exists() or Candidate.objects.filter(email_alt=email).exists():
        return getErrorResponse("Canidate with this email is already registered")


    webform_id = request.data.get("webform_id", None)
    form_filled = request.data.get("form_filled", None)

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
        fs = FileSystemStorage(settings.RESUME_URL_ROOT)
        filename = fs.save(resume.name, resume)
        # url = 'https://196034-584727-raikfcquaxqncofqfm.stackpathdns.com/wp-content/uploads/2022/02/Stockholm-Resume-Template-Simple.pdf'
        print(url)
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
                            candidate.email = email
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
                        return getErrorResponse('Failed to parse resume and create candidate' + str(e))

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
            try:
                candidate.exp_years = int ( float(res["ResumeParserData"]["WorkedPeriod"]["TotalExperienceInYear"] ) )
            except Exception as e:
                print("Exception occurred while experience string conv to float")  
            try:
                candidate.exp_months = int (res["ResumeParserData"]["WorkedPeriod"]["TotalExperienceInMonths"])
            except Exception as e:
                print("Exception occurred while experience string conv to int")


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
                try:
                    candidateExperience.start_date = datetime.strptime(experience["StartDate"], "%d/%m/%Y").strftime("%Y-%m-%d")
                except:
                    print("Start date not in desired format")    
            if experience["EndDate"]:
                try:
                    candidateExperience.end_date = datetime.strptime(experience["EndDate"], "%d/%m/%Y").strftime("%Y-%m-%d")
                except:
                    print("End date not in desired format")
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
                try:
                    candidateQualification.start_date = datetime.strptime(qualification["StartDate"], "%d/%m/%Y").strftime("%Y-%m-%d")
                except:
                    print("Start date not in desired format")
            if qualification["EndDate"]:
                try:
                    candidateQualification.end_date = datetime.strptime(qualification["EndDate"], "%d/%m/%Y").strftime("%Y-%m-%d")
                except:
                    print("End date not in desired format")
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


# creating a Candidate using the online Form only and not the Resume Parser

def createCandidatewithoutResumeParser(request):

    account = request.user
    # account = request.data.get('company')
    # account = Company.getById(account)

    # Paranoid validation :p
    company = Company.getById(account.company_id)
    # company = Company.getById(account)
    if not company:
        return {
            'code': 400,
            'msg': 'Company not found!'
        }

    data = request.data
    print(data)

    # Validating the job id 
    job_id = data.get('job_id')

    if not job_id: 
        return getErrorResponse('Bad request')
    
    job = Job.getById(job_id)
    if not job:
        return {
            'code': 400,
            'data': 'Job not found!'
        }

    # entering Candidate Details
    first_name = data.get('first_name')

    if not first_name or len(first_name)<3:
        return {
            'code': 400,
            'msg': 'Enter a valid First Name!'
        }
    
    # Middle Name and last name are optional
    middle_name = data.get('middle_name', None)
    last_name = data.get('last_name', None)

    
    # Checking the mobile number because yess, we are paranoid
    mobile = data.get('mobile', None)
    
    if not mobile or len(mobile)<10:
        return {
            'code': 400,
            'msg': 'Enter a valid Mobile Number!'
        }
    if Candidate.getByPhone(job=job, mobile=mobile).exists():
        return getErrorResponse("Mobile Number already exists for other candidate")

    # Checking and validating email because once again we will be acting paranoid!
    email = data.get('email', None)
    if not email or not getDomainFromEmail(email):
        return {
            'code': 400,
            'msg': 'Invalid email address'
        }
    if Candidate.getByEmail(job=job, email=email).exists():
        return getErrorResponse("Email already exists for other candidate")
    
    # optional
    email_alt = data.get('alt_email', None)
    if email_alt and not getDomainFromEmail(email):
        return {
            'code': 400,
            'msg': 'Invalid email address'
        }

    # Checing the oprions in Marital State, because yesss, this could be an error
    marital_status = data.get('marital_status', None)
    if marital_status and marital_status not in ['Single', 'Married']:
        return {
            'code': 400,
            'msg': 'Invalid marital status!! \n Enter either \'Single\' or \'Married\''
        }

    # Checking the gender options becauseeee yessss!!! we are paranoid
    gender = data.get('gender', None)
    if gender and gender not in ['Female', 'Male']:
        return {
            'code': 400,
            'msg' : 'Invalid gender!! \n Enter either \'Male\' or \'Female\''
        }
    
    # front end select, so no validation required
    date_of_birth = datetime.strptime(data.get('date_of_birth', None),'%Y-%m-%d').date()
    
    last_applied = data.get('last_applied', None)
    pincode = data.get('pincode', None)
    street = data.get('address', None)
    city = data.get('city', None)
    state = data.get('state', None)
    country = data.get('country', None)

    # Calculating Age
    today = date.today()
    age =  today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    if age<18:
        return {
            'code': 400,
            'msg' : 'Candidate\'s age should be greater than 18 yrs!'
        }

    # These are optional fields
    exp_years = data.get('exp_years', None)
    exp_months = data.get('exp_months', None)
    admission_date = data.get('admission_date', None)
    graduation_date = data.get('graduation_date', None)
    


    # FINALLY, The moment where we create our candidate
    candidate = Candidate()
    candidate.job = job
    candidate.first_name = first_name

    if middle_name:
        candidate.middle_name = middle_name

    if last_name:
        candidate.last_name = last_name

    candidate.mobile = mobile
    candidate.email = email
    
    if email_alt: 
        candidate.email_alt = email_alt

    if marital_status: 
        candidate.marital_status = marital_status
    
    if gender:
        gender = gender
    
    candidate.date_of_birth = date_of_birth
    candidate.age = age
    candidate.last_applied = last_applied
    candidate.pincode = pincode
    candidate.street = street
    candidate.city = city
    if not state:
        return {
            'code': 400,
            'msg': 'State required'
        }
    else:
        candidate.state = State.getById(state)
    if not country:
        return {
            'code': 400,
            'msg': 'Country required'
        }
    else:
        candidate.country = Country.getById(country)

    if exp_months:
        candidate.exp_months = exp_months
    
    if exp_years:
        candidate.exp_years = exp_years
    
    if admission_date: 
        candidate.admission_date = admission_date

    if graduation_date:
        candidate.graduation_date = graduation_date

    # Saveddd siuuuuuuuu
    candidate.save()

    candidate_id = Candidate.objects.filter().last()

    serializer = CandidateDetailsSerializer(candidate_id)

    return {
        'code': 200, 
        'data': "Candidate Created Successfully!!",
        'id': serializer.data
    }

def updatePipelineStatus(request):
    account = request.user

    # Paranoid validation :p
    company = Company.getById(account.company_id)
    if not company:
        return {
            'code': 400,
            'msg': 'Company not found!'
        }
    
    data = request.data

    # Validating the candidate id 
    candidate_id = data.get('id')

    if not candidate_id: 
        return getErrorResponse('Bad request')

    candidate = Candidate.getByIdAndCompany(id=candidate_id, company=company)
    if not candidate:
        return {
            'code': 400,
            'data': 'Candidate not found!'
        }
    
    # Provide valid options from front end
    candidate.pipeline_stage_status = data.get('pipeline-stage-status')
    # Need validation
    # 1. Selected pipeline stage status already exists and same with pipeline stage
    candidate.pipeline_stage = data.get('pipeline-stage')
    candidate.save()

    return {
        'code': 200, 
        'data': "Candidate Pipeline Updated Successfully!!"
    }

from settings.models import Webform
def saveApplicantWebForms(request):
    
    data = request.data    
    job_id = data.get('job', None)   
    candidate_id = data.get('candidate', None)   
    # webform = data.get('webform', None)   
    assingment = data.get('assingment', None)
    form = data.get('form', None)   

    print('info', data)
    if not candidate_id:
        return {
            'code': 400,
            'msg': 'Candidate required'
        }

    if not job_id:
        return {
            'code': 400,
            'msg': 'Job required'
        }

    if  not assingment:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }        

    if not form:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }
    temp_form= json.dumps(form)
    form = json.loads(temp_form)
    job = Job(id=job_id)
    if not job:
        return {
            'code': 400,
            'msg': 'Job does not exist'
        }

    candidate = Candidate(id=candidate_id)
    if not candidate:
        return {
            'code': 400,
            'msg': 'Webform does not exist'
        }
    
    # try:
    instance = ApplicantWebForm()
    instance.job = job
    instance.candidate = candidate
    # if form:
    #     instance.form = json.loads(form)
    if assingment:
        temp_assignment= json.dumps(assingment)
        instance.assingment = json.loads(temp_assignment)
    instance.form = form
    instance.save()
    
    # except:
    #     return {
    #         'code': 200,
    #         'msg': 'Something went wrong :(',
    #     }

    return {
        'code': 200,
        'msg': 'Applicant webform created successfully',
    }