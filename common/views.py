from django.shortcuts import render
import os
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from .import helper
from .utils import makeResponse


class DataApi(APIView):
    def get(self, request):
        data = helper.getAllData()
        return makeResponse(data)
    

class CountryApi(APIView):
    def get(self, request):
        data = helper.getCountries(request)
        return makeResponse(data)


class StatesApi(APIView):
    def get(self, request):
        data = helper.getStatesForCountry(request)
        return makeResponse(data)


class CitiesApi(APIView):
    def get(self, request):
        data = helper.getCitiesForState(request)
        return makeResponse(data)

class NotesApi(APIView):
    def get(self, request):
        data = helper.getNoteTypes(request)
        return makeResponse(data)