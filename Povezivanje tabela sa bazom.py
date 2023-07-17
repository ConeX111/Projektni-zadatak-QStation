import sqlite3


conn = sqlite3.connect("studenti.db")


cursor = conn.cursor()

# Kreiranje tabele "Studenti"
cursor.execute("""CREATE TABLE Studenti (
               IDStudenta INTEGER PRIMARY KEY,
               Ime CHAR(15), 
               Prezime CHAR(15),  
               BrojIndeksa INTEGER, 
               GodinaStudija INTEGER)""")


cursor.execute("""CREATE TABLE Predmeti (
                ID INTEGER PRIMARY KEY, 
                IDPredmeta INTEGER, 
                NazivPredmeta TEXT, 
                Profesor TEXT, 
                IDStudenta INTEGER,
                FOREIGN KEY (IDStudenta) REFERENCES Studenti(IDStudenta))""")

# Kreiranje tabele "Ispiti"
cursor.execute("""CREATE TABLE Ispiti (
                ID INTEGER PRIMARY KEY, 
                IDStudenta INTEGER, 
                IDPredmeta INTEGER, 
                DatumIspita DATE, 
                FOREIGN KEY (IDStudenta) REFERENCES Studenti(IDStudenta))""")

# Kreiranje tabele "Ocjene"
cursor.execute("""CREATE TABLE Ocjena (
                ID INTEGER PRIMARY KEY, 
                IDStudenta INTEGER, 
                IDOcjene INTEGER, 
                IDPredmeta INTEGER,
                Ocjenaa INTEGER, 
                FOREIGN KEY (IDStudenta) REFERENCES Studenti(IDStudenta))""")



conn.commit()

conn.close()