import enum

class Stat(enum.Enum):
    HP = 0
    ATTACK = 1
    DEFENSE = 2
    SPECIAL_ATTACK = 3
    SPECIAL_DEFENSE = 4
    SPEED = 5

class StatsList:
    def __init__(self, hp, attack, defense, special_attack, special_defense, speed) -> None:
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed

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
    def __init__(self, up_stat: Stat, down_stat: Stat) -> None:
        self.up_stat = up_stat
        self.down_stat = down_stat

class Ability:
    def __init__(self) -> None:
        ...

class LevelingRate:
    def __init__(self) -> None:
        pass
    