class Player:
    
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, deck):
        """Draw a card from the deck and add it to the player's hand."""
        card = deck.draw()  # Use the draw method from the Deck class
        if card:  # Check if the card exists before adding it
            self.hand.append(card)
        return card

    def play_card(self, card):
        """Play a card from the player's hand and remove it."""
        self.hand.remove(card)
        return card

    def sort_hand(self):
        """Sort the player's hand by color and then by value."""
        self.hand = sorted(self.hand, key=lambda card: (card["color"], card["value"]))