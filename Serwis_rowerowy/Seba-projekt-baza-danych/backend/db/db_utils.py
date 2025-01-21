import psycopg2
import os
from urllib.parse import urlparse

def execute_procedure(procedure_name, params):
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
            cursor.callproc(procedure_name, params)
            result = cursor.fetchall()
            conn.commit()
            if result:
                return result
    except Exception as e:
        print(f"Error executing procedure {procedure_name}: {e}")
        conn.rollback()
    finally:
        conn.close()