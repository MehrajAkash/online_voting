#from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Election, Candidate, Vote


class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 2


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'start_date', 'end_date', 'total_votes']
    list_editable = ['is_active']
    inlines = [CandidateInline]

    def total_votes(self, obj):
        return Vote.objects.filter(election=obj).count()
    total_votes.short_description = 'Total Votes'


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'party', 'election', 'vote_count']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'candidate', 'election', 'voted_at']
    readonly_fields = ['voter', 'candidate', 'election', 'voted_at']