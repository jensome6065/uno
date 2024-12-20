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
        while first_card.color == 'Wild' or first_card.value == 'Skip' or first_card.value == 'Reverse' or first_card.value == '+2':
            first_card = self.deck.draw_card()
        self.playing_stack.append(first_card)
        
        self.root = root
        self.update_game_display()
    
    def start_game(self):
        for player in self.players:
            for _ in range(7):
                player.draw(self.deck)
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
            self.top_card_canvas.create_text(50, 70, text="Number", font=('Arial', 16, 'bold'), fill='black')
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
            card_canvas.create_text(50, 70, text="Number", font=('Arial', 16, 'bold'), fill='black')
        else:
            card_canvas.create_text(50, 70, text=card.value, font=('Arial', 16, 'bold'), fill='black')

        return card_canvas

    def card_value_sort_key(self, card):
        """Helper method to provide sorting key for card values."""
        special_values = {'Skip': 10, 'Reverse': 11, '+2': 12, 'Color': 13, '+4': 14, 'Number': 15, 'Swap': 16, 'Trash': 17}
        return int(card.value) if card.value.isdigit() else special_values.get(card.value, 15)

    def check_and_display_uno(self):
        """Check if any player has one card and display 'UNO'."""
        for player in self.players:
            if len(player.hand) == 1:
                self.player_info_labels[player.name].config(text=f"{player.name}: UNO")
            else:
                self.player_info_labels[player.name].config(text=f"{player.name}: {len(player.hand)} cards")
    
    def check_for_winner(self):
        """Check if any player has zero cards and end the game."""
        for player in self.players:
            if len(player.hand) == 0:
                messagebox.showinfo("Game Over", f"{player.name} wins the game!")
                self.root.destroy() 
                return
       
    def move_to_next_player(self):
        """Move to the next player after the current player plays a card."""
        self.current_player = (self.current_player + self.direction) % len(self.players)
        self.root.after(500, self.update_game_display) 

    def on_draw_card(self):
        """Handle the event when a player draws a card."""
        player = self.players[self.current_player]
        try:
            drawn_card = self.deck.draw_card(self.playing_stack)
            player.hand.append(drawn_card)

            if self.is_valid_play(drawn_card):
                self.on_card_play(len(player.hand) - 1) 
            else:
                self.move_to_next_player()
        except IndexError:
            messagebox.showwarning("Deck Empty", "No cards left to draw, and discard pile cannot be reshuffled.")
        self.update_game_display()

    def is_valid_play(self, player_card):
        """Check if the card played by the player is valid."""
        top_card = self.playing_stack[-1]

        if top_card.value == 'Swap':
            return True
        
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

    def handle_special_cards(self, card):
        """Handle special cards (Skip, +2, Reverse, and Wild cards)."""
        if card.value == 'Skip':
            self.current_player = (self.current_player + self.direction) % len(self.players)
        elif card.value == '+2':
            self.handle_draw_two(card)
        elif card.value == 'Reverse':
            self.direction *= -1
        elif card.value == 'Swap':
            self.handle_swap(self.players[self.current_player])
        elif card.value == 'Trash':
            self.handle_wild_trash(card)
        elif card.value == '+4':
            next_player_index = (self.current_player + self.direction) % len(self.players)
            self.players[next_player_index].draw(self.deck, 4)  # Next player draws 4 cards
            
            # Skip the player who drew the +4
            self.current_player = (self.current_player + 2 * self.direction) % len(self.players)  # Skip over the current player
            
            # Move to the next player
            self.move_to_next_player()
        self.check_for_winner()

    def handle_draw_two(self, card):
        """Handle the +2 card stacking mechanism."""
        total_draws = 2
        current_player_index = (self.current_player + self.direction) % len(self.players)
        
        while True:
            next_player = self.players[current_player_index]
            
            if any(c.value == '+2' for c in next_player.hand):
                self.current_player = current_player_index
                next_player_turn = False
                
                for idx, c in enumerate(next_player.hand):
                    if c.value == '+2':
                        self.on_card_play(idx)
                        total_draws += 2
                        current_player_index = (current_player_index + self.direction) % len(self.players)
                        break
            else:
                next_player.draw(self.deck, total_draws)
                self.current_player = current_player_index
                self.move_to_next_player()
                break

    def handle_swap(self, player):
        """Handle the Swap card effect."""
        fewest_cards_player = min(self.players, key=lambda p: len(p.hand))

        swap_card = None
        for card in player.hand:
            if card.color == 'Wild' and card.value == 'Swap':
                swap_card = card
                break

        if not swap_card:
            messagebox.showerror("Error", "Swap card not found in player's hand!")
            return

        player.hand.remove(swap_card)  
        self.playing_stack.append(swap_card)  

        player.hand, fewest_cards_player.hand = fewest_cards_player.hand, player.hand

        self.update_game_display()
        self.move_to_next_player()

    def handle_wild_trash(self, card):
        """Handle the Wild Trash card effect."""
        player = self.players[self.current_player]

        available_colors = {c.color for c in player.hand if c.color != 'Wild'}
        
        if not available_colors:
            messagebox.showwarning("No Available Colors", "You have no colored cards to trash.")
            return

        color_dialog = tk.Toplevel(self.root)
        color_dialog.title("Choose a Color to Trash")
        color_dialog.geometry("300x200")
        color_dialog.configure(bg="lightblue")

        def choose_trash_color(selected_trash_color):
            """Choose which color to trash and then select a new top color."""
            cards_to_trash = [c for c in player.hand if c.color == selected_trash_color]
            for c in cards_to_trash:
                player.hand.remove(c)
                self.playing_stack.append(c)

            color_dialog.destroy()

            self.ask_for_wild_color(card)

        for color in available_colors:
            tk.Button(
                color_dialog,
                text=color,
                width=15,
                height=2,
                command=lambda color=color: choose_trash_color(color),
                bg=color.lower()
            ).pack(pady=10)

        color_dialog.grab_set()  

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

    def ask_for_wild_color(self, card):
        """Ask the player to choose a color after playing a Wild card."""
        color_dialog = tk.Toplevel(self.root)
        color_dialog.title("Choose a color")
        color_dialog.geometry("300x200")
        color_dialog.configure(bg="lightblue")

        available_colors = {c.color for c in self.players[self.current_player].hand if c.color != 'Wild'}
        if not available_colors:
            available_colors = ['Red', 'Yellow', 'Green', 'Blue'] 

        def set_color(selected_color):
            card.color = selected_color 
            self.playing_stack.append(card) 

            player = self.players[self.current_player]
            if card in player.hand:
                player.play_card(card)  
            
            color_dialog.destroy()

            if card.value == '+4':
                next_player_index = (self.current_player + self.direction) % len(self.players)
                self.players[next_player_index].draw(self.deck, 4) 
                self.current_player = (self.current_player + 2 * self.direction) % len(self.players)
            else:
                self.move_to_next_player()

            self.update_game_display()

        for color in available_colors:
            tk.Button(
                color_dialog,
                text=color,
                width=15,
                height=2,
                command=lambda color=color: set_color(color),
                bg=color.lower()
            ).pack(pady=10)

        color_dialog.grab_set()

    def ask_for_wild_number(self, card):
        """Ask the player to type a number for the Wild Number card."""
        number_dialog = tk.Toplevel(self.root)
        number_dialog.title("Choose a Number")
        number_dialog.geometry("300x200")
        number_dialog.configure(bg="lightblue")

        instruction_label = tk.Label(
            number_dialog, text="Type a number between 0 and 9:", font=('Arial', 14), bg="lightblue")
        instruction_label.pack(pady=10)

        number_entry = tk.Entry(number_dialog, font=('Arial', 14))
        number_entry.pack(pady=10)

        def set_number():
            """Set the number for the Wild card."""
            try:
                selected_number = int(number_entry.get())
                if 0 <= selected_number <= 9:
                    card.value = str(selected_number)  
                    self.playing_stack.append(card)  
                    player = self.players[self.current_player]
                    player.play_card(card)  
                    number_dialog.destroy()
                    self.move_to_next_player()
                    self.update_game_display()
                else:
                    messagebox.showwarning("Invalid Input", "Please enter a number between 0 and 9.")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid number.")

        confirm_button = tk.Button(number_dialog, text="Confirm", command=set_number, font=('Arial', 14), bg="lightgreen")
        confirm_button.pack(pady=10)

        number_dialog.grab_set()

    def on_card_play(self, card_index):
        """Handle the event when a card is played."""
        player = self.players[self.current_player]
        card = player.hand[card_index]

        if card.color == 'Wild':
            if card.value == 'Trash':
                self.handle_wild_trash(card)
            elif card.value == 'Swap':
                self.handle_swap(player)
            elif card.value == 'Number':
                self.ask_for_wild_number(card)
                self.handle_special_cards(card)
            elif card.value == '+4':
                # Modified +4 logic to first ask for color
                self.ask_for_wild_color(card, is_plus_four=True)
            else:
                self.ask_for_wild_color(card)  
        elif self.is_valid_play(card):
            player.play_card(card)
            self.playing_stack.append(card)

            if len(player.hand) == 0:
                self.check_for_winner()
                return

            self.handle_special_cards(card)

            self.root.after(500, self.move_to_next_player)
        else:
            messagebox.showwarning("Invalid Play", "That card is not valid!")

    def ask_for_wild_color(self, card, is_plus_four=False):
        """Ask the player to choose a color after playing a Wild card."""
        color_dialog = tk.Toplevel(self.root)
        color_dialog.title("Choose a color")
        color_dialog.geometry("300x200")
        color_dialog.configure(bg="lightblue")

        available_colors = {c.color for c in self.players[self.current_player].hand if c.color != 'Wild'}
        if not available_colors:
            available_colors = ['Red', 'Yellow', 'Green', 'Blue'] 

        def set_color(selected_color):
            card.color = selected_color 
            self.playing_stack.append(card) 

            player = self.players[self.current_player]
            if card in player.hand:
                player.play_card(card)  
            
            color_dialog.destroy()

            if is_plus_four:
                # If it's a +4 card, ask the next player if they want to challenge
                self.challenge_plus_four(card, selected_color)
            else:
                self.move_to_next_player()
                self.update_game_display()

        for color in available_colors:
            tk.Button(
                color_dialog,
                text=color,
                width=15,
                height=2,
                command=lambda color=color: set_color(color),
                bg=color.lower()
            ).pack(pady=10)

        color_dialog.grab_set()

    def challenge_plus_four(self, card, chosen_color):
        """Ask the next player if they want to challenge the +4 card."""
        next_player_index = (self.current_player + self.direction) % len(self.players)
        next_player = self.players[next_player_index]

        challenge_dialog = tk.Toplevel(self.root)
        challenge_dialog.title("Challenge +4?")
        challenge_dialog.geometry("300x200")
        challenge_dialog.configure(bg="lightblue")

        tk.Label(challenge_dialog, 
                 text=f"{next_player.name}, do you want to challenge the +4?", 
                 font=('Arial', 14), 
                 bg="lightblue", 
                 wraplength=250).pack(pady=20)

        def accept_plus_four():
            """Accept the +4 card and draw 4 cards."""
            next_player.draw(self.deck, 4)
            self.current_player = (self.current_player + 2 * self.direction) % len(self.players)
            challenge_dialog.destroy()
            self.move_to_next_player()
            self.update_game_display()

        def challenge_plus_four_play():
            """Challenge the +4 card play."""
            current_player_hand = self.players[self.current_player].hand
            can_play_color = any(
                card.color == chosen_color or 
                card.value == self.playing_stack[-2].value 
                for card in current_player_hand
            )

            challenge_dialog.destroy()

            if can_play_color:
                # Current player played +4 illegally and must draw 6 cards
                messagebox.showinfo("Challenge Successful", 
                                    f"{self.players[self.current_player].name} must draw 6 cards!")
                self.players[self.current_player].draw(self.deck, 6)
                self.current_player = next_player_index
            else:
                # Challenge failed, next player draws 4
                next_player.draw(self.deck, 4)
                self.current_player = (self.current_player + 2 * self.direction) % len(self.players)

            self.move_to_next_player()
            self.update_game_display()

        tk.Button(challenge_dialog, text="Accept +4", 
                  command=accept_plus_four, 
                  bg="green", 
                  font=('Arial', 12)).pack(pady=10)

        tk.Button(challenge_dialog, text="Challenge", 
                  command=challenge_plus_four_play, 
                  bg="red", 
                  font=('Arial', 12)).pack(pady=10)

        challenge_dialog.grab_set()

    def next_player_draw(self, num_cards):
        """Let the next player draw the specified number of cards."""
        next_player = self.players[(self.current_player + self.direction) % len(self.players)]
        next_player.draw(self.deck, num_cards)
        self.update_game_display()
     
def main():
    root = tk.Tk()
    root.withdraw
    
    num_players = simpledialog.askinteger("Number of Players", "Enter the number of players (2-4):", minvalue=2, maxvalue=4)
    if num_players is None:
        return 

    player_names = []
    for i in range(num_players):
        while True:
            player_name = simpledialog.askstring("Player Name", f"Enter name for Player {i+1}:")
            if player_name and player_name.strip():
                player_names.append(player_name.strip())
                break
            else:
                messagebox.showwarning("Invalid Input", "Player name cannot be empty!")

    root.deiconify()
    root.title("UNO Game")
    root.configure(bg='lightblue')

    game = UNOGame(player_names, root)
    game.start_game()
    root.mainloop()

if __name__ == "__main__":
    main()