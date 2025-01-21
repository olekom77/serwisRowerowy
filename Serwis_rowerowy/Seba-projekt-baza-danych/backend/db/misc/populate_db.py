import psycopg2
from psycopg2 import sql
import os
from urllib.parse import urlparse

# Dane przykładowe, uruchamiane tylko raz, można uruchomić skrypt ponownie w przypadku losowego usunięcia danych

def run():
    # Połączenie z bazą danych
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        result = urlparse(database_url)
        conn = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
    else:
        raise ValueError("DATABASE_URL environment variable not set")

    # Utworzenie kursora
    cur = conn.cursor()
    cur.execute("SET search_path TO sklep;")

    # Resetowanie sekwencji
    def reset_sequence(table_name, sequence_name):
        cur.execute(sql.SQL("SELECT setval(pg_get_serial_sequence(%s, %s), coalesce(max({}), 1), false) FROM {}").format(sql.Identifier(sequence_name), sql.Identifier(table_name)),
                    [table_name, sequence_name])

    reset_sequence('klienci', 'id_klienta')
    reset_sequence('uslugi', 'id_uslugi')
    reset_sequence('pracownicy', 'id_pracownika')
    reset_sequence('rowery', 'id_rowera')
    reset_sequence('zlecenia', 'id_zlecenia')

    # Dane przykładowe
    klienci = [
        ('Jan', 'Kowalski', '123456789', 'jan.kowalski@example.com'),
        ('Anna', 'Nowak', '987654321', 'anna.nowak@example.com'),
        ('Piotr', 'Zieliński', '111222333', 'piotr.zielinski@example.com'),
        ('Katarzyna', 'Wiśniewska', '444555666', 'katarzyna.wisniewska@example.com'),
        ('Marek', 'Kowalczyk', '777888999', 'marek.kowalczyk@example.com'),
        ('Agnieszka', 'Nowicka', '000111222', 'agnieszka.nowicka@example.com'),
        ('Tomasz', 'Lewandowski', '333444555', 'tomasz.lewandowski@example.com')
    ]

    uslugi = [
        (100.00, 'Serwis roweru', 'Pełny serwis roweru'),
        (50.00, 'Wymiana opony', 'Wymiana przedniej opony'),
        (75.00, 'Regulacja hamulców', 'Regulacja przednich i tylnych hamulców'),
        (120.00, 'Wymiana łańcucha', 'Wymiana łańcucha na nowy'),
        (200.00, 'Naprawa przerzutek', 'Naprawa przednich i tylnych przerzutek'),
        (150.00, 'Naprawa amortyzatora', 'Naprawa przedniego amortyzatora'),
        (80.00, 'Wymiana pedałów', 'Wymiana pedałów na nowe'),
        (60.00, 'Czyszczenie napędu', 'Kompleksowe czyszczenie napędu'),
        (90.00, 'Wymiana klocków hamulcowych', 'Wymiana przednich i tylnych klocków hamulcowych'),
        (110.00, 'Centrowanie kół', 'Centrowanie przedniego i tylnego koła'),
        (130.00, 'Wymiana suportu', 'Wymiana suportu na nowy'),
        (140.00, 'Naprawa piasty', 'Naprawa przedniej lub tylnej piasty'),
        (70.00, 'Wymiana linek przerzutek', 'Wymiana linek przednich i tylnych przerzutek'),
        (85.00, 'Wymiana linek hamulcowych', 'Wymiana linek przednich i tylnych hamulców'),
        (95.00, 'Regulacja przerzutek', 'Regulacja przednich i tylnych przerzutek')
    ]

    pracownicy = [
        ('Mechanik', 'Piotr', 'Zieliński', 3000.00, '123123123'),
        ('Sprzedawca', 'Katarzyna', 'Wiśniewska', 2500.00, '321321321'),
        ('Mechanik', 'Marek', 'Kowalczyk', 3200.00, '456456456'),
        ('Mechanik', 'Agnieszka', 'Nowicka', 2600.00, '654654654'),
        ('Kierownik', 'Tomasz', 'Lewandowski', 4000.00, '789789789'),
        ('Magazynier', 'Paweł', 'Wójcik', 2800.00, '987987987'),
        ('Księgowość', 'Ewa', 'Kaczmarek', 3500.00, '123321123')
    ]

    rowery = [
        ('Górski', 'Trek', 'X-Caliber', 1),
        ('Miejski', 'Giant', 'Escape', 2),
        ('Szosa', 'Specialized', 'Allez', 3),
        ('Gravel', 'Cannondale', 'Topstone', 4),
        ('Elektryczny', 'Cube', 'Reaction Hybrid', 5),
        ('Fatbike', 'Norco', 'Bigfoot', 6),
        ('MTB', 'Scott', 'Spark', 7),
        ('Trekkingowy', 'Merida', 'Crossway', 2),
        ('BMX', 'Haro', 'Freestyler', 3)
    ]

    zlecenia = [
        (1, 1, '2023-01-01', 'Zgłoszone', 1),
        (2, 2, '2023-01-02', 'Przyjęte do realizacji', 3),
        (3, 3, '2023-01-03', 'W trakcie realizacji', 3),
        (4, 4, '2023-01-04', 'W trakcie realizacji - opłacono', 4),
        (5, 5, '2023-01-05', 'Zrealizowano - do opłacenia', 1),
        (6, 6, '2023-01-06', 'Zrealizowano - opłacone', 1),
        (7, 7, '2023-01-07', 'Zrealizowano - nieopłacone', 3),
        (8, 8, '2023-01-08', 'Anulowane', 1),
        (9, 9, '2023-01-09', 'Zgłoszone', 3),
        (1, 10, '2023-01-10', 'Przyjęte do realizacji', 3),
        (2, 11, '2023-01-11', 'W trakcie realizacji', 4),
        (3, 12, '2023-01-12', 'W trakcie realizacji - opłacono', 1)
    ]

    # Wstawianie danych do tabel
    cur.executemany(
        sql.SQL("INSERT INTO klienci (imie, nazwisko, numer_telefonu, email) VALUES (%s, %s, %s, %s)"),
        klienci
    )

    cur.executemany(
        sql.SQL("INSERT INTO uslugi (cena, nazwa, opis) VALUES (%s, %s, %s)"),
        uslugi
    )

    cur.executemany(
        sql.SQL("INSERT INTO pracownicy (stanowisko, imie, nazwisko, wynagrodzenie, numer_telefonu) VALUES (%s, %s, %s, %s, %s)"),
        pracownicy
    )

    cur.executemany(
        sql.SQL("INSERT INTO rowery (typ_roweru, marka, model, klient_id) VALUES (%s, %s, %s, %s)"),
        rowery
    )

    cur.executemany(
        sql.SQL("INSERT INTO zlecenia (rower, usluga, data_zlecenia, status, wykonawca) VALUES (%s, %s, %s, %s, %s)"),
        zlecenia
    )

    # Zatwierdzenie zmian
    conn.commit()

    # Zamknięcie połączenia
    cur.close()
    conn.close()