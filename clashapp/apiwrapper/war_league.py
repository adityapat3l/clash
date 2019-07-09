from clashapp.apiwrapper.player import BasicPlayer, Player
from .helpers.utils import try_enum
from clashapp.apiwrapper.clan import Clan, BasicClan


class WarLeague:
    """Represents a Searched Player that the API returns.
    Depending on which method calls this, some attributes may
    be ``None``.
    This class inherits both :class:`Player` and :class:`BasicPlayer`,
    and thus all attributes of these classes can be expected to be present
    Attributes
    -----------
    best_trophies:
        :class:`int` - The players top trophy count
    best_versus_trophies:
        :class:`int` - The players top versus trophy count
    war_stars:
        :class:`int` - The players war star count
    town_hall:
        :class:`int` - The players TH level
    builder_hall:
        :class:`int` - The players BH level
    versus_attacks_wins:
        :class:`int` - The players total BH wins
    """
    # __slots__ = ('best_trophies', 'war_stars', 'town_hall',
    #              'builder_hall', 'best_versus_trophies', 'versus_attacks_wins')

    def __init__(self, data):
        self._data = data
        self.state = data.get('state')
        self.season = data.get('season')
        self.rounds = data.get('rounds')  # List of Dictionary

    @property
    def _clans(self):
        """|iter|
        Returns an iterable of :class:`BasicClan`: A list of clans.
        """
        return iter(Clan(mdata) for mdata in self._data.get('clans', {}))

    @property
    def clans(self):
        """List[:class:`BasicClan`]: A list of clans"""
        return list(self._clans)


class WarLeagueRound:

    # data = /clans/{}/currentwar/leaguegroup

    def __init__(self, data):
        self._data = data
        self.state = data.get('state')
        self.team_size = data.get('teamSize')
        self.prep_start_time = data.get('preparationStartTime')
        self.start_time = data.get('startTime')
        self.end_time = data.get('endTime')
        self.war_start_time = data.get('warStartTime')

        self.clan = Clan(data.get('clan'))
        self.clan_stars = data.get('clan', {}).get('stars')
        self.clan_destruction = data.get('clan', {}).get('destructionPercentage')
        self.clan_attacks = data.get('clan', {}).get('attacks')

        self.opponent = Clan(data.get('opponent'))
        self.opponent_stars = data.get('opponent', {}).get('stars')
        self.opponent_destruction = data.get('opponent', {}).get('destructionPercentage')
        self.opponent_attacks = data.get('opponent', {}).get('attacks')


    @property
    def _clan_member_attacks(self):
        return iter(MemberAttack(mdata) for mdata in self._data.get('clan').get('members'))

    @property
    def clan_members_attacks(self):
        return list(self._clan_member_attacks)

    @property
    def _opponent_member_attacks(self):
        return iter(MemberAttack(mdata) for mdata in self._data.get('opponent').get('members'))

    @property
    def opponent_members_attacks(self):
        return list(self._opponent_member_attacks)


class Member:
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
        self._data = data
        self.player = try_enum(Player, data)
        self.raw_map_position = data.get('mapPosition')
        self.order = data.get('attacks', {}).get('order')

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
    """
    def __init__(self, data):
        super().__init__(data=data)
        self.stars = data.get('attacks', {}).get('stars', 0)
        self.destruction = data.get('attacks', {}).get('destructionPercentage', 0)
        self.defender_tag = data.get('attacks', {}).get('defenderTag')

    @property
    def is_3_star_attack(self):
        return self.stars == 3


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
        self.stars = data.get('attacks', {}).get('stars', 0)
        self.destruction = data.get('attacks', {}).get('destructionPercentage', 0)
        self.defender_tag = data.get('attacks', {}).get('defenderTag')

    @property
    def is_3_star_attack(self):
        return self.stars == 3

