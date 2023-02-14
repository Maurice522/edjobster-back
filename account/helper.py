import email
from xml import dom
from .models import Account, Company, TokenEmailVerification, TokenResetPassword
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializer import AccountSerializer, CompanySerializer
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from common.mail_utils import EmailVerificationMailer, ResetPasswordMailer
from common.encoder import decode
from common.utils import isValidUuid, getDomainFromEmail
from common.models import Country, State, City
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import os


def checkCompany(request):

    email = request.GET.get('email', None)

    if not email:
        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    if Account.getByEmail(email):
        return {
            'code': 400,
            'msg': 'Email already exists'
        } 

    domain = getDomainFromEmail(email)

    if not domain:
        return {
            'code': 400,
            'msg': 'Invalid email address'
        }

    company = Company.getByDomain(email)

    if company:
        return {
            'code': 200,
            'msg': 'Company is already exists',
            'data': {
                'name': company.name,
                'domain': company.domain,
            }
        }
    return {
        'code': 200,
        'msg': 'New account'
    }

def signupUserAccount(request):

    data = request.data

    firstName = data.get('first_name', None)
    lastName = data.get('last_name', None)
    mobile = data.get('mobile', None)
    email = data.get('email', None)

    if not firstName or not lastName or not mobile or not email:

        return {
            'code': 400,
            'msg': 'invalid request'
        }

    domain = getDomainFromEmail(email)

    if not domain:
        return {
            'code': 400,
            'msg': 'Invalid email address'
        }

    if Account.getByMobile(mobile):
        return {
            'code': 400,
            'msg': 'Mobile already exists'
        }

    if Account.getByEmail(email):
        return {
            'code': 400,
            'msg': 'Email already exists'
        } 

    account = Account()
    account.first_name = firstName
    account.last_name = lastName
    account.mobile = mobile
    account.email = email
    account.role = Account.USER
    account.username = email

    account.is_staff = False
    account.is_active = True
    account.is_superuser = False
    account.verified = False
    account.save()       

    token = TokenEmailVerification.createToken(account)
    sendMail = EmailVerificationMailer(token)
    sendMail.start()

    data = {
        'code': 200,
        'msg': 'Account created successfully. We have sent you email to verify your account.',
    }

    return data        

def signUpAccount(request):

    data = request.data

    print('data', request.data)

    role = data.get('role', None)
    firstName = data.get('first_name', None)
    lastName = data.get('last_name', None)
    mobile = data.get('mobile', None)
    email = data.get('email', None)
    companyName = data.get('company', None)

    pincode = data.get('pincode', None)
    gstNo = data.get('gst_no', None)
    locLat = data.get('loc_lat', None)
    locLon = data.get('loc_lon', None)
    address = data.get('address', None)
    landmark = data.get('landmark', None)
    cityId = data.get('city', None)

    print('info', firstName, lastName, mobile, email, companyName,
          pincode, address, landmark, cityId)

    if not firstName or not lastName or not mobile or not email or not companyName or not pincode or not address or not landmark or not cityId:

        return {
            'code': 400,
            'msg': 'invalid request'
        }

    domain = getDomainFromEmail(email)

    if not domain:
        return {
            'code': 400,
            'msg': 'Invalid email address'
        }

    account = None

    if Account.getByMobile(mobile):
        return {
            'code': 400,
            'msg': 'Mobile already exists'
        }

    if Account.getByEmail(email):
        return {
            'code': 400,
            'msg': 'Email already exists'
        }

    mCity = City.getById(cityId)

    account = Account()
    account.first_name = firstName
    account.last_name = lastName
    account.mobile = mobile
    account.email = email
    account.role = Account.ADMIN
    account.username = email

    account.is_staff = False
    account.is_active = True
    account.is_superuser = False
    account.verified = False
    account.save()

    company = Company()
    company.admin = account
    company.name = companyName
    company.domain = domain
    company.pincode = pincode
    company.gst_no = gstNo
    company.loc_lat = locLat
    company.loc_lon = locLon
    company.address = address
    company.landmark = landmark
    company.state = mCity.state
    company.country = mCity.state.country
    company.city = mCity
    company.save()

    account.company_id = company.id
    account.save()

    token = TokenEmailVerification.createToken(account)
    sendMail = EmailVerificationMailer(token)
    sendMail.start()

    data = {
        'code': 200,
        'msg': 'Account created successfully. We have sent you email to verify your account.',
    }

    return data


def signInAccount(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return {
            'code': 400,
            'msg': 'username and password required'
        }
    print(username, password)
    account = Account.objects.filter(username=username).first()

    if not account:
        return {
            'code': 400,
            'msg': 'Invalid username and password'
        }

    if not account.verified:
        token = TokenEmailVerification.createToken(account)
        sendMail = EmailVerificationMailer(token)
        sendMail.start()
        return {
            'code': 400,
            'msg': 'Your account is not verified. Please verify your email address'
        }

    if not account.is_active:
        return {
            'code': 400,
            'msg': 'Your account is not active. Please contact support for more details'
        }

    # if not account.approved:
    #     return {
    #         'code': 400,
    #         'msg': 'Your account is not approved by admin. You can come back later to check or you can reach out to the admin to approve and activate your account'
    #     }        

    # if not account.check_password(password):
    #     return {
    #         'code': 400,
    #         'msg': 'Invalid username and password!'
    #     }

    serialized_account = AccountSerializer(account)

    company = Company.getById(account.company_id)

    serialized_company = CompanySerializer(company)

    refresh = RefreshToken.for_user(account)
    access = AccessToken.for_user(account)

    print('account', account)
    print('refresh', refresh)
    print('access', access)

    data = {
        'code': 200,
        'refresh': str(refresh),
        'access': str(access),
        'account': serialized_account.data,
        'company': serialized_company.data,
    }

    print ('return', data)

    return data


def getAccountProfile(request):

    account = request.user

    serialized_account = AccountSerializer(account).data

    print('company', account.company_id)
    company = Company.getById(account.company_id)
    print('company', company)
    serialized_company = CompanySerializer(company)

    data = {
        'code': 200,
        'account': serialized_account,
        'company': serialized_company.data,
    }

    return data


def getCompanyInfo(request):

    account = request.user

    company = Company.getById(account.company_id)
    print('company', company)
    serialized_company = CompanySerializer(company)

    data = {
        'code': 200,
        'company': serialized_company.data,
    }

    return data


def updateCompanyInfo(request):

    account = request.user

    if not account or account.role != Account.ADMIN:
        return {
            'code': 400,
            'msg': 'Access denied!'
        }

    company = Company.getById(account.company_id)
    if not company:
        return {
            'code': 400,
            'msg': 'Company not found!'
        }

    data = request.data

    print('data', request.data)
    companyName = data.get('company', None)
    website = data.get('website', None)
    description = data.get('description', None)
    pincode = data.get('pincode', None)
    gstNo = data.get('gst_no', None)
    locLat = data.get('loc_lat', None)
    locLon = data.get('loc_lon', None)
    address = data.get('address', None)
    landmark = data.get('landmark', None)
    tag = data.get('tag', None)
    cityId = data.get('city', None)

    print('info', companyName, pincode, address, landmark, cityId)

    if not companyName or not pincode or not address or not landmark or not cityId or not website or not description:

        return {
            'code': 400,
            'msg': 'invalid request'
        }

    account = None

    mCity = City.getById(cityId)

    if not mCity:
        return {
            'code': 400,
            'msg': 'City not found'
        }

    mState = mCity.state
    mCountry = mState.country

    company.tag = tag
    company.name = companyName
    company.website = website
    company.description = description
    company.pincode = pincode
    company.gst_no = gstNo
    company.loc_lat = locLat
    company.loc_lon = locLon
    company.address = address
    company.landmark = landmark
    company.state = mState
    company.country = mCountry
    company.city = mCity
    company.save()

    companyData = CompanySerializer(company)
    return {
        'code': 200,
        'company': companyData.data,
    }


def updateAccount(request):

    account = request.user

    data = request.data

    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)
    mobile = data.get('mobile', None)
    email = data.get('email', None)

    if not first_name or not last_name or not email or not mobile:

        return{
            'code': 404,
            'msg': 'Invalid Request !!!'
        }

    account.first_name = first_name
    account.last_name = last_name

    if mobile:
        new_account = Account.getByMobile(mobile)

        if new_account:
            if new_account.id != account.id:
                return{
                    'code': 404,
                    'msg': 'Mobile Number Already Exist !!! '
                }

    new_account = Account.getByEmail(email)
    if new_account:
        if account.id != new_account.id:
            return {
                'code': 400,
                'msg': 'Email Already Exist !!! '
            }

    account.email = email
    account.username = email
    account.mobile = mobile
    account.save()

    return{
        'code': 200,
        'account': {
            'first_name': account.first_name,
            'last_name': account.last_name,
            'email': account.email,
            'mobile': account.mobile,
        }
    }


def updateMobile(request):

    data = request.data

    account = request.user

    mobile = data.get('mobile', None)

    if not mobile:
        return{
            'code': 400,
            'msg': ' Access denied'
        }

    if not account:

        return{
            'code': 404,
            'msg': 'Account not found !!! '
        }

    new_account = Account.getByMobile(mobile)

    if new_account:

        if new_account.id != account.id:

            return{
                'code': 404,
                'msg': 'Ooppsss , Mobile Number Already Exist !!! '
            }

    account.username = mobile

    account.save()

    return{
        'code': 200,
        'msg': 'Mobile number is succesfully Updated'
    }

def updateLogo(request):

    account = request.user

    if account.role != Account.ADMIN:
        return {
            'code': 400,
            'msg': 'Access Denied!'
        }

    company = Company.getById(account.company_id)

    if not company:
        return {
            'code': 400,
            'msg': 'Company doest exists!'
        }

    logo = request.FILES['logo']
    if logo:

        try:
            if company.logo != None:
                if os.path.isfile(company.logo.path):
                    os.remove(company.logo.path)
        except Exception:
            pass
        company.logo = logo
        company.save()

        return {
            'code': 200,
            'msg': 'Logo updated successfully'
        }

    return {
        'code': 400,
        'msg': 'Bad request'
    }


def checkMobile(request):

    data = request.data

    account = request.user

    mobile = data.get('mobile', None)
    exists = data.get('exists', False)

    if not mobile:
        return{
            'code': 400,
            'msg': ' Access denied'
        }

    new_account = Account.getByMobile(mobile)

    msg = ''
    code = 0
    if new_account:
        if exists:
            code = 200
        else:
            code = 400

        msg = 'Mobile already exist'
    else:
        if exists:
            code = 400
        else:
            code = 200

        msg = 'Account not exists'

    return {
        'code': code,
        'msg': msg
    }


def checkEmail(request):

    data = request.data

    account = request.user

    email = data.get('email', None)

    if not email:
        return{
            'code': 400,
            'msg': ' Access denied'
        }

    new_account = Account.getByEmail(email)

    if new_account:
        return {
            'code': 400,
            'msg': 'Email Already Exist !!!'
        }

    return {
        'code': 200,
        'msg': 'Email not registerd'

    }


def resetPassword(request):

    account = request.user
    data = request.data

    #password = request.POST.get('password', None)
    token = data.get('token', None)
    password = data.get('password', None)

    if not token or not password:

        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    print('token', token)
    try:
        tokenId = decode(token)
    except:
        return {
            'code': 400,
            'msg': 'Bad request'
        }

    print('token', tokenId)

    if not isValidUuid(tokenId):
        return {
            'code': 400,
            'msg': 'Bad request'
        }

    token = TokenResetPassword.getByTokenId(tokenId)

    if not token:
        return {
            'code': 400,
            'msg': 'Bad request'
        }

    account = token.user
    account.set_password(password)
    account.save()
    token.delete()

    return{
        'code': 200,
        'msg': 'New password Set succesfully',
    }


def changePassword(request):

    account = request.user
    data = request.data

    #password = request.POST.get('password', None)
    old_password = data.get('old_password', None)
    new_password = data.get('new_password', None)

    if not old_password or not new_password:

        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    if not account.check_password(old_password):

        return {
            "code": 400,
            "msg": "Old password doesnt match"
        }

    account.set_password(new_password)

    account.save()

    return{
        'code': 200,
        'msg': 'New password Set succesfully',
    }


def forgotPasswordAccount(request):
    data = request.data

    email = data.get('email', None)

    if not email:

        return {
            'code': 400,
            'msg': 'Invalid request'
        }

    account = Account.getByEmail(email)

    if account:

        token = TokenResetPassword.createToken(account)
        sendMail = ResetPasswordMailer(token)
        sendMail.start()

        return{
            'code': 200,
            'msg': 'We have sent you email to reset password.',
        }
    return {
        'code': 400,
        'msg': 'Account not found !!!'
    }


def listMembrs(request):
    account = request.user

    members = Account.getMembers(account.company_id)

    accountSerializer = AccountSerializer(members, many=True)

    return {
        'code': 200,
        'list': accountSerializer.data
    }


def addMember(request):

    adminUser = request.user

    data = request.data

    print('addMember', request.data)

    firstName = data.get('first_name', None)
    lastName = data.get('last_name', None)
    mobile = data.get('mobile', None)
    email = data.get('email', None)
    role = data.get('role', None)

    department = data.get('department', None)
    designation = data.get('designation', None)

    if not firstName or not lastName or not email or not role or not designation or not designation:

        return {
            'code': 404,
            'msg': 'invalid request'
        }

    if adminUser.role != Account.ADMIN:
        return {
            'code': 400,
            'msg': 'Only admin can add members'
        }

    if mobile:
        if Account.getByMobile(mobile):
            return {
                'code': 400,
                'msg': 'Mobile already exists'
            }

    if Account.getByEmail(email):
        return {
            'code': 400,
            'msg': 'Email already exists'
        }

    if role not in [Account.ADMIN, Account.USER]:
        return {
            'code': 400,
            'msg': 'Invalid role'
        }

    account = Account()
    account.first_name = firstName
    account.last_name = lastName
    account.mobile = mobile
    account.email = email
    account.role = role
    account.username = email
    account.department = department
    account.designation = designation
    account.addedBy = adminUser.account_id

    account.is_staff = False
    account.is_active = True
    account.is_superuser = False
    account.verified = True

    if request.FILES != None:
        print("files")
        print(request.FILES)
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            account.photo = photo    

    account.save()

    account.company_id = adminUser.company_id
    account.save()

    token = TokenEmailVerification.createToken(account)
    sendMail = EmailVerificationMailer(token)
    sendMail.start()

    data = {
        'code': 200,
        "msg": "Account created successfully! We have sent a verification email to " + email + ".\nPlease check and verify your account.",
    }

    return data


def updateMember(request):

    adminUser = request.user

    data = request.data

    print('updateMember', data)

    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)
    mobile = data.get('mobile', None)
    email = data.get('email', None)
    role = data.get('role', None)

    department = data.get('department', None)
    designation = data.get('designation', None)

    accountId = data.get('account_id', None)

    if not first_name or not last_name or not email or not accountId or role not in [Account.ADMIN, Account.USER] or not department or not designation:
        return{
            'code': 404,
            'msg': 'Invalid Request !!!'
        }

    if adminUser.role != Account.ADMIN:
        return {
            'code': 400,
            'msg': 'Only admin can add members'
        }

    account = Account.getById(accountId)
    if not account:
        return {
            'code': 400,
            'msg': 'Member not found'
        }

    account.first_name = first_name
    account.last_name = last_name

    if mobile:
        new_account = Account.getByMobile(mobile)

        if new_account:
            if new_account.id != account.id:
                return{
                    'code': 404,
                    'msg': 'Mobile Number Already Exist !!! '
                }

    new_account = Account.getByEmail(email)
    if new_account:
        if account.id != new_account.id:
            return {
                'code': 400,
                'msg': 'Email Already Exist !!! '
            }

    account.email = email
    account.username = email
    account.mobile = mobile
    account.role = role
    account.department = department
    account.designation = designation
    photo = None

    if request.FILES != None:
        if photo in request.FILES:
            photo = request.FILES['photo']
            try:
                if updateAccount.photo != None:
                    if os.path.isfile(updateAccount.photo.path):
                        os.remove(updateAccount.photo.path)
            except Exception:
                pass
            updateAccount.photo = photo

    account.save()

    return{
        'code': 200,
        'msg': 'Member details updated sucessfully!'
    }

def updatePhoto(request):

    account = request.user

    if request.FILES != None and 'photo' in request.FILES :
        photo = request.FILES['photo']
        if photo:
            try:
                if account.photo != None:
                    if os.path.isfile(account.photo.path):
                        os.remove(account.photo.path)
            except Exception:
                pass
            account.photo = photo
            account.save()

            return {
                'code': 200,
                'msg': 'Photo updated successfully'
            }

    return {
        'code': 400,
        'msg': 'Profile photo required'
    }

def updateMemberPhoto(request):

    adminUser = request.user

    if adminUser.role != Account.ADMIN:
        return {
            'code': 400,
            'msg': 'access denied!'
        }

    accountId = request.data.get('account_id', None)
    if not accountId:
        return {
            'code': 400,
            'msg': 'Bad request!'
        }
    account = Account.getById(accountId)
    if not account:
        return {
            'code': 400,
            'msg': 'Member not found'
        }

    if request.FILES != None and 'photo' in request.FILES :
        photo = request.FILES['photo']
        if photo:
            try:
                if account.photo != None:
                    if os.path.isfile(account.photo.path):
                        os.remove(account.photo.path)
            except Exception:
                pass
            account.photo = photo
            account.save()

            return {
                'code': 200,
                'msg': 'Photo updated successfully'
            }

    return {
        'code': 400,
        'msg': 'Profile photo required'
    }    

def updateMemberRole(request):
    
    adminUser = request.user
    data = request.data
    print('activate >> ', data)

    role = data.get('role', None)
    accountId = data.get('account_id', None)

    if adminUser.role != Account.ADMIN:
        return {
            'code': 400,
            'msg': 'Only admin can add members'
        }

    print('activate >> ', adminUser.account_id, accountId)

    if not role or not accountId or role not in Account.ROLE_LIST:
        return {
            'code': 400,
            'msg': 'Bad request!'
        }

    account = Account.getById(accountId)
    if not account:
        return {
            'code': 400,
            'msg': 'Member not found'
        }

    print('activate >> ', adminUser, account)

    if adminUser == account:
        return {
            'code': 400,
            'msg': 'Cannot change role of yourself'
        }
    
    account.role = role

    return {
        'code': 200,
        'msg': 'Role updated successfully'
    }

def activateMember(request):
    
    adminUser = request.user
    data = request.data
    print('activate >> ', data)

    status = data.get('status', None)
    accountId = data.get('account_id', None)

    if adminUser.role != Account.ADMIN:
        return {
            'code': 400,
            'msg': 'Only admin can add members'
        }

    print('activate >> ', adminUser.account_id, accountId)

    if not status or not accountId:
        return {
            'code': 400,
            'msg': 'Bad request!'
        }

    account = Account.getById(accountId)
    if not account:
        return {
            'code': 400,
            'msg': 'Member not found'
        }

    print('activate >> ', adminUser, account)

    if adminUser == account:
        return {
            'code': 400,
            'msg': 'Cannot deactivate account of yourself'
        }

    if status not in ['A', 'D']:
        return {
            'code': 400,
            'msg': 'Invalid status'
        }

    msg = ''
    if status == 'A':
        msg = 'Account activated successfully!'
        account.is_active = True
    else:
        msg = 'Account deactivated successfully!'
        account.is_active = False

    account.save()

    return {
        'code': 200,
        'msg': msg
    }

def approveMember(request):
 
    adminUser = request.user
    data = request.data
    print('approveMember >> ', data)

    status = data.get('status', None)
    accountId = data.get('account_id', None)

    if adminUser.role != Account.ADMIN:
        return {
            'code': 400,
            'msg': 'Only admin can add members'
        }

    print('activate >> ', adminUser.account_id, accountId)

    if not status or not accountId:
        return {
            'code': 400,
            'msg': 'Bad request!'
        }

    account = Account.getById(accountId)
    if not account:
        return {
            'code': 400,
            'msg': 'Member not found'
        }

    print('activate >> ', adminUser, account)

    if adminUser == account:
        return {
            'code': 400,
            'msg': 'Cannot deactivate account of yourself'
        }

    if status not in ['A', 'D']:
        return {
            'code': 400,
            'msg': 'Invalid status'
        }

    msg = ''
    if status == 'A':
        msg = 'Account activated successfully!'
        account.verified = True
    else:
        msg = 'Account deactivated successfully!'
        account.verified = False

    account.save()

    return {
        'code': 200,
        'msg': msg
    }    


def deleteMember(request):
    adminUser = request.user
    account_id = request.GET.get('account_id', None)

    if adminUser.role != Account.ADMIN:
        return {
            'code': 400,
            'msg': 'Only admin can add members'
        }

    if not account_id:
        return {
            'code': 400,
            'msg': 'Bad request!'
        }

    if adminUser.account_id == account_id:
        return {
            'code': 400,
            'msg': 'Cannot delete account of yourself'
        }
    company = Company.getByUser(adminUser)
    account = Account.getByIdAndCompany(account_id, company)
    if not account:
        return {
            'code': 400,
            'msg': 'Member not found'
        }

    if account.company_id != adminUser.company_id:
        return {
            'code': 400,
            'msg': 'Access denied!'
        }

    account.delete()

    return {
        'code': 200,
        'msg': 'Member deleted successfully!'
    }


def activateAccount(request):

    tokenId = request.data.get('token')
    password = request.data.get('password')

    print('token', tokenId)
    if not tokenId or not password:
        return {
            'code': 400,
            'msg': 'Bad request'
        }

    try:
        tokenId = decode(tokenId)
    except:
        return {
            'code': 400,
            'msg': 'Bad request'
        }
    if not isValidUuid(tokenId):
        return {
            'code': 400,
            'msg': 'Bad request'
        }

    token = TokenEmailVerification.getByTokenId(tokenId)
    print("token", token)

    if not token or not password:
        return {
            'code': 400,
            'msg': 'Bad request!'
        }

    if token.user:
        user = token.user
        user.verified = True
        user.set_password(password)
        user.save()
        token.delete()

        return {
            'code': 200,
            'msg': 'Your account has been successfully created, but it is not active yet. The admin of your institute needs to approve and activate your account. You can come back later to check or you can reach out to the admin to approve and activate your account'
        }

    return {
        'code': 400,
        'msg': 'Bad request!!'
    }


def verifyToken(request):
    tokenId = request.GET.get('token', None)

    print('token', tokenId)
    if tokenId:
        tokenId = decode(tokenId)

    if not isValidUuid(tokenId):
        return {
            'code': 400,
            'msg': 'Bad request'
        }

    token = TokenEmailVerification.getByTokenId(tokenId)
    print("token", token)

    if not token:
        return {
            'code': 400,
            'msg': 'Bad request!'
        }

    if token.user:
        user = token.user

        return {
            'code': 200,
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        }

    return {
        'code': 400,
        'msg': 'Bad request!!'
    }


def activateEmail(tokenId):
    return TokenEmailVerification.getByTokenId(decode(tokenId))


def approveVerifyMember(request):
 
    adminUser = request.user
    data = request.data
    print('approving and Verifying >> ', data)

    status = data.get('status', None)
    accountId = data.get('account_id', None)

    if adminUser.role != Account.ADMIN:
        return {
            'code': 400,
            'msg': 'Only admin can add members'
        }

    print('activate >> ', adminUser.account_id, accountId)

    if not status or not accountId:
        return {
            'code': 400,
            'msg': 'Bad request!'
        }

    account = Account.getById(accountId)
    if not account:
        return {
            'code': 400,
            'msg': 'Member not found'
        }

    print('activate >> ', adminUser, account)

    if adminUser == account:
        return {
            'code': 400,
            'msg': 'Cannot deactivate account of yourself'
        }

    if status not in ['A', 'D']:
        return {
            'code': 400,
            'msg': 'Invalid status'
        }

    msg = ''
    if status == 'A':
        msg = 'Account activated successfully!'
        account.approved = True
        account.verified = True
    else:
        msg = 'Account deactivated successfully!'
        account.approved = False
        account.verified = False

    account.save()

    return {
        'code': 200,
        'msg': msg
    }    