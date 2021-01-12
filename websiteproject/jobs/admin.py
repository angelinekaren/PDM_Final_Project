from django.contrib import admin
from .models import Job, ApplicantsJobMap

# create a tabular inline inside the job admin
class ApplicantsInline(admin.TabularInline):
    model = ApplicantsJobMap

    def get_readonly_fields(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return []
        else:
            return ('applicant',)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

# job admin
class JobAdmin(admin.ModelAdmin):
    exclude = ('creator',)
    inlines = (ApplicantsInline,)

    # superuser can view all the jobs posted
    def get_queryset(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return Job.objects.all()
        else:
            # current logged in company user can only view the jobs they have posted
            return Job.objects.filter(creator=request.user.company)

    # superuser can view all the position name along with the company creator
    def get_list_display(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ('position_name', 'creator',)
        else:
            # company user view only the position name (it is created by them)
            return ('position_name',)

    # the creator is set only when we creating an object and not update
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user.company
            obj.save()

admin.site.register(Job, JobAdmin)
