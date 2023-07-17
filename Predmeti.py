import sqlite3
from sqlite3 import Error


class Predmeti():
    def __init__(self, id_studenta, id_predmeta, naziv_predmeta, profesor):
        self.id_studenta = id_studenta
        self.id_predmeta = id_predmeta
        self.naziv_predmeta = naziv_predmeta
        self.profesor = profesor

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
def create_predmet(conn, predmet):
    try:
        sql = """INSERT INTO Predmeti (ID, NazivPredmeta, Profesor, IDStudenta) VALUES(?,?,?,?)"""

        cur = conn.cursor()
        params = (predmet.id_predmeta, predmet.naziv_predmeta, predmet.profesor, predmet.id_studenta)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def update_predmet(conn, predmet):
    try:
        sql = """UPDATE Predmeti SET ID=?, NazivPredmeta=?, Profesor=? WHERE IDStudenta=?"""

        cur = conn.cursor()
        params = (predmet.id_predmeta, predmet.naziv_predmeta, predmet.profesor, predmet.id_studenta)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def select_ime_studenta(conn, IDStudenta):
    try:
        cur = conn.cursor()
        cur.execute("SELECT Ime FROM Studenti WHERE IDStudenta=?", (IDStudenta,))

        ime = cur.fetchone()[0]
        return ime
    except Error as e:
        print(e)
def select_all_predmet():
    conn = create_connection("studenti.db")
    sql = """SELECT * FROM Predmeti;"""
    cur = conn.cursor()
    cur.execute(sql)
    ans = cur.fetchall()
    conn.close()
    return ans

def select_student_predmet(conn, id_studenta):
    try:
        sql = """SELECT * FROM Predmeti WHERE IDStudenta = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_studenta,))
        ans = cur.fetchone()
        return ans
    except Error as e:
        print(e)

def delete_student_predmet(conn, id_studenta):
    try:
        sql = """DELETE FROM Predmeti WHERE IDStudenta = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_studenta,))
        conn.commit()
    except Error as e:
        print(e)


conn = create_connection("studenti.db")
if conn is not None:
    while True:
        izbor = int(input("Unesite 0 za kraj programa Predmeti, 1 za novi unos PREDMETA, 2 za azuriranje PREDMETA, 3 za brisanje PREDMETA: "))
        if izbor == 0:
            break
        elif izbor == 1:
            id_studenta = int(input("Unesite ID studenta:"))
            id_predmeta = int(input("Unesite ID predmeta:"))
            naziv_predmeta = input("Unesite naziv predmeta:")
            profesor = input("Unesite ime profesora:")
            p = Predmeti(id_studenta, id_predmeta, naziv_predmeta, profesor)
            create_predmet(conn, p)

            ime_studenta = select_ime_studenta(conn, id_studenta)
            print(f"Informacije o predmetu studenta {ime_studenta} uspjesno sacuvane u bazu")

        elif izbor == 2:
            id_studenta = int(input("Unesite ID studenta kojem zelite promijeniti predmet: "))

            predmet = None
            ans = select_all_predmet()
            for a in ans:
                if a[2] == id_studenta:
                    predmet = Predmeti(a[0], a[1], a[2], a[3])
                    break

            if predmet is not None:
                print("Unesite nove podatke predmetu studenta")
                id_predmeta = int(input("ID predmeta:"))
                naziv_predmeta = input("Naziv predmeta:")
                profesor = input("Ime profesora:")

                if id_predmeta:
                    predmet.id_predmeta = id_predmeta
                if naziv_predmeta:
                    predmet.naziv_predmeta = naziv_predmeta
                if profesor:
                    predmet.profesor = profesor
                update_predmet(conn, predmet)
                print("Uspjesno azurirani podaci")
            else:
                print("Student sa tim ID-em ne postoji")

        elif izbor == 3:
            id_studenta = int(input("Unesite ID studenta kojem zelite obrisati podatke o PREDMETU:"))
            predmeti = select_all_predmet()
            if predmeti is not None:
                delete_student_predmet(conn, id_studenta)
                print("Predmet je obrisan")
            else:
                print("Student sa tim ID-em ne postoji u bazi")
else:
    print("Error! Cannot create the database connection.")
