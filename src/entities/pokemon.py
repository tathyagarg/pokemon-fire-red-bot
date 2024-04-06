import re
import math
import random
import typing
from entities import item, move, abstracts, data

def level_reach(level: int) -> typing.Callable[["PokemonInstance"], bool]:
    def check(pokemon: PokemonInstance) -> bool:
        return pokemon.level >= level
    return check

def level_reach_and_holding(level: int, held_item: item.Item) -> typing.Callable[["PokemonInstance"], bool]:
    def check(pokemon: PokemonInstance) -> bool:
        return pokemon.level >= level and pokemon.held_item == held_item
    return check

class PokemonDiscordData:
    def __init__(self, emoji: str) -> None:
        self.emoji: str = emoji

class Pokemon:
    all_pokemon: list = []  # list[Pokemon]
    def __init__(
            self,
            name: str,
            discord_data: PokemonDiscordData,
            pokedex_number: int,
            _typing: tuple[abstracts.Type, abstracts.Type],
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
        self.name: str = name
        self.discord_data: PokemonDiscordData = discord_data
        self.pokedex_number: int = pokedex_number

        self.typing = self.primary_type, self.secondary_type = _typing
        self.matchup: dict[abstracts.Type, int | float] = data.COMBOS[self.primary_type, self.secondary_type]

        self.abilities: list[abstracts.Ability] = abilities
        self.gender_ratio: float = gender_ratio
        self.catch_rate: int = catch_rate

        self.base_exp_yield: int = exp_yield
        self.leveling_rate: abstracts.LevelingRate = leveling_rate
        self.ev_yield: abstracts.StatsList = ev_yield

        self.base_stats: abstracts.StatsList = base_stats
        self.learnset: dict[int, move.Move | tuple[move.Move, ...]] = learnset

        self.evolution: int | tuple[int, ...] = evolution_pokedex_number  # becomes Pokemon type
        self.evolution_condition: typing.Callable | tuple[typing.Callable] = evolution_condition

        Pokemon.all_pokemon.append(self)

    @classmethod
    def connect_evolutions(cls) -> None:
        for pokemon in cls.all_pokemon:
            if isinstance(pokemon.evolution, tuple):
                result: list[Pokemon] = []
                for idx in pokemon.evolution:
                    result.append(cls.all_pokemon[idx-1])
                
                pokemon.evolution = tuple(result)
            elif pokemon.evolution:
                pokemon.evolution = cls.all_pokemon[pokemon.evolution-1]

class PokemonInstance:
    def __init__(
            self,
            parent: Pokemon,
            nick: str = None,
            level: int = None,
            nature: abstracts.Nature = None,
            ivs: abstracts.StatsList = None,
            evs: abstracts.StatsList = None,
            held_item: item.Item = None,
            hp: int = None
    ) -> None:
        self.instance_of: Pokemon = parent
        self.nick: str = nick or parent.name
        self.level: int = level or random.randint(1, 100)
        self.nature: abstracts.Nature = nature or random.choices(abstracts.Nature.natures)[0]
        self.ivs: abstracts.StatsList = ivs or abstracts.StatsList(*random.choices(range(1, 32), k=6))
        self.evs: abstracts.StatsList = evs or abstracts.StatsList(*[0 for _ in range(6)])
        self.held_item: item.Item = held_item

        self.hp: int = hp or -1

    def encode(self) -> str:
        ivs: list[str] = list(map(str, self.ivs))
        evs: list[str] = list(map(str, self.evs))
        hp: int = self.hp if self.hp != -1 else self.max_hp
        held_item: int = self.held_item.index if isinstance(self.held_item, item.Item) else -1
        return f'{self.instance_of.pokedex_number}~{self.nick!r}~{self.level}~{self.nature.index}~{".".join(ivs)}~{".".join(evs)}~{held_item}~{hp}'
    
    @classmethod
    def decode(self, encoded_string: str):
        """
        :return: PokemonInstance from the encoded string
        """
        regex: str = r"~(?=(?:[^']*'[^']*')*[^']*$)"
        split: list[str] = re.split(regex, encoded_string)
        parent_id, nick, level, nature_id, ivs, evs, held_item_id, hp = split

        parent_id, level, nature_id = list(map(int, [parent_id, level, nature_id]))
        nick: str = nick[1:-1]
        ivs: abstracts.StatsList = abstracts.StatsList(*list(map(int, ivs.split('.'))))
        evs: abstracts.StatsList = abstracts.StatsList(*list(map(int, evs.split('.'))))

        held_item: item.Item | None = item.Item.items[int(held_item_id)-1] if held_item_id != '-1' else None

        parent: Pokemon = Pokemon.all_pokemon[parent_id-1]
        nature: abstracts.Nature = abstracts.Nature.natures[nature_id-1]

        return PokemonInstance(parent=parent, nick=nick, level=level, nature=nature, ivs=ivs, evs=evs, held_item=held_item, hp=hp)

    @property
    def max_hp(self) -> int:
        a: int = math.floor(self.evs.hp / 4)
        b: int = 2 * self.instance_of.base_stats.hp + self.ivs.hp + math.floor(a)
        c: float = b * self.level / 100
        d: int = math.floor(c) + self.level + 10
        return d
    
    def calculate_stat(self, nature: float, ev: int, iv: int, bs: int) -> int:
        a: int = math.floor(ev / 4)
        b: int = 2 * bs + iv + a
        c: int = math.floor(b * self.level / 100) + 5
        d: int = math.floor(c * nature)
        return d
    
    @property
    def attack(self) -> int:
        return self.calculate_stat(
            nature=self.nature.multiplier_on(stat=abstracts.Stat.ATTACK),
            ev=self.evs.attack,
            iv=self.ivs.attack,
            bs=self.instance_of.base_stats.attack
        )
    
    @property
    def defense(self) -> int:
        return self.calculate_stat(
            nature=self.nature.multiplier_on(stat=abstracts.Stat.DEFENSE),
            ev=self.evs.defense,
            iv=self.ivs.defense,
            bs=self.instance_of.base_stats.defense
        )

    @property
    def special_attack(self) -> int:
        return self.calculate_stat(
            nature=self.nature.multiplier_on(stat=abstracts.Stat.SPECIAL_ATTACK),
            ev=self.evs.special_attack,
            iv=self.ivs.special_attack,
            bs=self.instance_of.base_stats.special_attack
        )

    @property
    def special_defense(self) -> int:
        return self.calculate_stat(
            nature=self.nature.multiplier_on(stat=abstracts.Stat.SPECIAL_DEFENSE),
            ev=self.evs.special_defense,
            iv=self.ivs.special_defense,
            bs=self.instance_of.base_stats.special_defense
        )
    
    @property
    def speed(self) -> int:
        return self.calculate_stat(
            nature=self.nature.multiplier_on(stat=abstracts.Stat.SPEED),
            ev=self.evs.speed,
            iv=self.ivs.speed,
            bs=self.instance_of.base_stats.speed
        )

BULBASAUR: Pokemon = Pokemon(
    name='Bulbasaur',
    discord_data=PokemonDiscordData(emoji='<:001_bulbasaur:1224869651323027466>'),
    pokedex_number=1,
    _typing=(abstracts.Type.GRASS, abstracts.Type.POISON),
    abilities=[data.OVERGROW],
    gender_ratio=87.5,
    catch_rate=45,
    exp_yield=64,
    leveling_rate=abstracts.LevelingRate.MEDIUM_SLOW,
    ev_yield=abstracts.StatsList(hp=0, attack=0, defense=0, special_attack=1, special_defense=0, speed=0),
    base_stats=abstracts.StatsList(hp=45, attack=49, defense=49, special_attack=65, special_defense=65, speed=45),
    learnset={
        1: (data.TACKLE, data.GROWL),
        3: data.VINE_WHIP
    },
    evolution_pokedex_number=2,
    evolution_condition=level_reach(16)
)

IVYSAUR: Pokemon = Pokemon(
    name='Ivysaur',
    discord_data=PokemonDiscordData(emoji='<:002_ivysaur:1224869926297272491>'),
    pokedex_number=2,
    _typing=(abstracts.Type.GRASS, abstracts.Type.POISON),
    abilities=[data.OVERGROW],
    gender_ratio=87.5,
    catch_rate=45,
    exp_yield=141,
    leveling_rate=abstracts.LevelingRate.MEDIUM_SLOW,
    ev_yield=abstracts.StatsList(hp=0, attack=0, defense=0, special_attack=1, special_defense=1, speed=0),
    base_stats=abstracts.StatsList(hp=60, attack=62, defense=63, special_attack=80, special_defense=80, speed=60),
    learnset={
        1: (data.TACKLE, data.GROWL, data.LEECH_SEED),
        4: data.GROWL,
        7: data.LEECH_SEED,
        10: data.VINE_WHIP
    },
    evolution_pokedex_number=3,
    evolution_condition=level_reach(32)
)

VENASAUR: Pokemon = Pokemon(
    name='Venasaur',
    discord_data=PokemonDiscordData(emoji="<:003_venasaur:1225147158127186022>"),
    pokedex_number=3,
    _typing=(abstracts.Type.GRASS, abstracts.Type.POISON),
    abilities=[data.OVERGROW],
    gender_ratio=87.5,
    catch_rate=45,
    exp_yield=208,
    leveling_rate=abstracts.LevelingRate.MEDIUM_SLOW,
    ev_yield=abstracts.StatsList(hp=0, attack=0, defense=0, special_attack=2, special_defense=1, speed=0),
    base_stats=abstracts.StatsList(hp=80, attack=82, defense=83, special_attack=100, special_defense=100, speed=80),
    learnset={
        1: (data.TACKLE, data.GROWL, data.LEECH_SEED, data.VINE_WHIP),
        4: data.GROWL,
        7: data.LEECH_SEED,
        10: data.VINE_WHIP
    },
    evolution_pokedex_number=None,
    evolution_condition=None
)

Pokemon.connect_evolutions()
