from clashapp.models import PlayerStatsHistoric, ClanStatsCurrent, PlayerStatsCurrent
import pandas as pd
from clashapp import db
from webui.webapp import celery

player_history_query = '''
SELECT created_time,
      {metric} -
      first_value({metric}) OVER (PARTITION BY player_tag ORDER BY created_time) AS {metric}_gained
FROM player_stats_historic
WHERE player_tag = '{player_tag}'
 AND {metric} IS NOT NULL
and created_time >= '2019-04-09'
'''


@celery.task(acks_late=True)
def get_player_name(player_tag):
    player = PlayerStatsCurrent.query.filter_by(player_tag=player_tag).first()
    return player.player_name


@celery.task
def player_limited_history_start(player_tag, metric='current_trophies', **kwargs):

    start_time = kwargs.get('start_time')
    end_time = kwargs.get('end_time')

    a = db.engine.execute(player_history_query.format(metric=metric, player_tag=player_tag))
    names = [row for row in a]
    df = pd.DataFrame(names)
    df.columns = ['created_time', metric]
    return df


@celery.task
def get_player_history_df(player_tag, metric='current_trophies'):

    history_df = PlayerStatsHistoric.query.filter_by(player_tag=player_tag).all()

    created_time_list = []
    data_list = []
    for fact in history_df:
        data_list.append(getattr(fact, metric))
        created_time_list.append(fact.created_time)

    df = pd.DataFrame({'created_time': created_time_list, metric: data_list})

    return df


@celery.task
def get_clan_player_dropdown_list(clan_name='For Aiur'):
    clan = ClanStatsCurrent.query.filter_by(clan_name=clan_name).first()

    output = []
    for member in clan.clan_members:
        player_dict = {}
        player_dict['label'] = member.player_name
        player_dict['value'] = member.player_tag

        output.append(player_dict)

    sorted_output = sorted(output, key=lambda k: k['label'].lower())

    return sorted_output


if __name__ == '__main__':
    print(get_player_name('#8292J8QV8'))