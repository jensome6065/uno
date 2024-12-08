import tkinter as tk
from tkinter import messagebox
import random

# Define Card and Deck classes (same as before)
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"{self.color} {self.value}"

class Deck:
    def __init__(self):
        self.colors = ['Red', 'Yellow', 'Green', 'Blue']
        self.values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw Two']
        self.wild_cards = ['Wild', 'Wild Draw Four']
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
            self.cards.append(Card('Wild', 'Wild'))
            self.cards.append(Card('Wild', 'Wild Draw Four'))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

# Player Class
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

# UNO Game Class
class UNOGame:
    def __init__(self, players, root):
        self.deck = Deck()
        self.players = [Player(name) for name in players]
        self.current_player = 0
        self.direction = 1
        self.playing_stack = [self.deck.draw_card()]
        self.root = root
        self.update_game_display()

    def update_game_display(self):
        """Update the game state on the GUI."""
        self.clear_widgets()

        # Show the top card
        top_card = self.playing_stack[-1]
        top_card_text = f"Top card: {top_card.color} {top_card.value}"
        self.top_card_label = tk.Label(self.root, text=top_card_text, font=('Arial', 18), bg='lightblue', padx=10, pady=10)
        self.top_card_label.grid(row=0, column=0, columnspan=5)

        # Display player's hand as drawn cards
        player = self.players[self.current_player]
        self.hand_buttons = []
        self.hand_canvases = []
        for idx, card in enumerate(player.hand):
            # Create canvas to draw the card
            card_canvas = self.create_card_canvas(self.root, card, idx)
            self.hand_canvases.append(card_canvas)

            # Create invisible button over the card for interaction with text indicating the card
            card_button = tk.Button(self.root, width=10, height=5, relief="flat", text=f"{card.color}\n{card.value}", 
                                    command=lambda idx=idx: self.on_card_play(idx), font=('Arial', 10), bg='lightgrey', bd=0)
            card_button.grid(row=2, column=idx, padx=5, pady=5)
            card_button.config(state="normal")  # Make button interactable

            # Position button just below the card canvas
            self.hand_buttons.append(card_button)

        # Show whose turn it is
        self.turn_label = tk.Label(self.root, text=f"{player.name}'s turn", font=('Arial', 16), bg='lightblue', pady=10)
        self.turn_label.grid(row=3, column=0, columnspan=5)

        # Draw Card Button
        self.draw_button = tk.Button(self.root, text="Draw Card", width=20, height=2,
                                     command=self.on_draw_card, bg="lightgreen", relief="raised")
        self.draw_button.grid(row=4, column=0, columnspan=5)

    def clear_widgets(self):
        """Clear all existing widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_card_canvas(self, root, card, idx):
        """Draw the card with color, value and circles on a canvas."""
        card_canvas = tk.Canvas(root, width=100, height=150, bg='white', bd=0, relief="flat")
        card_canvas.grid(row=1, column=idx, padx=5, pady=5)

        # Draw the background color based on the card's color
        if card.color != 'Wild':
            card_canvas.create_rectangle(5, 5, 95, 145, fill=card.color.lower(), outline='black', width=2)

        # Draw circles in the center for card values
        card_canvas.create_oval(25, 40, 75, 100, fill='white', outline='black', width=2)  # Draw circle
        card_canvas.create_text(50, 70, text=card.value, font=('Arial', 16, 'bold'), fill='black')  # Add card value

        return card_canvas

    def on_card_play(self, card_index):
        """Handle the event when a card is played."""
        player = self.players[self.current_player]
        card = player.hand[card_index]

        if card.color == 'Wild':  # If it's a Wild card, ask for a new color
            self.ask_for_wild_color(card)
        elif self.is_valid_play(card):
            player.play_card(card)
            self.playing_stack.append(card)

            # Handle Draw 2 or Draw 4 cards
            if card.value == 'Draw Two':
                self.next_player_draw(2)
            elif card.value == 'Wild Draw Four':
                self.next_player_draw(4)

            self.update_game_display()

            if player.has_won():
                messagebox.showinfo("UNO", f"{player.name} has won the game!")
                self.root.quit()
                return

            self.current_player = (self.current_player + self.direction) % len(self.players)
            self.update_game_display()
        else:
            messagebox.showwarning("Invalid Play", "That card is not valid!")

    def is_valid_play(self, player_card):
        """Check if the card played is valid based on the top card."""
        top_card = self.playing_stack[-1]
        return (player_card.color == top_card.color or 
                player_card.value == top_card.value or 
                player_card.color == 'Wild')

    def next_player_draw(self, num_cards):
        """Let the next player draw the specified number of cards."""
        next_player = self.players[(self.current_player + self.direction) % len(self.players)]
        next_player.draw(self.deck, num_cards)
        self.update_game_display()

    def ask_for_wild_color(self, card):
        """Ask the player to choose a color after playing a Wild card."""
        color_dialog = tk.Toplevel(self.root)
        color_dialog.title("Choose a color")
        
        # Create buttons for each color choice
        color_choices = ['Red', 'Yellow', 'Green', 'Blue']
        color_buttons = []

        def set_color(selected_color):
            self.playing_stack[-1].color = selected_color  # Set the new color to the top card
            player = self.players[self.current_player]
            player.play_card(card)  # Discard the Wild card
            color_dialog.destroy()  # Close the dialog
            self.update_game_display()  # Update the game display after color selection

        for color in color_choices:
            btn = tk.Button(color_dialog, text=color, width=10, height=2,
                            command=lambda color=color: set_color(color))
            btn.pack(pady=10)

    def on_draw_card(self):
        """Handle the event when a player draws a card."""
        player = self.players[self.current_player]
        player.draw(self.deck)
        self.update_game_display()

        if player.has_won():
            messagebox.showinfo("UNO", f"{player.name} has won the game!")
            self.root.quit()
            return

        self.current_player = (self.current_player + self.direction) % len(self.players)
        self.update_game_display()

    def start_game(self):
        for player in self.players:
            for _ in range(7):
                player.draw(self.deck)
        self.update_game_display()

# GUI setup
def main():
    root = tk.Tk()
    root.title("UNO Game")
    root.configure(bg='lightblue')
    
    player_names = ['Player 1', 'Player 2']
    game = UNOGame(player_names, root)
    game.start_game()

    root.mainloop()

if __name__ == "__main__":
    main()
