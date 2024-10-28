import random

def build_deck():
    # creates the original standard uno deck
    deck = []
    colors = ["R", "Y", "G", "B"]
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "+2", "skip", "reverse"]
    wilds = ["W", "W +4"]

    for color in colors: 
        for value in values:
            card = f"{color} {value}"
            deck.append(card)
            if value != 0: 
                deck.append(card)
    deck.extend(wilds * 4)
    random.shuffle(deck)
    return deck