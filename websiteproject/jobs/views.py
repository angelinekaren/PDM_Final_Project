from django.shortcuts import render, redirect
from .models import Job, ApplicantsJobMap
from account.models import Applicant, CustomUser, Company
from django.contrib import messages
from django.views.generic import ListView
from .forms import JobForm, StatusForm, JobApplyForm
from .filters import StatusFilter, JobFilter
from django.core.mail import send_mail

# view all the jobs position available posted by various of company
def get_jobs(request):
    # get all jobs from the DB
    job = Job.objects.all()
    myFilter = JobFilter(request.GET, queryset=job)
    job = myFilter.qs
    context = {
        'job': job,
        'myFilter': myFilter,
    }
    return render(request, 'jobs/job.html', context)

# view a single job
def get_job(request, id):
    jobs = Job.objects.get(pk=id)
    context = {
        'jobs': jobs,
    }
    return render(request, 'jobs/jobs.html', context)

# view the form to apply/subscribe to a certain job posting
def subscribe_job(request, id):
    form = JobApplyForm(request.POST)
    applicant = Applicant.objects.get(applicant_id=request.user.applicant.applicant_id)
    subscriber = ApplicantsJobMap.objects.filter(applicant=applicant, job=id)
    if not subscriber:
        if request.method == 'POST':
            if form.is_valid():
                applied = form.save(commit=False)
                applied.applicant = applicant
                applied.save()
                messages.success(request, 'You have successfully applied for this job!')
                return redirect('jobs_view')
        else:
            return redirect('jobs_view')
    else:
        messages.error(request, 'You already applied for the Job!')
        return redirect('jobs_view')

# view the form for company users to add new jobs position
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.creator = request.user.company
            job.save()
            messages.success(request, 'Job is successfully added')
            return redirect('posted_job')
    else:
        form = JobForm()
    return render(request, 'jobs/add_job.html', {'job_form': form})

# view all the jobs position that are made by the current logged in company user
def posted_jobs(request):
    posted_job = Job.objects.filter(creator=request.user.company)
    return render(request, 'jobs/posted_job.html', {'posted_job': posted_job})

# view all the applicants for that certain job posting
class job_applicants(ListView):
    model = ApplicantsJobMap
    template_name = "jobs/job_applicant.html"
    context_object_name = "assign_job"
    paginate_by = 1

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return ApplicantsJobMap.objects.filter(job_id=self.kwargs["id"]).order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = Job.objects.get(id=self.kwargs["id"])
        return context

# view the form to delete a certain job posting
def delete_job(request, pk):
    job = Job.objects.get(id=pk)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job is successfully deleted')
        return redirect('posted_job')

    context = {'item': job}
    return render(request, 'jobs/delete_job.html', context)

# a view to update the status of a certain applicant
def update(request, applicant_id):
    applicants = ApplicantsJobMap.objects.get(id=applicant_id)
    formset = StatusForm(instance=applicants)
    # HTTP method POST -> forms submitted by a user
    if request.method == 'POST':
        formset = StatusForm(request.POST, instance=applicants) # a form bound to the POST data
        if formset.is_valid(): # if all the validation rules has passed
            formset = formset.save(commit=False)
            formset.save()
            messages.success(request, 'Applicant status update successful')
            return redirect('posted_job')
    else:
        formset = StatusForm(instance=applicants) # display the forms, so it could be filled
    context = {'formset': formset}
    return render(request, 'jobs/status.html', context)

# applicant users to view all the status for jobs that they have applied/subscribed to
def status(request):
    status_applicant = ApplicantsJobMap.objects.filter(applicant=request.user.applicant)
    myFilter = StatusFilter(request.GET, queryset=status_applicant)
    status_applicant = myFilter.qs
    context = {
        'status': status_applicant,
        'myFilter': myFilter,
    }
    return render(request, "jobs/status_applicant.html", context)

# view the form for applicant users to contact the admin for the website
def contact(request):
    if request.method == 'POST':
        message_name = request.POST['message_name']
        message_email = request.POST['message_email']
        message = request.POST['message']

        send_mail(
            message_name,  #subject
            message,  #message
            message_email,  #from email
            ['angelinekarenn@gmail.com'],  #to email
        )
        messages.success(request, 'Thanks. We received your email and will respond shortly')

        return render(request, 'jobs/message.html', {'message_name': message_name})
    else:
        return render(request, 'jobs/message.html', {})

# view the form for company users to contact the applicant by their gmail
def contact_applicants(request):
    if request.method == 'POST':
        message_name_applicant = request.POST['message_name_applicant']
        message_email_company = request.POST['message_email_company']
        message_email_applicant = request.POST['message_email_applicant']
        message_applicant = request.POST['message_applicant']

        send_mail(
            message_name_applicant,  #subject
            message_applicant,  #message
            message_email_company,  #from email
            [message_email_applicant],  #to email
        )
        messages.success(request, 'Email has been sent to the applicant email.')

        return render(request, 'jobs/message_applicant.html', {'message_name_applicant': message_name_applicant})
    else:
        return render(request, 'jobs/message_applicant.html', {})