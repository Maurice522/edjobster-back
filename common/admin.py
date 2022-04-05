from django.contrib import admin

from .models import Country, State, City, NoteType
my_modules = [Country, State, City, NoteType]

admin.site.register(my_modules)
