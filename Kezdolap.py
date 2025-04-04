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





label = Label(root, text="MigaBiga", font=("Arial", 40))
label.pack(pady=10)

def Filmlist():
    subprocess.Popen(["python", "probalos.py"])
movie_button = Button(root, text="Filmlista", command=Filmlist, font=("Arial",24),width=7,height=2)
movie_button.pack(pady=5)
root.mainloop()