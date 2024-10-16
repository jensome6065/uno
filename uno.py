# python3 -m pip install PySimpleGUI
import PySimpleGUI as sg

layout = [[sg.Text("welcome to our UNO game!", font = ('Helvetica', 40), justification = 'center')],
          [sg.Button("start", font = ('Helvetica', 20), size = (10, 2))]]

window = sg.Window("UNO game", layout, size = (800, 600))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "start":
        sg.popup("game is starting...")
        break

window.close()