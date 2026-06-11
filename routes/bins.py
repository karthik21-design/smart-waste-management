from flask import Blueprint, jsonify
from flask_mysqldb import MySQL

bins_blueprint = Blueprint('bins', __name__)

@bins_blueprint.route('/bins', methods=['GET'])
def get_bins():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bins")
    rows = cur.fetchall()
    return jsonify(rows)

@bins_blueprint.route('/bins/<int:bin_id>', methods=['PUT'])
def update_bin_fill_level(bin_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE bins SET fill_level = %s WHERE bin_id = %s", (request.json['fill_level'], bin_id))
    mysql.connection.commit()
    return jsonify({'message': 'Bin fill level updated successfully'})
