from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
from config import Config
import random
import numpy as np
import requests as req
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

from routes.bins import bins_blueprint
app.register_blueprint(bins_blueprint)

@app.route('/')
def index():
    return render_template('index.html')

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
        cur.execute(
            "INSERT INTO fill_history (bin_id, fill_level) VALUES (%s, %s)",
            (bin_id, level)
        )
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'simulated'})

@app.route('/alerts')
def get_alerts():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.bin_name, b.location, b.fill_level 
        FROM bins b 
        WHERE b.fill_level >= 80 
        ORDER BY b.fill_level DESC
    """)
    rows = cur.fetchall()
    alerts = []
    for row in rows:
        alerts.append({
            'bin_name': row[0],
            'location': row[1],
            'fill_level': row[2]
        })
    cur.close()
    return jsonify(alerts)

@app.route('/predict/<int:bin_id>')
def predict(bin_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT fill_level,
        UNIX_TIMESTAMP(recorded_at) as ts
        FROM fill_history
        WHERE bin_id=%s
        ORDER BY recorded_at
        LIMIT 10
    """, (bin_id,))
    rows = cur.fetchall()
    cur.close()

    if len(rows) < 3:
        return jsonify({
            'prediction': 'Not enough data yet',
            'current_level': 0,
            'predicted_next': None,
            'will_be_full': False
        })

    X = np.array([r[1] for r in rows]).reshape(-1, 1)
    y = np.array([r[0] for r in rows])

    model = LinearRegression()
    model.fit(X, y)

    next_ts = X[-1][0] + 3600
    predicted = model.predict([[next_ts]])[0]
    predicted = max(0, min(100, round(predicted)))

    return jsonify({
        'bin_id': bin_id,
        'current_level': int(y[-1]),
        'predicted_next': int(predicted),
        'will_be_full': predicted >= 80
    })

@app.route('/chat', methods=['POST'])
def chat():
    question = request.json.get('question', '')
    cur = mysql.connection.cursor()
    cur.execute("SELECT bin_name, location, fill_level FROM bins")
    bins = cur.fetchall()
    cur.close()

    bin_status = "\n".join([
        f"{b[0]} at {b[1]}: {b[2]}% full"
        for b in bins
    ])

    prompt = f"You are a smart waste management assistant. Current bin status: {bin_status}. User question: {question}. Give a short helpful answer."

    try:
        response = req.post(
            'http://localhost:11434/api/generate',
            json={'model': 'llama3.2:3b', 'prompt': prompt, 'stream': False}
        )
        answer = response.json().get('response', 'Sorry, could not answer!')
    except:
        answer = 'AI service not available right now!'

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)