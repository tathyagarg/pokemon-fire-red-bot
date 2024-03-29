import move
import abstracts

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
            move_list: list[move.Move],
            evolution,
            evolution_condition  # Callable
    ) -> None:
        self.name = name
        self.pokedex_number = pokedex_number

        self.typing = self.primary_type, self.secondary_type = typing
        self.matchup = abstracts.COMBOS[
            str(self.primary_type), str(self.secondary_type)
        ]

        self.abilities = abilities
        self.gender_ratio = gender_ratio
        self.catch_rate = catch_rate

        self.base_exp_yield = exp_yield
        self.leveling_rate = leveling_rate
        self.ev_yield = ev_yield

        self.base_stats = base_stats
        self.move_list = move_list

        self.evolution: Pokemon = evolution
        self.evolution_condition = evolution_condition
