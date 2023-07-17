import sqlite3
from sqlite3 import Error

class Studenti():
    def __init__(self,  id_studenta, ime, prezime, broj_indeksa, godina_studija):
        self.id_studenta = id_studenta
        self.ime = ime
        self.prezime = prezime
        self.broj_indeksa = broj_indeksa
        self.godina_studija = godina_studija


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

#Dodaje novog studenta u tabelu Studenti
def create_studenti(conn, studenti):
    try:
        sql = """INSERT INTO Studenti (IDStudenta, Ime, Prezime, BrojIndeksa, GodinaStudija) VALUES(?,?,?,?,?)"""
        cur = conn.cursor()
        params = (studenti.id_studenta, studenti.ime, studenti.prezime, studenti.broj_indeksa, studenti.godina_studija)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def update_studenti(conn, studenti):
    try:
        sql = f"""UPDATE Studenti SET Ime = ?, Prezime = ?,
        GodinaStudija = ?, BrojIndeksa = ? WHERE IDStudenta = ?"""
        cur = conn.cursor()
        params = (studenti.ime, studenti.prezime, studenti.godina_studija, studenti.broj_indeksa, studenti.id_studenta)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def delete_studenti(con, id_studenta):
    try:
        sql = """DELETE FROM Studenti WHERE IDStudenta = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_studenta,))
        conn.commit()
    except Error as e:
        print(e)
def select_all_studenti(conn):
        sql = """SELECT * FROM Studenti;"""
        cur = conn.cursor()
        cur.execute(sql)
        ans = cur.fetchall()
        return ans
def select_studenti(conn, id_studenta):
    try:
        sql = """SELECT * FROM Studenti WHERE IDStudenta = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_studenta,))
        ans = cur.fetchone()
        return ans
    except Error as e:
        print(e)

conn = create_connection("studenti.db")
if conn is not None:
    while True:
        izbor = int(input("Unesite 0 za kraj programa STUDENTI, 1 za unos novog STUDENTA, 2 za azuriranje STUDENTA, 3 za brisanje STUDENTA  :"))

        if izbor == 0:
            break
        #Unosenje novog Studenta u tabelu Studenti
        elif izbor == 1:
            id_studenta = int(input("Unesite ID studenta:"))
            ime_studenta = input("Unesite ime studenta:")
            prezime_studenta = input("Unesite prezime studenta:")
            broj_indeksa = input("Unesite broj indeksa studenta:")
            godina_studija = input("Unesite godinu studija studenta:")
            s = Studenti(id_studenta, ime_studenta, prezime_studenta,
                          broj_indeksa, godina_studija)
            create_studenti(conn, s)
            print("Student je uspjesno dodan u bazu")

        #Azuriranje podataka studenta
        elif izbor == 2:
            id_studenta = int(input("Unesite ID studenta kojeg zelite da azurirate: "))

            studenti = None
            ans = select_all_studenti(conn)
            for a in ans:
                if a[0] == id_studenta:
                    studenti = Studenti(a[0], a[1], a[2], a[3], a[4])
                    break

            if studenti is not None:

                print("Unesite nove podatke o studentu:")
                ime_studenta = input("Ime (ostavite prazno ako ne želite da mijenjate):")
                prezime_studenta = input("Prezime (ostavite prazno ako ne želite da mijenjate):")
                godina_studija = input("Godina studija (ostavite prazno ako ne želite da mijenjate):")
                broj_indeksa = input("Broj indeksa (ostavite prazno ako ne želite da mijenjate):")

                if ime_studenta:
                    studenti.ime = ime_studenta
                if prezime_studenta:
                    studenti.prezime = prezime_studenta
                if broj_indeksa:
                    studenti.broj_indeksa = broj_indeksa
                if godina_studija:
                    studenti.godina_studija = godina_studija

                update_studenti(conn, studenti)
                print("Podaci o studentu su ažurirani.")
            else:
                print("Student sa unijeti ID-em ne postoji.")

        # Brisanje studenta iz tabele
        elif izbor == 3:
            id_studenta = int(input("Unesite ID studenta kojeg zelite da obrisete:"))
            studenti = select_studenti(conn, id_studenta)
            if studenti is not None:
                delete_studenti(conn, id_studenta)
                print("Student je obrisan")
            else:
                print("Student sa tim ID-em ne postoji u bazi")
else:
    print("Error! Cannot create the database connection.")
