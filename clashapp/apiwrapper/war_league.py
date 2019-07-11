from clashapp.apiwrapper.player import BasicPlayer, Player
from .helpers.utils import try_enum
from clashapp.apiwrapper.clan import SearchClan, LeagueClan
from clashapp.apiwrapper.api import LeagueAPI


class WarLeague:
    """
    Represents the Base Data for a War League
    Data comes from /clans/{}/currentwar/leaguegroup
    -----------
    state:
        :class:`str` - If the League is active or Not
    season:
        :class:`str` - The name of the season
    clans:
        :class:`list` - A list of class Clan
    rounds:
        :class:`list` - The list of class WarLeagueRound
    """
    __slots__ = ('state', 'season', 'town_hall',
                 '_data')

    def __init__(self, data):
        self._data = data
        self.state = data.get('state')
        self.season = data.get('season')
        # self.rounds = data.get('rounds')

    @property
    def _clans(self):
        return iter(SearchClan(mdata) for mdata in self._data.get('clans', {}))

    @property
    def clans(self):
        return list(self._clans)

    @property
    def _rounds(self):
        raw_rounds = self._data.get('rounds')
        rounds_list = [war_round['warTags'] for war_round in raw_rounds]
        rounds = [Round(val, idx+1) for idx, val in enumerate(rounds_list)]
        return rounds

    @property
    def rounds(self):
        return list(self._rounds)


class Round:
    """
    Represents 1 day of warring in CWL
    Each CWL has 7 rounds (war days)
    Each round has 4 battles
    -----------
    round_number:
        :class:`int` - Battle Number of the CWL (1-8)
    battles:
        :class:`list` - The list of class WarLeagueBattle
    """

    def __init__(self, data, pos):
        self._data = data  # List of List
        self.round_number = pos

    @property
    def battles(self):
        battle_data = [LeagueAPI().get_league_war_details(battle) for battle in self._data]
        return [WarLeagueBattle(data=battle_data[idx], war_tag=val) for idx, val in enumerate(self._data)]


class WarLeagueBattle:
    """
     Represents 1 Battle in CWL.
     Any particular day of CWL has 4 battles (8 clans)
     Data comes from /clanwarleagues/wars/{}
     -------
     tag:
         :class:`str` - The battle tag
     state:
         :class:`str` - Is the battle ongoing or ended?
     clan_size:
         :class:`int` - The size of the eligible member base for the clan in CWL
     opponent_size:
         :class:`int` - The size of the eligible member base for the opposing clan in CWL
     clan:
         :class:`ClanRound` - Contains data of LeagueClan() data along with stars, destruction etc for that battle.
     opponent:
         :class:`ClanRound` - Same as `clan` but for the opposing clan.
     """
    def __init__(self, data, war_tag=None):
        self._data = data
        self.tag = war_tag
        self.state = data.get('state')
        self.clan_size = data.get('teamSize')
        self.opponent_size = None  # TODO: MAKE FUNCTION FOR THIS
        self.prep_start_time = data.get('preparationStartTime')
        self.start_time = data.get('startTime')
        self.end_time = data.get('endTime')

    @property
    def clan(self):
        return ClanRound(self._data.get('clan'))

    @property
    def opponent(self):
        # return
        return ClanRound(self._data.get('opponent'))

    # @property
    # def _clan_member_attacks(self):
    #     return iter(MemberAttack(mdata) for mdata in self._data.get('clan').get('members'))
    #
    # @property
    # def clan_members_attacks(self):
    #     return list(self._clan_member_attacks)
    #
    # @property
    # def _opponent_member_attacks(self):
    #     return iter(MemberAttack(mdata) for mdata in self._data.get('opponent').get('members'))
    #
    # @property
    # def opponent_members_attacks(self):
    #     return list(self._opponent_member_attacks)


class ClanRound(LeagueClan):
    """
     Represents 1 round for a specific Clan
     -------
     stars:
         :class:`int` - The number of stars gained by the clan
     destruction:
         :class:`float` - Destruction % as shown in-game
     total_attacks:
         :class:`int` - The number of total attacks used by the clan
     attacks:
         :class:`list` - A list of MemberAttacks() for that round for the clan
    """
    def __init__(self, data):
        super().__init__(data=data)
        self._data = data
        self.stars = data.get('stars')
        self.destruction = data.get('destructionPercentage')  # This is faulty. The API calculates this incorrectly.
        self.total_attacks = data.get('attacks')

    @property
    def _attacks(self):
        return iter(MemberAttack(mdata) for mdata in self._data.get('members', {}))

    @property
    def attacks(self):
        return list(self._attacks)




class Member(Player):
    """
    Represents a Member in a Clan War League battle.
    ------------------
    raw_map_position:
        :class:`int` - The position on the map if all eligible members played in the war of infinite size.
    order:
        :class:`int` - The attack in which order was performed in war
    map_position:
    :class: `int` - The position on the real map of the war (with 15 or 30 members)
    """
    def __init__(self, data):
        super().__init__(data=data)
        self._data = data
        self.player = try_enum(Player, data)
        self.raw_map_position = data.get('mapPosition')
        if data.get('attacks'):
            self.order = data.get('attacks', {})[0].get('order')

    @property
    def map_position(self):
        return


class MemberAttack(Member):
    """
    Represents a Member Attack that is returned by the War League Data
    Depending on which method calls this, some attributes may
    be ``None``.
    -----------
    stars:
        :class:`int` - The stars earned in the attack
    destruction:
        :class:`float` - The attack percentage gained from destruction
    defender_tag:
        :class:`str` - The defender tag of the attack
    order:
        :class:`int` - The order of the attack.
    """
    def __init__(self, data):
        super().__init__(data=data)

        self._attacks = data.get('attacks')

        self.exists = self._attacks is not None
        self.stars = data.get('attacks', [{}])[0].get('stars', 0)
        self.destruction = data.get('attacks', [{}])[0].get('destructionPercentage', 0)
        self.defender_tag = data.get('attacks', [{}])[0].get('defenderTag')
        self.attacker_tag = data.get('attacks', [{}])[0].get('attackerTag')

        self.order = data.get('attacks', [{}])[0].get('order')

    @property
    def is_3_star_attack(self):
        return self.stars == 3

    @property
    def attacker(self):
        return  #  Class of Player

    @property
    def defender(self):
        return #  Class of defender


# TODO: Parse the API to find the defense of the war. This is fake vars right now
class MemberDefense(Member):
    """
    Represents a Member Attack that is returned by the War League Data
    Depending on which method calls this, some attributes may
    be ``None``.
    -----------
    stars:
        :class:`int` - The stars earned in the attack
    destruction:
        :class:`float` - The attack percentage gained from destruction
    defender_tag:
        :class:`str` - The defender tag of the attack
    """
    def __init__(self, data):
        super().__init__(data=data)
        self.stars = data.get('stars', 0)
        self.destruction = data.get('destructionPercentage', 0)
        self.defender_tag = data.get('defenderTag')


    @property
    def is_3_star_attack(self):
        return self.stars == 3

