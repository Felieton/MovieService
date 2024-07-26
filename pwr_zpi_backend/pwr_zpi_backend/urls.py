"""pwr_zpi_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt

from movie_service.views import FacebookLogin, GoogleLogin, \
    RegistrationRedirectView, ReverseMatchNullView, ScraperAPIView
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView, \
    RegisterView

dj_rest_auth_register_urls = [
    path('', RegisterView.as_view(), name='rest_register'),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
]

dj_rest_auth_urls = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include(dj_rest_auth_register_urls)),
    path('facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    # empty view needed for reverse match by dj_rest_auth
    path('account-confirm-email/', ReverseMatchNullView.as_view(), name='account_email_verification_sent'),
    path('social-signup-reverse/', ReverseMatchNullView.as_view(), name='socialaccount_signup')
]

urlpatterns = [
    path('o/', include(dj_rest_auth_urls)),
    re_path(
        r'^o/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
        RegistrationRedirectView.as_view(),
        name='account_confirm_email',
    ),
    path('', include('movie_service.urls')),
    path('scraper/', csrf_exempt(ScraperAPIView.as_view()), name='scraper'),
    path('admin/', admin.site.urls),
]
