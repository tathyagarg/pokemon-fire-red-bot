from commons import Direction

class Scene:
    def __init__(
        self, 
        image: str, 
        size: tuple[int, int], 
        starting_position: tuple[int, int],
        walls: list[tuple[int, int, Direction]],
        interactions: dict[tuple[int, int, Direction], str]
    ) -> None:
        self.image = image
        self.size = size
        self.starting_position = starting_position
        self.walls = walls
        self.interactions = interactions

starting_room = Scene(
    image='assets/scenes/scene1.png',
    size=(11, 9),
    starting_position=(5, 6),
    walls=[
        (0, 2, Direction.BACK),
        (1, 2, Direction.BACK),
        (2, 2, Direction.BACK),
        (3, 2, Direction.BACK),
        (4, 2, Direction.BACK),
        (5, 2, Direction.BACK),
        (6, 2, Direction.BACK_RIGHT),
        (6, 3, Direction.RIGHT),
        (7, 4, Direction.BACK),
        (8, 4, Direction.BACK),
        (9, 2, Direction.BACK),
        (10, 2, Direction.BACK),
        (5, 3, Direction.FRONT),
        (4, 4, Direction.RIGHT),
        (4, 5, Direction.RIGHT),
        (6, 4, Direction.LEFT),
        (6, 5, Direction.LEFT),
        (0, 5, Direction.RIGHT),
        (0, 6, Direction.RIGHT),
        (2, 5, Direction.LEFT),
        (2, 6, Direction.LEFT),
        (1, 4, Direction.FRONT),
        (1, 7, Direction.BACK),
    ],
    interactions={}
)

SCENES = [
    starting_room
]
