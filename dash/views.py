from django.shortcuts import render, redirect, get_object_or_404
from dash.models import Category, Job_Listing, Feedback, Nature, Job_Proposal
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

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
    jobs = Job_Listing.objects.exclude(created_by=request.user)
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

        if source == 'new_application':
            Job_Proposal.objects.create(
                created_by = created_by,
                email = email,
                website = website,
                application = application,
                job = job_name,
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

        if source == 'new_job':
            category_instance = get_object_or_404(Category, category=category_name)

            if category_instance == None:
                Category.objects.create(category=category_name)
                
            nature_instance = get_object_or_404(Nature, name=nature_name)
            Job_Listing.objects.create(
                created_by = created_by,
                job = job,
                category = category_instance,
                description = description,
                location = location,
                nature = nature_instance,
                payment = payment
            )
            messages.success(request, "New Task/Job Listing Posted")
            return redirect('my_posted_listings')
        
        elif source == 'edit_job':
            job_id = request.POST.get('id')
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

    categories = Category.objects.all()
    job_nature = Nature.objects.all()
    jobs = Job_Listing.objects.filter(created_by=request.user)
    context = {'my_jobs': jobs, 'categories': categories, 'job_nature': job_nature}
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
        return redirect('my_applied_listings')
    
    my_applications = Job_Proposal.objects.filter(created_by=request.user)
    context = {'my_applications': my_applications}
    return render(request, 'dash_my_applied_listings.html', context)


def short_tasks(request):
    return render(request, 'dash_short_tasks.html')


def feedback(request):
    feedback = Feedback.objects.all()
    context = {'feedbacks': feedback}
    return render(request, 'dash_feedback.html', context)