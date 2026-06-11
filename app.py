from flask import Flask
from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL
from flask import Flask, render_template, jsonify, request
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
import requests as req

@app.route('/chat', methods=['POST'])
def chat():
    question = request.json.get('question', '')
    
    # Get current bin status for context
    cur = mysql.connection.cursor()
    cur.execute("SELECT bin_name, location, fill_level FROM bins")
    bins = cur.fetchall()
    cur.close()
    
    bin_status = "\n".join([
        f"{b[0]} at {b[1]}: {b[2]}% full" 
        for b in bins
    ])
    
    prompt = f"""You are a smart waste management assistant.
Current bin status:
{bin_status}

User question: {question}
Give a short helpful answer."""

    response = req.post('http://localhost:11434/api/generate', 
        json={
            'model': 'llama3.2:3b',
            'prompt': prompt,
            'stream': False
        })
    
    answer = response.json().get('response', 'Sorry, I could not answer!')
    return jsonify({'answer': answer})
if __name__ == '__main__':
    app.run(debug=True)