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

    def draw(self, deck):
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
        for idx, card in enumerate(player.hand):
            btn = tk.Button(self.root, width=12, height=6, relief="raised", command=lambda idx=idx: self.on_card_play(idx))
            self.draw_card_on_button(btn, card)  # Draw the card on the button
            btn.grid(row=1, column=idx)
            self.hand_buttons.append(btn)

        # Show whose turn it is
        self.turn_label = tk.Label(self.root, text=f"{player.name}'s turn", font=('Arial', 16), bg='lightblue', pady=10)
        self.turn_label.grid(row=2, column=0, columnspan=5)

        # Draw Card Button
        self.draw_button = tk.Button(self.root, text="Draw Card", width=20, height=2,
                                     command=self.on_draw_card, bg="lightgreen", relief="raised")
        self.draw_button.grid(row=3, column=0, columnspan=5)

    def clear_widgets(self):
        """Clear all existing widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def draw_card_on_button(self, btn, card):
        """Draw a card with color and value on the button."""
        # Set color based on the card's color
        card_color = self.get_card_color(card)
        btn.config(bg=card_color)  # Change button's background color to match the card color
        btn.config(text=card.value)  # Display the card value as text on the button
        btn.config(fg="white", font=("Arial", 16, "bold"))  # Set text properties

    def get_card_color(self, card):
        """Return the color for the card."""
        if card.color == 'Wild':
            return 'gray'  # Wild cards have a gray color
        return card.color.lower()  # Red, Blue, Green, Yellow

    def on_card_play(self, card_index):
        """Handle the event when a card is played."""
        player = self.players[self.current_player]
        card = player.hand[card_index]
        if self.is_valid_play(card):
            player.play_card(card)
            self.playing_stack.append(card)
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
