def find(predicate, seq):
    for element in seq:
        if predicate(element):
            return element
    return None

def get(iterable, **attrs):
    def predicate(elem):
        for attr, val in attrs.items():
            nested = attr.split('__')
            obj = elem
            for attribute in nested:
                obj = getattr(obj, attribute)

            if obj != val:
                return False
        return True

    return find(predicate, iterable)


def try_enum(_class, data, **kwargs):
    if data is None:
        return None
    return _class(data=data, **kwargs)




HOME_TROOP_ORDER = [
    'Barbarian',
    'Archer',
    'Giant',
    'Goblin',
    'Wall Breaker',
    'Balloon',
    'Wizard',
    'Healer',
    'Dragon',
    'P.E.K.K.A',
    'Baby Dragon',
    'Miner',
    'Electro Dragon',
    'Minion',
    'Hog Rider',
    'Valkyrie',
    'Golem',
    'Witch',
    'Lava Hound',
    'Bowler',
    'Ice Golem',
    'Wall Wrecker',
    'Battle Blimp',
    'Stone Slammer'
]

BUILDER_TROOPS_ORDER = [
    'Raged Barbarian',
    'Sneaky Archer',
    'Boxer Giant',
    'Beta Minion',
    'Bomber',
    'Baby Dragon',
    'Cannon Cart',
    'Night Witch',
    'Drop Ship',
    'Super P.E.K.K.A'
]

SPELL_ORDER = [
    'Lightning Spell',
    'Healing Spell',
    'Rage Spell',
    'Jump Spell',
    'Freeze Spell',
    'Clone Spell',
    'Poison Spell',
    'Earthquake Spell',
    'Haste Spell',
    'Skeleton Spell',
    'Bat Spell'
]

HERO_ORDER = [
    'Barbarian King',
    'Archer Queen',
    'Grand Warden',
    'Battle Machine'
]

SIEGE_MACHINE_ORDER = [
    'Wall Wrecker',
    'Battle Blimp',
    'Stone Slammer'
]

ACHIEVEMENT_ORDER = [
    'Bigger Coffers',
    'Get those Goblins!',
    'Bigger & Better',
    'Nice and Tidy',
    'Release the Beasts',
    'Gold Grab',
    'Elixir Escapade',
    'Sweet Victory!',
    'Empire Builder',
    'Wall Buster',
    'Humiliator',
    'Union Buster',
    'Conqueror',
    'Unbreakable',
    'Friend in Need',
    'Mortar Mauler',
    'Heroic Heist',
    'League All-Star',
    'X-Bow Exterminator',
    'Firefighter',
    'War Hero',
    'Treasurer',
    'Anti-Artillery',
    'Sharing is caring',
    'Keep your village safe',
    'Master Engineering',
    'Next Generation Model',
    'Un-Build It',
    'Champion Builder',
    'High Gear',
    'Hidden Treasures',
    'Games Champion',
    'Dragon Slayer',
    'War League Legend',
    'Keep your village safe'
]