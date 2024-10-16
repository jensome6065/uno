# python3 -m pip install PySimpleGUI
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