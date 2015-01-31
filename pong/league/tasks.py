from celery import Celery
from pong.league.models import *
from datetime import date
app = Celery('tasks')

@app.task
def log_rank():
    print '*** UPDATING ***'
    for league in League.objects.all():
        metas = LeaguePlayerMap.objects.filter(league_fk=league).order_by('-rating')

        for n in xrange(0, len(metas), 1):
            PositionHistory.objects.create(
                position=n+1,
                date=date.today(),
                league_fk=metas[n].league_fk,
                player_fk=metas[n].player_fk
            )