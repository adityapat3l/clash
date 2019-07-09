from clashapp.apiwrapper.base import Troop, Spell, Hero, Achievement
from collections import OrderedDict
from .helpers.utils import try_enum, HERO_ORDER, BUILDER_TROOPS_ORDER, HOME_TROOP_ORDER, SPELL_ORDER


class Player:
    """Represents the most stripped down version of a player.
    All other player classes inherit this.
    Attributes
    ------------
    tag:
        :class:`str` - The clan tag
    name:
        :class:`str` - The clan name
    """
    __slots__ = ('name', 'tag', '_data', 'town_hall')

    def __init__(self, data):
        self._data = data
        self.name = data['name']
        self.tag = data.get('tag')
        self.town_hall = data.get('townHallLevel')
    #
    # def __str__(self):
    #     return self.name


class BasicPlayer(Player):
    """Represents a Basic Player that the API returns.
    Depending on which method calls this, some attributes may
    be ``None``.
    This class inherits :class:`Player`, and thus all attributes
    of :class:`Player` can be expected to be present.
    Attributes
    -----------
    clan:
        :class:`Basic Clan` - The clan the member belongs to. May be ``None``
    level:
        :class:`int` - The player level.
    trophies:
        :class:`int` - The player's trophy count.
    versus_trophies:
        :class:`int` - The player's versus trophy count.
    clan_rank:
        :class:`int` - The members clan rank
    clan_previous_rank
        :class:`int` - The members clan rank last season
    league_rank:
        :class:`int` - The player's current rank in their league for this season
    donations:
        :class:`int` - The members current donation count
    received:
        :class:`int` - The member's current donation received count
    attack_wins:
        :class:`int` - The players current attack wins for this season
    defense_wins:
        :class:`int` - The players current defense wins for this season
    """
    __slots__ = ('clan', 'level', 'trophies', 'versus_trophies',
                 'clan_rank', 'clan_previous_rank', 'league_rank', 'donations',
                 'received', 'attack_wins', 'defense_wins')

    def __init__(self, data, clan=None):
        super(BasicPlayer, self).__init__(data)

        self._data = data
        self.clan = clan
        self.level = data.get('expLevel')
        self.trophies = data.get('trophies')
        self.versus_trophies = data.get('versusTrophies')
        self.clan_rank = data.get('clanRank')
        self.clan_previous_rank = data.get('clanRank')
        try:
            self.league_rank = data.get('league', {}).get('name', 'Unranked')
        except AttributeError:
            self.league_rank = 'Unranked'
        self.donations = data.get('donations')
        self.received = data.get('donationsReceived')
        self.attack_wins = data.get('attackWins')
        self.defense_wins = data.get('defenseWins')

        if not self.clan:
            cdata = data.get('clan')
            if cdata:
                from .clan import BasicClan  # hack because circular imports
                self.clan = BasicClan(data=cdata)

    @property
    def role(self):
        """:class:`str`: The members role in the clan - member, elder, etc."""
        role = self._data.get('role')
        if role == 'admin':
            return 'elder'
        return role


class SearchPlayer(BasicPlayer):
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
    __slots__ = ('best_trophies', 'war_stars', 'town_hall',
                 'builder_hall', 'best_versus_trophies', 'versus_attacks_wins')

    def __init__(self, data):
        super(SearchPlayer, self).__init__(data=data)

        from .clan import Clan  # hack because circular imports
        self._data = data
        self.clan = try_enum(Clan, data.get('clan'))
        self.best_trophies = data.get('bestTrophies')
        self.war_stars = data.get('warStars')
        self.builder_hall = data.get('builderHallLevel')
        self.best_versus_trophies = data.get('bestVersusTrophies')
        self.versus_attacks_wins = data.get('versusBattleWins')

    @property
    def _achievements(self):
        """|iter|
        Returns an iterable of :class:`Achievement`: the player's achievements."""
        return iter(Achievement(data=adata, player=self)
                    for adata in self._data.get('achievements', []))

    @property
    def achievements(self):
        """List[:class:`Achievement`]: List of the player's achievements"""
        return list(self._achievements)

    @property
    def troops(self):
        """List[:class:`Troop`]: List of the player's troops"""
        return [Troop(data=sdata, player=self)
                for sdata in self._data.get('troops', [])]

    @property
    def heroes(self):
        """List[:class:`Hero`]: List of the player's heroes"""
        return [Hero(data=hdata, player=self)
                for hdata in self._data.get('heroes', [])]

    @property
    def spells(self):
        """List[:class:`Spell`]: List of the player's spells"""
        return [Spell(data=sdata, player=self)
                for sdata in self._data.get('spells', [])]

    @property
    def achievements_dict(self, attr='name'):
        """:class:`dict` - {name: :class:`Achievement`} A dict of achievements by name.
        Pass in an attribute of :class:`Achievement` to get that attribute as the key
        """
        return {getattr(m, attr): m for m in self._achievements}

    @property
    def home_troops_dict(self, attr='name'):
        """:class:`dict` - {name: :class:`Troop`}: A dict of home base troops by name.
        Pass in an attribute of :class:`Troop` to get that attribute as the key
        """
        return {getattr(m, attr): m for m in self.troops if m.is_home_base}

    @property
    def builder_troops_dict(self, attr='name'):
        """:class:`dict` - {name: :class:`Troop`}: A dict of builder base troops by name.
        Pass in an attribute of :class:`Troop` to get that attribute as the key
        """
        return {getattr(m, attr): m for m in self.troops if m.is_builder_base}

    @property
    def heroes_dict(self, attr='name'):
        """:class:`dict` - {name: :class:`Hero`}: A dict of heroes by name.
        Pass in an attribute of :class:`Hero` to get that attribute as the key
        """
        return {getattr(m, attr): m for m in self.heroes}

    @property
    def spells_dict(self, attr='name'):
        """:class:`dict` - {name: :class:`Spell`}: A dict of spells by name.
        Pass in an attribute of :class:`Spell` to get that attribute as the key
        """
        return {getattr(m, attr): m for m in self.spells}

    @property
    def ordered_home_troops(self):
        """:class:`collections.OrderedDict` - An ordered dict of troops by name.
        This will return troops in the order found in both barracks and labatory in-game.
        """
        key_order = {k: v for v, k in enumerate(HOME_TROOP_ORDER)}
        return OrderedDict(sorted(self.home_troops_dict.items(), key=lambda i: key_order.get(i[0])))

    @property
    def ordered_builder_troops(self):
        """:class:`collections.OrderedDict` - An ordered dict of home base troops by name.
        This will return troops in the order found in both barracks and labatory in-game.
        """
        key_order = {k: v for v, k in enumerate(BUILDER_TROOPS_ORDER)}
        return OrderedDict(sorted(self.builder_troops_dict.items(), key=lambda i: key_order.get(i[0])))

    @property
    def ordered_spells(self):
        """:class:`collections.OrderedDict` - An ordered dict of spells by name.
        This will return spells in the order found in both spell factory and labatory in-game.
        """
        key_order = {k: v for v, k in enumerate(SPELL_ORDER)}
        return OrderedDict(sorted(self.spells_dict.items(), key=lambda i: key_order.get(i[0])))

    @property
    def ordered_heroes(self):
        """:class:`collections.OrderedDict` - An ordered dict of heroes by name.
        This will return heroes in the order found in the labatory in-game.
        """
        key_order = {k: v for v, k in enumerate(HERO_ORDER)}
        return OrderedDict(sorted(self.heroes_dict.items(), key=lambda i: key_order.get(i[0])))

    def _db_achievement_load_dict(self):
        """:class:`dict` - {name: :class:`Achievement`} A dict of achievements by name.
        Pass in an attribute of :class:`Achievement` to get that attribute as the key

        Output: {'db_attribute_value: value}
        Example: {'town_halls_destroyed: 106}
        """
        db_attributes = {'Humiliator':'town_halls_destroyed',
                         'Wall Buster': 'walls_destroyed',
                         'Sharing is caring': 'spells_donated',
                         'Friend in Need': 'troops_donated',
                         'Games Champion': 'clan_game_points',
                         'Nice and Tidy': 'obstacles_removed',
                         'Heroic Heist': 'dark_looted',
                         'Elixir Escapade': 'elixer_looted',
                         'Gold Grab': 'gold_looted'}

        output = {db_attributes[m.name]: m.value
                        for m in self._achievements
                        if m.name in db_attributes.keys()}

        return output


    def _db_hero_load_dict(self):
        """:class:`dict` - {name: :class:`Achievement`} A dict of achievements by name.
        Pass in an attribute of :class:`Achievement` to get that attribute as the key

        Output: {'db_attribute_value: value}
        Example: {'town_halls_destroyed: 106}
        """
        db_attributes = {'Barbarian King': 'barbarian_king',
                         'Archer Queen': 'archer_queen',
                         'Grand Warden': 'grand_warden',
                         'Battle Machine': 'battle_machine'}

        output = {db_attributes[m.name]: m.level
                  for m in self.heroes
                  if m.name in db_attributes.keys()}

        return output

    def _db_troop_load_dict(self):
        """:class:`dict` - {name: :class:`Achievement`} A dict of achievements by name.
        Pass in an attribute of :class:`Achievement` to get that attribute as the key

        Output: {'db_attribute_value: value}
        Example: {'town_halls_destroyed: 106}
        """
        db_attributes = {'Barbarian': 'barbarian',
                         'Archer': 'archer',
                         'Goblin': 'goblin',
                         'Giant': 'giant',
                         'Wall Breaker': 'wall_breaker',
                         'Balloon': 'balloon',
                         'Wizard': 'wizard',
                         'Healer': 'healer',
                         'Dragon': 'dragon',
                         'P.E.K.K.A': 'pekka',
                         'Minion': 'minion',
                         'Hog Rider': 'hog_rider',
                         'Valkyrie': 'valkyrie',
                         'Golem': 'golem',
                         'Witch': 'witch',
                         'Lava Hound': 'lava_hound',
                         'Bowler': 'bowler',
                         'Baby Dragon': 'baby_dragon',
                         'Miner': 'miner',
                         'Wall Wrecker': 'wall_wrecker',
                         'Battle Blimp': 'battle_blimp',
                         'Ice Golem': 'ice_golem',
                         'Electro Dragon': 'electro_dragon'}

        output = {db_attributes[m.name]: m.level
                  for m in self.troops
                  if m.name in db_attributes.keys()}

        return output


    def _db_spell_load_dict(self):
        """:class:`dict` - {name: :class:`Achievement`} A dict of achievements by name.
        Pass in an attribute of :class:`Achievement` to get that attribute as the key

        Output: {'db_attribute_value: value}
        Example: {'town_halls_destroyed: 106}
        """
        db_attributes = {'Lightning Spell': 'lightning',
                         'Healing Spell': 'healing',
                         'Rage Spell': 'rage',
                         'Jump Spell': 'jump',
                         'Freeze Spell': 'freeze',
                         'Poison Spell': 'poison',
                         'Earthquake Spell': 'earthquake',
                         'Haste Spell': 'haste',
                         'Clone Spell': 'clone',
                         'Skeleton Spell': 'skeleton',
                         'Bat Spell': 'bat'}

        output = {db_attributes[m.name]: m.level
                  for m in self.spells
                  if m.name in db_attributes.keys()}

        return output






