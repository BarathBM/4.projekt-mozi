import sqlite3

conn = sqlite3.connect("mozi.db")
c = conn.cursor()

# Termek
c.execute('''
CREATE TABLE IF NOT EXISTS termek (
    terem_szam INTEGER PRIMARY KEY,
    film_cim TEXT,
    ev INTEGER,
    mufaj TEXT,
    jatekido INTEGER,
    kapacitas INTEGER
)
''')

# Foglalasok
c.execute('''
CREATE TABLE IF NOT EXISTS foglalasok (
    foglalas_id INTEGER PRIMARY KEY AUTOINCREMENT,
    keresztnev TEXT,
    vezeteknev TEXT,
    terem_szam INTEGER,
    szek_szam INTEGER,
    jegytipus TEXT,
    FOREIGN KEY (terem_szam) REFERENCES termek (terem_szam)
)
''')

# Minta adatok (csak első futáskor)
c.execute("SELECT COUNT(*) FROM termek")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO termek VALUES (1, 'Oppenheimer', 2023, 'Dráma', 180, 100)")
    c.execute("INSERT INTO termek VALUES (2, 'Dűne 2', 2024, 'Sci-fi', 165, 80)")

conn.commit()
conn.close()
