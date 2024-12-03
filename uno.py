import random
import PySimpleGUI as sg
from player import Player
from cards import Deck, Card


# Function to map card color to display color
def map_color(color_name):
    color_map = {"Red": "#FF0000", "Yellow": "#FFFF00", "Green": "#00FF00", "Blue": "#0000FF", "Wild": "#000000"}
    return color_map.get(color_name, "#FFFFFF")


# Function to draw UNO card graphically (cards are now dictionaries)
def draw_uno_card(graph, card, pos):
    x, y = pos
    color = map_color(card["color"])
    value = card["value"]
    card_type = 'number' if value.isdigit() else 'special'
    
    # Draw the card rectangle
    graph.draw_rectangle((x, y), (x + 90, y + 135), line_color='black', fill_color=color)
    
    # Draw the card circle (for the value)
    graph.draw_circle((x + 45, y + 67), 35, fill_color='white', line_color='black', line_width=2)
    
    # Draw the value text based on the card type (normal or special)
    font_size = 30 if card_type == 'number' else 20
    graph.draw_text(value, (x + 45, y + 67), font=('Helvetica', font_size), color='black', text_location=sg.TEXT_LOCATION_CENTER)


# Display a player's hand graphically and make cards clickable
def display_hand(window, player, graph):
    graph.erase()  # Clear the graph before drawing
    card_positions = []
    x, y = 10, 300
    buttons = []

    # Create a column layout for the buttons
    button_column = []

    for idx, card in enumerate(player.hand):
        color = map_color(card["color"])
        card_type = 'number' if card["value"].isdigit() else 'special'
        draw_uno_card(graph, card, (x, y))
        card_positions.append((x, y, card, idx))  # Track the card position and its index
        
        # Create a button over the card (centered) with the same size as the card
        button = sg.Button(card["value"], key=f'card_{idx}', size=(9, 13), pad=(0, 0), font=('Helvetica', 10), 
                           button_color=('black', color), visible=True)
        button_column.append(button)
        
        x += 100  # Space cards horizontally
    
    # Add the button column layout to the window
    window.extend_layout(window['graph'], [[sg.Column([button_column], key="button_column")]])

    return card_positions


# Draw the top card on the deck (centered)
def draw_top_card(graph, card):
    """Draws the top card on the deck."""
    graph.erase()  # Clear any previous card
    color = map_color(card["color"])
    draw_uno_card(graph, card, (10, 10))


# Main game logic to play UNO
def play_uno():
    sg.theme("DarkBlue")
    num_players = int(sg.popup_get_text("Enter number of players (2-4):", title="UNO Game"))
    deck = Deck()

    # Initialize players
    players = [Player(f"Player {i+1}") for i in range(num_players)]
    for player in players:
        for _ in range(7):  # Deal 7 cards to each player
            player.draw_card(deck)
        player.sort_hand()

    discard_pile = [deck.draw()]

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
        player = players[turn]
        top_card = discard_pile[-1]

        sg.popup(f"{player.name}'s turn! Top card: {top_card['color']} {top_card['value']}", title="Turn Info")
        card_positions = display_hand(window, player, graph)  # Display the player's hand
        draw_top_card(deck_graph, top_card)  # Draw the top card on the deck

        turn_ended = False
        while not turn_ended:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                window.close()
                return

            if event == "Draw Card":
                drawn_card = player.draw_card(deck)
                sg.popup(f"You drew: {drawn_card['color']} {drawn_card['value']}", title="Card Drawn")
                continue

            if event == "End Turn":
                sg.popup(f"{player.name} ends their turn.", title="End Turn")
                turn_ended = True
                continue

            # Handle card button click
            if event.startswith('card_'):
                card_idx = int(event.split('_')[1])
                card = player.hand[card_idx]
                if card["color"] == "Wild" or top_card["color"] == "Wild" or card["color"] == top_card["color"] or card["value"] == top_card["value"]:
                    player.play_card(card)
                    discard_pile.append(card)
                    sg.popup(f"{player.name} played: {card['color']} {card['value']}")
                    turn_ended = True
                else:
                    sg.popup("Invalid move. Please choose a valid card.")
                    continue

        if not player.hand:
            sg.popup(f"{player.name} wins the game! 🎉", title="Game Over")
            break

        turn = (turn + direction) % len(players)

    window.close()


# Run the game
if __name__ == "__main__":
    play_uno()