from clashapp import db
from sqlalchemy.sql import text
import datetime

SQL_QUERY = """ 
select * from m_player_stats
where 
{sql_text}
and metric_name = '{metric_name}'
limit 1
"""

def get_data(metric_name=None, player_name=None, player_tag=None):

    assert metric_name
    assert player_name or player_tag

    player_info = player_tag or player_name

    with db.engine.connect() as con:

        if player_tag:
            player_text = "player_tag = '{}'".format(player_tag)
        else:
            player_text = "player_name = '{}'".format(player_name)

        query = text(SQL_QUERY.format(metric_name=metric_name, sql_text=player_text))
        cur = con.execute(query, created_time=datetime.datetime(2019, 4, 10))

        results = cur.fetchall()
        headers = cur.keys()

        return results


def format_data(message_data, **kwargs):

    message_parts = message_data.split()[1:]

    metric_key = None
    player_name = None
    metric_name = None

    print(message_parts)

    if len(message_parts) == 1:
        player_name = message_parts[0]

    if len(message_parts) == 2:
        player_name = message_parts[0]
        metric_name = message_parts[1]
        metric_key = metric_key_dict[metric_name]

    string_list = []

    metric_key = metric_key or metric_key_dict[kwargs.get('metric_name')]
    player_name = player_name or kwargs.get('player_name')

    results = get_data(metric_name=metric_key, player_name=player_name, player_tag=None)

    metric_value = results[4]

    msg_text = '''`{} : {} {}`'''.format(player_name, metric_value, metric_name or kwargs.get('metric_name'))

    string_list.append(msg_text)

    formatted_text = ''.join(string_list)
    return formatted_text


metric_key_dict = {
    'dark': 'achv_dark_looted',
    'elixer': 'achv_elixer_looted',
    'gold': 'achv_gold_looted',
    'trophies': 'current_trophies',
    'donations_given': 'donations_given',
    'donations_received': 'donations_received',
    'war_stars': 'war_stars'
}