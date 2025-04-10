import sqlite3
import ttkbootstrap as tb
from tkinter import Toplevel, Label, Button, Entry, OptionMenu, StringVar
from ttkbootstrap.widgets import Progressbar
from fpdf import FPDF

root = tb.Window(themename="darkly")
root.title("Adatbázis létrehozása")
root.geometry("800x600")

# Adatbázis létrehozása és inicializálása
def create_database():
    conn = sqlite3.connect("mozi.db")
    cursor = conn.cursor()

    # Táblák létrehozása (ha még nem léteznek)
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
        jegytipus TEXT,
        FOREIGN KEY (terem_szam) REFERENCES Termek(terem_szam)
    )
    """)

    # Filmek hozzáadása, ha még nem léteznek
    filmek = [
        (1, "Dűne: Második rész", "Sci-Fi", 2024, 165, 100),
        (2, "Oppenheimer", "Dráma", 2023, 180, 80),
        (3, "Avatar 2", "Akció", 2022, 192, 120),
        (4, "Interstellar", "Sci-Fi", 2014, 169, 120),
        (5, "A Hobbit: Váratlan utazás", "Fantasy", 2012, 169, 150),
        (6, "Star Wars: Az ébredő Erő", "Akció", 2015, 138, 200),
        (7, "Inception", "Sci-Fi", 2010, 148, 130),
        (8, "The Dark Knight", "Akció", 2008, 152, 180),
        (9, "Forrest Gump", "Dráma", 1994, 142, 100),
        (10, "Pulp Fiction", "Krimi", 1994, 154, 110),
        (11, "The Matrix", "Sci-Fi", 1999, 136, 150),
        (12, "The Lord of the Rings: The Return of the King", "Fantasy", 2003, 201, 250),
    ]

    for film in filmek:
        cursor.execute("SELECT COUNT(*) FROM Termek WHERE terem_szam=?", (film[0],))
        if cursor.fetchone()[0] == 0:  # Ha nem létezik már a terem_szam
            cursor.execute("INSERT INTO Termek VALUES (?, ?, ?, ?, ?, ?)", film)
    
    conn.commit()
    conn.close()


# Filmek listája és jegyfoglalás
def Filmlist():
    window = Toplevel(root)
    window.title("Filmek és foglalások")
    
    conn = sqlite3.connect("mozi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Termek")
    films = cursor.fetchall()

    for i, film in enumerate(films):
        film_title = film[1]
        seat_button = Button(window, text=f"{film_title} (Kattints a jegyfoglaláshoz)", command=lambda f=film: open_booking(f), font=("Arial", 16), bg="black", fg="white")
        seat_button.grid(row=i, column=0, padx=20, pady=10)
    
    conn.close()

# Jegyfoglalás
def open_booking(film):
    window = Toplevel(root)
    window.title(f"{film[1]} - Jegyfoglalás")

    # Film adatai
    Label(window, text=f"Film: {film[1]}", font=("Arial", 14)).pack(pady=10)
    Label(window, text=f"Műfaj: {film[2]}", font=("Arial", 12)).pack(pady=5)
    Label(window, text=f"Évszám: {film[3]}", font=("Arial", 12)).pack(pady=5)
    Label(window, text=f"Játékidő: {film[4]} perc", font=("Arial", 12)).pack(pady=5)
    
    # Foglalás
    Label(window, text="Keresztnév: ", font=("Arial", 12)).pack(pady=5)
    first_name_entry = Entry(window, font=("Arial", 12))
    first_name_entry.pack(pady=5)

    Label(window, text="Vezetéknév: ", font=("Arial", 12)).pack(pady=5)
    last_name_entry = Entry(window, font=("Arial", 12))
    last_name_entry.pack(pady=5)

    Label(window, text="Jegytípus: ", font=("Arial", 12)).pack(pady=5)
    ticket_types = ["Felnőtt", "Diák", "Nyugdíjas"]
    ticket_type_var = StringVar(window)
    ticket_type_var.set(ticket_types[0])
    ticket_menu = OptionMenu(window, ticket_type_var, *ticket_types)
    ticket_menu.pack(pady=5)

    # Foglaltság lekérése
    conn = sqlite3.connect("mozi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Foglalasok WHERE terem_szam=?", (film[0],))
    reserved_seats = cursor.fetchone()[0]
    available_seats = film[5] - reserved_seats
    occupancy_percentage = (reserved_seats / film[5]) * 100
    meter = Progressbar(window, maximum=100, value=occupancy_percentage)
    if occupancy_percentage < 40:
        meter.configure(bootstyle="success")
    elif occupancy_percentage < 90:
        meter.configure(bootstyle="warning")
    else:
        meter.configure(bootstyle="danger")
    meter.pack(pady=20)

    # Foglalás rögzítése
    def book_ticket():
        nonlocal available_seats  # Így most már használhatjuk az 'available_seats' változót
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        ticket_type = ticket_type_var.get()

        if available_seats > 0:
            cursor.execute("INSERT INTO Foglalasok (keresztnev, vezeteknev, terem_szam, szek_szam, jegytipus) VALUES (?, ?, ?, ?, ?)",
                           (first_name, last_name, film[0], reserved_seats + 1, ticket_type))
            conn.commit()

            # PDF generálás
            pdf = FPDF()
            pdf.add_page()

            # Alapértelmezett betűtípus beállítása
            pdf.set_font("Arial", size=12)

            # PDF tartalom hozzáadása
            pdf.cell(200, 10, txt=f"Foglalás - {film[1]}", ln=True)
            pdf.cell(200, 10, txt=f"Neved: {replace_special_chars(first_name)} {replace_special_chars(last_name)}", ln=True)
            pdf.cell(200, 10, txt=f"Jegytípus: {ticket_type}", ln=True)
            pdf.cell(200, 10, txt=f"Foglalás száma: {reserved_seats + 1}", ln=True)

            # PDF mentése
            pdf.output(f"{replace_special_chars(first_name)}_{replace_special_chars(last_name)}_jegy.pdf")

            available_seats -= 1  # Csökkentjük a szabad helyek számát
            meter.configure(value=(reserved_seats + 1) / film[5] * 100)

            # Visszajelzés
            Label(window, text="Foglalás sikeres!", font=("Arial", 14), fg="green").pack(pady=10)
        else:
            Label(window, text="Nincs több szabad hely!", font=("Arial", 14), fg="red").pack(pady=10)

    book_button = Button(window, text="Foglalás", command=book_ticket, font=("Arial", 16), width=15, bg="black", fg="white")
    book_button.pack(pady=20)

# Ékezetek eltávolítása vagy helyettesítése
def replace_special_chars(text):
    special_chars = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ö': 'o', 'ő': 'o', 'ú': 'u', 'ü': 'u', 'ű': 'u'}
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)
    return text

# Statikus grafikon készítése
def show_statistics():
    conn = sqlite3.connect("mozi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT terem_szam, COUNT(*) * 100.0 / kapacitas FROM Termek JOIN Foglalasok ON Termek.terem_szam = Foglalasok.terem_szam GROUP BY Termek.terem_szam")
    stats = cursor.fetchall()
    conn.close()

    rooms = [f"Terem {row[0]}" for row in stats]
    occupancy = [row[1] for row in stats]
    
    # A grafikonot itt generálhatod pl. Plotly vagy más eszközzel

create_database()

label = Label(root, text="MigaBiga", font=("Arial", 40))
label.pack(pady=10)

movie_button = Button(root, text="Filmlista", command=Filmlist, font=("Arial",24), width=7, height=2, bg="black", fg="white")
movie_button.pack(pady=5)

stats_button = Button(root, text="Statisztika", command=show_statistics, font=("Arial",24), width=7, height=2, bg="black", fg="white")
stats_button.pack(pady=5)

root.mainloop()
