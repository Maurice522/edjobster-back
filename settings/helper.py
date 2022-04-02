from collections import namedtuple
import email
import re
from unicodedata import category
from account.models import Account, Company, TokenEmailVerification, TokenResetPassword
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import authenticate
from common.encoder import decode
from common.utils import isValidUuid, getDomainFromEmail
from common.models import Country, State, City
import json
from settings.models import Degree, Department, Designation, EmailCategory, EmailFields, EmailTemplate, Location, Pipeline, PipelineStatus, PipelineStage
from settings.serializer import DegreeSerializer, DepartmentSerializer, DesignationSerializer, EmailCategorySerializer, EmailFieldSerializer, EmailTemplateSerializer, LocationSerializer, PipelineStatusSerializer, PipelineSerializer, PipelineStageSerializer


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

    company = Company.getByUser(request.user)
    pipelineStages = PipelineStage.getForCompany(company=company)

    serializer = PipelineStageSerializer(pipelineStages, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def savePipelineStage(request):

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
        pipelineStage = PipelineStage.getById(id, company)
        if not pipelineStage:
            return {
                'code': 400,
                'msg': 'Pipeline Stage not found'
            }
        if pipelineStage.name != name and PipelineStage.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Pipeline Stage with name '+name+' already exists.'
            } 
    else:
        if PipelineStage.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'pipeline Stage with name '+name+' already exists.'
            } 
        pipelineStage = PipelineStage()    
        pipelineStage.company = company
    
    pipelineStage.name = name
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
            'msg': 'Pipeline Stage deleted succesfully!',
            'data': getPipelineStages(request)['data']
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
    }        


def getPipelineStatus(request):

    stage_id = request.GET.get('stage', None)   

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

    pipelineStages = PipelineStatus.getForStage(stage=stage)
    serializer = PipelineStatusSerializer(pipelineStages, many=True)

    return {
        'code': 200,
        'data': serializer.data
    }    

def savePipelineStatus(request):

    company = Company.getByUser(request.user)    
    
    data = request.data    
    stage_id = data.get('stage', None)   
    name = data.get('name', None)   
    id = data.get('id', None)   

    if not name or not stage:
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
    
    if id:
        pipelineStatus = PipelineStatus.getById(id, stage)
        if not pipelineStatus:
            return {
                'code': 400,
                'msg': 'Pipeline Status not found'
            }
        if pipelineStatus.name != name and PipelineStatus.getByName(name=name, stage=stage):
            return {
                'code': 400,
                'msg': 'Pipeline Status with name '+name+' already exists.'
            } 
    else:
        if PipelineStatus.getByName(name=name, stage=stage):
            return {
                'code': 400,
                'msg': 'Pipeline Status with name '+name+' already exists.'
            } 

        pipelineStatus = PipelineStatus()    
        pipelineStatus.stage = stage

    
    pipelineStatus.name = name
    pipelineStatus.save()

    return getPipelineStatus(request)

def deletePipelineStatus(request): 

    id = request.GET.get('id', None)
    company = Company.getByUser(request.user)

    if id:
        pipelineStatus = PipelineStatus.getByIdAndCompany(id, company)
        if not pipelineStatus:
            return {
                'code': 400,
                'msg': 'Pipeline Status not found'
            }

        pipelineStatus.delete()
        return {
            'code': 200,
            'msg': 'Pipeline Status deleted succesfully!',
            'data': getPipelineStatus(request)['data']
        }

    return {
        'code': 400,
        'msg': 'Invalid request'
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
    name = data.get('name', None)   
    type = data.get('type', None)   
    category = data.get('category', None)   
    subject = data.get('subject', None)   
    message = data.get('message', None)   

    if not name or not category or not type or not type in EmailTemplate.EMAIL_TYPES or not message or not subject:
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
        if email.name != name and EmailTemplate.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Email Template with name '+name+' already exists.'
            } 
    else:
        if EmailTemplate.getByName(name=name, company=company):
            return {
                'code': 400,
                'msg': 'Email Template with name '+name+' already exists.'
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
    
    email.name = name
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