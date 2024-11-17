from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from chats.models import To_Do, My_Note, Chat_Message
import logging


# Get logger
# logger.debug(user_profile)
logger = logging.getLogger(__name__)


def user_profile(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(User, username=request.user)
        context = {'profile': profile}
        return context
    
    else:
        context = {}
        return context


def to_do(request):
    if request.user.is_authenticated:
        list_items = To_Do.objects.filter(user=request.user)
        context = {'to_do_items': list_items}
        return context
    
    else:
        context = {}
        return context


def notes(request):
    if request.user.is_authenticated:
        my_notes = My_Note.objects.filter(user=request.user)
        context = {'notes': my_notes}
        return context
    
    else:
        context = {}
        return context


def recent_messages(request):
    if request.user.is_authenticated:
        user = request.user
        messages = Chat_Message.objects.filter(sender=user).union(Chat_Message.objects.filter(receiver=user)).order_by('-create_date')
        recent_users = {}

        for message in messages:
            other_user = message.receiver if message.sender == user else message.sender

            if other_user not in recent_users:
                recent_users[other_user] = message

        user_messages = list(recent_users.values())
        context = {'recent_messages': user_messages}
        return context
    
    else:
        context = {}
        return context

