from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login, logout, authenticate
from account.models import CustomUser
from account.forms import (CompanySignUpForm, ApplicantSignUpForm,
                           CompanyEditProfileForm, ApplicantEditProfileForm)
from django.contrib import messages

# view for user to choose whether thay want to be registered as company/applicant
def register_view(request):
    return render(request, 'account/register.html')

# register view for company user
class company_register(CreateView):
    model = CustomUser
    form_class = CompanySignUpForm
    template_name = 'account/company_register.html'

    def validation(self, form):
        user = form.save()
        login(self.request, user)  #if the form is save, the user will be logged in
        return redirect('home')

#register view for applicant user
class applicant_register(CreateView):
    model = CustomUser
    form_class = ApplicantSignUpForm
    template_name = 'account/applicant_register.html'

    def validation(self, form):
        user = form.save()
        login(self.request, user)  #if the form is save, the user will be logged in
        return redirect('home')

# login view for users
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


# for users to logout form their account
def logout_view(request):
    logout(request)
    return redirect("home")

# their user account profile view
def account_profile(request):
    return render(request, 'account/account_profile.html', {})

# view the form to update the account profile for company user
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

# view the form to update the account profile for applicant user
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
