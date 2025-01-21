from flask import Blueprint, jsonify, request
from db.db_conn import db
from models.service import Service
from db.db_utils import execute_procedure

service_routes = Blueprint('service_routes', __name__)

@service_routes.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([service.to_dict() for service in services])

@service_routes.route('/services', methods=['POST'])
def add_service():
    data = request.get_json()
    try:
        execute_procedure('dodaj_usluge', (
            data['nazwa'],
            data['opis'],
            data['cena']
        ))
        return jsonify({"message": "Service added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@service_routes.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    data = request.get_json()
    try:
        execute_procedure('aktualizuj_usluge', (
            service_id,
            data['nazwa'],
            data['opis'],
            data['cena']
        ))
        return jsonify({"message": "Service updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@service_routes.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    try:
        execute_procedure('usun_usluge', (service_id,))
        return jsonify({"message": "Service deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400