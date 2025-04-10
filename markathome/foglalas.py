from tkinter import Toplevel, Label, Entry, Button, messagebox, StringVar, OptionMenu
import sqlite3
from pdfgen import general_pdf

def foglalas_ablak(terem_szam):
    ablak = Toplevel()
    ablak.title("📝 Jegyfoglalás")

    Label(ablak, text="Vezetéknév:").grid(row=0, column=0, pady=5, padx=5)
    vnev_entry = Entry(ablak)
    vnev_entry.grid(row=0, column=1)

    Label(ablak, text="Keresztnév:").grid(row=1, column=0, pady=5)
    knev_entry = Entry(ablak)
    knev_entry.grid(row=1, column=1)

    Label(ablak, text="Jegytípus:").grid(row=2, column=0, pady=5)
    jegytipus_var = StringVar(ablak)
    jegytipus_var.set("felnőtt")
    OptionMenu(ablak, jegytipus_var, "felnőtt", "diák", "nyugdíjas").grid(row=2, column=1)

    Label(ablak, text="Székszám(ok) vesszővel:").grid(row=3, column=0, pady=5)
    szek_entry = Entry(ablak)
    szek_entry.grid(row=3, column=1)

    def mentes():
        vnev = vnev_entry.get().strip()
        knev = knev_entry.get().strip()
        jegytipus = jegytipus_var.get()
        szek_input = szek_entry.get().strip()

        if not vnev or not knev or not szek_input:
            messagebox.showerror("Hiba", "Minden mezőt ki kell tölteni!")
            return

        try:
            szekek = [int(s.strip()) for s in szek_input.split(",")]
        except:
            messagebox.showerror("Hiba", "Hibás székszám formátum!")
            return

        conn = sqlite3.connect("mozi.db")
        c = conn.cursor()

        # Kapacitás lekérdezés
        c.execute("SELECT kapacitas, film_cim FROM termek WHERE terem_szam=?", (terem_szam,))
        eredmeny = c.fetchone()
        if not eredmeny:
            messagebox.showerror("Hiba", "Nem található a terem!")
            return

        kapacitas, film_cim = eredmeny

        # Foglalt székek lekérése
        c.execute("SELECT szek_szam FROM foglalasok WHERE terem_szam=?", (terem_szam,))
        foglalt_szekek = {row[0] for row in c.fetchall()}

        # Ellenőrzés
        for szek in szekek:
            if szek in foglalt_szekek:
                messagebox.showerror("Hiba", f"A {szek}. szék már foglalt.")
                return
            if szek < 1 or szek > kapacitas:
                messagebox.showerror("Hiba", f"A {szek}. szék nem létezik.")
                return

        # Foglalás
        for szek in szekek:
            c.execute('''
                INSERT INTO foglalasok (keresztnev, vezeteknev, terem_szam, szek_szam, jegytipus)
                VALUES (?, ?, ?, ?, ?)
            ''', (knev, vnev, terem_szam, szek, jegytipus))

        conn.commit()
        conn.close()

        general_pdf(f"{vnev} {knev}", film_cim, terem_szam, szekek, jegytipus)
        messagebox.showinfo("Siker", "Foglalás sikeres! PDF jegy elkészült.")
        ablak.destroy()

    Button(ablak, text="Foglalás mentése", command=mentes).grid(row=4, column=0, columnspan=2, pady=10)
