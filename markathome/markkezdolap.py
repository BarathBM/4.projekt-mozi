from tkinter import *
from ttkbootstrap import Style
import sqlite3
from film_info import megjelenit_film_ablak

style = Style(theme="cyborg")
root = style.master
root.title("🎬 Mozi Jegyfoglaló Rendszer")
root.geometry("600x400")

Label(root, text="Elérhető filmek", font=("Helvetica", 18)).pack(pady=10)

conn = sqlite3.connect("mozi.db")
c = conn.cursor()
c.execute("SELECT terem_szam, film_cim FROM termek")
filmek = c.fetchall()
conn.close()

for terem_szam, cim in filmek:
    Button(root, text=f"{cim} (Terem {terem_szam})", 
           command=lambda tsz=terem_szam: megjelenit_film_ablak(tsz),
           width=30).pack(pady=5)

root.mainloop()
