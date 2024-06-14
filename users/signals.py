from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import *
from projects.models import Project
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def creteProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name=user.first_name,
            email =user.email,
        )
        
        subject = 'Welcome to DevSearch'
        recipient = 'Glad you joined us!'
        send_mail(
            subject,
            recipient,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass




