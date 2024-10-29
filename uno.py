# python3 -m pip install PySimpleGUI
'''
import PySimpleGUI as sg
import random

def buildDeck():
    deck = []
    colors = ["R", "Y", "G", "B"]
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "+2", "skip", "reverse"]
    wilds = ["W", "W +4"]
    for c in colors: 
        for v in values:
            cardVal = "{} {}".format(c, v)
            deck.append(cardVal)
            if v != 0:
                deck.append(cardVal)
    deck.extend(wilds)
    return deck

layout = [[sg.Text("welcome to our UNO game!", font = ('Helvetica', 40), justification = 'center')],
          [sg.Button("start", font = ('Helvetica', 20), size = (10, 2))]]

window = sg.Window("UNO game", layout, size = (800, 600))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "start":
        while True:
            numPlayers = sg.popup_get_text("enter number of players (2-4):", title = "number of players")
            if numPlayers and numPlayers.isdigit():
                numPlayers = int(numPlayers)
                if 2 <= numPlayers <= 4:
                    break
                else:
                    sg.popup("please enter a number between 2 and 4.")
            else:
                sg.popup("invalid")
        
        deck = buildDeck()
        allGiven = {f"player {i+1}": random.sample(deck, 7) for i in range(numPlayers)}
        
        for player, cards in allGiven.items():
            sg.popup(f"{player}'s hand:\n" + "\n".join(cards), title=f"{player}'s cards")

window.close()
'''
import PySimpleGUI as sg

# Define card dimensions
card_width, card_height = 200, 300

layout = [
    [sg.Graph((card_width, card_height), (0, 0), (card_width, card_height), key='graph')]
]

window = sg.Window('UNO Card', layout, finalize=True)
graph = window['graph']

# Function to draw a card
def draw_uno_card(graph, card_type, text, color):
    # Draw the card background
    graph.draw_rectangle((10, 10), (190, 290), line_color='black', fill_color=color)
    
    # Draw the inner circle
    graph.draw_circle((100, 150), 70, fill_color='white', line_color='black', line_width=2)
    
    # Draw the central text or symbol
    if card_type == 'number':
        graph.draw_text(text, (100, 150), font=('Helvetica', 60), color='black', text_location=sg.TEXT_LOCATION_CENTER)
    else:
        graph.draw_text(text, (100, 150), font=('Helvetica', 30), color='black', text_location=sg.TEXT_LOCATION_CENTER)
    
    # Draw the corner text
    graph.draw_text(text, (30, 270), font=('Helvetica', 20), color='white', text_location=sg.TEXT_LOCATION_CENTER)
    graph.draw_text(text, (170, 30), font=('Helvetica', 20), color='white', text_location=sg.TEXT_LOCATION_CENTER)

# Draw a red number 5 card
#draw_uno_card(graph, 'number', '5', '#FF0000')

# Draw a blue reverse card
#draw_uno_card(graph, 'special', '⇄', '#0000FF')

# Draw a yellow skip card
#draw_uno_card(graph, 'special', '⦸', '#FFFF00')

# Draw a green draw two card
#draw_uno_card(graph, 'special', '+2', '#00FF00')

# Draw a wild card
#draw_uno_card(graph, 'special', 'WILD', '#000000')

# To keep window open
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

