from flask import Flask, render_template, request
import sqlite3
import random
import os

app = Flask(__name__)

# DB create
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_no INTEGER,
            name TEXT,
            item TEXT,
            qty INTEGER,
            total INTEGER
        )
    ''')

    conn.commit()
    conn.close()

init_db()

menu = {
    "Burger": 50,
    "briyani": 100,
    "Sandwich": 40,
    "Tea": 10,
    "Coffee": 20
}

@app.route('/')
def home():
    return render_template('index.html', menu=menu)

@app.route('/order', methods=['POST'])
def order():
    name = request.form['name']
    item = request.form['item']
    qty = int(request.form['qty'])

    price = menu[item] * qty
    order_no = random.randint(1000, 9999)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
              (order_no, name, item, qty, price))

    conn.commit()

    # DEBUG (important)
    print("Inserted:", order_no, name)
    print("DB path:", os.path.abspath('database.db'))

    conn.close()

    order_data = {
        "order_no": order_no,
        "name": name,
        "item": item,
        "qty": qty,
        "total": price
    }

    return render_template('result.html', order=order_data)

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM orders")
    data = c.fetchall()

    conn.close()

    orders = []
    for row in data:
        orders.append({
            "order_no": row[0],
            "name": row[1],
            "item": row[2],
            "qty": row[3],
            "total": row[4]
        })

    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)