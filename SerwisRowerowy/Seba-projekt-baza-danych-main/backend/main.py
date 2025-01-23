from flask import Flask
import os
from db.db_conn import init_db as initialize_db_conn, db
from flask_cors import CORS
import db.misc.populate_db as populate_db
import db.misc.procedures_gen as procedures_gen

# Inicjalizacja aplikacji Flask
app = Flask(__name__)
CORS(app)  # Dodanie obsługi CORS

# Konfiguracja bazy danych
print("URI bazy danych: " + os.getenv("DATABASE_URL"))

# Inicjalizacja bazy danych
initialize_db_conn(app)

# Importowanie modeli
from models.client import Client
from models.bike import Bike
from models.service import Service
from models.employee import Employee
from models.order import Order

# Importowanie endpointów
from routes.client_routes import client_routes
from routes.bike_routes import bike_routes
from routes.service_routes import service_routes
from routes.employee_routes import employee_routes
from routes.order_routes import order_routes
from routes.export_routes import export_routes

# Rejestracja blueprintów
app.register_blueprint(client_routes, url_prefix="/api")
app.register_blueprint(bike_routes, url_prefix="/api")
app.register_blueprint(service_routes, url_prefix="/api")
app.register_blueprint(employee_routes, url_prefix="/api")
app.register_blueprint(order_routes, url_prefix="/api")
app.register_blueprint(export_routes, url_prefix="/api")

# Inicjalizacja bazy danych
def initialize_database():
    try:
        db.create_all()
        # Sprawdzenie, czy baza danych jest pusta
        if not any(db.session.query(model).first() for model in [Client, Bike, Service, Employee, Order]):
            print("Baza danych jest pusta. Tworzenie przykładowych danych...")
            populate_db.run()
            procedures_gen.create_procedures()
        print("Tabele zostały pomyślnie utworzone lub już istnieją.")
    except Exception as e:
        print(f"Błąd podczas inicjalizacji bazy danych: {e}")

if __name__ == "__main__":
    with app.app_context():
        initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=True)