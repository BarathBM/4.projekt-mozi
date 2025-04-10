from tkinter import Toplevel, Label, Button
from ttkbootstrap.widgets import Meter
import sqlite3
from foglalas import foglalas_ablak

def megjelenit_film_ablak(terem_szam):
    ablak = Toplevel()
    ablak.title("Film információk és foglalás")

    conn = sqlite3.connect("mozi.db")
    c = conn.cursor()

    c.execute("SELECT film_cim, ev, mufaj, jatekido, kapacitas FROM termek WHERE terem_szam=?", (terem_szam,))
    film = c.fetchone()

    c.execute("SELECT COUNT(*) FROM foglalasok WHERE terem_szam=?", (terem_szam,))
    foglalt = c.fetchone()[0]

    cim, ev, mufaj, jatekido, kapacitas = film
    szabad = kapacitas - foglalt
    szazalek = int((foglalt / kapacitas) * 100) if kapacitas else 0
    szin = "success" if szazalek < 40 else "warning" if szazalek < 90 else "danger"

    Label(ablak, text=f"{cim} ({ev})", font=("Helvetica", 14)).pack()
    Label(ablak, text=f"Műfaj: {mufaj}, Játékidő: {jatekido} perc").pack()
    Label(ablak, text=f"Szabad helyek: {szabad} / {kapacitas}").pack(pady=10)

    Meter(ablak, amountused=szazalek, amounttotal=100, bootstyle=szin, 
          metertype="full", subtext="Foglaltság").pack(pady=10)

    Button(ablak, text="Foglalás indítása", command=lambda: foglalas_ablak(terem_szam)).pack(pady=10)

    conn.close()
