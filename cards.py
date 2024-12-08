import random

class Deck:
    def __init__(self):
        self.cards = self.build_deck()
        random.shuffle(self.cards)

    def build_deck(self):
        colors = ["Red", "Yellow", "Green", "Blue"]
        values = [str(i) for i in range(10)] + ["Skip", "Reverse", "+2"]
        deck = [Card(color, value) for color in colors for value in values]
        deck += deck  # Two of each non-zero card
        deck += [Card("Wild", "Wild"), Card("Wild", "Wild +4")] * 4  # Wild cards
        return deck

    def draw(self):
        return self.cards.pop() if self.cards else None


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"{self.color} {self.value}"

    def is_playable_on(self, top_card):
        return (
            self.color == "Wild" or
            top_card.color == "Wild" or
            self.color == top_card.color or
            self.value == top_card.value
        )