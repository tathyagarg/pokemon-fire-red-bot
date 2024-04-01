import move
import abstracts
import data
import random
import item
import math
import typing

def level_reach(level: int):
    def check(pokemon: PokemonInstance):
        return pokemon.level >= level
    return check

def level_reach_and_holding(level: int, held_item: item.Item):
    def check(pokemon: PokemonInstance):
        return pokemon.level >= level and pokemon.held_item == held_item
    return check

class Pokemon:
    all_pokemon = []
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
            learnset: dict[int, move.Move | tuple[move.Move, ...]],
            evolution_pokedex_number: int | tuple[int, ...],
            evolution_condition: typing.Callable | tuple[typing.Callable, ...]  # Callable
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

        self.evolution_pokedex = evolution_pokedex_number
        self.evolution_condition = evolution_condition

        Pokemon.all_pokemon.append(self)

    @classmethod
    def connect_evolutions(cls):
        for pokemon in cls.all_pokemon:
            if isinstance(pokemon.evolution_pokedex, tuple):
                result = []
                for idx in pokemon.evolution_pokedex:
                    result.append(cls.all_pokemon[idx-1])
                
                pokemon.evolution_pokedex = tuple(result)
            elif pokemon.evolution_pokedex:
                pokemon.evolution_pokedex = cls.all_pokemon[pokemon.evolution_pokedex-1]

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
        self.nature = nature or random.choices(abstracts.Nature.natures)
        self.ivs = ivs or abstracts.StatsList(*random.choices(range(1, 32), k=6))
        self.evs = evs or abstracts.StatsList(*[0 for _ in range(6)])
        self.held_item = held_item

    def encode(self) -> str:
        return f'{self.instance_of.pokedex_number}~{self.nick!r}~{self.level}~{self.nature}~{".".join(self.ivs)}~{".".join(self.evs)}~{self.held_item}'

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
    name='Bulbasaur',
    pokedex_number=1,
    typing=(abstracts.Type.GRASS, abstracts.Type.POISON),
    abilities=[data.OVERGROW],
    gender_ratio=87.5,
    catch_rate=45,
    exp_yield=64,
    leveling_rate=abstracts.LevelingRate.MEDIUM_SLOW,
    ev_yield=abstracts.StatsList(hp=0, attack=0, defense=0, special_attack=1, special_defense=0, speed=0),
    base_stats=abstracts.StatsList(hp=45, attack=49, defense=49, special_attack=65, special_defense=65, speed=45),
    learnset={
        1: (move.TACKLE, move.GROWL),
        3: (move.VINE_WHIP)
    },
    evolution="Ivysaur",
    evolution_condition=level_reach(16)
)
