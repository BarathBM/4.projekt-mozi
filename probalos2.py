import sqlite3
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import Toplevel, Label, BOTH
from ttkbootstrap.widgets import Meter

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

def load_films():
    conn = sqlite3.connect("mozi.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Termek.terem_szam, Termek.film_cim, Termek.kapacitas - COALESCE(foglalasok_db, 0) AS szabad_helyek
        FROM Termek
        LEFT JOIN (
            SELECT terem_szam, COUNT(*) AS foglalasok_db FROM Foglalasok GROUP BY terem_szam
        ) AS F ON Termek.terem_szam = F.terem_szam
    """)
    films = cursor.fetchall()
    conn.close()
    
    film_lista.delete(*film_lista.get_children())
    for film in films:
        film_lista.insert("", "end", values=film)

def show_film_details(event):
    selected_item = film_lista.selection()
    if not selected_item:
        return
    
    film_data = film_lista.item(selected_item)["values"]
    if not film_data:
        return

    terem_szam, film_cim, szabad_helyek = film_data

    conn = sqlite3.connect("mozi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Termek WHERE terem_szam=?", (terem_szam,))
    film = cursor.fetchone()
    conn.close()

    if not film:
        return

    _, cim, mufaj, evszam, jatekido, kapacitas = film
    foglalt_helyek = kapacitas - szabad_helyek
    foglaltsagi_szint = (foglalt_helyek / kapacitas) * 100 if kapacitas > 0 else 0

    film_window = Toplevel(root)
    film_window.title(f"{cim} - Részletek")
    
    Label(film_window, text=f"Film címe: {cim}", font=("Arial", 14, "bold")).pack(pady=5)
    Label(film_window, text=f"Műfaj: {mufaj}", font=("Arial", 12)).pack(pady=5)
    Label(film_window, text=f"Évszám: {evszam}", font=("Arial", 12)).pack(pady=5)
    Label(film_window, text=f"Játékidő: {jatekido} perc", font=("Arial", 12)).pack(pady=5)
    Label(film_window, text=f"Terem kapacitása: {kapacitas} fő", font=("Arial", 12)).pack(pady=5)
    Label(film_window, text=f"Szabad helyek: {szabad_helyek} fő", font=("Arial", 12)).pack(pady=5)

    if foglaltsagi_szint <= 40:
        szin = "success"  
    elif foglaltsagi_szint < 90:
        szin = "warning"  
    else:
        szin = "danger"  

    meter = Meter(
        film_window,
        bootstyle=szin,
        subtext="Foglaltság",
        interactive=False,
        textright="%",
        amounttotal=100,
        amountused=foglaltsagi_szint,
    )
    meter.pack(pady=10)

root = tb.Window(themename="darkly")
root.title("Jegyfoglaló Rendszer")
root.geometry("800x600")

Label(root, text="Válassz filmet:", font=("Arial", 16)).pack(pady=10)

film_lista = tb.Treeview(root, columns=("terem", "cim", "helyek"), show="headings")
film_lista.heading("terem", text="Terem")
film_lista.heading("cim", text="Film címe")
film_lista.heading("helyek", text="Szabad helyek")
film_lista.pack(fill=BOTH, expand=True, padx=10, pady=10)

film_lista.bind("<Double-1>", show_film_details) 

create_database()
load_films()

root.mainloop()
