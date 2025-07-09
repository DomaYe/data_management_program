import cx_Oracle
from generator import generate_data, Person, Pet, Occupation
import os
from dotenv import load_dotenv

# Oracle Instant Client inicializálása
load_dotenv()  # .env fájl betöltése, ha létezik

# Oracle Instant Client inicializálása környezeti változó alapján
oracle_ic_path = os.getenv("ORACLE_IC_PATH")
if oracle_ic_path:
    cx_Oracle.init_oracle_client(lib_dir=os.path.expanduser(oracle_ic_path))
else:
    # Ha nincs megadva, az alapértelmezett rendszerbeállításokra hagyatkozunk
    print("Figyelmeztetés: ORACLE_IC_PATH nincs beállítva, alapértelmezett kliens elérési út lesz használva.")

# Oracle SQL kapcsolódás
def get_oracle_connection():
    # Kapcsolati adatok betöltése környezeti változókból
    hostname = os.getenv("ORACLE_HOST")
    port = os.getenv("ORACLE_PORT", "1521")
    service_name = os.getenv("ORACLE_SERVICE_NAME")
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")

    dsn = f"{hostname}:{port}/{service_name}"

    try:
        connection = cx_Oracle.connect(
            user=user,
            password=password,
            dsn=dsn
        )
        print("Sikeresen csatlakozott az Oracle adatbázishoz.")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Adatbázis hiba: {error.message}")
        return None

# Táblák létrehozása
def create_tables(connection):
    cursor = connection.cursor()
    try:
        # Táblák törlése, ha már léteznek
        for table in ["Occupations", "Services", "Pets", "Persons"]:
            try:
                cursor.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
                print(f"{table} tábla törölve.")
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                if error.code != 942:  # ORA-00942: table or view does not exist
                    print(f"{table} tábla törlése hiba: {error.message}")

        # Táblák létrehozása
        cursor.execute("""
            CREATE TABLE Persons (
                person_id NUMBER PRIMARY KEY,
                full_name VARCHAR2(100),
                address VARCHAR2(255)
            )
        """)
        print("Persons tábla létrehozva.")

        cursor.execute("""
            CREATE TABLE Pets (
                pet_id VARCHAR2(50) PRIMARY KEY,
                owner_id NUMBER,
                pet_name VARCHAR2(100),
                species VARCHAR2(50),
                FOREIGN KEY (owner_id) REFERENCES Persons(person_id)
            )
        """)
        print("Pets tábla létrehozva.")

        cursor.execute("""
            CREATE TABLE Occupations (
                occupation_id VARCHAR2(50) PRIMARY KEY,
                person_id NUMBER,
                occupation VARCHAR2(100),
                company VARCHAR2(100),
                FOREIGN KEY (person_id) REFERENCES Persons(person_id)
            )
        """)
        print("Occupations tábla létrehozva.")

        connection.commit()
        print("Táblák létrehozva.")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Táblalétrehozási hiba: {error.message}")
    finally:
        cursor.close()

# Adatok beszúrása
def insert_data(connection, persons, pets, occupations):
    cursor = connection.cursor()
    try:
        # Adatok beszúrása Persons táblába
        for person in persons:
            cursor.execute("""
                INSERT INTO Persons (person_id, full_name, address)
                VALUES (:1, :2, :3)
            """, (person.person_id, person.full_name, person.address))

        # Adatok beszúrása Pets táblába
        for pet in pets:
            cursor.execute("""
                INSERT INTO Pets (pet_id, owner_id, pet_name, species)
                VALUES (:1, :2, :3, :4)
            """, (pet.pet_id, pet.owner_id, pet.pet_name, pet.species))

        # Adatok beszúrása Occupations táblába
        for occupation in occupations:
            cursor.execute("""
                INSERT INTO Occupations (occupation_id, person_id, occupation, company)
                VALUES (:1, :2, :3, :4)
            """, (occupation.occupation_id, occupation.person_id, occupation.occupation, occupation.company))

        connection.commit()
        print("Adatok beszúrva.")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Adatbeszúrási hiba: {error.message}")
    finally:
        cursor.close()

# Fő futtatás
if __name__ == "__main__":
    # Generálj adatokat
    persons, pets, occupations = generate_data(10)

    # Kapcsolódás az Oracle adatbázishoz
    conn = get_oracle_connection()
    if conn:
        create_tables(conn)
        insert_data(conn, persons, pets, occupations)
        conn.close()
        print("Kapcsolat lezárva.")
