from rest_framework import serializers
from .models import Account, Company
from settings.models import Department, Designation

class AccountSerializer(serializers.ModelSerializer):

    department = serializers.SerializerMethodField()
    designation = serializers.SerializerMethodField()

    def get_department(self, obj):
        if obj.department:
            department = Department.getByDid(obj.department)
            if department:
                return department.name
        return None

    def get_designation(self, obj):
        if obj.designation:
            designation = Designation.getByDid(obj.designation)
            if designation:
                return designation.name
        return None

    class Meta:
        model = Account
        fields = ['account_id', 'photo', 'first_name', 'last_name', 'role', 'company_id', 'mobile', 'email',
                  'is_active', 'verified', 'department', 'designation']


class CompanySerializer(serializers.ModelSerializer):

    admin_id = serializers.IntegerField(source='admin.id')
    admin_first_name = serializers.CharField(source='admin.first_name')
    admin_last_name = serializers.CharField(source='admin.last_name')
    admin_email = serializers.CharField(source='admin.email')

    city_id = serializers.IntegerField(source='city.id')
    city_name = serializers.CharField(source='city.name')
    state_id = serializers.IntegerField(source='state.id')
    state_name = serializers.CharField(source='state.name')
    country_id = serializers.IntegerField(source='country.id')
    country_name = serializers.CharField(source='country.name')

    class Meta:
        model = Company
        fields = ['id', 'logo', 'name', 'domain', 'admin_id', 'admin_first_name',
                  'admin_last_name', 'admin_email', 'address', 'landmark', 'pincode', 'loc_lat', 'loc_lon', 'city_id', 'city_name', 'state_id', 'state_name',
                  'country_id', 'country_name']
