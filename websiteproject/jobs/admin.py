from django.contrib import admin
from .models import Job, ApplicantsJobMap


class ApplicantsInline(admin.TabularInline):
    model = ApplicantsJobMap

    def get_readonly_fields(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return []
        else:
            return ('applicant',)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class JobAdmin(admin.ModelAdmin):
    exclude = ('creator',)
    inlines = (ApplicantsInline,)

    def get_queryset(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return Job.objects.all()
        else:
            return Job.objects.filter(creator=request.user.company)

    def get_list_display(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ('position_name', 'creator',)
        else:
            return ('position_name',)


    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user.company
            obj.save()

admin.site.register(Job, JobAdmin)
