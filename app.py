from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
if __name__== "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1",port=5000)
app.secret_key = 'some_random_data'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "inventory"

mysql = MySQL(app)
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/selldrinks')
def sell():
    return render_template('sell.html',)

@app.route('/home')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM softdrinktbl")
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('index.html', drinks=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name_of_drink']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_number = request.form['batch_number']
        drink_subtype = request.form['drink_subtype']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO softdrinktbl (name_of_drink, price, quantity, expiry_date, batch_number, drink_subtype) VALUES (%s, %s, %s, %s, %s, %s)", (name, price, quantity, expiry_date, batch_number, drink_subtype))
        mysql.connection.commit()
        return redirect(url_for('Index'))
        
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    cursor = mysql.connection.cursor()

    if request.method == "POST":
        name = request.form['name_of_drink']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_number = request.form['batch_number']
        subtype = request.form['subtype']

        cursor.execute("""
            UPDATE drinks_inventory
            SET name_of_drink = %s, price = %s, quantity = %s, expiry_date = %s, batch_number = %s, subtype = %s
            WHERE ID = %s
        """, (name, price, quantity, expiry_date, batch_number, subtype, id))

        mysql.connection.commit()
        cursor.close()
        flash(f"{name} updated successfully!", "success")
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM drinks_inventory WHERE ID = %s", (id,))
    drink = cursor.fetchone()
    cursor.close()
    return render_template("update_drinks.html",
