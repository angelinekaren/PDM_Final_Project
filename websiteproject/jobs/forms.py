from django import forms
from .models import Job, ApplicantsJobMap
from account.models import Applicant

# form for company users to make new job position
class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = (
            'company',
            'position_name',
            'text_description',
            'min_age',
            'max_age',
            'gender',
            'salary',
        )

        def save(self):
            jobs = super(JobForm, self).save()
            jobs.company = self.cleaned_data.get('company')
            jobs.position_name = self.cleaned_data.get('position_name')
            jobs.text_description = self.cleaned_data.get('text_description')
            jobs.min_age = self.cleaned_data.get('min_age')
            jobs.max_age = self.cleaned_data.get('max_age')
            jobs.gender = self.cleaned_data.get('gender')
            jobs.salary = self.cleaned_data.get('salary')
            jobs.save()
            return jobs

# form for company users to update their applicant status
class StatusForm(forms.ModelForm):
    applicant = forms.ModelChoiceField(
        queryset=Applicant.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control input-sm'}),
        required=False
    )

    class Meta:
        model = ApplicantsJobMap
        fields = ['applicant', 'job', 'status', 'feedback']

# form for applicant users to apply for a job
class JobApplyForm(forms.ModelForm):
    class Meta:
        model = ApplicantsJobMap
        fields = ['job',]