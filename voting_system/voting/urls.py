from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('vote/', views.vote_list, name='vote_list'),
    path('vote/<int:election_id>/', views.vote, name='vote'),
    path('results/<int:election_id>/', views.results, name='results'),
]