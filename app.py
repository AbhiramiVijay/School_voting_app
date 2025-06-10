
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secret123'

# Ensure database exists
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            student_id TEXT PRIMARY KEY,
            head_boy TEXT,
            head_girl TEXT,
            asst_head_boy TEXT,
            asst_head_girl TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Candidate list for each position
candidates = {
    "head_boy": [
        {"name": "Francis Xavier K.T", "image": "Francis.jpg"},
        {"name": "Joe J Vazhapilly", "image": "Joe.jpg"},
        {"name": "Nikhil Krishna T.S", "image": "Nikhil.jpg"},
        {"name": "Rishikesh R Menon", "image": "Rishikesh.jpg"}
        
    ],
    "head_girl": [
        {"name": "Anshika Anoop", "image": "Anshika.jpg"},
        {"name": "Axilin Xavier", "image": "Axilin.jpg"},
        {"name": "Megha Sreekumar", "image": "Megha.jpeg"},
        {"name": "Nivedya Hareesh", "image": "Nivedya.jpg"},
        {"name": "Varsha K.M", "image": "Varsha.jpg"},
    ],
    "asst_head_boy": [
        {"name": "Abhimanyu V.K", "image": "Abhimanyu.jpg"},
        {"name": "Aimon Anoop", "image": "Aimon.jpg"},
         {"name": "Antony B Kuttikkatt", "image": "Antony.jpg"},
        {"name": "Neerad s Menon", "image": "Neerad.jpg"}
    ],
    "asst_head_girl": [
        {"name": "Jewel Deepak", "image": "Jewel.jpg"},
        {"name": "Leocadia Joshy", "image": "Leocadia.jpg"},
        {"name": "Sarah Paul", "image": "Sarah.jpg"}
    ]
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/vote', methods=['POST'])
def vote():
    student_id = request.form['student_id']
    if not student_id:
        return "Student ID required", 400

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM votes WHERE student_id = ?", (student_id,))
    if c.fetchone():
        conn.close()
        return render_template('already_voted.html')

    session['student_id'] = student_id
    conn.close()
    return render_template('voting.html', candidates=candidates, school_name="Christ Vidyanikethann")

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    if 'student_id' not in session:
        return redirect(url_for('home'))

    student_id = session['student_id']
    head_boy = request.form['head_boy']
    head_girl = request.form['head_girl']
    asst_head_boy = request.form['asst_head_boy']
    asst_head_girl = request.form['asst_head_girl']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO votes (student_id, head_boy, head_girl, asst_head_boy, asst_head_girl)
        VALUES (?, ?, ?, ?, ?)
    ''', (student_id, head_boy, head_girl, asst_head_boy, asst_head_girl))
    conn.commit()
    conn.close()

    session.pop('student_id', None)
    return render_template('thanks.html')

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/results', methods=['POST'])
def results():
    password = request.form['password']
    if password != "adminpass":
        return "Unauthorized", 403

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    results = {}
    positions = ["head_boy", "head_girl", "asst_head_boy", "asst_head_girl"]
    for position in positions:
        c.execute(f"SELECT {position}, COUNT(*) FROM votes GROUP BY {position}")
        results[position] = c.fetchall()

    conn.close()
    return render_template('results.html', results=results, positions=positions, school_name="Christ Vidyanikethann")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
