from django.db.models.signals import post_save
from django.dispatch import receiver
from dash.models import Job_Listing, Notification, User


# @receiver(post_save, sender=Job_Listing)
# def create_task_notification(sender, instance, created):
#     if created:
#         users = User.objects.all()
        
#         for user in users:
#             Notification.objects.create(
#                 user=user,
#                 message=f"New Task Available: {instance.title}"
#             )
