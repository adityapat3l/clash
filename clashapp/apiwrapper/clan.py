from itertools import chain
# from .helpers.iterators import PlayerIterator
from .helpers.utils import get


class Clan:
    """Represents the most stripped down version of clan info.
    All other clan classes inherit this.
    Attributes
    -----------
    tag : str
        The clan tag.
    name : str
        The clan name.
    """
    __slots__ = ('tag', 'name', '_data')

    def __init__(self, data):
        self._data = data
        self.tag = data.get('tag')
        self.name = data.get('name')
    #
    # def __str__(self):
    #     return self.name


class BasicClan(Clan):
    """Represents a Basic Clan that the API returns.
    Depending on which method calls this, some attributes may
    be ``None``.
    This class inherits :class:`Clan`, and thus all attributes
    of :class:`Clan` can be expected to be present.
    Attributes
    -----------
    level:
        :class:`int` - The clan level.
    points:
        :class:`int` - The clan trophy points.
    versus_points:
        :class:`int` - The clan versus trophy points.
    member_count:
        :class:`int` - The member count of the clan
    rank:
        :class:`int` - The clan rank for it's location this season
    previous_rank:
        :class:`int` - The clan rank for it's location in the previous season
    """
    __slots__ = ('level', 'points', 'versus_points',
                 'member_count', 'rank', 'previous_rank')

    def __init__(self, data):
        super().__init__(data=data)

        self.level = data.get('clanLevel')
        self.points = data.get('clanPoints')
        self.versus_points = data.get('clanVersusPoints')
        self.member_count = data.get('members')
        self.rank = data.get('rank')
        self.previous_rank = data.get('previous_rank')


class SearchClan(BasicClan):
    """Represents a Searched Clan that the API returns.
    Depending on which method calls this, some attributes may
    be ``None``.
    This class inherits both :class:`Clan` and :class:`BasicClan`,
    and thus all attributes of these classes can be expected to be present.
    Attributes
    -----------
    type:
        :class:`str` - The clan type: open, closed, invite-only etc.
    required_trophies:
        :class:`int` - The required trophies to join
    war_frequency:
        :class:`str` - The war frequency of the clan
    war_win_streak:
        :class:`int` - The current war win streak of the clan
    war_wins:
        :class:`int` - The total war wins of the clan
    war_ties:
        :class:`int` - The total war ties of the clan
    war_losses:
        :class:`int` - The total war losses of the clan
    public_war_log:
        :class:`bool` - Indicates whether the war log is public
    description:
        :class:`str` - The clan description
    """
    __slots__ = ('type', 'required_trophies', 'war_frequency', 'war_win_streak',
                 'war_wins', 'war_ties', 'war_losses', 'public_war_log',
                 'description')

    def __init__(self, data):
        super().__init__(data=data)

        self.type = data.get('type')
        self.required_trophies = data.get('requiredTrophies')
        self.war_frequency = data.get('warFrequency')
        self.war_win_streak = data.get('warWinStreak')
        self.war_wins = data.get('warWins')
        self.war_ties = data.get('warTies')
        self.war_losses = data.get('warLosses')
        self.public_war_log = data.get('isWarLogPublic')
        self.description = data.get('description', '')

    @property
    def _members(self):
        """|iter|
        Returns an iterable of :class:`BasicPlayer`: A list of clan members.
        """
        from .player import BasicPlayer  # hack because circular imports
        return iter(BasicPlayer(mdata) for mdata in self._data.get('memberList', []))

    @property
    def members(self):
        """List[:class:`SearchPlayer`]: A list of clan members"""
        return list(self._members)

    @property
    def member_dict(self, attr='tag'):
        """Dict: {attr: :class:`SearchPlayer`}: A dict of clan members by tag.
        Pass in an attribute of :class:`SearchPlayer` to get that attribute as the key
        """
        return {getattr(m, attr): m for m in self._members}

    def get_member(self, **attrs):
        """Returns the first :class:`SearchPlayer` that meets the attributes passed
        This will return the first member matching the attributes passed.
        An example of this looks like:
        .. code-block:: python3
            member = SearchClan.get_member(tag='tag')
        This search implements the :func:`coc.utils.get` function
        """
        return get(self._members, **attrs)


class LeagueClan(BasicClan):
    """Represents a Clash of Clans League Clan
    This class inherits both :class:`Clan` and :class:`BasicClan`,
    and thus all attributes of these classes can be expected to be present.
    """
    def __init__(self, data):
        super().__init__(data=data)

    @property
    def _members(self):
        """|iter|
        Returns an iterable of :class:`LeaguePlayer`: all players participating in this league season"""
        from .player import Player  # hack because circular imports
        return iter(Player(data=mdata) for mdata in self._data.get('members', []))

    @property
    def members(self):
        """List[:class:`LeaguePlayer`} A list of players participating in this league season"""
        return list(self._members)