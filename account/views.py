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


class AccountSignUpApi(APIView):

    def post(self, request):

        data = helper.signUpAccount(request)
        return makeResponse(data)


class ProfileApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = helper.getAccountProfile(request)

        return makeResponse(data)

    def put(self, request):
        data = helper.updateAccount(request)
        return makeResponse(data)


class AccountSignInApi(APIView):

    def post(self, request):

        data = helper.signInAccount(request)
        return makeResponse(data)


class ForgotPasswordApi(APIView):

    def post(self, request):
        data = helper.forgotPasswordAccount(request)
        return makeResponse(data)


class UpdateAccountApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.updateAccount(request)
        return makeResponse(data)


class UpdatePhotoApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.updatePhoto(request)
        return makeResponse(data)

class UpdateMemberPhotoApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.updateMemberPhoto(request)
        return makeResponse(data)

class UpdateMemberRoleApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.updateMemberRole(request)
        return makeResponse(data)

class UpdateLogoApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.updateLogo(request)
        return makeResponse(data)


class CompanyInfoApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.getCompanyInfo(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.updateCompanyInfo(request)
        return makeResponse(data)


class MobileApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = helper.updateMobile(request)
        return makeResponse(data)


class CheckMobileApi(APIView):

    def post(self, request):
        data = helper.checkMobile(request)
        return makeResponse(data)


class CheckEmailApi(APIView):

    def post(self, request):
        data = helper.checkEmail(request)
        return makeResponse(data)


class CheckTokenApi(APIView):

    def post(self, request):
        data = helper.checkEmail(request)
        return makeResponse(data)


class ActvateAccountApi(APIView):

    def post(self, request):
        data = helper.activateAccount(request)
        return makeResponse(data)

class ApproveAccountApi(APIView):

    def post(self, request):
        data = helper.approveMember(request)
        return makeResponse(data)

class VerifyTokenApi(APIView):

    def get(self, request):
        data = helper.verifyToken(request)
        return makeResponse(data)


class ResetPasswordApi(APIView):

    def post(self, request):
        data = helper.resetPassword(request)
        return makeResponse(data)


class ChangePasswordApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.changePassword(request)
        return makeResponse(data)


class MembersApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = helper.listMembrs(request)
        return makeResponse(data)

    def post(self, request):
        data = helper.addMember(request)
        return makeResponse(data)

    def delete(self, request):
        data = helper.deleteMember(request)
        return makeResponse(data)

class UpdateMemberApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.updateMember(request)
        return makeResponse(data)

class PhotoUpdateApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.updatePhoto(request)
        return makeResponse(data)

class ActivateMemberApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.activateMember(request)
        return makeResponse(data)


class DeleteMemberApi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = helper.deleteMember(request)
        return makeResponse(data)

# class ApproveUser(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = helper.approveVerifyMember(request)
#         return makeResponse(data)