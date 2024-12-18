from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from chats.models import Profile, Company, Chat_Message, My_Note, To_Do
import logging


# Get logger
logger = logging.getLogger(__name__)

# Create your views here.


def is_user_logged_in(user):
    # Check if the user has an active session
    sessions = Session.objects.filter(expire_date__gte=now())

    for session in sessions:
        data = session.get_decoded()

        if str(user.id) == str(data.get('_auth_user_id')):
            return True
        
    return False


def manage_notes_and_tasks(request):
    if request.method == 'POST':
        note = request.POST.get('note')
        to_do = request.POST.get('todo_item')
        source = request.POST.get('source')
        user = request.user

        if source == 'new_note':
            My_Note.objects.create(user=user, note=note)
            messages.success(request, 'Note posted')
            return redirect('start_chats')

        elif source == 'new_todo':
            To_Do.objects.create(user=user, item=to_do)
            messages.success(request, 'New task added')
            return redirect('start_chats')


def index_view(request):
    manage_notes_and_tasks(request)
    context = {}
    return render(request, 'chats_start.html', context)


def settings_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        company = None

        # Retrieve company from form
        company_name = request.POST.get('company')

        if company_name:
            company, company_created = Company.objects.get_or_create(name=company_name, defaults={'owner': user})

            if company_created:
                company.owner = user
                company.save()
                    
            else:
                company = None
        
        avatar = request.FILES.get('avatar')

        if avatar:
            profile.avatar = avatar

        profile.phone = request.POST.get('phone')
        profile.company = company
        profile.bio = request.POST.get('bio')
        profile.save()
        messages.success(request, 'Profile details updated')
        return redirect('settings')

    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'chats_settings.html', context)


def text_messages(request, username):
    if request.method == 'POST':
        receiver_name = request.POST.get('receiver')
        receiver = get_object_or_404(User, username=receiver_name)
        sender = request.user
        body = request.POST.get('body')
        Chat_Message.objects.create(sender=sender, receiver=receiver, body=body)
        return HttpResponseRedirect(request.path_info)

    manage_notes_and_tasks(request)
    user = get_object_or_404(User, username=username)
    messages = Chat_Message.objects.filter((Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))).order_by('create_date')
    other_user_logged_in = is_user_logged_in(user)
    context = {'chat_messages': messages, 'other_user': user, 'other_user_logged_in': other_user_logged_in,}
    return render(request, 'chats_text_messages.html', context)





















