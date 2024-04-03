from .abstracts import Type, MoveCategory

TYPE = Type
MC = MoveCategory

class Move:
    def __init__(
            self,
            typing: TYPE,
            category: MC,
            PP: int,
            power: int,
            accuracy: int | float,
            contact: bool,
            protect: bool,
            mirror_move: bool,
            kings_rock: bool
    ) -> None:
        self.typing = typing
        self.category = category

        self.PP = PP
        self.power = power
        self.accuracy = accuracy

        self.contact = contact
        self.protect = protect
        self.mirror_move = mirror_move
        self.kings_rock = kings_rock
