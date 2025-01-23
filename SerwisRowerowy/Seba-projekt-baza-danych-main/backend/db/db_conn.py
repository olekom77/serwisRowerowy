from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import json

db = SQLAlchemy()

def init_db(app):
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL environment variable is not set.")
        return

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    # Utworzenie schematu sklep, jeśli nie istnieje
    with app.app_context():
        try:
            db.session.execute(text("CREATE SCHEMA IF NOT EXISTS sklep"))
            db.session.commit()
        except SQLAlchemyError as e:
            print(f"Błąd podczas tworzenia schematu 'sklep': {e}")
            db.session.rollback()

def export_data_to_json():
    try:
        with db.engine.connect() as connection:

            connection.execute(text("SET search_path TO sklep"))

            result = connection.execute(text("SELECT * FROM klienci"))
            clients = [dict(row) for row in result.mappings()]

            result = connection.execute(text("SELECT * FROM rowery"))
            bikes = [dict(row) for row in result.mappings()]

            result = connection.execute(text("SELECT * FROM uslugi"))
            services = [dict(row) for row in result.mappings()]

            result = connection.execute(text("SELECT * FROM pracownicy"))
            employees = [dict(row) for row in result.mappings()]

            result = connection.execute(text("SELECT * FROM zlecenia"))
            orders = [dict(row) for row in result.mappings()]

            # Fetch foreign key relationships
            result = connection.execute(text("""
                SELECT
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM
                    information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY'
            """))
            relationships = [dict(row) for row in result.mappings()]

        data = {
            "clients": clients,
            "bikes": bikes,
            "services": services,
            "employees": employees,
            "orders": orders,
            "relationships": relationships
        }

        return data

    except SQLAlchemyError as e:
        print(f"Error exporting data to JSON: {e}")
        return None