import random
import PySimpleGUI as sg
from player import Player
from cards import Deck, Card

# Function to map card color to display color
def map_color(color_name):
    color_map = {"Red": "#FF0000", "Yellow": "#FFFF00", "Green": "#00FF00", "Blue": "#0000FF", "Wild": "#000000"}
    return color_map.get(color_name, "#FFFFFF")


# Function to display a player's hand graphically as buttons
def display_hand(window, player, update_only=False):
    """Display the player's hand as buttons."""
    if not update_only:
        # Clear the hand area for a full redraw
        window["hand_area"].update([])

    # Dynamically create card buttons
    hand_layout = []
    for idx, card in enumerate(player.hand):
        button = sg.Button(
            f"{card.color}\n{card.value}",
            size=(10, 5),
            key=f"card_{idx}",
            button_color=('black', map_color(card.color)),
            pad=(5, 5),
            font=('Helvetica', 12)
        )
        hand_layout.append(button)

    # Add the hand buttons to the hand area
    window["hand_area"].update(hand_layout)


# Function to update the top card display
def update_top_card_display(window, top_card):
    """Update the top card display."""
    window["top_card"].update(f"{top_card.color}\n{top_card.value}")
    window["top_card"].update(button_color=('black', map_color(top_card.color)))


# Layout with enhancements (added fonts, spacing, and card area organization)
def create_layout():
    layout = [
        [sg.Text("UNO Game", font=("Helvetica", 20, "bold"), justification="center")],
        [sg.Text("Top Card:", font=("Helvetica", 14)), sg.Button("", size=(12, 6), key="top_card", disabled=True)],
        [sg.Text("Player's Turn: ", size=(12, 1), font=("Helvetica", 12), key="player_turn")],
        [
            sg.Button("<", size=(3, 2), key="scroll_left"),  # Scroll left button
            sg.Column([[]], size=(850, 150), key="hand_area", justification="center"),
            sg.Button(">", size=(3, 2), key="scroll_right")  # Scroll right button
        ],
        # Deck area display
        [sg.Text("Deck", font=("Helvetica", 14)), 
         sg.Button("Draw", size=(10, 2), key="draw_card", font=('Helvetica', 12), pad=(5, 5)),
         sg.Text("Deck Remaining Cards: ", font=("Helvetica", 12)), sg.Text("", key="deck_count", font=("Helvetica", 12))],
        [sg.Button("End Turn", size=(12, 2)), sg.Button("Exit", size=(12, 2))]
    ]
    return layout


# Get number of players function
def get_number_of_players():
    """Prompt user for number of players between 2 and 4."""
    layout = [
        [sg.Text("How many players? (2-4)", font=("Helvetica", 16))],
        [sg.InputText("", key="num_players", size=(5, 1), justification='center')],
        [sg.Button("OK", font=("Helvetica", 14))]
    ]

    window = sg.Window("UNO Game - Players", layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            window.close()
            return None

        if event == "OK":
            try:
                num_players = int(values["num_players"])
                if 2 <= num_players <= 4:
                    window.close()
                    return num_players
                else:
                    sg.popup_error("Please enter a number between 2 and 4.")
            except ValueError:
                sg.popup_error("Invalid input. Please enter a valid number.")


# Main function to run the game
def play_uno():
    sg.theme("DarkBlue")

    # Step 1: Ask for the number of players
    num_players = get_number_of_players()
    if num_players is None:
        return

    # Step 2: Initialize deck and players
    deck = Deck()

    # Initialize players
    players = [Player(f"Player {i + 1}") for i in range(num_players)]
    for player in players:
        for _ in range(7):
            player.draw_card(deck)

    discard_pile = [deck.draw()]  # Start with one card in the discard pile
    top_card = discard_pile[-1]

    # Create window layout
    window = sg.Window("UNO Game", create_layout(), finalize=True)

    # Initially display the player's hand and top card
    update_top_card_display(window, top_card)
    display_hand(window, players[0])

    turn = 0
    current_card_index = 0  # To manage the horizontal scrolling of hand
    while True:
        player = players[turn]
        top_card = discard_pile[-1]
        update_top_card_display(window, top_card)

        window["player_turn"].update(f"Player {turn + 1}'s Turn")
        window["deck_count"].update(f"Remaining Deck Cards: {len(deck.cards)}")  # Update deck count display

        turn_ended = False
        while not turn_ended:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                window.close()
                return

            # Scroll left button
            if event == "scroll_left" and current_card_index > 0:
                current_card_index -= 1
                display_hand(window, player, update_only=True)

            # Scroll right button
            elif event == "scroll_right" and current_card_index < len(player.hand) - 1:
                current_card_index += 1
                display_hand(window, player, update_only=True)

            # Card button click event
            elif event.startswith("card_"):
                card_idx = int(event.split("_")[1])
                selected_card = player.hand[card_idx]

                # Check if the card is playable
                if selected_card.is_playable_on(top_card):
                    # Remove card from player's hand and add it to the discard pile
                    played_card = player.play_card(selected_card)
                    discard_pile.append(played_card)
                    sg.popup(f"{player.name} played: {played_card.color} {played_card.value}")

                    # Update the top card and player's hand display
                    update_top_card_display(window, played_card)
                    display_hand(window, player)
                    window["deck_count"].update(f"Remaining Deck Cards: {len(deck.cards)}")

                    # Switch to the next player
                    turn = (turn + 1) % num_players
                    turn_ended = True

                else:
                    sg.popup("Card not playable! Choose a valid card or draw a new one.")

            # Draw Card button clicked
            elif event == "Draw":
                drawn_card = player.draw_card(deck)
                sg.popup(f"You drew: {drawn_card.color} {drawn_card.value}")

                # Add the new card to the display
                display_hand(window, player, update_only=True)
                window["deck_count"].update(f"Remaining Deck Cards: {len(deck.cards)}")

            # End Turn button clicked
            elif event == "End Turn":
                turn_ended = True

        if not player.hand:
            sg.popup(f"{player.name} wins the game! 🎉")
            break

    window.close()


# Run the game
if __name__ == "__main__":
    play_uno()