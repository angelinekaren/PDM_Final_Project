from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login, logout, authenticate
from account.models import CustomUser
from account.forms import (CompanySignUpForm, ApplicantSignUpForm,
                           CompanyEditProfileForm, ApplicantEditProfileForm)
from django.contrib import messages


def register_view(request):
    return render(request, 'account/register.html')


class company_register(CreateView):
    model = CustomUser
    form_class = CompanySignUpForm
    template_name = 'account/company_register.html'

    def validation(self, form):
        user = form.save()
        login(self.request, user)  #if the form is save, the user will be logged in
        return redirect('home')


class applicant_register(CreateView):
    model = CustomUser
    form_class = ApplicantSignUpForm
    template_name = 'account/applicant_register.html'

    def validation(self, form):
        user = form.save()
        login(self.request, user)  #if the form is save, the user will be logged in
        return redirect('home')


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, 'Username OR password is incorrect')

    return render(request, "account/login.html", {})


def logout_view(request):
    logout(request)
    return redirect("home")


def account_profile(request):
    return render(request, 'account/account_profile.html', {})


def company_update_profile(request):
    if request.method == 'POST':
        form = CompanyEditProfileForm(request.POST, request.FILES, instance=request.user.company)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account is successfully updated')
            return redirect('account_profile')
    else:
        form = CompanyEditProfileForm(instance=request.user.company)
        context = {'update_form': form}
        return render(request, 'account/update_profile.html', context)


def applicant_update_profile(request):
    if request.method == 'POST':
        form = ApplicantEditProfileForm(request.POST, request.FILES, instance=request.user.applicant)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account is successfully updated')
            return redirect('account_profile')
    else:
        form = ApplicantEditProfileForm(instance=request.user.applicant)
    return render(request, 'account/applicant_update.html', {'applicant_update': form})
