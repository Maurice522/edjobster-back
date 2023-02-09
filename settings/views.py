from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .import helper
from .models import EmailTemplate
from .serializer import EmailTemplateSerializer
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

from rest_framework import mixins, generics
from .models import Location
from .serializer import LocationSerializer

class LocationsDetailApi(mixins.RetrieveModelMixin, generics.GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DepartmentApi(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

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

from rest_framework import mixins, generics
from .models import Pipeline, PipelineStage
from .serializer import PipelineSerializer, PipelineStageSerializer

class PipelinesDetailApi(mixins.RetrieveModelMixin, generics.GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)  

class PipelineStageUpdate(
    mixins.RetrieveModelMixin,
    generics.UpdateAPIView
    ):
    queryset = PipelineStage.objects.all()
    serializer_class = PipelineStageSerializer
    lookup_field = "id"

    def perform_update(self, serializer):
        instance = serializer.save()


class PipelineStageDelete(mixins.RetrieveModelMixin,generics.DestroyAPIView):
    queryset = PipelineStage.objects.all()
    serializer_class = PipelineStageSerializer
    lookup_field = "id"

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

class PipelinesDetailCompanyApi(mixins.RetrieveModelMixin, generics.GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer
    lookup_field = 'company'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)  


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

class EmailTemplateDetailApi(mixins.RetrieveModelMixin, generics.GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class WebformApi(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getWebforms(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveWebForms(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteWebforms(request)
        return makeResponse(data)                   

class WebformFieldsApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getWebformFields(request)
        return makeResponse(data)        

class ContactsApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getContacts(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveContacts(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteContacts(request)
        return makeResponse(data) 