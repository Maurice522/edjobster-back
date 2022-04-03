from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .import helper
from common.utils import makeResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class LocationsApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getLocations(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveLocation(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteLocation(request)
        return makeResponse(data)        

class DepartmentApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getDepartments(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveDepartment(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteDepartment(request)
        return makeResponse(data)                

class DesignationApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getDesignations(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveDesignation(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteDecignation(request)
        return makeResponse(data)             

class DegreeApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getDegrees(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveDegree(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteDegree(request)
        return makeResponse(data)                     

class PipelineDetails(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getPipelineStageDetails(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.savePipelineStatus(request)
        return makeResponse(data)


class PipelineStageApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getPipelineStages(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.savePipelineStage(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deletePipelineStage(request)
        return makeResponse(data)             

class PipelinesApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getPipelines(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.savePipeline(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deletePipeline(request)
        return makeResponse(data)                     



class EmailFieldApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getEmailFileds(request)
        return makeResponse(data)

class EmailCategoryApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getEmailCategories(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveEmailCategory(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteEmailCategory(request)
        return makeResponse(data)   

class EmailTemplateApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getEmailTemplates(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveEmailTemplate(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteEmailTemmplate(request)
        return makeResponse(data)           