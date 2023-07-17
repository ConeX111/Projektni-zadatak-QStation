import sqlite3
from sqlite3 import Error

class Ocjena():
    def __init__(self, id_ocjene, id_studenta, id_predmeta, ocjenaa):
        self.id_ocjene = id_ocjene
        self.id_studenta = id_studenta
        self.id_predmeta = id_predmeta
        self.ocjenaa = ocjenaa

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
def create_ocjena(conn, ocjena):
    try:
        sql = """INSERT INTO Ocjena (ID, IDStudenta, IDPredmeta, Ocjenaa) VALUES(?,?,?,?)"""
        cur = conn.cursor()
        params = (ocjena.id_ocjene, ocjena.id_studenta, ocjena.id_predmeta, ocjena.ocjenaa)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def update_ocjena(conn, ocjena):
    try:
        sql = """UPDATE Ocjena SET ID=?, IDPredmeta=?, Ocjenaa=? WHERE IDStudenta=?"""
        cur = conn.cursor()
        params = (ocjena.id_ocjene, ocjena.id_studenta, ocjena.id_predmeta, ocjena.ocjenaa)
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

def select_all_ocjena(conn):
    sql = """SELECT * FROM Ocjena;"""
    cur = conn.cursor()
    cur.execute(sql)
    ans = cur.fetchall()
    return ans

def select_studenti_ocjena(conn, id_studenta):
    try:
        sql = """SELECT * FROM Ocjena WHERE IDStudenta = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_studenta,))
        ans = cur.fetchone()
        return ans
    except Error as e:
        print(e)

def delete_studenti_ocjena(con, id_studenta):
    try:
        sql = """DELETE FROM Ocjena WHERE IDStudenta = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_studenta,))
        conn.commit()
    except Error as e:
        print(e)

conn = create_connection("studenti.db")
if conn is not None:
    while True:
        izbor = int(input("Unesite 0 za kraj programa Ocjena, 1 za novi unos Ocjene, 2 za azuriranje Ocjene, 3 za brisanje podataka o Ocjeni: "))
        if izbor == 0:
            break
        elif izbor == 1:
            id_ocjena = int(input("Unesite ID ocjene:"))
            id_studenta = int(input("Unesite ID studenta:"))
            id_predmeta = int(input("Unesite ID predmeta:"))
            ocjenaa = int(input("Unesite ocjenu:"))
            o = Ocjena(id_ocjena, id_studenta, id_predmeta, ocjenaa )
            create_ocjena(conn, o)
            ime_studenta = select_ime_studenta(conn, id_studenta)
            print(f"Informacije o ocjenama za studenta {ime_studenta} uspjesno sacuvane u bazu")

        elif izbor == 2:
            id_studenta = int(input("Unesite ID studenta kojem zelite promijeniti Ocjenu: "))

            ocjena = None
            ans = select_all_ocjena(conn)
            for a in ans:
                if a[1] == id_studenta:
                    ocjena = Ocjena(a[0], a[1], a[2], a[3])
                    break

            if ocjena is not None:
                id_ocjena = int(input("Unesite ID ocjene:"))
                id_studenta = int(input("Unesite ID studenta:"))
                id_predmeta = int(input("Unesite ID predmeta:"))
                ocjenaa = int(input("Unesite ocjenu:"))

                if id_ocjena:
                    ocjena.id_ocjene = id_ocjena
                if id_studenta:
                    ocjena.id_studenta = id_studenta
                if id_predmeta:
                    ocjena.id_predmeta = id_predmeta
                if ocjenaa:
                    ocjena.ocjenaa = ocjenaa
                update_ocjena(conn, ocjena)
                print("Uspjesno azurirani podaci")
            else:
                print("Student sa tim ID-em ne postoji")

        elif izbor == 3:
            id_studenta = int(input("Unesite ID studenta kojem zelite obrisati podatke o OCJENAMA:"))
            studenti = select_studenti_ocjena(conn, id_studenta)
            if studenti is not None:
                delete_studenti_ocjena(conn, id_studenta)
                print("Ocjene studenta su obrisane")
            else:
                print("Student sa tim ID-em ne postoji u bazi")
else:
    print("Error! Cannot create the database connection.")