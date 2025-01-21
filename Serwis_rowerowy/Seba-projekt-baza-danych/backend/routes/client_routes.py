from flask import Blueprint, jsonify, request
from db.db_conn import db
from models.client import Client
from db.db_utils import execute_procedure

client_routes = Blueprint('client_routes', __name__)

@client_routes.route('/clients', methods=['GET'])
def get_clients():
    try:
        clients = db.session.query(Client).all()
        return jsonify([client.to_dict() for client in clients]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@client_routes.route('/clients', methods=['POST'])
def add_client():
    data = request.get_json()
    try:
        execute_procedure('dodaj_klienta', (
            data['imie'],
            data['nazwisko'],
            data['numer_telefonu'],
            data['email']
        ))
        return jsonify({"message": "Client added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@client_routes.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    data = request.get_json()
    try:
        execute_procedure('aktualizuj_klienta', (
            client_id,
            data['imie'],
            data['nazwisko'],
            data['numer_telefonu'],
            data['email']
        ))
        return jsonify({"message": "Client updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@client_routes.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    try:
        execute_procedure('usun_klienta', (client_id,))
        return jsonify({"message": "Client deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400