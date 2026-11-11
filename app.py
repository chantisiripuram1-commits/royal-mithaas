
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "royal_mithaas_secret_key"


# MySQL Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add your MySQL password if you have one
        database="royal_mithaas"  # Change this to your database name
    )


# Home
@app.route("/")
def home():
    return render_template("index.html")


# About Us
@app.route("/about")
def about():
    return render_template("about.html")


# All Sweets
@app.route("/products")
def products():
    return render_template("products.html")


# Contact Us
@app.route("/contact")
def contact():
    return render_template("contact.html")


# My Orders
@app.route("/my-orders")
def my_orders():
    return render_template("my_orders.html")


# Checkout
@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        mobile = request.form.get("mobile", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not all([name, email, mobile, password, confirm_password]):
            flash("Please fill in all fields.")
            return redirect(url_for("signup"))

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for("signup"))

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            password_hash = generate_password_hash(password)

            sql = """
                INSERT INTO customers (name, email, mobile, password)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(sql, (name, email, mobile, password_hash))
            connection.commit()

            # Save the new customer's name in the session
            session["user_name"] = name
            session["user_email"] = email

            flash("Account created successfully!")
            return redirect(url_for("home"))

        except IntegrityError:
            flash("This email is already registered. Please login.")
            return redirect(url_for("login"))

        except mysql.connector.Error as error:
            print("Signup database error:", error)
            flash("Something went wrong. Please check your database connection.")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    return render_template("signup.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            sql = "SELECT * FROM customers WHERE email = %s"
            cursor.execute(sql, (email,))

            user = cursor.fetchone()

            if user and check_password_hash(user["password"], password):

                # Save the actual registered customer's name
                session["user_name"] = user["name"]
                session["user_email"] = user["email"]

                flash("Login successful!")
                return redirect(url_for("home"))

            else:
                flash("Invalid email or password.")

        except mysql.connector.Error as error:
            print("Login database error:", error)
            flash("Unable to login. Please check your database connection.")

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():

    session.pop("user_name", None)
    session.pop("user_email", None)

    flash("You have logged out successfully!")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
