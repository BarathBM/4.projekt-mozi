import sqlite3
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import Toplevel, Label, Button, BOTH
from ttkbootstrap.widgets import Meter
from tkinter import *
import subprocess
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
    foglaltsagi_szint = (foglalt_helyek / kapacitas) * 100


    film_window = Toplevel(root)
    film_window.title(f"{cim} - Részletek")
    
    Label(film_window, text=f"Film címe: {cim}", font=("Arial", 14, "bold")).pack(pady=5)
    Label(film_window, text=f"Műfaj: {mufaj}", font=("Arial", 12)).pack(pady=5)
    Label(film_window, text=f"Évszám: {evszam}", font=("Arial", 12)).pack(pady=5)
    Label(film_window, text=f"Játékidő: {jatekido} perc", font=("Arial", 12)).pack(pady=5)
    Label(film_window, text=f"Terem kapacitása: {kapacitas} fő", font=("Arial", 12)).pack(pady=5)
    Label(film_window, text=f"Szabad helyek: {szabad_helyek} fő", font=("Arial", 12)).pack(pady=5)

    szin = "success" if foglaltsagi_szint <= 40 else "warning" if foglaltsagi_szint < 90 else "danger"

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