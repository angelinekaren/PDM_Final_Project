from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(
        verbose_name="email",
        max_length=60,
        unique=True,
    )

    def get_name(self):
        return self.name

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_company(self):
        return self.is_company

    def get_applicant(self):
        return self.is_applicant


class Company(models.Model):
    company = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField(default="profile_pic.png", null=True, blank=True)

    def __str__(self):
        return str(self.company)

    def get_profile_pic(self):
        return self.profile_pic



class Applicant(models.Model):
    applicant = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    GENDER_MALE = 'Male'
    GENDER_FEMALE = 'Female'
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.CharField(max_length=20, default=GENDER_MALE, choices=GENDER_CHOICES)
    age = models.CharField(max_length=10, null=True)
    mobile_phone = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=30, null=True)
    WILL_RELOCATE = "I'm willing"
    WONT_RELOCATE = "I'm not willing"
    RELOCATE_CHOICES = (
        (WILL_RELOCATE, "I'm willing"),
        (WONT_RELOCATE, "I'm not willing"),
    )
    will_relocate = models.CharField(max_length=20, default=WILL_RELOCATE, choices=RELOCATE_CHOICES)
    profile_pic = models.ImageField(default="profile_pic.png", null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.applicant)

    def get_age(self):
        return self.age

    def get_profile_pic(self):
        return self.profile_pic

    def get_email(self):
        return self.applicant.email

    def get_name(self):
        return self.applicant.name

    def get_gender(self):
        return self.gender

    def get_mobile_phone(self):
        return self.mobile_phone

    def get_city(self):
        return self.city

    def get_will_relocate(self):
        return self.will_relocate

