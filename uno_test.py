import tkinter as tk
from tkinter import messagebox, simpledialog
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
        self.wild_cards = ['Wild', 'Wild Draw Four', 'Wild Number']  # Add new Wild Number card
        self.cards = []
        self.create_deck()
        self.shuffle()

    def create_deck(self):
        # Existing color card creation remains the same
        for color in self.colors:
            for value in self.values:
                if value != '0':
                    self.cards.append(Card(color, value))
                    self.cards.append(Card(color, value))
                else:
                    self.cards.append(Card(color, value))
        
        # Add Wild cards, including the new Wild Number card
        for _ in range(4):
            self.cards.append(Card('Wild', 'Wild'))
            self.cards.append(Card('Wild', 'Wild Draw Four'))
            self.cards.append(Card('Wild', 'Wild Number'))  # Add Wild Number card

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

        if card.color == 'Wild':
            if card.value == 'Wild Number':
                self.ask_for_wild_number(card)
            elif card.value == 'Wild Draw Four':
                # Ask for color first
                color_dialog = tk.Toplevel(self.root)
                color_dialog.title("Choose a Color")
                
                color_choices = ['Red', 'Yellow', 'Green', 'Blue']
                
                def set_color(selected_color):
                    # Determine the next player
                    next_player_index = (self.current_player + self.direction) % len(self.players)
                    next_player = self.players[next_player_index]
                    
                    # Make the next player draw 4 cards
                    next_player.draw(self.deck, 4)
                    
                    # Play the Wild Draw Four card
                    player.play_card(card)
                    
                    # Change the color of the top card
                    wild_card = Card(selected_color, 'Wild Draw Four')
                    self.playing_stack.append(wild_card)
                    
                    # Move to the player after the one who drew
                    self.current_player = (next_player_index + self.direction) % len(self.players)
                    
                    color_dialog.destroy()
                    self.update_game_display()

                # Create color selection buttons
                for color in color_choices:
                    btn = tk.Button(color_dialog, text=color, width=10, height=2,
                                    command=lambda c=color: set_color(c))
                    btn.pack(pady=10)
            else:
                self.ask_for_wild_color(card)
        elif self.is_valid_play(card):
            player.play_card(card)
            self.playing_stack.append(card)

            # Handle special cards
            if card.value == 'Skip':
                # Skip the next player by moving the current player index
                self.current_player = (self.current_player + 2 * self.direction) % len(self.players)
            elif card.value == 'Draw Two':
                # Move to next player and make them draw
                self.current_player = (self.current_player + self.direction) % len(self.players)
                self.next_player_draw(2)
                # Move to the player after the one who drew
                self.current_player = (self.current_player + self.direction) % len(self.players)
            elif card.value == 'Reverse':
                # Reverse the direction of play
                self.direction *= -1
            
            if player.has_won():
                messagebox.showinfo("UNO", f"{player.name} has won the game!")
                self.root.quit()
                return

            # If it's not a special card that already moved the player, 
            # move to the next player
            if card.value not in ['Skip', 'Draw Two', 'Reverse', 'Wild Draw Four']:
                self.current_player = (self.current_player + self.direction) % len(self.players)

            self.update_game_display()
        else:
            messagebox.showwarning("Invalid Play", "That card is not valid!")
                        
    def ask_for_wild_number(self, card):
        """Ask the player to choose a color and a number for the Wild Number card."""
        # First, choose a color
        color_dialog = tk.Toplevel(self.root)
        color_dialog.title("Choose a Color")
        
        color_choices = ['Red', 'Yellow', 'Green', 'Blue']
        
        def on_color_select(selected_color):
            color_dialog.destroy()
            # After color selection, ask for a number
            number_dialog = tk.Toplevel(self.root)
            number_dialog.title("Choose a Number")
            
            # Create a simple dialog to choose a number between 0 and 9
            chosen_number = simpledialog.askinteger(
                "Wild Number", 
                "Choose a number (0-9):", 
                parent=number_dialog, 
                minvalue=0, 
                maxvalue=9
            )
            
            if chosen_number is not None:
                # Create a new card with the chosen color and number
                wild_number_card = Card(selected_color, str(chosen_number))
                
                # Play the card
                player = self.players[self.current_player]
                player.play_card(card)
                self.playing_stack.append(wild_number_card)
                
                # Update game display
                self.update_game_display()
                
                # Move to next player
                self.current_player = (self.current_player + self.direction) % len(self.players)
                self.update_game_display()
            else:
                messagebox.showwarning("Invalid Choice", "You must choose a number!")

        # Create color selection buttons
        for color in color_choices:
            btn = tk.Button(color_dialog, text=color, width=10, height=2,
                            command=lambda c=color: on_color_select(c))
            btn.pack(pady=10)

    def create_card_canvas(self, root, card, idx):
        """Draw the card with color, value and circles on a canvas."""
        card_canvas = tk.Canvas(root, width=100, height=150, bg='white', bd=0, relief="flat")
        card_canvas.grid(row=1, column=idx, padx=5, pady=5)

        # Draw the background color based on the card's color
        if card.color != 'Wild':
            card_canvas.create_rectangle(5, 5, 95, 145, fill=card.color.lower(), outline='black', width=2)
        else:
            # For Wild cards, draw a multicolor background
            colors = ['red', 'blue', 'green', 'yellow']
            for i, color in enumerate(colors):
                card_canvas.create_rectangle(
                    5, 5 + i*35, 95, 5 + (i+1)*35, 
                    fill=color, outline='black', width=1
                )

        # Draw circles in the center for card values
        card_canvas.create_oval(25, 40, 75, 100, fill='white', outline='black', width=2)
        # Modify text display for Wild Number card
        if card.color == 'Wild' and card.value == 'Wild Number':
            card_canvas.create_text(50, 70, text="Wild\nNumber", font=('Arial', 12, 'bold'), fill='black')
        else:
            card_canvas.create_text(50, 70, text=card.value, font=('Arial', 16, 'bold'), fill='black')

        return card_canvas
    
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
