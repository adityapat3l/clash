from clashapp.models import PlayerStatsHistoric, ClanStatsCurrent, PlayerStatsCurrent
import pandas as pd
from clashapp import db
from webui.webapp import celery
import time
import datetime
import logging
import os
from . import timber_handler

cur_dir = os.getcwd()
today_date = datetime.datetime.utcnow()

log_dir = os.path.join(cur_dir, 'logs/{date:%Y}/{date:%m}/{date:%d}'.format(date=today_date))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(level=logging.INFO,
                    filename=log_dir+'/webui.log',
                    filemode='a',
                    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)
logger.addHandler(timber_handler)

player_history_query = '''
SELECT created_time,
      {metric} -
      first_value({metric}) OVER (PARTITION BY player_tag ORDER BY created_time) AS {metric}_gained
FROM player_stats_historic
WHERE player_tag = '{player_tag}'
 AND {metric} IS NOT NULL
and created_time >= '2019-04-09'
'''


# @celery.task
def get_player_name(player_tag):
    player = PlayerStatsCurrent.query.filter_by(player_tag=player_tag).first()
    return player.player_name


# @celery.task
def player_limited_history_start(player_tag, metric='current_trophies', **kwargs):

    start_time = kwargs.get('start_time')
    end_time = kwargs.get('end_time')

    dt_metric_tuple = db.engine.execute(player_history_query.format(metric=metric, player_tag=player_tag))
    df = pd.DataFrame(dt_metric_tuple)
    df.columns = ['created_time', metric]

    return df


# @celery.task
def get_player_history_df(player_tag, metric='current_trophies'):
    history_df = PlayerStatsHistoric.query.filter_by(player_tag=player_tag).all()

    created_time_list = []
    data_list = []
    for fact in history_df:
        data_list.append(getattr(fact, metric))
        created_time_list.append(fact.created_time)

    df = pd.DataFrame({'created_time': created_time_list, metric: data_list})

    return df


# @celery.task
def get_clan_player_dropdown_list(clan_tag='#YUPCJJCR'):
    clan = ClanStatsCurrent.query.filter_by(clan_tag=clan_tag).first()

    output = []
    for member in clan.clan_members:
        player_dict = {}
        player_dict['label'] = member.player_name
        player_dict['value'] = member.player_tag

        output.append(player_dict)

    sorted_output = sorted(output, key=lambda k: k['label'].lower())

    return sorted_output


def get_clan_dropdown_list():
    clan_list = ClanStatsCurrent.query.all()
    output = [{'label': clan.clan_name,
               'value': clan.clan_tag}
              for clan in clan_list]

    sorted_output = sorted(output, key=lambda k: k['label'].lower())

    return sorted_output


# def get_player_name(player_tag):
#     result = _get_player_name.delay(player_tag)
#     while not result.ready():
#         time.sleep(0.5)
#     player_name = result.get()
#     return player_name
#
#
# def get_clan_player_dropdown_list(clan_name='For Aiur'):
#     logger.info('Getting Dropdown for clan: {}'.format(clan_name))
#     result = _get_clan_player_dropdown_list.delay(clan_name=clan_name)
#     while not result.ready():
#         logger.info('Waiting on Dropdown')
#         time.sleep(0.5)
#     drop_down_list = result.get()
#     return drop_down_list
#
#
# def get_player_history_df(player_tag, metric='current_trophies'):
#     logger.info('Getting Player History for player: {} for metric: {}'.format(player_tag, metric))
#     result = _get_player_history_df.delay(player_tag, metric=metric)
#     while not result.ready():
#         logger.info('Waiting on Player History')
#         time.sleep(0.5)
#
#     df_json = result.get()
#     df = pd.read_json(df_json)
#
#     df.reset_index(drop=True, inplace=True)
#     df.sort_values('created_time', inplace=True)
#
#     return df
#
#
# def player_limited_history_start(player_tag, metric='current_trophies', **kwargs):
#     logger.info('Getting Player History for player: {} for metric: {}'.format(player_tag, metric))
#     result = _player_limited_history_start.delay(player_tag, metric=metric)
#     while not result.ready():
#         logger.info('Waiting on Player History')
#         time.sleep(0.5)
#     df_json = result.get()
#     df = pd.read_json(df_json)
#
#     df.reset_index(drop=True, inplace=True)
#     df.sort_values('created_time', inplace=True)
#
#     return df


if __name__ == '__main__':
    print(get_clan_player_dropdown_list())