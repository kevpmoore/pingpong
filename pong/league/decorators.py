from models import Player, League, LeaguePlayerMap
from rest_framework import status
from rest_framework.response import Response


def league_membership_required(fn):
    def wrapper(request, *args, **kwargs):
        try:
            request = request.request
            league_name = request.DATA['league_name']
            league = League.objects.get(league_name=league_name)

            league.player_set.get(id=request.user.id)

            return fn(request, *args, **kwargs)
        except Exception, e:
            return Response([{'type': 'danger', 'msg': 'You must be part of the league for that.'}], status=status.HTTP_403_FORBIDDEN)
    return wrapper