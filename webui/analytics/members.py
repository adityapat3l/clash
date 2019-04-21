from clashapp.models import PlayerStatsHistoric, ClanStatsCurrent, PlayerStatsCurrent
import pandas as pd
from clashapp import db

class StaticPlayerStats:

    def __init__(self, **kwargs):
        self.player_name = kwargs.get('player_name')
        self.player_tag = kwargs.get('player_tag')
        self._player_obj = kwargs.get('player_obj')

    @classmethod
    def create_member_from_tag(cls, player_tag):
        player = PlayerStatsCurrent.query.filter(PlayerStatsCurrent.player_tag == player_tag).first()

        return cls(player_name=player.player_name, player_tag=player.player_tag, player_obj=player)