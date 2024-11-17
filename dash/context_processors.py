from django.db.models import Q
from dash.models import Job_Listing, Notification
import logging


# Get logger
logger = logging.getLogger(__name__)


def search_jobs(request):
    q = request.GET.get('q', '')

    if request.user.is_authenticated:
        jobs = Job_Listing.objects.exclude(created_by=request.user).filter(
            Q(job__icontains=q) |
            Q(created_by__username__icontains=q) |
            Q(category__category__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q) |
            Q(nature__name__icontains=q),
            status='posted'
        )

    else:
        jobs = Job_Listing.objects.filter(
            Q(job__icontains=q) |
            Q(created_by__username__icontains=q) |
            Q(category__category__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q) |
            Q(nature__name__icontains=q),
            status='posted'
        )
        
    context = {'search_query': q, 'listings': jobs}
    return context


def notes_context(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        latest_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-create_date')[:5]

    else:
        count = 0
        latest_notifications = []

    context = {'total_unread_notes': count, 'latest_notes': latest_notifications}
    return context





