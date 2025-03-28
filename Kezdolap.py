from tkinter import *
import sqlite3

root = Tk()
root.title("Adatbázis létrehozása")
root.geometry("400x400")
seat_window = Toplevel(root)
seat_window.title("Székfoglalás")
Label(seat_window, text="Itt foglalhatod le a széked.").pack(pady=10)

def Filmlist():
    Filmek = Toplevel(root)
    Filmek.title("Filmlista")
    Label(Filmek, text="Itt láthatod az elérhető filmeket.").pack(pady=10)

def Jegylist():
    ticket_window = Toplevel(root)
    ticket_window.title("Jegyeim")

    Label(ticket_window, text="Itt találod a jegyeidet.").pack(pady=10)



# Címke
label = Label(root, text="Válassz egy lehetőséget:", font=("Arial", 12))
label.pack(pady=10)

# Gombok
seat_button = Button(root, text="Székfoglalás")
seat_button.pack(pady=5)

movie_button = Button(root, text="Filmlista", command=Filmlist)
movie_button.pack(pady=5)

ticket_button = Button(root, text="Jegyeim", command=Jegylist)
ticket_button.pack(pady=5)


root.mainloop()