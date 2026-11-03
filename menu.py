# Menu for the record collection database application
# front-end GUI using Tkinter 
import tkinter as tk
class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("Record Collection Database")
        self.root.geometry("400x300")
        self.label = tk.Label(self.root, text="Welcome to the Record Collection Database!")
        self.label.pack(pady=20)
        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.pack(pady=20)

    def start(self):
        self.label.config(text="Starting the application...")
        self.start_button.config(state=tk.DISABLED)
        self.root.update()
        # Here you would typically launch the main application window or perform other initialization tasks.
        self.root.destroy()  # Close the menu window after starting the main application