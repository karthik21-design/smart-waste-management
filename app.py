from flask import Flask
from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

from routes.bins import bins_blueprint
app.register_blueprint(bins_blueprint)

@app.route('/')
def index():
    return render_template('index.html')
import random

@app.route('/simulate')
def simulate():
    cur = mysql.connection.cursor()
    cur.execute("SELECT bin_id FROM bins")
    bins = cur.fetchall()
    for (bin_id,) in bins:
        level = random.randint(10, 100)
        cur.execute(
            "UPDATE bins SET fill_level=%s WHERE bin_id=%s",
            (level, bin_id)
        )
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'simulated'})
if __name__ == '__main__':
    app.run(debug=True)