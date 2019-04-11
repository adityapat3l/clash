class PlayerStats:
    def __init__(self, full_hist_df):
        self.full_hist_df = full_hist_df.copy(deep=True)
        self.player_df = None

        self.full_hist_df['player_name'] = self.full_hist_df['player_name'].str.lower()

    def set_player_tag(self, player_tag):
        self.player_df = self.full_hist_df[self.full_hist_df['player_tag'] == player_tag]

    def get_clan_df(self, clan_tag):
        self.clan_df =  self.full_hist_df[self.full_hist_df['clan_tag'] == clan_tag]

    def get_improvement_message(self, metric, player_tag=None, player_name=None):

        player_name = player_name.lower()

        assert player_tag or player_name, "Please input either player_tag or player_name"

        if player_name and not player_tag:
            player_df = self.full_hist_df[self.full_hist_df['player_name'] == player_name]

            player_tag_list = player_df['player_tag'].unique()

            if player_tag_list.shape[0] > 1:
                raise ValueError("Duplicate Player Name. Please enter a player tag")

        else:
            player_df = self.full_hist_df[self.full_hist_df['player_tag'] == player_tag]

        player_df = player_df[~player_df[metric].isna()]

        last_ts = player_df['created_time'].max()
        first_ts = player_df['created_time'].min()

        max_metric = player_df.loc[player_df['created_time'] == last_ts][metric]
        min_metric = player_df.loc[player_df['created_time'] == first_ts][metric]

        diff = int(max_metric) - int(min_metric)

        message = '{player_name} changed {diff} in {metric} between {first_ts} and {last_ts}'.format(
                                                                    player_name=player_name.title(),
                                                                    diff=diff,
                                                                    metric=metric,
                                                                    last_ts=last_ts,
                                                                    first_ts=first_ts)

        return message