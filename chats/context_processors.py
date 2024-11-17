from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from chats.models import To_Do, My_Note
import logging


# Get logger
# logger.debug(user_profile)
logger = logging.getLogger(__name__)


def user_profile(request):
    if request.user.is_authenticated:
        profile = User.objects.get(username=request.user)
        context = {'profile': profile}
        return context


def to_do(request):
    if request.user.is_authenticated:
        list_items = To_Do.objects.filter(user=request.user)
        context = {'to_do_items': list_items}
        return context


def notes(request):
    if request.user.is_authenticated:
        my_notes = My_Note.objects.filter(user=request.user)
        context = {'notes': my_notes}
        return context

