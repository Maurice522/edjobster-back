import imp
from job.serializer import JobsSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins, generics
from .import helper
from common.utils import makeResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from settings.models import Webform
from .models import Job, Assesment
from .serializer import AssesmentSerializer
from candidates.models import Candidate
from candidates.serializer import CandidateDetailsSerializer

class AssesmentCategoryApi(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        data = helper.getAssesmentCategories(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveAssesmentCategory(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteAssesmentCategory(request)
        return makeResponse(data)    


class AssismentDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Assesment.objects.all()
    serializer_class = AssesmentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class AssesmentQuestionApi(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

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

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getAssesments(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.saveAssesment(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteAssesment(request)
        return makeResponse(data)           

class JobsList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
from rest_framework.response import Response
class JobsDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.all()
    serializer_class = JobsSerializer

    def get(self, request, *args, **kwargs):
        job = self.get_object()
        serializer = self.get_serializer(job)
        data = serializer.data
        data['department'] = serializer.get_department(job)
        data['members'] = serializer.get_members(job)
        
        # Giving the pipeline stage info as well 
        
        candidates = Candidate.getByJob(job=job)

        pipeline_stage_stats = {}
        pipeline_stage_status_stats = {}

        for candidate in candidates:

            # For pipeline stage list
            if candidate.pipeline_stage:
                if str(candidate.pipeline_stage).lower() in pipeline_stage_stats.keys():
                    pipeline_stage_stats[str(candidate.pipeline_stage).lower()] += 1
                else:
                    pipeline_stage_stats[str(candidate.pipeline_stage).lower()] = 1

            # For pipeline stage status
            if candidate.pipeline_stage_status:
                if str(candidate.pipeline_stage_status).lower() in pipeline_stage_status_stats.keys():
                    pipeline_stage_status_stats[str(candidate.pipeline_stage_status).lower()] += 1
                else:
                    pipeline_stage_status_stats[str(candidate.pipeline_stage_status).lower()] = 1
        
        data["pipeline_stage_stats"] = pipeline_stage_stats
        data["pipeline_stage_status_stats"] = pipeline_stage_status_stats
        
        return Response(data)
    
class JobsCandidates(mixins.RetrieveModelMixin, generics.GenericAPIView):    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.all()
    serializer_class = JobsSerializer

    def get_candidate(self, job):
        if job:
            candidate = Candidate.objects.filter(job=job.id)
            return candidate
        return None
    
    def get(self, request, *args, **kwargs):
        job = self.get_object()
        candidates = self.get_candidate(job)
       
        candidate_data=[] 
        for candidate in candidates:
            data = CandidateDetailsSerializer(candidate).data
            candidate_data.append(data)
        return Response(candidate_data)

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

class CreateJobApi(APIView):
    def post(self, request):

        data = request.data
        print(data)

        title = data['title']
        vacancies = data['vacancies']
        department = data['department']
        owner = data['owner']
        assesment = data['assesment']
        member_ids = data['member_ids']
        type = data['type']
        nature = data['nature']
        education = data['education']
        speciality = data['speciality']
        description = data['description']
        exp_min = data['exp_min']
        exp_max = data['exp_max']
        salary_min = data['salary_min']
        salary_max = data['salary_max']
        salary_type = data['salary_type']
        currency = data['currency']
        city = data['city']
        state = data['state']
        job_boards = data['job_boards']
        pipeline = data['pipeline']
        active = data['active']
        status = data['status']
        webform_id = data['webform_id']

        job = Job(title= title,vacancies = vacancies, department = department, owner = owner, assesment = assesment , type = type , nature = nature ,speciality = speciality , description = description , exp_max = exp_max , exp_min = exp_min , salary_min = salary_min , salary_max = salary_max , salary_type = salary_type , currency = currency , city = city , state = state ,job_boards = job_boards , pipeline = pipeline ,active = active , webform_id = webform_id, job_status = status )
        job.save()

        return makeResponse(data)

class JobDetailsApi(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getJobDetails(request)
        return makeResponse(data)

class BoardApi(APIView):

    def post(self, request):
        data = helper.getJobsBoard(request)
        return makeResponse(data)     

class JobCandidateList(APIView):

    def get(self, request):
        data = helper.getJobCandidateList(request) 
        return makeResponse(data)  


class JobNotesApi(APIView):

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


class JobStats(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getJobStats(request)
        return makeResponse(data)

class DashboardJobStats(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getDashboardJobStats(request)
        return makeResponse(data)

class JobStatusStats(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getJobStatusStats(request)
        return makeResponse(data)