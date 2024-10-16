import tkinter as tk
from tkinter import messagebox
TK_SILENCE_DEPRECATION = 1

def start():
    messagebox.showinfo("UNO", "uno is starting!")

root = tk.Tk()
root.title("UNO")

root.geometry("700x500")

messagebox.showinfo("UNO", "welcome to our UNO game!")

startButton = tk.Button(root, text = "start", font=("Helvetica", 18), command = start)
startButton.pack(pady = 200)

root.mainloop()