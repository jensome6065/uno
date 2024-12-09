import random

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"{self.color} {self.value}"

class Deck:
    def __init__(self):
        self.colors = ['Red', 'Yellow', 'Green', 'Blue']
        self.values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2']
        self.wild_cards = ['Wild Color', 'Wild +4', 'Wild Number', 'Wild Swap', 'Wild Trash'] 
        self.cards = []
        self.create_deck()
        self.shuffle()

    def create_deck(self):
        for color in self.colors:
            for value in self.values:
                if value != '0':
                    self.cards.append(Card(color, value))
                    self.cards.append(Card(color, value))
                else:
                    self.cards.append(Card(color, value))
        
        for _ in range(4):
            self.cards.append(Card('Wild', 'Color'))
            self.cards.append(Card('Wild', '+4'))
            self.cards.append(Card('Wild', 'Number'))
            self.cards.append(Card('Wild', 'Swap')) 
            self.cards.append(Card('Wild', 'Trash'))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()