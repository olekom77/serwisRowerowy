from flask import Blueprint, jsonify, request
from db.db_conn import db
from models.order import Order
from sqlalchemy import text
from db.db_utils import execute_procedure

order_routes = Blueprint('order_routes', __name__)

@order_routes.route('/orders', methods=['POST'])
def add_order():
    data = request.get_json()
    try:
        execute_procedure('dodaj_zlecenie', (
            data['rower'],
            data['usluga'],
            data['data_zlecenia'],
            data['status'],
            data['wykonawca']
        ))
        return jsonify({"message": "Order added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@order_routes.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    try:
        execute_procedure('aktualizuj_zlecenie', (
            order_id,
            data['status'],
            data['wykonawca']
        ))
        return jsonify({"message": "Order updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@order_routes.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        execute_procedure('usun_zlecenie', (order_id,))
        return jsonify({"message": "Order deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@order_routes.route('/order-statuses', methods=['GET'])
def get_order_statuses():
    result = db.session.execute(text("""
        SELECT conname, pg_get_constraintdef(oid) as consrc
        FROM pg_constraint
        WHERE conname = 'check_order_status'
    """))
    constraint = result.fetchone()
    if constraint:
        statuses = constraint.consrc.split("'")[1::2]
        return jsonify(statuses)
    return jsonify([]), 404