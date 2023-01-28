from collections import namedtuple
import email
import re
from unicodedata import category
from account.models import Account, Company, TokenEmailVerification, TokenResetPassword
from candidates.models import Candidate
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import authenticate
from common.encoder import decode
from common.utils import isValidUuid, getDomainFromEmail
from common.models import Country, State, City
import json
from .models import Degree, Department, Designation, EmailCategory, EmailFields, EmailTemplate, Location, Pipeline, PipelineStage, Webform
from .serializer import DegreeSerializer, PipelineStagListSerializer, DepartmentSerializer, DesignationSerializer, EmailCategorySerializer, EmailFieldSerializer, EmailTemplateSerializer, LocationSerializer, PipelineSerializer, PipelineStageSerializer, WebformDataSerializer, WebformListSerializer


def getCompanyByUser(user):
    return Company.getByUser(user.use)

#INSTITUTE SETTINGS
def getLocations(request):

    company = Company.getByUser(request.user)
    locations = Location.getForCompany(company=company)

    serializer = LocationSerializer(locations, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }

def saveLocation(request):

    data = request.data
    name = data.get('name', None)
    address = data.get('address', None)
    city = data.get('city', None)
    pincode = data.get('pincode', None)
    loc_lat = data.get('loc_lat', None)
    loc_lon = data.get('loc_lon', None)

    company = Company.getByUser(request.user)

    if not company or not name or not address or not city or not pincode:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    city = City.getById(city)    

    id = data.get('id', None)
    if id:
        location = Location.getById(id, company)
        if not location:
            return {
                'code': 400,
                'msg': 'location not found'
            }
    else:
        location = Location()
        location.company = company

    location.name = name
    location.address = address
    location.city = city
    location.state = city.state
    location.country = city.state.country
    location.pincode = pincode
    location.loc_lat = loc_lat
    location.loc_lon = loc_lon

    location.save()

    return getLocations(request)

def deleteLocation(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        location = Location.getById(id, company)
        if not location:
            return {
                'code': 400,
                'msg': 'Location not found'
            }

        location.delete()
        return {
            'code': 200,
            'msg': 'Location deleted succesfully!',
            'data': getLocations(request)['data']
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
    }

def getDepartments(request):

    company = Company.getByUser(request.user)
    departments = Department.getForCompany(company=company)

    serializer = DepartmentSerializer(departments, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def saveDepartment(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    name = data.get('name', None)   

    if not name:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    id = data.get('id', None)

    if id:
        department = Department.getById(id, company)
        if not department:
            return {
                'code': 400,
                'msg': 'Department not found'
            }
        if department.name != name and Department.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Department with name '+name+' already exists.'
            } 
    else:
        if Department.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Department with name '+name+' already exists.'
            } 

        department = Department()   
        department.company = company
    
    department.name = name
    department.save()

    return getDepartments(request)

def deleteDepartment(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        department = Department.getById(id, company)
        if not department:
            return {
                'code': 400,
                'msg': 'Department not found'
            }

        department.delete()
        return {
            'code': 200,
            'msg': 'Department deleted succesfully!',
            'data': getDepartments(request)['data']
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
    }    

def getDegrees(request):

    company = Company.getByUser(request.user)
    degrees = Degree.getForCompany(company=company)

    serializer = DegreeSerializer(degrees, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def saveDegree(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    name = data.get('name', None)   

    if not name:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    id = data.get('id', None)

    if id:
        degree = Degree.getById(id, company)
        if not degree:
            return {
                'code': 400,
                'msg': 'Degree not found'
            }
        if degree.name != name and Degree.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Degree with name '+name+' already exists.'
            } 
    else:
        if Degree.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Degree with name '+name+' already exists.'
            } 

        degree = Degree()    
        degree.company = company

    
    degree.name = name
    degree.save()

    return getDegrees(request)

def deleteDegree(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        degree = Degree.getById(id, company)
        if not degree:
            return {
                'code': 400,
                'msg': 'Degree not found'
            }

        degree.delete()
        return {
            'code': 200,
            'msg': 'Degree deleted succesfully!',
            'data': getDegrees(request)['data']
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
    }        

def getDesignations(request):

    company = Company.getByUser(request.user)
    designation = Designation.getForCompany(company=company)

    serializer = DesignationSerializer(designation, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def saveDesignation(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    name = data.get('name', None)   

    if not name:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    id = data.get('id', None)

    if id:
        designation = Designation.getById(id, company)
        if not designation:
            return {
                'code': 400,
                'msg': 'Designation not found'
            }
        if designation.name != name and Designation.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Designation with name '+name+' already exists.'
            } 
    else:
        if Designation.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Designation with name '+name+' already exists.'
            } 

        designation = Designation()    
        designation.company = company
    
    designation.name = name
    designation.save()

    return getDesignations(request)

def deleteDecignation(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        designation = Designation.getById(id, company)
        if not designation:
            return {
                'code': 400,
                'msg': 'Designation not found'
            }

        designation.delete()
        return {
            'code': 200,
            'msg': 'Designation deleted succesfully!',
            'data': getDesignations(request)['data']
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
    }        

#PIPELINES
def getPipelineStages(request):
    pipeline_id = request.GET.get('id')
    company = Company.getByUser(request.user)
    if not company:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }
    
    pipeline = Pipeline.getById(id = pipeline_id, company=company)

    if not pipeline:
        return {
            'code': 400,
            'msg': 'Pipeline not Valid'
        }

    pipelineStages = PipelineStage.getByPipeline(company=company, pipeline=pipeline)

    serializer = PipelineStagListSerializer(pipelineStages, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def savePipelineStage(request):
    pipeline_id = request.GET.get('id')
    company = Company.getByUser(request.user)    
    
    data = request.data    

    pipeline = Pipeline.getById(id = pipeline_id, company=company)

    if not pipeline:
        return {
            'code': 400,
            'msg': 'Pipeline not Valid'
        }

    id = data.get('id', None)

    update = False

    if id:
        pipelineStage = PipelineStage.getByPipeline(company=company, pipeline=pipeline)
        if not pipelineStage:
            return {
                'code': 400,
                'msg': 'Pipeline Stage not found'
            }
        update = True
    else:
        pipelineStage = PipelineStage()    
        pipelineStage.company = company

        
    
    if data.get('name'):
        pipelineStage.name = data.get('name')

    if data.get('status'):
        pipelineStage.status = data.get('status')
    pipelineStage.pipeline = pipeline

    if not update: 
        pipelineStage.save()

    return getPipelineStages(request)

def deletePipelineStage(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        pipelineStage = PipelineStage.getById(id, company)
        if not pipelineStage:
            return {
                'code': 400,
                'msg': 'Pipeline Stage not found'
            }

        pipelineStage.delete()
        return {
            'code': 200,
            'msg': 'Pipeline Stage deleted succesfully!'
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
    }        


def getPipelineStageDetails(request):

    stage_id = request.GET.get('id', None)   

    if not stage_id:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    company = Company.getByUser(request.user)    
    stage = PipelineStage.getById(stage_id, company)
    if not stage:
        return {
            'code': 400,
            'msg': 'Pipeline Status not found'
        }

    serializer = PipelineStageSerializer(stage, many=False)

    return {
        'code': 200,
        'data': serializer.data
    }    

def savePipelineStatus(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    stage_id = data.get('stage', None)   
    status = data.get('status', None)   

    if not stage_id or not isinstance(status, list):
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    stage = PipelineStage.getById(stage_id, company)
    if not stage:
        return {
            'code': 400,
            'msg': 'Pipeline Status not found'
        }
    
    stage.status = status
    stage.save()

    serializer = PipelineStageSerializer(stage, many=False)

    return {
        'code': 200,
        'msg' : 'Pipeline stage updated!',
        'data': serializer.data
    }   


def getPipelines(request):

    company = Company.getByUser(request.user)
    pipelines = Pipeline.getForCompany(company=company)

    serializer = PipelineSerializer(pipelines, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def savePipeline(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    name = data.get('name', None)   
    fields = data.get('fields', None)   
    
    if not name or not fields or not isinstance(fields, list):
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    id = data.get('id', None)

    if id:
        pipeline = Pipeline.getById(id, company)
        if not pipeline:
            return {
                'code': 400,
                'msg': 'Pipeline not found'
            }
        if pipeline.name != name and Pipeline.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Pipeline with name '+name+' already exists.'
            } 
    else:
        if Pipeline.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Pipeline with name '+name+' already exists.'
            } 

        pipeline = Pipeline()    
        pipeline.company = company

    pipeline.name = name
    pipeline.fields = fields
    pipeline.save()

    return getPipelines(request)

def deletePipeline(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        pipeline = Pipeline.getById(id, company)
        if not pipeline:
            return {
                'code': 400,
                'msg': 'Pipeline not found'
            }

        pipeline.delete()
        return {
            'code': 200,
            'msg': 'Pipeline deleted succesfully!',
            'data': getPipelines(request)['data']
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
    }          

#EMAILS

def getEmailFileds(request):

    fields = EmailFields.getAll()

    serializer = EmailFieldSerializer(fields, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }        

def getEmailCategories(request):

    company = Company.getByUser(request.user)
    emails = EmailCategory.getForCompany(company=company)

    serializer = EmailCategorySerializer(emails, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def saveEmailCategory(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    name = data.get('name', None)   

    if not name:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    id = data.get('id', None)

    if id:
        category = EmailCategory.getById(id, company)
        if not category:
            return {
                'code': 400,
                'msg': 'Email Category not found'
            }
        if category.name != name and EmailCategory.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Email Category with name '+name+' already exists.'
            } 
    else:
        if EmailCategory.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Email Category with name '+name+' already exists.'
            } 
        category = EmailCategory()   
        category.company = company

    category.name = name
    category.save()

    return getEmailCategories(request)

def deleteEmailCategory(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        category = EmailCategory.getById(id, company)
        if not category:
            return {
                'code': 400,
                'msg': 'Email Category not found'
            }

        category.delete()
        return {
            'code': 200,
            'msg': 'Email Category deleted succesfully!',
            'data': getEmailCategories(request)['data']
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
    }         

def getEmailTemplates(request):

    company = Company.getByUser(request.user)
    emails = EmailTemplate.getForCompany(company=company)

    serializer = EmailTemplateSerializer(emails, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def saveEmailTemplate(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    type = data.get('type', None)   
    category = data.get('category', None)   
    subject = data.get('subject', None)   
    message = data.get('message', None)   

    if not category or not type or not type in EmailTemplate.EMAIL_TYPES or not message or not subject:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    category = EmailCategory.getById(category, company)    
    if not category:
        return {
            'code': 400,
            'msg': 'Category not found!'
        }

    id = data.get('id', None)

    if id:
        email = EmailTemplate.getById(id, company)
        if not email:
            return {
                'code': 400,
                'msg': 'Email not found'
            }
        if email.subject != subject and EmailTemplate.getByName(subject=subject, company=company):
            return {
                'code': 400,
                'msg': 'Email Template with subject '+subject+' already exists.'
            } 
    else:
        if EmailTemplate.getByName(subject=subject, company=company):
            return {
                'code': 400,
                'msg': 'Email Template with name '+subject+' already exists.'
            } 

        email = EmailTemplate()  
        email.company = company  

    if request.FILES != None:
        print("attachments")
        print(request.FILES)
        if 'attachment' in request.FILES:
            file = request.FILES['attachment']
            if email.attachment:
                email.attachment.delete()
            email.attachment = file    
    
    email.category = category
    email.type = type
    email.subject = subject
    email.message = message
    email.save()

    return getEmailTemplates(request)

def deleteEmailTemmplate(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        email = EmailTemplate.getById(id, company)
        if email and email.attachment:
                email.attachment.delete()
        if not email:
            return {
                'code': 400,
                'msg': 'Email Template not found'
            }

        email.delete()
        return {
            'code': 200,
            'msg': 'Email Template deleted succesfully!',
            'data': getEmailTemplates(request)['data']
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
    }        


def getWebforms(request):

    company = Company.getByUser(request.user)

    id = request.GET.get('id', None)

    if id:
        form = Webform.getById(id, company)
        if not form:
            return {
                'code': 400,
                'msg': 'Form not found'
            }
        serializer = WebformDataSerializer(form)
    else:
        forms = Webform.getForCompany(company=company)
        serializer = WebformListSerializer(forms, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def saveWebForms(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    name = data.get('name', None)   
    form = data.get('form', None)   

    if not company or not name or not form:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    id = data.get('id', None)

    if id:
        webform = Webform.getById(id, company)
        if not webform:
            return {
                'code': 400,
                'msg': 'Email not found'
            }
        if webform.name != name:
            if Webform.getByName(name, company):
                return {
                    'code': 400,
                    'msg': 'Webform with name '+name+' already exists!'
                }
    else:
        if Webform.getByName(name, company):
            return {
                'code': 400,
                'msg': 'Webform with name '+name+' already exists!'
            }

        webform = Webform()  
        webform.company = company


    webform.name = name
    webform.form = form

    webform.save()

    return {
        'code': 200,
        'msg': 'Webform saved successfully!'
    }

def deleteWebforms(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        form = Webform.getById(id, company)

        if not form:
            return {
                'code': 400,
                'msg': 'Webform not found'
            }

        form.delete()
        return {
            'code': 200,
            'msg': 'Webform deleted succesfully!',
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
    }            

def getWebformFields(request):

    return {
        'code': 200,
        'data': [
            {
                'name': 'First Name',
                'value': 'first_name',
                'type': 'text'
            },
            {
                'name': 'Middle Name',
                'value': 'middle_name',
                'type': 'text'
            },
            {
                'name': 'Last Name',
                'value': 'last_name',
                'type': 'text'
            },
            {
                'name': 'Phone Number',
                'value': 'phone',
                'type': 'number'
            },
            {
                'name': 'Mobile Number',
                'value': 'mobile',
                'type': 'number'
            },
            {
                'name': 'Email',
                'value': 'email',
                'type': 'email'
            },
            {
                'name': 'Alternate Email',
                'value': 'email_alt',
                'type': 'email'
            },
            {
                'name': 'Marrital Status',
                'value': 'marital_status',
                'type': 'select',
                'options': ['Single', 'Married']
            },
            {
                'name': 'Gender',
                'value': 'gender',
                'type': 'select',
                'options': Candidate.GENDER_LIST
            },
            {
                'name': 'Date of Birth',
                'value': 'date_of_birth',
                'type': 'date'
            },
            {
                'name': 'Last Applied',
                'value': 'last_applied',
                'type': 'datetime'
            },
            {
                'name': 'Street',
                'value': 'street',
                'type': 'text'
            },
            {
                'name': 'Pincode',
                'value': 'pincode',
                'type': 'number'
            },
            {
                'name': 'City',
                'value': 'city',
                'type': 'text'
            },
            {
                'name': 'State',
                'value': 'state',
                'type': 'state'
            },
            {
                'name': 'Country',
                'value': 'country',
                'type': 'country'
            },
            {
                'name': 'Age',
                'value': 'age',
                'type': 'number'
            },
            {
                'name': 'Experience in years',
                'value': 'exp_years',
                'type': 'number'
            },
            {
                'name': 'Experience in months',
                'value': 'exp_months',
                'type': 'number'
            },
            {
                'name': 'Highest Qualification',
                'value': 'qualification',
                'type': 'select',
                'options': Candidate.QUALIFICATION_LIST
            },
            {
                'name': 'Current Job',
                'value': 'cur_job',
                'type': 'text'
            },
            {
                'name': 'Current Job',
                'value': 'cur_job',
                'type': 'text'
            },
            {
                'name': 'Current Employer',
                'value': 'cur_employer',
                'type': 'text'
            },
            {
                'name': 'Certifications',
                'value': 'certifications',
                'type': 'text'
            },
            {
                'name': 'Functional Area',
                'value': 'fun_area',
                'type': 'text'
            },
            {
                'name': 'Subjects',
                'value': 'subjects',
                'type': 'text'
            },
            {
                'name': 'Skills',
                'value': 'skills',
                'type': 'text'
            },
            {
                'name': 'Resume',
                'value': 'resume',
                'type': 'file'
            }
        ]
    }     