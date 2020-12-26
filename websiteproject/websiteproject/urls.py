"""websiteproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from personal.views import (
    home_screen,
)

from account.views import (
    register_view,
    company_register,
    applicant_register,
    login_view,
    logout_view,
    account_profile,
    company_update_profile,
    applicant_update_profile,
)

from jobs.views import (
    get_jobs,
    get_job,
    subscribe_job,
    add_job,
    posted_jobs,
    job_applicants,
    delete_job,
    update,
    status,
    contact,
    contact_applicants,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen, name="home"),
    path('register/', register_view, name="register"),
    path('company_register/', company_register.as_view(success_url="/login/"), name="company_register"),
    path('applicant_register/', applicant_register.as_view(success_url="/login/"), name="applicant_register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('status/', status, name="status"),
    path('account_profile/', account_profile, name='account_profile'),
    path('company_update/', company_update_profile, name='company_update'),
    path('applicant_update/', applicant_update_profile, name='applicant_update'),
    path('jobs/', get_jobs, name='jobs_view'),
    path('jobs/<int:id>', get_job, name="job_view"),
    path('jobs/<int:id>/subscribe', subscribe_job, name="subscribe_view"),
    path('add_jobs/', add_job, name='add_jobs'),
    path('posted_jobs/', posted_jobs, name='posted_job'),
    path('posted_jobs/<int:id>', job_applicants.as_view(), name="assign_job"),
    path('delete_job/<str:pk>', delete_job, name='delete_job'),
    path('status/<int:applicant_id>/', update, name="update_applicant"),
    path('update/contact/', contact, name='contact'),
    path('contact_applicant/', contact_applicants, name='contact_applicants'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='account/reset_password.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_complete'),
]

if settings.DEBUG: # our environment development
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
