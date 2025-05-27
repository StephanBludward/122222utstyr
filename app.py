from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = 'loans.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment TEXT,
            borrower TEXT,
            loan_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM loans')
    loans = c.fetchall()
    conn.close()
    return render_template('index.html', loans=loans)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        equipment = request.form['equipment']
        borrower = request.form['borrower']
        loan_date = request.form['loan_date']

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('INSERT INTO loans (equipment, borrower, loan_date) VALUES (?, ?, ?)',
                  (equipment, borrower, loan_date))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
