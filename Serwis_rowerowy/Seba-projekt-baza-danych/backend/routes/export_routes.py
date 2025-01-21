from flask import Blueprint, jsonify
from db.db_conn import export_data_to_json

export_routes = Blueprint('export_routes', __name__)

@export_routes.route('/export', methods=['GET'])
def export_data():
    try:
        data = export_data_to_json()
        if data is None:
            raise Exception("Failed to export data")
        return jsonify({"message": "Data exported successfully", "data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500