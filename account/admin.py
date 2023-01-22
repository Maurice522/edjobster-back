from django.contrib import admin

from .models import Account, Company, TokenEmailVerification
# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'first_name','last_name','role','company')
    list_filter = ("account_id",)
    search_fields = ['role', 'mobile', 'company']

admin.site.register(Account, AccountAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display=('admin','name','id','website')
    list_filter=('id',)
admin.site.register(Company,CompanyAdmin)

class TokenEmailVerificationAdmin(admin.ModelAdmin):
    list_display=('id','user','is_verified')
    list_filter=('created',)
admin.site.register(TokenEmailVerification,TokenEmailVerificationAdmin)