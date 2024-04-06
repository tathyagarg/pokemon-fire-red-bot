class Item:
    items: list = []  # list[Item]
    def __init__(self, name: str, emoji: str, effect) -> None:
        self.name: str = name
        self.emoji: str = emoji
        self.effect = effect

        self.index: int = len(Item.items)
        Item.items.append(self)

    def __str__(self) -> str:
        return self.name

