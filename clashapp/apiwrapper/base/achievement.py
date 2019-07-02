
class Achievement:
    """Represents a Clash of Clans Achievement.
    Attributes
    -----------
    player:
        :class:`SearchPlayer` - The player this achievement is assosiated with
    name:
        :class:`str` - The name of the achievement
    stars:
        :class:`int` - The current stars achieved for the achievement
    value:
        :class:`int` - The number of X things attained for this achievement
    target:
        :class:`int` - The number of X things required to complete this achievement
    info:
        :class:`str` - Information regarding the achievement
    completion_info:
        :class:`str` - Information regarding completion of the achievement
    village:
        :class:`str` - Either `home` or `builderBase`
    """

    __slots__ = ('player', 'name', 'stars', 'value', 'target',
                 'info', 'completion_info', 'village', '_data')

    def __str__(self):
        return self.name

    def __init__(self, *, data, player):
        self._data = data

        self.player = player
        self.name = data['name']
        self.stars = data.get('stars')
        self.value = data['value']
        self.target = data['target']
        self.info = data['info']
        self.completion_info = data.get('completionInfo')
        self.village = data['village']

    @property
    def is_builder_base(self):
        """:class:`bool`: Helper property to tell you if the achievement belongs to the builder base"""
        return self.village == 'builderBase'

    @property
    def is_home_base(self):
        """:class:`bool`: Helper property to tell you if the achievement belongs to the home base"""
        return self.village == 'home'

    @property
    def is_completed(self):
        """:class:`bool`: Indicates whether the achievement is completed (3 stars achieved)"""
        return self.stars == 3