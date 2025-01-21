import psycopg2
import os
from urllib.parse import urlparse

def create_procedures():
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
    try:
        with conn.cursor() as cursor:
            cursor.execute("SET search_path TO sklep;")
            # Procedura Insert dla ZLECENIA
            cursor.execute("""
            CREATE OR REPLACE FUNCTION sklep.dodaj_zlecenie(
                p_rower INT,
                p_usluga INT,
                p_data_zlecenia DATE,
                p_status VARCHAR(50),
                p_wykonawca INT
            )
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM ROWERY WHERE ID_ROWERA = p_rower) THEN
                    RAISE EXCEPTION 'Rower o ID % nie istnieje.', p_rower;
                END IF;

                IF NOT EXISTS (SELECT 1 FROM USLUGI WHERE ID_USLUGI = p_usluga) THEN
                    RAISE EXCEPTION 'Usługa o ID % nie istnieje.', p_usluga;
                END IF;

                IF NOT EXISTS (SELECT 1 FROM PRACOWNICY WHERE ID_PRACOWNIKA = p_wykonawca) THEN
                    RAISE EXCEPTION 'Pracownik o ID % nie istnieje.', p_wykonawca;
                END IF;

                INSERT INTO ZLECENIA (Rower, Usluga, Data_zlecenia, Status, Wykonawca)
                VALUES (p_rower, p_usluga, p_data_zlecenia, p_status, p_wykonawca);
            END;
            $$ LANGUAGE plpgsql;
            """)

            # Procedura UPDATE dla ZLECENIA
            cursor.execute("""
            CREATE OR REPLACE FUNCTION aktualizuj_zlecenie(
                p_id_zlecenia INT,
                p_status VARCHAR(50),
                p_wykonawca INT
            )
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM ZLECENIA WHERE ID_ZLECENIA = p_id_zlecenia) THEN
                    RAISE EXCEPTION 'Zlecenie o ID % nie istnieje.', p_id_zlecenia;
                END IF;

                IF NOT EXISTS (SELECT 1 FROM PRACOWNICY WHERE ID_PRACOWNIKA = p_wykonawca) THEN
                    RAISE EXCEPTION 'Pracownik o ID % nie istnieje.', p_wykonawca;
                END IF;

                UPDATE ZLECENIA
                SET Status = p_status,
                    Wykonawca = p_wykonawca
                WHERE ID_ZLECENIA = p_id_zlecenia;
            END;
            $$ LANGUAGE plpgsql;
            """)

            # Procedura DELETE dla ZLECENIA
            cursor.execute("""
            CREATE OR REPLACE FUNCTION usun_zlecenie(p_id_zlecenia INT)
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM ZLECENIA WHERE ID_ZLECENIA = p_id_zlecenia) THEN
                    RAISE EXCEPTION 'Zlecenie o ID % nie istnieje.', p_id_zlecenia;
                END IF;

                DELETE FROM ZLECENIA WHERE ID_ZLECENIA = p_id_zlecenia;
            END;
            $$ LANGUAGE plpgsql;
            """)

            # Procedury dla tabeli KLIENCI
            cursor.execute("""
            CREATE OR REPLACE FUNCTION dodaj_klienta(
                p_imie VARCHAR(50),
                p_nazwisko VARCHAR(50),
                p_numer_telefonu VARCHAR(25),
                p_email VARCHAR(100)
            )
            RETURNS VOID AS $$
            BEGIN
                INSERT INTO KLIENCI (Imie, Nazwisko, Numer_telefonu, Email)
                VALUES (p_imie, p_nazwisko, p_numer_telefonu, p_email);
            END;
            $$ LANGUAGE plpgsql;
            """)

            cursor.execute("""
            CREATE OR REPLACE FUNCTION aktualizuj_klienta(
                p_id_klienta INT,
                p_imie VARCHAR(50),
                p_nazwisko VARCHAR(50),
                p_numer_telefonu VARCHAR(25),
                p_email VARCHAR(100)
            )
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM KLIENCI WHERE ID_KLIENTA = p_id_klienta) THEN
                    RAISE EXCEPTION 'Klient o ID % nie istnieje.', p_id_klienta;
                END IF;

                UPDATE KLIENCI
                SET Imie = p_imie,
                    Nazwisko = p_nazwisko,
                    Numer_telefonu = p_numer_telefonu,
                    Email = p_email
                WHERE ID_KLIENTA = p_id_klienta;
            END;
            $$ LANGUAGE plpgsql;
            """)

            cursor.execute("""
            CREATE OR REPLACE FUNCTION usun_klienta(p_id_klienta INT)
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM KLIENCI WHERE ID_KLIENTA = p_id_klienta) THEN
                    RAISE EXCEPTION 'Klient o ID % nie istnieje.', p_id_klienta;
                END IF;

                DELETE FROM KLIENCI WHERE ID_KLIENTA = p_id_klienta;
            END;
            $$ LANGUAGE plpgsql;
            """)

            # Procedury dla tabeli ROWERY
            cursor.execute("""
            CREATE OR REPLACE FUNCTION dodaj_rower(
                p_typ_roweru VARCHAR(50),
                p_marka VARCHAR(50),
                p_model VARCHAR(50),
                p_klient INT
            )
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM KLIENCI WHERE ID_KLIENTA = p_klient) THEN
                    RAISE EXCEPTION 'Klient o ID % nie istnieje.', p_klient;
                END IF;

                INSERT INTO ROWERY (Typ_roweru, Marka, Model, Klient)
                VALUES (p_typ_roweru, p_marka, p_model, p_klient);
            END;
            $$ LANGUAGE plpgsql;
            """)

            cursor.execute("""
            CREATE OR REPLACE FUNCTION aktualizuj_rower(
                p_id_rowera INT,
                p_typ_roweru VARCHAR(50),
                p_marka VARCHAR(50),
                p_model VARCHAR(50),
                p_klient INT
            )
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM ROWERY WHERE ID_ROWERA = p_id_rowera) THEN
                    RAISE EXCEPTION 'Rower o ID % nie istnieje.', p_id_rowera;
                END IF;

                IF NOT EXISTS (SELECT 1 FROM KLIENCI WHERE ID_KLIENTA = p_klient) THEN
                    RAISE EXCEPTION 'Klient o ID % nie istnieje.', p_klient;
                END IF;

                UPDATE ROWERY
                SET Typ_roweru = p_typ_roweru,
                    Marka = p_marka,
                    Model = p_model,
                    Klient = p_klient
                WHERE ID_ROWERA = p_id_rowera;
            END;
            $$ LANGUAGE plpgsql;
            """)

            cursor.execute("""
            CREATE OR REPLACE FUNCTION usun_rower(p_id_rowera INT)
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM ROWERY WHERE ID_ROWERA = p_id_rowera) THEN
                    RAISE EXCEPTION 'Rower o ID % nie istnieje.', p_id_rowera;
                END IF;

                DELETE FROM ROWERY WHERE ID_ROWERA = p_id_rowera;
            END;
            $$ LANGUAGE plpgsql;
            """)

            # Procedury dla tabeli USLUGI
            cursor.execute("""
            CREATE OR REPLACE FUNCTION dodaj_usluge(
                p_cena DECIMAL(10,2),
                p_nazwa VARCHAR(100),
                p_opis TEXT
            )
            RETURNS VOID AS $$
            BEGIN
                INSERT INTO USLUGI (cena, nazwa, opis)
                VALUES (p_cena, p_nazwa, p_opis);
            END;
            $$ LANGUAGE plpgsql;
            """)

            cursor.execute("""
            CREATE OR REPLACE FUNCTION aktualizuj_usluge(
                p_id_uslugi INT,
                p_cena DECIMAL(10,2),
                p_nazwa VARCHAR(100),
                p_opis TEXT
            )
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM USLUGI WHERE ID_USLUGI = p_id_uslugi) THEN
                    RAISE EXCEPTION 'Usługa o ID % nie istnieje.', p_id_uslugi;
                END IF;

                UPDATE USLUGI
                SET cena = p_cena,
                    nazwa = p_nazwa,
                    opis = p_opis
                WHERE ID_USLUGI = p_id_uslugi;
            END;
            $$ LANGUAGE plpgsql;
            """)

            cursor.execute("""
            CREATE OR REPLACE FUNCTION usun_usluge(p_id_uslugi INT)
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM USLUGI WHERE ID_USLUGI = p_id_uslugi) THEN
                    RAISE EXCEPTION 'Usługa o ID % nie istnieje.', p_id_uslugi;
                END IF;

                DELETE FROM USLUGI WHERE ID_USLUGI = p_id_uslugi;
            END;
            $$ LANGUAGE plpgsql;
            """)

            # Procedury dla tabeli PRACOWNICY
            cursor.execute("""
            CREATE OR REPLACE FUNCTION dodaj_pracownika(
                p_stanowisko VARCHAR(50),
                p_imie VARCHAR(50),
                p_nazwisko VARCHAR(50),
                p_wynagrodzenie DECIMAL(10,2),
                p_numer_telefonu VARCHAR(25)
            )
            RETURNS VOID AS $$
            BEGIN
                INSERT INTO PRACOWNICY (Stanowisko, Imie, Nazwisko, Wynagrodzenie, Numer_telefonu)
                VALUES (p_stanowisko, p_imie, p_nazwisko, p_wynagrodzenie, p_numer_telefonu);
            END;
            $$ LANGUAGE plpgsql;
            """)

            cursor.execute("""
            CREATE OR REPLACE FUNCTION aktualizuj_pracownika(
                p_id_pracownika INT,
                p_stanowisko VARCHAR(50),
                p_imie VARCHAR(50),
                p_nazwisko VARCHAR(50),
                p_wynagrodzenie DECIMAL(10,2),
                p_numer_telefonu VARCHAR(25)
            )
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM PRACOWNICY WHERE ID_PRACOWNIKA = p_id_pracownika) THEN
                    RAISE EXCEPTION 'Pracownik o ID % nie istnieje.', p_id_pracownika;
                END IF;

                UPDATE PRACOWNICY
                SET Stanowisko = p_stanowisko,
                    Imie = p_imie,
                    Nazwisko = p_nazwisko,
                    Wynagrodzenie = p_wynagrodzenie,
                    Numer_telefonu = p_numer_telefonu
                WHERE ID_PRACOWNIKA = p_id_pracownika;
            END;
            $$ LANGUAGE plpgsql;
            """)

            cursor.execute("""
            CREATE OR REPLACE FUNCTION usun_pracownika(p_id_pracownika INT)
            RETURNS VOID AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM PRACOWNICY WHERE ID_PRACOWNIKA = p_id_pracownika) THEN
                    RAISE EXCEPTION 'Pracownik o ID % nie istnieje.', p_id_pracownika;
                END IF;

                DELETE FROM PRACOWNICY WHERE ID_PRACOWNIKA = p_id_pracownika;
            END;
            $$ LANGUAGE plpgsql;
            """)

            # Procedura wyszukiwania wszystkich klientów wraz z ich rowerami
            cursor.execute("""
            CREATE OR REPLACE FUNCTION wyszukaj_klientow_z_rowerami()
            RETURNS TABLE (
                klient_id INT,
                imie VARCHAR(50),
                nazwisko VARCHAR(50),
                numer_telefonu VARCHAR(25),
                email VARCHAR(100),
                rower_id INT,
                typ_roweru VARCHAR(50),
                marka VARCHAR(50),
                model VARCHAR(50)
            ) AS $$
            BEGIN
                RETURN QUERY
                SELECT
                    k.ID_KLIENTA, k.Imie, k.Nazwisko, k.Numer_telefonu, k.Email,
                    r.ID_ROWERA, r.Typ_roweru, r.Marka, r.Model
                FROM KLIENCI k
                LEFT JOIN ROWERY r ON k.ID_KLIENTA = r.Klient;
            END;
            $$ LANGUAGE plpgsql;
            """)

            # Procedura lista zleceń z nazwą usługi, datą zlecenia oraz wykonawcą
            cursor.execute("""
            CREATE OR REPLACE FUNCTION lista_zlecen()
            RETURNS TABLE (
                zlecenie_id INT,
                nazwa_uslugi VARCHAR(100),
                data_zlecenia DATE,
                wykonawca VARCHAR(100)
            ) AS $$
            BEGIN
                RETURN QUERY
                SELECT
                    z.ID_ZLECENIA, u.nazwa, z.Data_zlecenia,
                    CONCAT(p.Imie, ' ', p.Nazwisko) AS wykonawca
                FROM ZLECENIA z
                JOIN USLUGI u ON z.Usluga = u.ID_USLUGI
                JOIN PRACOWNICY p ON z.Wykonawca = p.ID_PRACOWNIKA;
            END;
            $$ LANGUAGE plpgsql;
            """)

            # Procedura lista rowerów danego klienta
            cursor.execute("""
            CREATE OR REPLACE FUNCTION lista_rowerow_klienta(p_id_klienta INT)
            RETURNS TABLE (
                rower_id INT,
                typ_roweru VARCHAR(50),
                marka VARCHAR(50),
                model VARCHAR(50)
            ) AS $$
            BEGIN
                RETURN QUERY
                SELECT
                    r.ID_ROWERA, r.Typ_roweru, r.Marka, r.Model
                FROM ROWERY r
                WHERE r.Klient = p_id_klienta;
            END;
            $$ LANGUAGE plpgsql;
            """)

            # Procedura zwracająca wszystkie wartości z tabeli rowerów oraz dla danego ID klienta dane w formacie Imię Nazwisko (numer)
            cursor.execute("""
            CREATE OR REPLACE FUNCTION lista_rowerow_z_klientem()
            RETURNS TABLE (
                rower_id INT,
                typ_roweru VARCHAR(50),
                marka VARCHAR(50),
                model VARCHAR(50),
                klient_info VARCHAR(150)
            ) AS $$
            BEGIN
                RETURN QUERY
                SELECT
                    r.id_rowera,
                    r.typ_roweru,
                    r.marka,
                    r.model,
                    CONCAT(k.imie, ' ', k.nazwisko, ' (', k.numer_telefonu, ')')::VARCHAR(150) AS klient_info
                FROM rowery r
                JOIN klienci k ON r.klient_id = k.id_klienta;
            END;
            $$ LANGUAGE plpgsql;
            """)
            conn.commit()
    except Exception as e:
        print(f"Error creating procedures: {e}")
        conn.rollback()
    finally:
        conn.close()



# Run the function to create procedures
if __name__ == "__main__":
    create_procedures()