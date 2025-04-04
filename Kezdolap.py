from tkinter import *
import sqlite3
import subprocess
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import Toplevel, Label, Button, BOTH
from ttkbootstrap.widgets import Meter

root = tb.Window(themename="darkly")
root.title("Adatbázis létrehozása")
root.geometry("800x6000")
def create_database():
    conn = sqlite3.connect("mozi.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Termek (
        terem_szam INTEGER PRIMARY KEY,
        film_cim TEXT NOT NULL,
        mufaj TEXT,
        evszam INTEGER,
        jatekido INTEGER,
        kapacitas INTEGER
    )
    """) 

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Foglalasok (
        foglalas_id INTEGER PRIMARY KEY AUTOINCREMENT,
        keresztnev TEXT NOT NULL,
        vezeteknev TEXT NOT NULL,
        terem_szam INTEGER,
        szek_szam INTEGER,
        FOREIGN KEY (terem_szam) REFERENCES Termek(terem_szam)
    )
    """)
    cursor.execute("SELECT COUNT(*) FROM Termek")
    if cursor.fetchone()[0] == 0:
        filmek = [
            (1, "Dűne: Második rész", "Sci-Fi", 2024, 165, 100),
            (2, "Oppenheimer", "Dráma", 2023, 180, 80),
            (3, "Avatar 2", "Akció", 2022, 192, 120),
        ]
        cursor.executemany("INSERT INTO Termek VALUES (?, ?, ?, ?, ?, ?)", filmek)
    
    conn.commit()
    conn.close()


def Folgalolist():
    seat_window = Toplevel(root)
    seat_window.title("Székfoglalás")
    Label(seat_window, text="Itt foglalhatod le a széked.").pack(pady=10)

def Filmlist():
    subprocess.Popen(["python", "probalos.py"])

label = Label(root, text="Válassz egy lehetőséget:", font=("Arial", 20))
label.pack(pady=10)


seat_button = Button(root, text="Székfoglalás", command=Folgalolist)
seat_button.pack(pady=5)

movie_button = Button(root, text="Filmlista", command=Filmlist)
movie_button.pack(pady=5)
root.mainloop()