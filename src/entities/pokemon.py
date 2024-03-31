import move
import abstracts
import data
import random
import item
import math

class Pokemon:  # Parent
    def __init__(
            self,
            name: str,
            pokedex_number: int,
            typing: tuple[abstracts.Type, abstracts.Type],
            abilities: list[abstracts.Ability],
            gender_ratio: float,
            catch_rate: int,
            exp_yield: int,
            leveling_rate: abstracts.LevelingRate,
            ev_yield: abstracts.StatsList,
            base_stats: abstracts.StatsList,
            learnset: list[move.Move],
            evolution,
            evolution_condition  # Callable
    ) -> None:
        self.name = name
        self.pokedex_number = pokedex_number

        self.typing = self.primary_type, self.secondary_type = typing
        self.matchup = data.COMBOS[
            str(self.primary_type), str(self.secondary_type)
        ]

        self.abilities = abilities
        self.gender_ratio = gender_ratio
        self.catch_rate = catch_rate

        self.base_exp_yield = exp_yield
        self.leveling_rate = leveling_rate
        self.ev_yield = ev_yield

        self.base_stats = base_stats
        self.learnset = learnset

        self.evolution: Pokemon = evolution
        self.evolution_condition = evolution_condition

class PokemonInstance:
    def __init__(
            self,
            parent: Pokemon,
            nick: str = None,
            level: int = None,
            nature: abstracts.Nature = None,
            ivs: abstracts.StatsList = None,
            evs: abstracts.StatsList = None,
            held_item: item.Item = None
    ) -> None:
        self.instance_of = parent
        self.nick = nick or parent.name
        self.level = level or random.randint(1, 100)
        self.nature = nature or random.choices(data.NATURES)
        self.ivs = ivs or abstracts.StatsList(*random.choices(range(1, 32), k=6))
        self.evs = evs or abstracts.StatsList(*[0 for _ in range(6)])
        self.held_item = held_item

    @property
    def max_hp(self):
        a = math.floor(self.evs.hp / 4)
        b = 2 * self.instance_of.base_stats.hp + self.ivs.hp + math.floor(a)
        c = b * self.level / 100
        d = math.floor(c) + self.level + 10
        return d
    
    def calculate_stat(self, nature, ev, iv, bs):
        a = math.floor(ev / 4)
        b = 2 * bs + iv + a
        c = math.floor(b * self.level / 100) + 5
        d = math.floor(c * nature)
        return d
    
    @property
    def attack(self):
        return self.calculate_stat(
            self.nature.multiplier_on(abstracts.Stat.ATTACK),
            self.evs.attack,
            self.ivs.attack,
            self.instance_of.base_stats.attack
        )
    
    @property
    def defense(self):
        return self.calculate_stat(
            self.nature.multiplier_on(abstracts.Stat.DEFENSE),
            self.evs.defense,
            self.ivs.defense,
            self.instance_of.base_stats.defense
        )

    @property
    def special_attack(self):
        return self.calculate_stat(
            self.nature.multiplier_on(abstracts.Stat.SPECIAL_ATTACK),
            self.evs.special_attack,
            self.ivs.special_attack,
            self.instance_of.base_stats.special_attack
        )

    @property
    def special_defense(self):
        return self.calculate_stat(
            self.nature.multiplier_on(abstracts.Stat.SPECIAL_DEFENSE),
            self.evs.special_defense,
            self.ivs.special_defense,
            self.instance_of.base_stats.special_defense
        )
    
    @property
    def speed(self):
        return self.calculate_stat(
            self.nature.multiplier_on(abstracts.Stat.SPEED),
            self.evs.speed,
            self.ivs.speed,
            self.instance_of.base_stats.speed
        )

BULBASAUR = Pokemon(
    name='Bulbasaur', pokedex_number=1, typing=(abstracts.Type.GRASS, abstracts.Type.POISON),
    abilities=[]
)
