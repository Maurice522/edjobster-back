from os import name
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from common.utils import isValidUuid
from common.models import Country, State, City
from datetime import datetime, timedelta


class Account(AbstractUser):

    USER = 'U'
    ADMIN = 'A'

    ROLE_LIST = [USER, ADMIN]

    ROLE = [
        (USER, 'User'),
        (ADMIN, 'Admin')
    ]

    account_id = models.UUIDField(
        primary_key=False, unique=True, editable=False)
    role = models.CharField(max_length=1, choices=ROLE, default=USER)
    mobile = models.CharField(
        max_length=20, unique=False, null=True, blank=True)
    photo = models.ImageField(
        upload_to='media/users/photos', default=None, null=True, blank=True)
    verified = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    company_id = models.UUIDField(default=None, null=True, blank=True)
    designation = models.IntegerField(default=None, null=True, blank=True)
    department = models.IntegerField(default=None, null=True, blank=True)
    addedBy = models.UUIDField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.account_id:
            self.account_id = uuid.uuid4()
        if self.email != self.username:
            self.email = self.username
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.mobile)+' '+str(self.email)[:20]

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    @staticmethod
    def getById(account_id):
        if Account.objects.filter(account_id=account_id).exists():
            return Account.objects.get(account_id=account_id)
        return None

    @staticmethod
    def getByIdAndCompany(account_id, company):
        if Account.objects.filter(company_id=company.id, account_id=account_id).exists():
            return Account.objects.get(account_id=account_id)
        return None        

    @staticmethod
    def getByAll():
        return Account.objects.all()

    @staticmethod
    def getByMobile(mobile):
        if Account.objects.filter(mobile=mobile).exists():
            return Account.objects.get(mobile=mobile)
        return None

    @staticmethod
    def getByEmail(email):
        if Account.objects.filter(email=email).exists():
            return Account.objects.get(email=email)
        return None

    @staticmethod
    def getMembers(company_id):
        return Account.objects.filter(company_id=company_id)

    @staticmethod
    def getByLogin(mobile, password):
        if Account.objects.filter(mobile=mobile, password=password).exists():
            return Account.objects.get(mobile=mobile)
        return None


class Company(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    admin = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=100, unique=False, null=True, blank=True)
    logo = models.ImageField(
        upload_to='media/companies/logos', default=None, null=True, blank=True)
    domain = models.CharField(
        max_length=50, unique=False, null=False, blank=False)
    gst_no = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=15, null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)
    address = models.TextField(max_length=500, blank=False, null=False)
    landmark = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.IntegerField(default=None, null=True, blank=True)
    country = models.ForeignKey(
        Country, default=None, null=True, verbose_name='Country', on_delete=models.SET_NULL)
    state = models.ForeignKey(
        State, default=None, null=True, verbose_name='State', on_delete=models.SET_NULL)
    city = models.ForeignKey(
        City, default=None, null=True, verbose_name='city', on_delete=models.SET_NULL)
    loc_lat = models.CharField(
        max_length=20, default=None, null=True, blank=True)
    loc_lon = models.CharField(
        max_length=20, default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.id) + ' ' + str(self.name)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    @staticmethod
    def getByUser(user):
        if Company.objects.filter(id=user.company_id).exists():
            return Company.objects.get(id=user.company_id)
        return None

    @staticmethod
    def getByDomain(domain):
        if Company.objects.filter(domain=domain).exists():
            return Company.objects.get(domain=domain)
        return None        

    @staticmethod
    def getById(id):
        if Company.objects.filter(id=id).exists():
            return Company.objects.get(id=id)
        return None

    @staticmethod
    def getByOwner(account):
        if Company.objects.filter(owner=account).exists():
            return Company.objects.get(owner=account)
        return None


class TokenResetPassword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        Account, default=1, verbose_name="User", on_delete=models.CASCADE
    )
    active = models.BooleanField(default=True)
    validity = models.DateTimeField()
    created = models.DateTimeField(
        auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id) + " : " + str(self.user.id)[:50]

    @staticmethod
    def getByTokenId(id):
        try:
            if TokenResetPassword.objects.filter(id=id).exists():
                return TokenResetPassword.objects.get(id=id)
            return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getByUser(user):
        try:
            if TokenResetPassword.objects.filter(user=user).exists():
                return TokenResetPassword.objects.get(user=user)
            return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def createToken(user):
        token = TokenResetPassword.getByUser(user)

        if not token:
            token = TokenResetPassword()
            token.user = user

        validity = datetime.now() + timedelta(hours=24)
        token.validity = validity
        token.active = True
        token.save()
        return token

    class Meta:
        verbose_name = "Token Reset Password"
        verbose_name_plural = "Tokens Reset Password"


class TokenEmailVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        Account, default=1, verbose_name="User", on_delete=models.CASCADE
    )
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(
        auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id) + " : " + str(self.user.id)[:50]

    @staticmethod
    def getByTokenId(id):
        try:
            if TokenEmailVerification.objects.filter(id=id).exists():
                return TokenEmailVerification.objects.get(id=id)
            return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getByUser(user):
        try:
            if TokenEmailVerification.objects.filter(user=user).exists():
                return TokenEmailVerification.objects.get(user=user)
            return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def createToken(user):
        token = TokenEmailVerification.getByUser(user)
        if not token:
            token = TokenEmailVerification()
            token.user = user
        token.is_verified = False
        token.save()
        return token

    class Meta:
        verbose_name = "Token Email Verification"
        verbose_name_plural = "Tokens Email Verification"
