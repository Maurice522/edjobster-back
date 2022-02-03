from django.contrib import admin

from .models import Country, State, City
my_modules = [Country, State, City]

admin.site.register(my_modules)
