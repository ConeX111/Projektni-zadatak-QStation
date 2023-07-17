import sqlite3
from sqlite3 import Error


class Ispiti():
    def __init__(self, id_ispita, id_studenta, id_predmeta, datum_ispita):
        self.id_ispita = id_ispita
        self.id_studenta = id_studenta
        self.id_predmeta = id_predmeta
        self.datum_ispita = datum_ispita

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
def create_ispiti(conn, ispiti):
    try:
        sql = """INSERT INTO Ispiti (ID, IDStudenta, IDPredmeta, DatumIspita) VALUES(?,?,?,?)"""
        cur = conn.cursor()
        params = (ispiti.id_ispita, ispiti.id_studenta, ispiti.id_predmeta, ispiti.datum_ispita)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def update_ispiti(conn, ispiti):
    try:
        sql = """UPDATE Ispiti SET ID=?, IDPredmeta=?, DatumIspita=? WHERE IDStudenta=?"""
        cur = conn.cursor()
        params = (ispiti.id_ispita, ispiti.id_studenta, ispiti.id_predmeta, ispiti.datum_ispita)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def select_ime_studenta(conn, IDStudenta):
    try:
        cur = conn.cursor()
        cur.execute("SELECT Ime FROM Studenti WHERE IDStudenta=?", (id_studenta,))
        ime = cur.fetchone()[0]
        return ime
    except Error as e:
        print(e)

def select_all_ispiti(conn):
    sql = """SELECT * FROM Ispiti;"""
    cur = conn.cursor()
    cur.execute(sql)
    ans = cur.fetchall()
    return ans

def select_studenti_ispiti(conn, id_studenta):
    try:
        sql = """SELECT * FROM Ispiti WHERE IDStudenta = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_studenta,))
        ans = cur.fetchone()
        return ans
    except Error as e:
        print(e)

def delete_studenti_ispiti(con, id_studenta):
    try:
        sql = """DELETE FROM Ispiti WHERE IDStudenta = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_studenta,))
        conn.commit()
    except Error as e:
        print(e)

conn = create_connection("studenti.db")
if conn is not None:
    while True:
        izbor = int(input("Unesite 0 za kraj programa ISPITI, 1 za novi unos ISPITA, 2 za azuriranje ISPITA, 3 za brisanje podataka o ISPITU: "))
        if izbor == 0:
            break
        elif izbor == 1:
            id_ispita = int(input("Unesite ID ispita:"))
            id_studenta = int(input("Unesite ID studenta:"))
            id_predmeta = int(input("Unesite ID predmeta:"))
            datum_ispita = float(input("Unesite datum ispita:"))
            i = Ispiti(id_ispita, id_studenta, id_predmeta, datum_ispita)
            create_ispiti(conn, i)
            ime_studenta = select_ime_studenta(conn, id_studenta)
            print(f"Informacije o ispitima za studenta {ime_studenta} uspjesno sacuvane u bazu")

        elif izbor == 2:
            id_studenta = int(input("Unesite ID studenta kojem zelite promijeniti Ispit: "))

            ispiti = None
            ans = select_all_ispiti(conn)
            for a in ans:
                if a[1] == id_studenta:
                    ispiti = Ispiti(a[0], a[1], a[2], a[3])
                    break

            if ispiti is not None:
                print("Unesite nove podatke o ISPITIMA")
                id_ispita = int(input("ID ispita:"))
                id_studenta = int(input("ID studenta:"))
                id_predmeta = int(input("ID predmeta:"))
                datum_ispita = float(input("Datum ispita:"))

                if id_ispita:
                    ispiti.id_ispita = id_ispita
                if id_studenta:
                    ispiti.id_studenta = id_studenta
                if id_predmeta:
                    ispiti.id_predmeta = id_predmeta
                if datum_ispita:
                    ispiti.datum_ispita = datum_ispita
                update_ispiti(conn, ispiti)
                print("Uspjesno azurirani podaci")
            else:
                print("Student sa tim ID-em ne postoji")

        elif izbor == 3:
            id_studenta = int(input("Unesite ID studenta kojem zelite obrisati podatke o ISPITIMA:"))
            studenti = select_studenti_ispiti(conn, id_studenta)
            if studenti is not None:
                delete_studenti_ispiti(conn, id_studenta)
                print("Ispiti studenta su obrisani")
            else:
                print("Student sa tim ID-em ne postoji u bazi")
else:
    print("Error! Cannot create the database connection.")