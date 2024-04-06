import enum

class Stat(enum.Enum):
    HP = 0
    ATTACK = 1
    DEFENSE = 2
    SPECIAL_ATTACK = 3
    SPECIAL_DEFENSE = 4
    SPEED = 5

class StatsList:
    def __init__(self, hp: int, attack: int, defense: int, special_attack: int, special_defense: int, speed: int) -> None:
        self.hp: int = hp
        self.attack: int = attack
        self.defense: int = defense
        self.special_attack: int = special_attack
        self.special_defense: int = special_defense
        self.speed: int = speed

    def __iter__(self) -> iter:
        return iter([self.hp, self.attack, self.defense, self.special_attack, self.special_defense, self.speed])


class Type(enum.Enum):
    NORMAL = 0
    FIRE = 1
    WATER = 2
    ELECTRIC = 3
    GRASS = 4
    ICE = 5
    FIGHTING = 6
    POISON = 7
    GROUND = 8
    FLYING = 9
    PSYCHIC = 10
    BUG = 11
    ROCK = 12
    GHOST = 13
    DRAGON = 14
    DARK = 15
    STEEL = 16

    def __str__(self) -> str:
        return self.name

class MoveCategory(enum.Enum):
    PHYSICAL = 0
    SPECIAL = 1
    STATUS = 2

class Nature:
    natures: list = []  # list[Nature]
    def __init__(self, name: str, up_stat: Stat, down_stat: Stat) -> None:
        self.name: str = name
        self.up_stat: Stat = up_stat
        self.down_stat: Stat = down_stat

        self.index: int = len(Nature.natures)
        Nature.natures.append(self)

    def multiplier_on(self, stat: Stat) -> float:
        if self.up_stat == self.down_stat:
            return 1.
        elif stat == self.up_stat:
            return 1.1
        elif stat == self.down_stat:
            return 0.9
        else:
            return 1.

    def __str__(self) -> str:
        return self.name

class Ability:
    def __init__(self, name: str, effect) -> None:
        self.name: str = name
        self.effect = effect

class LevelingRate(enum.Enum):
    MEDIUM_FAST = 0
    MEDIUM_SLOW = 1
    FAST = 2
    SLOW = 3
    