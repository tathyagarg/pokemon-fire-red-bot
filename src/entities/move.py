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

TACKLE = Move(typing=TYPE.NORMAL, category=MC.PHYSICAL, PP=35,
              power=40, accuracy=100, contact=True, protect=True, mirror_move=True, kings_rock=True)

GROWL = Move(typing=TYPE.NORMAL, category=MC.STATUS, PP=40, power=0, accuracy=100, contact=False,
             protect=True, mirror_move=True, kings_rock=False)

VINE_WHIP = Move(typing=TYPE.GRASS, category=MC.PHYSICAL, PP=25, power=45, accuracy=100, contact=True,
                 protect=True, mirror_move=True, kings_rock=True)
