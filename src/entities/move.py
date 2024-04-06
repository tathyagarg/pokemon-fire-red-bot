from .abstracts import Type, MoveCategory

MC = MoveCategory

class Move:
    def __init__(
            self,
            typing: Type,
            category: MC,
            PP: int,
            power: int,
            accuracy: int | float,
            contact: bool,
            protect: bool,
            mirror_move: bool,
            kings_rock: bool
    ) -> None:
        self.typing: Type = typing
        self.category: MC = category

        self.PP: int = PP
        self.power: int = power
        self.accuracy: int | float = accuracy

        self.contact: bool = contact
        self.protect: bool = protect
        self.mirror_move: bool = mirror_move
        self.kings_rock: bool = kings_rock
