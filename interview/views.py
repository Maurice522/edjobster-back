from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .import helper
from common.utils import makeResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class InterviewApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getInterviews(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.scheduleInterview(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.delteInterview(request)
        return makeResponse(data)                

class InterviewDetailsApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.interviewDetails(request)
        return makeResponse(data)

class LatestInterviewDetailsApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.latestInterviewDetails(request)
        return makeResponse(data)