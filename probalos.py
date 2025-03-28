from tkinter import *
import sqlite3
import os
from PIL import Image
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, Toplevel, Entry, Label, Button, IntVar, Spinbox
from fpdf import FPDF


root=tb.Window(themename="darkly")
root.title("Jegyfoglalos")
root.geometry("800x600")

label = tb.Label(root, text="Válassz filmet:", font=("Arial", 16))
label.pack(pady=10)
    
film_lista = tb.Treeview(root, columns=("terem", "cim", "helyek"), show="headings")
film_lista.heading("terem", text="Terem")
film_lista.heading("cim", text="Film címe")
film_lista.heading("helyek", text="Szabad helyek")
film_lista.pack(fill=BOTH, expand=True, padx=10, pady=10)

def Folgalolist():
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


label = Label(root, text="Válassz egy lehetőséget:", font=("Arial", 12))
label.pack(pady=10)


seat_button = Button(root, text="Székfoglalás", command=Folgalolist)
seat_button.pack(pady=5)

movie_button = Button(root, text="Filmlista", command=Filmlist)
movie_button.pack(pady=5)

ticket_button = Button(root, text="Jegyeim", command=Jegylist)
ticket_button.pack(pady=5)


root.mainloop()