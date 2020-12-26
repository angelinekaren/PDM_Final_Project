from django.contrib import admin
from account.models import CustomUser, Company, Applicant
from django.contrib.auth.admin import UserAdmin
from jobs.models import ApplicantsJobMap

class CandidateInline(admin.TabularInline):
    model = ApplicantsJobMap

    def get_readonly_fields(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ['job', 'status', 'feedback']

class ApplicantsAdmin(admin.ModelAdmin):
    inlines = (CandidateInline,)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

class AccountAdmin(UserAdmin):
    list_display = ("email", "username", "date_joined", "last_login", "is_staff")
    search_fields = ("email", "username")
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = (['user_permissions', 'groups'])
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj and obj.id == request.user.id)





admin.site.register(CustomUser, AccountAdmin)
admin.site.register(Company)
admin.site.register(Applicant, ApplicantsAdmin)
