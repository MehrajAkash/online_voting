#from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from .models import Election, Candidate, Vote
from .forms import RegisterForm, VoteForm


def home(request):
    elections = Election.objects.filter(is_active=True)
    return render(request, 'voting/home.html', {'elections': elections})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('vote_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You can now vote.')
            return redirect('vote_list')
    else:
        form = RegisterForm()
    return render(request, 'voting/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('vote_list')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('vote_list')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'voting/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def vote_list(request):
    now = timezone.now()
    elections = Election.objects.filter(is_active=True, start_date__lte=now, end_date__gte=now)
    voted_election_ids = Vote.objects.filter(voter=request.user).values_list('election_id', flat=True)
    return render(request, 'voting/vote_list.html', {
        'elections': elections,
        'voted_election_ids': voted_election_ids,
    })


@login_required
def vote(request, election_id):
    election = get_object_or_404(Election, id=election_id, is_active=True)
    now = timezone.now()

    if now < election.start_date or now > election.end_date:
        messages.error(request, 'This election is not currently open.')
        return redirect('vote_list')

    if Vote.objects.filter(voter=request.user, election=election).exists():
        messages.warning(request, 'You have already voted in this election.')
        return redirect('results', election_id=election.id)

    if request.method == 'POST':
        form = VoteForm(election, request.POST)
        if form.is_valid():
            candidate = form.cleaned_data['candidate']
            Vote.objects.create(voter=request.user, candidate=candidate, election=election)
            messages.success(request, f'Your vote for {candidate.name} has been recorded!')
            return redirect('results', election_id=election.id)
    else:
        form = VoteForm(election)

    return render(request, 'voting/vote.html', {'election': election, 'form': form})


def results(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = election.candidates.all().order_by('-votes__id')

    candidate_data = []
    total_votes = Vote.objects.filter(election=election).count()

    for candidate in election.candidates.all():
        count = candidate.vote_count()
        percentage = round((count / total_votes * 100), 1) if total_votes > 0 else 0
        candidate_data.append({
            'candidate': candidate,
            'count': count,
            'percentage': percentage,
        })

    candidate_data.sort(key=lambda x: x['count'], reverse=True)

    return render(request, 'voting/results.html', {
        'election': election,
        'candidate_data': candidate_data,
        'total_votes': total_votes,
    })