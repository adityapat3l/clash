from clashapp.models import PlayerStatsHistoric, ClanStatsCurrent
import pandas as pd


def get_player_history_df(player_tag, metric='current_trophies'):

    history_df = PlayerStatsHistoric.query.filter_by(player_tag=player_tag).all()

    created_time_list = []
    data_list = []
    for fact in history_df:
        data_list.append(getattr(fact, metric))
        created_time_list.append(fact.created_time)

    df = pd.DataFrame(created_time_list, data_list).reset_index()
    df.columns = ['created_time', metric]

    return df


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
    print(get_player_history_df('#8292J8QV8'))