from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .import helper
from common.utils import makeResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import mixins, generics
from .models import ApplicantWebForm, Note
from .serializer import ApplicantWebFormSerializer, NoteSerializer

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


class CreateCandidateUsingResume(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.createCandidate(request)
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

class DetailNoteApi(mixins.RetrieveModelMixin, generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# Update Notes view 
class NotesUpdateApi(
    generics.UpdateAPIView
    ):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

class CreateCandidateUsingWebForm(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.createCandidatewithoutResumeParser(request)
        return makeResponse(data) 

class UpdateCandidatePipelineStatus(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.updatePipelineStatus(request)
        return makeResponse(data) 

# Details ApplicationWebForm view
class ApplicationWebFormByJobApi(
    generics.ListAPIView
    ):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lookup_field = self.kwargs['lookup_field']
        lookup_value = self.kwargs['lookup_value']
        queryset = ApplicantWebForm.objects.filter(**{lookup_field: lookup_value})
        return queryset

    serializer_class = ApplicantWebFormSerializer

# Update ApplicationWebForm view 
class ApplicationWebFormUpdateApi(
    generics.UpdateAPIView
    ):
    queryset = ApplicantWebForm.objects.all()
    serializer_class = ApplicantWebFormSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

# Update ApplicationWebForm view 
class ApplicationWebFormUpdateApi(
    generics.UpdateAPIView
    ):
    queryset = ApplicantWebForm.objects.all()
    serializer_class = ApplicantWebFormSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
# Delete ApplicationWebForm view 
class ApplicationWebFormDeleteApi(
    generics.DestroyAPIView
    ):
    queryset = ApplicantWebForm.objects.all()
    serializer_class = ApplicantWebFormSerializer

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
 
# Create ApplicationWebForm view
class ApplicationWebFormCreateApi(APIView):
    def post(self, request):
        data = helper.saveApplicantWebForms(request)
        return makeResponse(data)

class AssignJob(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = helper.assignJob(request)
        return makeResponse(data)

class UpdateCandidateStatusApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = helper.updateCandidatePipelineStage(request)
        return makeResponse(data)
