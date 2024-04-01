class Item:
    items = []
    def __init__(self, name, effect) -> None:
        self.name = name
        self.effect = effect

        self.index = len(Item.items)
        Item.items.append(self)

    def __str__(self) -> str:
        return str(self.index)

