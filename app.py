from flask import Flask, render_template, request, redirect
import random

app = Flask(__name__)

orders = []

menu = {
    "Burger": 50,
    "Pizza": 100,
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

    order_data = {
        "order_no": order_no,
        "name": name,
        "item": item,
        "qty": qty,
        "total": price
    }

    orders.append(order_data)

    return render_template('result.html', order=order_data)

@app.route('/admin')
def admin():
    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)