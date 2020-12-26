from django.db import models
from account.models import Company, Applicant
STATUS_PENDING = 'pending'
STATUS_ACCEPTED = 'accepted'
STATUS_REJECTED = 'rejected'
STATUS_CHOICES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_ACCEPTED, 'Accepted'),
    (STATUS_REJECTED, 'Rejected'),
)

GENDER_MALE = 'Male'
GENDER_FEMALE = 'Female'
GENDER_ALL = 'Not specified'
GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_ALL, 'Not specified')]


class Job(models.Model):
    company = models.CharField(max_length=255, blank=False)
    position_name = models.CharField(max_length=100)
    text_description = models.TextField()
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    gender = models.CharField(max_length=20, default=GENDER_ALL, choices=GENDER_CHOICES)
    salary = models.IntegerField()
    creator = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.position_name

    def get_company(self):
        return self.company

    def get_position_name(self):
        return self.position_name

    def get_text_description(self):
        return self.text_description

    def get_age(self):
        return f'{self.min_age}-{self.max_age}'

    def get_gender(self):
        return self.gender

    def get_salary(self):
        return f'Rp. {self.salary}'

    def get_creator(self):
        return self.creator


class ApplicantsJobMap(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='applicants', null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    feedback = models.TextField(blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.applicant)

    def get_applicant(self):
        return self.applicant

    def get_job(self):
        return self.job

    def get_status(self):
        return self.status

    def get_feedback(self):
        return self.feedback
