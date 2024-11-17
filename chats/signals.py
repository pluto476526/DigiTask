from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User
from chats.models import Profile, Chat_Message


@receiver(post_save, sender=User)
def create_user_profile(sender,instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



@receiver(user_logged_out)
def mark_messages_as_read(sender, request, user, **kwargs):
    if user.is_authenticated:
        # Mark all unread messages received by the user as read
        Chat_Message.objects.filter(receiver=user, read=False).update(read=True)
