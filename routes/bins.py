from flask import Blueprint, jsonify, request

bins_blueprint = Blueprint('bins', __name__)

def get_mysql():
    from app import mysql
    return mysql

@bins_blueprint.route('/bins', methods=['GET'])
def get_bins():
    mysql = get_mysql()
    cur = mysql.connection.cursor()
    cur.execute("SELECT bin_id, bin_name, bin_type, location, fill_level FROM bins")
    rows = cur.fetchall()
    bins = []
    for row in rows:
        bins.append({
            'bin_id': row[0],
            'bin_name': row[1],
            'bin_type': row[2],
            'location': row[3],
            'fill_level': row[4]
        })
    cur.close()
    return jsonify(bins)

@bins_blueprint.route('/bins/<int:bin_id>', methods=['PUT'])
def update_bin_fill_level(bin_id):
    mysql = get_mysql()
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE bins SET fill_level=%s WHERE bin_id=%s",
        (data['fill_level'], bin_id)
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Bin updated!'})