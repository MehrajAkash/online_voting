# from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.election.title})"

    def vote_count(self):
        return self.votes.count()


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'election')  # One vote per user per election

    def __str__(self):
        return f"{self.voter.username} voted in {self.election.title}"