from django.db import models
from users.models import Profile
import uuid

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE,)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(null=True, blank=True, max_length=2000)
    source_link = models.CharField(null=True, blank=True, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    total_votes = models.IntegerField(default=0, null=True, blank=True)
    vote_ration = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,default='default.jpg')
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ration','-total_votes','title']

    @property
    def updateVote(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.total_votes = totalVotes
        self.vote_ration = ratio
        self.save()
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset
    
    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
    
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices= VOTE_TYPE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.value)
    
    class Meta:
        unique_together = [['owner','project',]]



    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
