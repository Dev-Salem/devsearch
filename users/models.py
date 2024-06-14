from django.db import models
from django.contrib.auth.models import User
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    intro = models.CharField(max_length=200, blank=True, null=True)
    github_link = models.CharField(max_length=500, blank=True, null=True)
    website_link = models.CharField(max_length=500, blank=True, null=True)
    twitter_link = models.CharField(max_length=500, blank=True,null= True)
    image = models.ImageField(upload_to='profiles/', default='profiles/user-default.png')

    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ['created_at']

class Skill(models.Model) :
    owner = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created_at']