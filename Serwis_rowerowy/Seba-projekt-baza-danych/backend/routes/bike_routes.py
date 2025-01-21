from flask import Blueprint, jsonify, request
from models.bike import Bike
from db.db_utils import execute_procedure

bike_routes = Blueprint('bike_routes', __name__)

@bike_routes.route('/bikes', methods=['GET'])
def get_bikes():
    try:
        result = execute_procedure('lista_rowerow_z_klientem', ())
        bikes_data = []
        for row in result:
            bike = {
                'rower_id': row[0],
                'typ_roweru': row[1],
                'marka': row[2],
                'model': row[3],
                'klient': row[4]
            }
            bikes_data.append(bike)
        return jsonify(bikes_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bike_routes.route('/bikes', methods=['POST'])
def add_bike():
    data = request.get_json()
    try:
        execute_procedure('dodaj_rower', (
            data['typ_roweru'],
            data['marka'],
            data['model'],
            data['klient']
        ))
        return jsonify({"message": "Bike added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bike_routes.route('/bikes/<int:bike_id>', methods=['PUT'])
def update_bike(bike_id):
    data = request.get_json()
    try:
        execute_procedure('aktualizuj_rower', (
            bike_id,
            data['typ_roweru'],
            data['marka'],
            data['model'],
            data['klient']
        ))
        return jsonify({"message": "Bike updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bike_routes.route('/bikes/<int:bike_id>', methods=['DELETE'])
def delete_bike(bike_id):
    try:
        execute_procedure('usun_rower', (bike_id,))
        return jsonify({"message": "Bike deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400