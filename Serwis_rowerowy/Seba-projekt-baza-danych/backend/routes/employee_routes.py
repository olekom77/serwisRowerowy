from flask import Blueprint, jsonify, request
from db.db_conn import db
from models.employee import Employee
from sqlalchemy import text
from db.db_utils import execute_procedure

employee_routes = Blueprint('employee_routes', __name__)

@employee_routes.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])

@employee_routes.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    try:
        execute_procedure('dodaj_pracownika', (
            data['stanowisko'],
            data['imie'],
            data['nazwisko'],
            data['wynagrodzenie'],
            data['numer_telefonu']
        ))
        return jsonify({"message": "Employee added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@employee_routes.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    try:
        execute_procedure('aktualizuj_pracownika', (
            employee_id,
            data['stanowisko'],
            data['imie'],
            data['nazwisko'],
            data['wynagrodzenie'],
            data['numer_telefonu']
        ))
        return jsonify({"message": "Employee updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@employee_routes.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        execute_procedure('usun_pracownika', (employee_id,))
        return jsonify({"message": "Employee deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@employee_routes.route('/employee-positions', methods=['GET'])
def get_employee_positions():
    result = db.session.execute(text("""
        SELECT conname, pg_get_constraintdef(oid) as consrc
        FROM pg_constraint
        WHERE conname = 'check_stanowisko'
    """))
    constraint = result.fetchone()
    if constraint:
        positions = constraint.consrc.split("'")[1::2]
        return jsonify(positions)
    return jsonify([]), 404


@employee_routes.route('/employees-mechanics', methods=['GET'])
def get_mechanics():
    mechanics = Employee.query.filter_by(stanowisko='Mechanik').all()
    return jsonify([mechanic.to_dict() for mechanic in mechanics])
