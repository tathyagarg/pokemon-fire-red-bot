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
        (0, 2, Direction.UP),
        (1, 2, Direction.UP),
        (2, 2, Direction.UP),
        (3, 2, Direction.UP),
        (4, 2, Direction.UP),
        (5, 2, Direction.UP),
        (6, 2, Direction.UP_RIGHT),
        (6, 3, Direction.RIGHT),
        (7, 4, Direction.UP),
        (8, 4, Direction.UP),
        (9, 2, Direction.UP),
        (10, 2, Direction.UP),
        (5, 3, Direction.DOWN),
        (4, 4, Direction.RIGHT),
        (4, 5, Direction.RIGHT),
        (6, 4, Direction.LEFT),
        (6, 5, Direction.LEFT),
        (0, 5, Direction.RIGHT),
        (0, 6, Direction.RIGHT),
        (2, 5, Direction.LEFT),
        (2, 6, Direction.LEFT),
        (1, 4, Direction.DOWN),
        (1, 7, Direction.UP),
    ],
    interactions={}
)

SCENES = [
    starting_room
]
