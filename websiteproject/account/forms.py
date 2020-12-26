from django.contrib.auth.forms import UserCreationForm
from account.models import CustomUser, Company, Applicant
from django.db import transaction
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserChangeForm


User = get_user_model()

class CompanySignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta(UserCreationForm.Meta):
        model = CustomUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('username')
        user.name = self.cleaned_data.get('name')
        user.set_password(self.cleaned_data.get('password1'))
        user.is_staff = True
        user.is_company = True
        user.save()
        company = Company.objects.create(company=user)
        company.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError(f"Email {email} is already taken")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError(f"Username {username} is already taken")
        return username

    def clean(self):
        data = self.cleaned_data
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 != password1:
            raise forms.ValidationError("Passwords must match")
        return data

class ApplicantSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')
    age = forms.CharField(max_length=30)
    gender = forms.ChoiceField(choices=Applicant().GENDER_CHOICES)
    mobile_phone = forms.CharField(max_length=30)
    city = forms.CharField(max_length=30)
    will_relocate = forms.ChoiceField(choices=Applicant().RELOCATE_CHOICES)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta(UserCreationForm.Meta):
        model = CustomUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('username')
        user.name = self.cleaned_data.get('name')
        user.set_password(self.cleaned_data.get('password1'))
        user.is_staff = False
        user.is_applicant = True
        user.save()
        applicant = Applicant.objects.create(applicant=user)
        applicant.age = self.cleaned_data.get('age')
        applicant.gender = self.cleaned_data.get('gender')
        applicant.mobile_phone = self.cleaned_data.get('mobile_phone')
        applicant.city = self.cleaned_data.get('city')
        applicant.will_relocate = self.cleaned_data.get('will_relocate')
        applicant.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError(f"Email {email} is already taken")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError(f"Username {username} is already taken")
        return username

    def clean(self):
        data = self.cleaned_data
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 != password1:
            raise forms.ValidationError("Passwords must match")
        return data

class CompanyEditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = Company
        fields = (
            'profile_pic',
        )

class ApplicantEditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = Applicant
        fields = (
            'age',
            'gender',
            'mobile_phone',
            'city',
            'will_relocate',
            'profile_pic',
        )