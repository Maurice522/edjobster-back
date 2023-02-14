from rest_framework import serializers
from .models import Account, Company
from settings.models import Department, Designation
from django.conf import settings

class AccountSerializer(serializers.ModelSerializer):

    department = serializers.SerializerMethodField()
    designation = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    def get_department(self, obj):
        # if 'department' in obj:
        #     department = Department.getByDid(obj['department'])
        #     if department:
        #         return department.name
        return None

    def get_designation(self, obj):
        # if 'designation' in obj:
        #     designation = Designation.getByDid(obj['designation'])
        #     if designation:
        #         return designation.name
        return None

    class Meta:
        model = Account
        fields = ['account_id', 'photo', 'first_name', 'last_name', 'role', 'company_id', 'mobile', 'email',
                  'is_active', 'verified', 'department', 'designation']


    def get_photo(self, obj):
        # if 'photo' in obj:
        #     return obj['photo']
            # return settings.PHOTO_FILE_URL+obj['photo']['name'][19:]
        return None  

class CompanySerializer(serializers.ModelSerializer):

    admin_id = serializers.IntegerField(source='admin.id')
    admin_first_name = serializers.CharField(source='admin.first_name')
    admin_last_name = serializers.CharField(source='admin.last_name')
    admin_email = serializers.CharField(source='admin.email')

    city_id = serializers.IntegerField(source='city.id')
    city_name = serializers.CharField(source='city.name')
    state_id = serializers.IntegerField(source='city.state.id')
    state_name = serializers.CharField(source='city.state.name')
    country_id = serializers.IntegerField(source='city.state.country.id')
    country_name = serializers.CharField(source='city.state.country.name')
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'logo', 'name', 'domain', 'website', 'description', 'admin_id', 'admin_first_name',
                  'admin_last_name', 'admin_email', 'address', 'landmark', 'pincode', 'loc_lat', 'loc_lon', 'city_id', 'city_name', 'state_id', 'state_name',
                  'country_id', 'country_name', 'tag']

    def get_logo(self, obj):
        if obj.logo:
            return settings.LOGO_FILE_URL+obj.logo.name[22:]
        return None    