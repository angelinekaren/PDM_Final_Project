import django_filters

from .models import ApplicantsJobMap, Job

class StatusFilter(django_filters.FilterSet):
    class Meta:
        model = ApplicantsJobMap
        fields =['job', 'status']

class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['position_name', 'company']