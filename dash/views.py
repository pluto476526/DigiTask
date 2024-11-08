from django.shortcuts import render, redirect, get_object_or_404
from dash.models import Category, Job_Listing, Feedback, Nature, Job_Proposal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import logging

# Create your views here.

# Get logger
logger = logging.getLogger(__name__)


@login_required(login_url='sign_in')
def dash(request):
    return render(request, 'dash_index.html')


def categories(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        category = request.POST.get('category'),
        description = request.POST.get('description')

        if source == 'new_category':
            Category.objects.create(category=category, description=description)
            messages.success(request, "New category added")
            return redirect('categories')

        elif source == 'edit_category':
            item_id = request.POST.get('id')
            category = get_object_or_404(Category, id=item_id)
            category.category = request.POST.get('category')
            category.description = request.POST.get('description')
            category.save()
            messages.success(request, "Category succesfully updated.")
            return redirect('categories')

    else:
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'dash_categories.html', context)


def job_listings(request):
    jobs = Job_Listing.objects.exclude(created_by=request.user).filter(status='posted')
    context = {'listings': jobs}
    return render(request, 'dash_listings.html', context)


def job_details(request, pk):
    if request.method == 'POST':
        source = request.POST.get('source')
        created_by = request.user
        email = request.POST.get('email')
        website = request.POST.get('website')
        application = request.POST.get('application')
        job_name = get_object_or_404(Job_Listing, id=pk)
        nature = request.POST.get('nature')

        if source == 'new_application':
            Job_Proposal.objects.create(
                created_by = created_by,
                email = email,
                website = website,
                application = application,
                job = job_name,
                nature = nature,
            )
            messages.success(request, "Application sent succesfully")
            return redirect('job_details', pk=pk)

    job = get_object_or_404(Job_Listing, id=pk)
    context = {'job': job}
    return render(request, 'dash_job_details.html', context)


def my_posted_listings(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        created_by = request.user
        job = request.POST.get('job')
        category_name = request.POST.get('category')
        description = request.POST.get('description')
        location = request.POST.get('location')
        nature_name = request.POST.get('nature')
        payment = request.POST.get('payment')
        job_id = request.POST.get('id')
        app_job_id = request.POST.get('job_id')
        application_id = request.POST.get('application_id')
        tasker = request.POST.get('tasker')
        body = request.POST.get('message')
        rating = request.POST.get('rating')

        if source == 'new_job':
            category_instance = Category.objects.filter(category=category_name)
            nature_instance = get_object_or_404(Nature, name=nature_name)

            if not category_instance.exists():
                category_instance = Category.objects.create(category=category_name)
                Job_Listing.objects.create(
                    created_by = created_by,
                    job = job,
                    category = category_instance,
                    description = description,
                    location = location,
                    nature = nature_instance,
                    payment = payment,
                )
                messages.success(request, "New Task/Job Listing Posted")
                return redirect('my_posted_listings')
        
        elif source == 'edit_job':
            nature_instance = get_object_or_404(Nature, name=nature_name)
            job_item = get_object_or_404(Job_Listing, id=job_id)
            job_item.job = job
            job_item.description = description
            job_item.location = location
            job_item.nature = nature_instance
            job_item.payment = payment
            job_item.save()
            messages.success(request, "Task/Job Listing Updated Succesfully")
            return redirect('my_posted_listings')
        
        elif source == 'accept_application':
            accept = request.POST.get('accept_btn')
            mark_read = request.POST.get('mark_read')

            if accept is not None:
                user_instance = get_object_or_404(User, username=tasker)
                job_item = get_object_or_404(Job_Listing, id=app_job_id)
                job_item.status = 'assigned'
                job_item.tasker = user_instance
                job_item.save()
                proposal = get_object_or_404(Job_Proposal, id=application_id)
                proposal.status = 'accepted'
                proposal.save()
                messages.success(request, "Application accepted")
                return redirect('my_posted_listings')

            elif mark_read is not None:
                proposal = get_object_or_404(Job_Proposal, id=application_id)
                proposal.status = 'read'
                proposal.save()
                messages.success(request, "Application marked as read")
                return redirect('my_posted_listings')
        
        elif source == 'send_feedback':
            job_instance = get_object_or_404(Job_Listing, id=job_id)
            Feedback.objects.create(created_by=request.user, job=job_instance, body=body, rating=rating)
            messages.success(request, 'Message sent')
            return redirect('my_posted_listings')

    categories = Category.objects.all()
    job_nature = Nature.objects.all()
    jobs = Job_Listing.objects.filter(created_by=request.user)
    applications = {job.id: Job_Proposal.objects.filter(job=job, status='sent') for job in jobs}
    context = {'my_jobs': jobs, 'categories': categories, 'job_nature': job_nature, 'new_applications': applications}
    return render(request, 'dash_my_posted_listings.html', context)


def my_applied_listings(request):
    if request.method == 'POST':
        app_id = request.POST.get('id')
        application = get_object_or_404(Job_Proposal, id=app_id)
        application.email = request.POST.get('email')
        application.website = request.POST.get('website')
        application.application = request.POST.get('application')
        application.save()
        messages.success(request, "Application Updated succesfully")
        return redirect('dash_my_applied_listings')
    
    my_applications = Job_Proposal.objects.filter(created_by=request.user).select_related('job')
    context = {'my_applications': my_applications}
    return render(request, 'dash_my_applied_listings.html', context)


def short_tasks(request):
    nature_instance = get_object_or_404(Nature, name='Short Task')
    my_short_tasks = Job_Proposal.objects.filter(nature=nature_instance, created_by=request.user)
    pending_tasks = Job_Listing.objects.filter(nature=nature_instance, tasker=request.user, status='assigned')
    latest_short_tasks = Job_Listing.objects.filter(nature=nature_instance, status='posted').order_by('-create_date')[:5]
    completed_short_tasks = Job_Listing.objects.filter(nature=nature_instance, status='completed', tasker=request.user)
    context = {'my_short_tasks': my_short_tasks, 'latest_short_tasks': latest_short_tasks, 'pending_tasks': pending_tasks, 'completed_tasks': completed_short_tasks}
    return render(request, 'dash_short_tasks.html', context)


def pending_tasks(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        task_id = request.POST.get('id')

        if source == 'confirm_task':
            task = get_object_or_404(Job_Listing, id=task_id)
            task.status = 'posted'
            task.save()
            messages.success(request, 'Task confirmed')
            return redirect('pending_tasks')
        
        elif source == 'cancel_task':
            task = get_object_or_404(Job_Listing, id=task_id)
            task.status = 'rejected'
            task.save()
            messages.success(request, 'Task cancelled')
            return redirect('pending_tasks')

    tasks = Job_Listing.objects.exclude(created_by=request.user).filter(status='pending')
    context = {'tasks': tasks}
    return render(request, 'dash_pending_tasks.html', context)


def cancelled_tasks(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        task_id = request.POST.get('id')

        if source == 'confirm_task':
            task = get_object_or_404(Job_Listing, id=task_id)
            task.status = 'posted'
            task.save()
            messages.success(request, 'Task confirmed')
            return redirect('cancelled_tasks')
        
        elif source == 'cancel_task':
            task = get_object_or_404(Job_Listing, id=task_id)
            task.delete()
            messages.success(request, 'Task deleted')
            return redirect('cancelled_tasks')
        
    tasks = Job_Listing.objects.exclude(created_by=request.user).filter(status='rejected')
    context = {'tasks': tasks}
    return render(request, 'dash_cancelled_listings.html', context)


def ongoing_tasks(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        task_id = request.POST.get('id')

        if source == 'complete_task':
            task = get_object_or_404(Job_Listing, id=task_id)
            task.status = 'completed'
            task.save()
            messages.success(request, 'Task completed')
            return redirect('ongoing_tasks')
        
        elif source == 'cancel_task':
            task = get_object_or_404(Job_Listing, id=task_id)
            task.status = 'rejected'
            task.save()
            messages.success(request, 'Task cancelled')
            return redirect('ongoing_tasks')
        
    tasks = Job_Listing.objects.filter(status='assigned')
    context = {'tasks': tasks}
    return render(request, 'dash_ongoing_tasks.html', context)


def feedback(request):
    feedback = Feedback.objects.all()
    context = {'feedbacks': feedback}
    return render(request, 'dash_feedback.html', context)