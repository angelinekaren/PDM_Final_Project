import django_filters

from .models import ApplicantsJobMap, Job

# filter for the fields(job, status) in "ApplicantsJobMap" model
class StatusFilter(django_filters.FilterSet):
    class Meta:
        model = ApplicantsJobMap
        fields =['job', 'status']

# filter for the fields(position name, company) in "Job" model
class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['position_name', 'company']