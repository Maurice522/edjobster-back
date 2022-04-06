from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('sign-in/', views.AccountSignInApi.as_view(), name='sign-in'),
    path('sign-up/', views.AccountSignUpApi.as_view(), name='sign-up'),
    path('profile/', views.ProfileApi.as_view(), name='profile'),
    path('forgot-password/', views.ForgotPasswordApi.as_view(),
         name='forgot-password'),
    path('reset-password/', views.ResetPasswordApi.as_view(), name='reset-password'),
    path('change-password/', views.ChangePasswordApi.as_view(),
         name='change-password'),
    path('update-account/', views.UpdateAccountApi.as_view(), name='update-account'),
    path('member-photo/', views.UpdateMemberPhotoApi.as_view(), name='member-photo'),
    path('member-role/', views.UpdateMemberRoleApi.as_view(), name='member-role'),
    path('update-photo/', views.UpdatePhotoApi.as_view(), name='update-photo'),
    path('update-mobile/', views.MobileApi.as_view(), name='update-mobile'),
    path('check-mobile/', views.CheckMobileApi.as_view(), name='check-mobile'),
    path('check-email/', views.CheckEmailApi.as_view(), name='check-email'),

    path('company-logo/', views.UpdateLogoApi.as_view(), name='company-logo'),
    path('company-info/', views.CompanyInfoApi.as_view(), name='company-info'),

    path('activate/', views.ActvateAccountApi.as_view(), name='activate'),
    path('approve/', views.ApproveAccountApi.as_view(), name='approve'),
    path('verify-token/', views.VerifyTokenApi.as_view(), name='verify-token'),

    path('members/', views.MembersApi.as_view(), name='members'),
    path('member-update/', views.UpdateMemberApi.as_view(), name='member-update'),
    path('activate-member/', views.ActivateMemberApi.as_view(),
         name='activate-member'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='refreshtoken'),
    path('verifytoken/', TokenVerifyView.as_view, name='verifytoken'),
]
