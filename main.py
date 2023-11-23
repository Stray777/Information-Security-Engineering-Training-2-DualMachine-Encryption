import tkinter as tk
from UI import UI
from Server import Server


if __name__ == "__main__":
    server = Server()
    server.start()

    root = tk.Tk()
    window = UI(root)
    root.mainloop()
