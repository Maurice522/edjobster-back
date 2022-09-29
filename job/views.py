from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .import helper
from common.utils import makeResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class AssesmentCategoryApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getAssesmentCategories(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveAssesmentCategory(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteAssesmentCategory(request)
        return makeResponse(data)    


class AssesmentQuestionApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getAssesmentDetails(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveAssesmentQuestion(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteAssesmentQuestion(request)
        return makeResponse(data)    

class AssesmentApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getAssesments(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveAssesment(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteAssesment(request)
        return makeResponse(data)           

class JobApi(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getJobs(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveJob(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteJob(request)
        return makeResponse(data)             


class JobDetailsApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getJobDetails(request)
        return makeResponse(data)

class BoardApi(APIView):

    def post(self, request):
        data = helper.getJobsBoard(request)
        return makeResponse(data)        