from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from pong.league.views import IndexView, RegistrationView, PlayerLeagueView, \
    LeagueGamesView, ActionPlayerInviteView, CreatePlayerInviteView, LoginView, LogoutView, \
    PlayerRankingsView, LeagueHistoryView, LeagueJoinView, PlayerView, SlackView, \
    PositionHistoryView
from pong.tournament.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pong.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),

    #player
    url(r'^api/new-player/$', RegistrationView.as_view()),
    url(r'^api/login/$', LoginView.as_view()),
    url(r'^api/logout/$', LogoutView.as_view()),

    #leagues
    url(r'^api/leagues/graph/(?P<league_name>[A-Za-z0-9-_]+)/$', PositionHistoryView.as_view()),
    url(r'^api/leagues/$', PlayerLeagueView.as_view()),
    url(r'^api/leagues/(?P<league_name>[A-Za-z0-9-_]+)$', PlayerRankingsView.as_view()),
    url(r'^api/leagues/games/$', LeagueGamesView.as_view()),
    url(r'^api/leagues/games/(?P<league_name>[A-Za-z0-9-_]+)/$', LeagueHistoryView.as_view()),
    url(r'^api/leagues/join/$', LeagueJoinView.as_view()),
    url(r'^api/leagues/(?P<league_name>[A-Za-z0-9-_]+)/(?P<username>[A-Za-z0-9-_]+)/$', PlayerView.as_view()),


    #tournaments
    url(r'^api/create-tournament/$', TournamentView.as_view()),
    url(r'^api/create-tournament/(?P<league_name>[A-Za-z0-9-_]+)/$', TournamentView.as_view()),
    url(r'^api/tournament_active/$', TournamentFeature.as_view()),
    url(r'^api/tournament/(?P<tournament_name>[A-Za-z0-9-_]+)/$', TournamentGamesView.as_view()),

    #invites
    url(r'^api/invite/new/$', CreatePlayerInviteView.as_view()),
    url(r'^api/invite/action/$', ActionPlayerInviteView.as_view()),

    #stuff
    url(r'^api/slack-it/$', SlackView.as_view())
)
