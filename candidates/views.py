from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .import helper
from common.utils import makeResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ApplyApi(APIView):

    def post(self, request):
        data = helper.applyJob(request)
        return makeResponse(data)

class ApplyJobApi(APIView):

    def post(self, request):
        data = helper.applyWebformJob(request)
        return makeResponse(data)        

class ApplicationsApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getApplications(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.updateApplication(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteApplication(request)
        return makeResponse(data)    

class CandidatesApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getCandidates(request)
        return makeResponse(data)

class ApplicationsResumeApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.updateResume(request)
        return makeResponse(data)  

class ApplicationsResumeParseApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.parseResume(request)
        return makeResponse(data)                 

class CandidateDetailsApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.candidateDetails(request)
        return makeResponse(data)                

class NoteApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getAllNotes(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveNote(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteNote(request)
        return makeResponse(data)            