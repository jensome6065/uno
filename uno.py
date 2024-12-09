import tkinter as tk
from tkinter import messagebox, simpledialog
from player import Player
from cards import Deck, Card

class UNOGame:
    def __init__(self, players, root):
        self.deck = Deck()
        self.players = [Player(name) for name in players]
        self.current_player = 0
        self.direction = 1
        self.playing_stack = [self.deck.draw_card()]

        first_card = self.deck.draw_card()
        while first_card.value in ['Skip', 'Reverse', '+2', '+4', 'Color', 'Swap', 'Trash', 'Number']:
            first_card = self.deck.draw_card()
        self.playing_stack.append(first_card)
        
        self.root = root
        self.update_game_display()

    def update_game_display(self):
        """Update the game state on the GUI."""
        self.clear_widgets()

        top_card = self.playing_stack[-1]
        self.top_card_canvas = tk.Canvas(self.root, width=100, height=150, bg='white', bd=0, relief="flat")
        self.top_card_canvas.grid(row=0, column=2, pady=(30, 40)) 

        if top_card.color != 'Wild':
            self.top_card_canvas.create_rectangle(5, 5, 95, 145, fill=top_card.color.lower(), outline='black', width=2)
        else:
            colors = ['red', 'blue', 'green', 'yellow']
            for i, color in enumerate(colors):
                self.top_card_canvas.create_rectangle(
                    5, 5 + i * 35, 95, 5 + (i + 1) * 35,
                    fill=color, outline='black', width=1
                )

        self.top_card_canvas.create_oval(25, 40, 75, 100, fill='white', outline='black', width=2)

        if top_card.color == 'Wild' and top_card.value == 'Number':
            self.top_card_canvas.create_text(50, 70, text="Wild\nNumber", font=('Arial', 12, 'bold'), fill='black')
        else:
            self.top_card_canvas.create_text(50, 70, text=top_card.value, font=('Arial', 16, 'bold'), fill='black')

        self.deck_canvas = tk.Canvas(self.root, width=100, height=150, bg='black', bd=0, relief="flat")
        self.deck_canvas.grid(row=0, column=3, padx=10, pady=(30, 40)) 
        self.deck_canvas.create_oval(25, 40, 75, 100, fill='red', outline='black', width=2)
        self.deck_canvas.create_text(50, 70, text="UNO", font=('Arial', 24, 'bold'), fill='yellow')

        self.draw_button = tk.Button(
            self.root, text="Draw Card", width=15, height=2,
            command=self.on_draw_card, bg="lightgreen", relief="raised"
        )
        self.draw_button.grid(row=0, column=4, padx=10, pady=(30, 40)) 

        player = self.players[self.current_player]
        self.hand_buttons = []
        self.hand_canvases = []
        player.hand.sort(key=lambda card: (card.color, self.card_value_sort_key(card)))

        hand_start_column = 0  
        for idx, card in enumerate(player.hand):
            card_canvas = self.create_card_canvas(self.root, card, idx)
            self.hand_canvases.append(card_canvas)

            card_button = tk.Button(
                self.root, width=10, height=5, relief="flat",
                text=f"{card.color}\n{card.value}", command=lambda idx=idx: self.on_card_play(idx),
                font=('Arial', 10), bg='lightgrey', bd=0
            )
            card_button.grid(row=2, column=hand_start_column + idx, padx=10, pady=10) 
            self.hand_buttons.append(card_button)

        self.turn_label = tk.Label(self.root, text=f"{player.name}'s turn", font=('Arial', 30), bg='lightblue', pady=10)
        self.turn_label.grid(row=0, column=1, padx=10, pady=(30, 40), sticky='w')  

        self.player_info_labels = {}
        for idx, p in enumerate(self.players):
            label_text = f"{p.name}: {len(p.hand)} cards"
            label = tk.Label(self.root, text=label_text, font=('Arial', 20), bg='lightblue')
            label.grid(row=0, column=5 + idx, padx=10, pady=5)  
            self.player_info_labels[p.name] = label

        self.check_and_display_uno()

    def card_value_sort_key(self, card):
        """Helper method to provide sorting key for card values."""
        special_values = {'Skip': 10, 'Reverse': 11, '+2': 12, 'Color': 13, '+4': 14, 'Number': 15, 'Swap': 16, 'Trash': 17}
        return int(card.value) if card.value.isdigit() else special_values.get(card.value, 15)

    def clear_widgets(self):
        """Clear all existing widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_card_canvas(self, root, card, idx):
        """Draw the card with color, value, and circles on a canvas."""
        card_canvas = tk.Canvas(root, width=100, height=150, bg='white', bd=0, relief="flat")
        card_canvas.grid(row=1, column=idx, padx=5, pady=5)

        if card.color != 'Wild':
            card_canvas.create_rectangle(5, 5, 95, 145, fill=card.color.lower(), outline='black', width=2)
        else:
            colors = ['red', 'blue', 'green', 'yellow']
            for i, color in enumerate(colors):
                card_canvas.create_rectangle(
                    5, 5 + i * 35, 95, 5 + (i + 1) * 35,
                    fill=color, outline='black', width=1
                )

        card_canvas.create_oval(25, 40, 75, 100, fill='white', outline='black', width=2)  

        if card.color == 'Wild' and card.value == 'Number':
            card_canvas.create_text(50, 70, text="Wild\nNumber", font=('Arial', 12, 'bold'), fill='black')
        else:
            card_canvas.create_text(50, 70, text=card.value, font=('Arial', 16, 'bold'), fill='black')

        return card_canvas

    def on_card_play(self, card_index):
        """Handle the event when a card is played."""
        player = self.players[self.current_player]
        card = player.hand[card_index]

        if card.color == 'Wild':
            if card.value == 'Swap':
                self.handle_swap(player)
            elif card.value == 'Wild Number':
                self.ask_for_wild_number(card)
            elif card.value == 'Wild +4':
                next_player_index = (self.current_player + self.direction) % len(self.players)
                self.players[next_player_index].draw(self.deck, 4)
                self.current_player = (self.current_player + 2 * self.direction) % len(self.players)
                self.update_game_display()
            elif card.value == 'Wild Trash':
                self.handle_wild_trash(card)  
            else:
                self.ask_for_wild_color(card)
        elif self.is_valid_play(card):
            player.play_card(card)
            self.playing_stack.append(card)

            if len(player.hand) == 0:
                self.check_for_winner()
                return 

            self.handle_special_cards(card)
            self.move_to_next_player()
            self.update_game_display()

        else:
            messagebox.showwarning("Invalid Play", "That card is not valid!")

    def move_to_next_player(self):
        """Move to the next player after the current player plays a card."""
        self.current_player = (self.current_player + self.direction) % len(self.players)

    def on_draw_card(self):
        """Handle the event when a player draws a card."""
        player = self.players[self.current_player]
        player.draw(self.deck)

        if len(player.hand) == 0:
            self.check_for_winner()
            return  

        drawn_card = player.hand[-1] 
        if self.is_valid_play(drawn_card):
            self.on_card_play(len(player.hand) - 1) 
            return  

        self.move_to_next_player()
        self.update_game_display()

    def handle_swap(self, player):
        """Handle the Swap wildcard effect."""
        fewest_cards_player = min(self.players, key=lambda p: len(p.hand))
        player.hand, fewest_cards_player.hand = fewest_cards_player.hand, player.hand
        swap_card = None
        for card in player.hand:
            if card.color == 'Wild' and card.value == 'Swap':
                swap_card = card
                break
        if swap_card:
            player.hand.remove(swap_card)
            self.playing_stack.append(swap_card)

        self.move_to_next_player()
        self.update_game_display()

    def handle_wild_trash(self):
        """Handle the Wild Trash card effect."""
        player = self.players[self.current_player]

        color_dialog = tk.Toplevel(self.root)
        color_dialog.title("Choose a color to discard")

        color_choices = ['Red', 'Yellow', 'Green', 'Blue']

        def discard_color_cards(selected_color):
            cards_to_remove = [card for card in player.hand if card.color == selected_color]
            for card in cards_to_remove:
                player.hand.remove(card)
                self.playing_stack.append(card) 

            color_dialog.destroy()
            self.move_to_next_player() 
            self.update_game_display()  

        for color in color_choices:
            btn = tk.Button(color_dialog, text=color, width=10, height=2,
                            command=lambda color=color: discard_color_cards(color))
            btn.pack(pady=10)

    def handle_special_cards(self, card):
        """Handle special cards (Skip, +2, Reverse, and Wild cards)."""
        if card.value == 'Skip':
            self.current_player = (self.current_player + 2 * self.direction) % len(self.players)
        elif card.value == '+2':
            next_player_index = (self.current_player + self.direction) % len(self.players)
            self.players[next_player_index].draw(self.deck, 2)
            self.current_player = (self.current_player + 2 * self.direction) % len(self.players)
        elif card.value == 'Reverse':
            self.direction *= -1
        elif card.value == 'Swap':
            self.handle_swap(self.players[self.current_player])
        elif card.value == 'Trash':
            self.handle_wild_trash(card)

        self.check_for_winner()

    def ask_for_wild_color(self, card):
        """Ask the player to choose a color after playing a Wild card."""
        color_dialog = tk.Toplevel(self.root)
        color_dialog.title("Choose a color")

        color_choices = ['Red', 'Yellow', 'Green', 'Blue']
        
        def set_color(selected_color):
            self.playing_stack[-1].color = selected_color
            player = self.players[self.current_player]
            player.play_card(card)  
            color_dialog.destroy()  

            if card.value == '+4':
                next_player_index = (self.current_player + self.direction) % len(self.players)
                self.players[next_player_index].draw(self.deck, 4)
                self.current_player = (self.current_player + 2 * self.direction) % len(self.players)

            self.update_game_display()  

        for color in color_choices:
            btn = tk.Button(color_dialog, text=color, width=10, height=2,
                            command=lambda color=color: set_color(color))
            btn.pack(pady=10)

    def ask_for_wild_number(self, card):
        """Ask the player to choose a color and a number for the Wild Number card."""
        color_dialog = tk.Toplevel(self.root)
        color_dialog.title("Choose a Color")
        
        color_choices = ['Red', 'Yellow', 'Green', 'Blue']
        
        def on_color_select(selected_color):
            color_dialog.destroy()
            number_dialog = tk.Toplevel(self.root)
            number_dialog.title("Choose a Number")
            
            chosen_number = simpledialog.askinteger(
                "Wild Number", 
                "Choose a number (0-9):", 
                parent=number_dialog, 
                minvalue=0, 
                maxvalue=9
            )
            
            if chosen_number is not None:
                wild_number_card = Card(selected_color, str(chosen_number))
                
                player = self.players[self.current_player]
                player.play_card(card)
                self.playing_stack.append(wild_number_card)
                self.update_game_display()
                self.current_player = (self.current_player + self.direction) % len(self.players)
                self.update_game_display()
            else:
                messagebox.showwarning("Invalid Choice", "You must choose a number!")

        for color in color_choices:
            btn = tk.Button(color_dialog, text=color, width=10, height=2,
                            command=lambda c=color: on_color_select(c))
            btn.pack(pady=10)

    def ask_for_wild_trash_color(self, card):
        """Ask the player to choose a color to discard all matching color cards."""
        color_dialog = tk.Toplevel(self.root)
        color_dialog.title("Choose a Color to Discard")

        color_choices = ['Red', 'Yellow', 'Green', 'Blue']
        
        def on_color_select(selected_color):
            player = self.players[self.current_player]
            player.hand = [card for card in player.hand if card.color != selected_color]

            player.play_card(card)
            self.playing_stack.append(card)
            
            color_dialog.destroy()  
            self.update_game_display() 
            self.move_to_next_player()

        for color in color_choices:
            btn = tk.Button(color_dialog, text=color, width=10, height=2,
                            command=lambda c=color: on_color_select(c))
            btn.pack(pady=10)

    def is_valid_play(self, player_card):
        """Check if the card played by the player is valid."""
        top_card = self.playing_stack[-1]
        
        if player_card.color == 'Wild' and player_card.value == '+4':
            current_player_hand = self.players[self.current_player].hand
            for card in current_player_hand:
                if card.color == top_card.color or card.value == top_card.value:
                    return False
        
        return (
            player_card.color == top_card.color or
            player_card.value == top_card.value or
            player_card.color == 'Wild'
        )

    def next_player_draw(self, num_cards):
        """Let the next player draw the specified number of cards."""
        next_player = self.players[(self.current_player + self.direction) % len(self.players)]
        next_player.draw(self.deck, num_cards)
        self.update_game_display()

    def check_and_display_uno(self):
        """Check if any player has one card and display 'UNO'."""
        for player in self.players:
            if len(player.hand) == 1:
                self.player_info_labels[player.name].config(text=f"{player.name}: UNO")
            else:
                self.player_info_labels[player.name].config(text=f"{player.name}: {len(player.hand)} cards")

    def start_game(self):
        for player in self.players:
            for _ in range(7):
                player.draw(self.deck)
        self.update_game_display()

    def check_for_winner(self):
        """Check if any player has zero cards and end the game."""
        for player in self.players:
            if len(player.hand) == 0:
                messagebox.showinfo("Game Over", f"{player.name} wins the game!")
                self.root.destroy() 
                return
            
def main():
    root = tk.Tk()
    root.title("UNO Game")
    root.configure(bg='lightblue')
    
    num_players = simpledialog.askinteger("Number of Players", "Enter the number of players (2-4):", minvalue=2, maxvalue=4)
    if num_players is None:
        return  

    player_names = []
    for i in range(num_players):
        player_name = simpledialog.askstring("Player Name", f"Enter name for Player {i+1}:")
        player_names.append(player_name)
    
    game = UNOGame(player_names, root)
    game.start_game()

    root.mainloop()

if __name__ == "__main__":
    main()