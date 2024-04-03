class Item:
    items = []
    def __init__(self, name, emoji, effect) -> None:
        self.name = name
        self.emoji = emoji
        self.effect = effect

        self.index = len(Item.items)
        Item.items.append(self)

    def __str__(self) -> str:
        return self.name

