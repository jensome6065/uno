import PySimpleGUI as sg
import random

# Function to build the UNO deck
def build_deck():
    colors = ["Red", "Yellow", "Green", "Blue"]
    values = [str(i) for i in range(10)] + ["Skip", "Reverse", "+2"]
    deck = [f"{color} {value}" for color in colors for value in values]
    deck += deck  # Two of each non-zero card
    deck += ["Wild", "Wild +4"] * 4  # Wild cards
    random.shuffle(deck)
    return deck

# Initialize the game
def initialize_game(deck, num_players):
    hands = {f"Player {i+1}": [deck.pop() for _ in range(7)] for i in range(num_players)}
    discard_pile = [deck.pop()]
    return hands, discard_pile

# Function to draw a card graphically
def draw_uno_card(graph, card_type, text, color, pos):
    x, y = pos
    graph.draw_rectangle((x, y), (x + 90, y + 135), line_color='black', fill_color=color)
    graph.draw_circle((x + 45, y + 67), 35, fill_color='white', line_color='black', line_width=2)
    if card_type == 'number':
        graph.draw_text(text, (x + 45, y + 67), font=('Helvetica', 30), color='black', text_location=sg.TEXT_LOCATION_CENTER)
    else:
        graph.draw_text(text, (x + 45, y + 67), font=('Helvetica', 20), color='black', text_location=sg.TEXT_LOCATION_CENTER)
    graph.draw_text(text, (x + 10, y + 120), font=('Helvetica', 15), color='white', text_location=sg.TEXT_LOCATION_CENTER)
    graph.draw_text(text, (x + 80, y + 10), font=('Helvetica', 15), color='white', text_location=sg.TEXT_LOCATION_CENTER)

# Function to map card color to display color
def map_color(color_name):
    color_map = {"Red": "#FF0000", "Yellow": "#FFFF00", "Green": "#00FF00", "Blue": "#0000FF", "Wild": "#000000"}
    return color_map.get(color_name.split()[0], "#FFFFFF")

# Display a player's hand graphically and make cards selectable
def display_hand(graph, hand):
    graph.erase()  # Clear the graph before drawing
    card_positions = []
    x, y = 10, 300
    for idx, card in enumerate(hand):
        color = map_color(card)
        card_type = 'number' if card.split()[1].isdigit() else 'special'
        draw_uno_card(graph, card_type, card.split()[1], color, (x, y))
        card_positions.append((x, y, card, idx))  # Track the card position and its index
        x += 100  # Space cards horizontally
    return card_positions

# Draw the top card on the deck (centered)
def draw_top_card(graph, card):
    """Draws the top card on the deck."""
    graph.erase()  # Clear any previous card
    color = map_color(card)
    card_type = 'number' if card.split()[1].isdigit() else 'special'
    draw_uno_card(graph, card_type, card.split()[1], color, (10, 10))

# Check if a card is playable
def is_playable(card, top_card):
    if "Wild" in card:
        return True
    card_color, card_value = card.split(" ", 1)
    top_color, top_value = top_card.split(" ", 1)
    return card_color == top_color or card_value == top_value

# Main Game Loop
def play_uno():
    sg.theme("DarkBlue")
    num_players = int(sg.popup_get_text("Enter number of players (2-4):", title="UNO Game"))
    deck = build_deck()
    hands, discard_pile = initialize_game(deck, num_players)

    layout = [
        [sg.Text("UNO Game", font=("Helvetica", 20))],
        [sg.Graph((800, 450), (0, 0), (800, 450), background_color='white', key='graph')],
        [sg.Text("Top Card:", font=("Helvetica", 12)), 
         sg.Graph((100, 150), (0, 0), (100, 150), background_color='white', key='deck_graph')],
        [sg.Button("Draw Card"), sg.Button("End Turn"), sg.Button("Exit")]
    ]
    window = sg.Window("UNO Game", layout, finalize=True)
    graph = window['graph']
    deck_graph = window['deck_graph']

    turn = 0
    direction = 1
    while True:
        player = f"Player {turn + 1}"
        top_card = discard_pile[-1]
        hand = hands[player]

        # Display the player's hand
        sg.popup(f"{player}'s turn! Top card: {top_card}", title="Turn Info")
        card_positions = display_hand(graph, hand)
        draw_top_card(deck_graph, top_card)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                window.close()
                return

            # Check if a card was clicked
            if event == "Draw Card":
                drawn_card = deck.pop()
                sg.popup(f"You drew: {drawn_card}", title="Card Drawn")
                hand.append(drawn_card)
                card_positions = display_hand(graph, hand)
                draw_top_card(deck_graph, top_card)
                break

            if event == "End Turn":
                sg.popup(f"{player} ends their turn.", title="End Turn")
                break

            # Check for clicks on the cards in hand
            for pos in card_positions:
                x, y, card, card_idx = pos
                if x <= values['graph'][0] <= x + 90 and y <= values['graph'][1] <= y + 135:
                    # If the card was clicked, attempt to play it
                    if is_playable(card, top_card):
                        hand.remove(card)
                        discard_pile.append(card)
                        sg.popup(f"{player} played: {card}")
                        break
                    else:
                        sg.popup("Invalid move. Please choose a valid card.")
        
        # Check for win condition
        if not hand:
            sg.popup(f"{player} wins the game! 🎉", title="Game Over")
            break

        # Move to the next player
        turn = (turn + direction) % num_players

    window.close()

# Run the game
if __name__ == "__main__":
    play_uno()