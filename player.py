class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck, num_cards=1):
        for _ in range(num_cards):
            card = deck.draw_card()
            self.hand.append(card)

    def play_card(self, card):
        self.hand.remove(card)
        return card

    def has_won(self):
        return len(self.hand) == 0

    def __repr__(self):
        return f"{self.name} has {len(self.hand)} cards"