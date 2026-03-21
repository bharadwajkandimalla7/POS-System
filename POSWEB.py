import os
import sys
from flask import Flask, render_template, request, redirect

def resource_path(relative_path):
    """ Get absolute path for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__, template_folder=resource_path("templates"))

import sqlite3

db = sqlite3.connect("pos.db", check_same_thread=False)
db.row_factory = sqlite3.Row
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS product (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    BarCode TEXT,
    category TEXT,
    Price REAL,
    Quantity INTEGER
)
""")

db.commit()


# Home Menu
@app.route('/')
def menu():
    return render_template("menu.html")


# Add Product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        Name = request.form['Name']
        BarCode = request.form['BarCode']
        category = request.form['category']
        Price = request.form['Price']
        Quantity = request.form['Quantity']

        query = """
        INSERT INTO product (Name, BarCode, category, Price, Quantity)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (Name, BarCode, category, Price, Quantity))
        db.commit()
        return redirect('/view_products')

    return render_template("add_product.html")


# View Products
@app.route('/view_products')
def view_products():
    cursor.execute("SELECT * FROM product")
    products = [dict(row) for row in cursor.fetchall()]
    return render_template("view_products.html", products=products)


# Update Product
@app.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    if request.method == 'POST':
        Price = request.form['Price']
        Quantity = request.form['Quantity']

        query = "UPDATE product SET Price=?, Quantity=? WHERE product_id=?"
        cursor.execute(query, (Price, Quantity, id))
        db.commit()
        return redirect('/view_products')

    cursor.execute("SELECT * FROM product WHERE product_id=?", (id,))
    product = cursor.fetchone()
    return render_template("update_product.html", product=product)


# Delete Product
@app.route('/delete_product/<int:id>')
def delete_product(id):
    query = "DELETE FROM product WHERE product_id=?"
    cursor.execute(query, (id,))
    db.commit()
    return redirect('/view_products')


if __name__ == '__main__':
    app.run(debug=True)