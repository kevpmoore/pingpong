from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from pong.league.views import IndexView, RegistrationView, PlayerLeagueView, \
    LeagueGamesView, ActionPlayerInviteView, CreatePlayerInviteView, LoginView, LogoutView, \
    PlayerRankingsView, LeagueHistoryView, RandomLeaguesView


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
    url(r'^api/leagues/$', PlayerLeagueView.as_view()),
    url(r'^api/leagues/(?P<league_name>[\w]+)$', PlayerRankingsView.as_view()),
    url(r'^api/leagues/games/$', LeagueGamesView.as_view()),
    url(r'^api/leagues/games/(?P<league_name>[\w]+)/$', LeagueHistoryView.as_view()),
    url(r'^api/leagues/random/$', RandomLeaguesView.as_view()),

    #invites
    url(r'^api/invite/new/$', CreatePlayerInviteView.as_view()),
    url(r'^api/invite/action/$', ActionPlayerInviteView.as_view())
)
