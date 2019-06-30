from clashapp import db
from sqlalchemy.sql import text
import datetime
from clashapp.models import PlayerStatsCurrent
from discordapp.queries import SQL_QUERY


def send_user_help():

    output = """```\nUse any of the following commands:

'dark-looted': cb! dark-looted {player tag}
'exlixer-looted': cb! dark-looted {player tag}
'gold-looted': cb! dark-looted {player tag}

Search for your Player Tag by:

cb! find-tag {player name}
```
"""

    return output


def find_user_tag(player_name):

    player_name_list = PlayerStatsCurrent.query.filter_by(player_name=player_name).all()

    message_list = []

    for player in player_name_list:
        row_string = "{0} : {1}\n".format(player.player_name, player.player_tag)
        message_list.append(row_string)

    message_output = """```""" + ''.join(message_list) + """```"""

    return message_output

def format_results(player_name, results):
    message_list = []

    msg_header = """Stats for {player_name} for {command}\n"""
    message_list.append(msg_header)

    for row in results:
        row_string = "{0}    |    {1:,}\n".format(row[0], row[1])
        message_list.append(row_string)

    message_output = "```" + " ".join(message_list) + "```"
    return message_output.format(player_name=player_name, command=user_command)


def achv_gold_looted_summary(player_tag, max_len=7):
    player_name = PlayerStatsCurrent.query.filter_by(player_tag=player_tag).first().player_name

    player_sql_text = "and player_tag = '{0}'".format(player_tag)

    with db.engine.connect() as con:

        query = text(SQL_QUERY.format(metric_name='achv_gold_looted',
                                      sql_text=player_sql_text,
                                      max_len=max_len))
        cur = con.execute(query, created_time=datetime.datetime(2019, 4, 10))

    results = cur.fetchall()

    formatted_results = format_results(player_name, results)
    return formatted_results


def achv_elixer_looted_summary(player_tag, max_len=7):
    player_name = PlayerStatsCurrent.query.filter_by(player_tag=player_tag).first().player_name

    player_sql_text = "and player_tag = '{0}'".format(player_tag)

    with db.engine.connect() as con:

        query = text(SQL_QUERY.format(metric_name='achv_elixer_looted',
                                      sql_text=player_sql_text,
                                      max_len=max_len))
        cur = con.execute(query, created_time=datetime.datetime(2019, 4, 10))

    results = cur.fetchall()

    formatted_results = format_results(player_name, results)
    return formatted_results


def achv_dark_looted_summary(player_tag, max_len=7):

    player_name = PlayerStatsCurrent.query.filter_by(player_tag=player_tag).first().player_name

    player_sql_text = "and player_tag = '{0}'".format(player_tag)

    with db.engine.connect() as con:

        query = text(SQL_QUERY.format(metric_name='achv_dark_looted',
                                      sql_text=player_sql_text,
                                      max_len=max_len))
        cur = con.execute(query, created_time=datetime.datetime(2019, 4, 10))

    results = cur.fetchall()

    formatted_results = format_results(player_name, results)
    return formatted_results


def read_message(raw_message):

    user_tag = '#8292J8QV8'

    user_msg = raw_message[4:]  # get rid of "cb! " from the user message

    user_msg_parts = user_msg.split()
    global user_command
    user_command = user_msg_parts[0]

    if user_command == 'find-tag':
        user_name = ' '.join(user_msg_parts[1:])

        message_to_send = find_user_tag(user_name)
        return message_to_send

    elif user_command == 'help':
        message_to_send = send_user_help()
        return message_to_send

    command = user_command_key[user_command]

    if not user_command:
        return '''```Please enter msg in the following format: cb! {command} {user_tag}```'''

    if len(user_msg_parts) > 1:
        user_tag = user_msg_parts[1]
        message_to_send = command(user_tag)

        return message_to_send


user_command_key = {
    'dark-looted': achv_dark_looted_summary,
    'elixer-looted': achv_elixer_looted_summary,
    'gold-looted': achv_gold_looted_summary
}


if __name__ == '__main__':
    send_user_help()