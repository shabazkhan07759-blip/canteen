from flask import Flask, render_template, request, redirect
import sqlite3
import random

app = Flask(__name__)

# -------- DB --------
def init_db():
    conn = sqlite3.connect('canteen.db')
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

# -------- MENU PAGE --------
@app.route('/')
def menu():
    return render_template('menu.html')

# -------- ORDER --------
@app.route('/order', methods=['POST'])
def order():
    name = request.form['name']
    item = request.form['item']
    qty = request.form['qty']

    # validation
    if not qty.isdigit():
        return "❌ Quantity must be number"

    qty = int(qty)

    # prices
    prices = {
        "Pizza": 100,
        "Burger": 80,
        "Pasta": 90,
        "Sandwich": 70,
        "Cold Drink": 50,
        "tea": 30
    }

    price = prices.get(item, 0)
    total = price * qty

    # generate order number
    order_no = random.randint(1000, 9999)

    # save to DB
    conn = sqlite3.connect('canteen.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
              (order_no, name, item, qty, total))
    conn.commit()
    conn.close()

    order_data = {
        "order_no": order_no,
        "name": name,
        "item": item,
        "qty": qty,
        "total": total
    }

    return render_template('result.html', order=order_data)

# -------- ADMIN --------
@app.route('/admin')
def admin():
    conn = sqlite3.connect('canteen.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    orders = c.fetchall()
    conn.close()

    return render_template('admin.html', orders=orders)

# -------- RUN --------
if __name__ == '__main__':
    app.run(debug=True)