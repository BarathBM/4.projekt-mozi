import sqlite3
#Adatbázis létrehozása: egyszer kell lefuttatni!
#1. lépés: kapcsolódás adatbázishoz (sqlite3)
conn = sqlite3.connect("sample_db.db")

#2. lépés: Létrehozunk egy úgynevezett "kurzort". Ez a kurzor felelős azért, hogy a parancsainkat az sqlite feldolgozza és végrehajtsa
c = conn.cursor()

#3. lépés: végrehajtjuk a parancsot (itt tábla létrehozása először az attribútum nevével, majd a típusával)
c.execute(""" CREATE TABLE termek (
    Teremszám integer,
    Filmcím text,
    Műfaj text,
    Helyekszáma integer,
    Szabadhelyek integer,
    Idotartam time,
    Férőhelyek integer,
    Vetiteskezd time,
 )""")

c.execute(""" CREATE TABLE foglalasok(
    Teremszám integer,
    Filmcím text,
    Műfaj text,
    Szekszáma integer,
    Idotartam time,
    
 )""")


conn.commit()


conn.close()