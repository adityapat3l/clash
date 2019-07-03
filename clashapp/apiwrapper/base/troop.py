# Taken from https://github.com/mathsman5133/coc.py/blob/master/coc/miscmodels.py


class Troop:


    """Represents a Clash of Clans troop.
    Attributes
    -----------
    player:
        :class:`SearchPlayer` - The player this troop is assosiated with
    name:
        :class:`str` - The name of the troop
    level:
        :class:`int` - The level of the troop
    max_level:
        :class:`int` - The overall max level of the troop, excluding townhall limitations
    village:
        :class:`str` - Either `home` or `builderBase`
    """

    __slots__ = ('player', 'name', 'level',
                 'max_level', 'village')

    def __str__(self):
        return self.name

    def __init__(self, player, data):
        self.player = player
        self.name = data.get('name')
        self.level = data.get('level')
        self.max_level = data.get('maxLevel')
        self.village = data.get('village')

    @property
    def is_max(self):
        """:class:`bool`: Helper property to tell you if the troop is the max level"""
        return self.level == self.max_level

    @property
    def is_builder_base(self):
        """:class:`bool`: Helper property to tell you if the troop belongs to the builder base"""
        return self.village == 'builderBase'

    @property
    def is_home_base(self):
        """:class:`bool`: Helper property to tell you if the troop belongs to the home base"""
        return self.village == 'home'