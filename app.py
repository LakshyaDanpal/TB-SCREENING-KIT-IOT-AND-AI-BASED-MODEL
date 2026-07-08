from flask import Flask, render_template, request, redirect, flash, session, jsonify
import sqlite3, numpy as np, json
import dotenv
from dotenv import load_dotenv
import time
from PIL import Image
import numpy as np
from flask import send_from_directory
import hashlib
import requests
import pandas as pd
import joblib

# ---------------- Config ----------------
load_dotenv()
app = Flask(__name__)
app.secret_key = "supersecretkey"



# ---------------- Database ----------------
DB_FILE = "tb.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db()
    cur = conn.cursor()

    # User table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            role TEXT DEFAULT 'admin'
        )
    """)

    #  Patient table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            dob TEXT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# Initialize tables
create_tables()






# ---------------- Home ----------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO users (username, password, email, role)
                VALUES (?, ?, ?, ?)
            """, (username, hashed_password, email, "admin"))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username or email already exists!", "danger")
            conn.close()
            return redirect("/register")

        conn.close()
        flash("Registration successful! Please login to continue.", "success")
        return redirect("/login")

    return render_template("register.html")




# ---------------- Login ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            
            return redirect("/admin_dashboard" if user["role"] == "admin" else "/")
        else:
            flash("Invalid login!", "danger")
    return render_template("login.html")



@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if "username" not in session:
        return redirect("/login")
    return render_template("admin_dashboard.html")



@app.route("/submit_patient", methods=["POST"])
def submit_patient():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    dob = request.form.get("dob")
    message = request.form.get("message")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO patients (name, email, phone, dob, message)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, phone, dob, message))
    conn.commit()
    conn.close()

    # Just show control panel now
    return render_template("admin_dashboard.html", show_control=True)


@app.route("/toggle_value", methods=["POST"])
def toggle_value():
    current_value = int(request.json.get("current_value", 0))
    new_value = 1 if current_value == 0 else 0
  
    api_url = f"https://aislyntech.com/Api/v-update.php?id=1&action={new_value}"
    try:
        requests.get(api_url)
        return jsonify({"success": True, "new_value": new_value})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})



@app.route("/get_voice_data")
def get_voice_data():
    try:
        r = requests.get("https://aislyntech.com/Api/v-data-get.php", timeout=10)
        r.raise_for_status()
        data = r.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e), "data": []})


# Load the trained model once
model = joblib.load("saliva_rf_model.pkl")

feature_names = [
    "protein_peak_1", "protein_peak_2", "protein_peak_3", "protein_peak_4", "protein_peak_5",
    "protein_peak_6", "protein_peak_7", "protein_peak_8", "protein_peak_9"
]

@app.route("/detection", methods=["GET", "POST"])
def detection():
    if "username" not in session:
        return redirect("/login")

    prediction = None

    if request.method == "POST":
        try:
         
            user_input = {feature: [float(request.form[feature])] for feature in feature_names}

            
            X_new = pd.DataFrame(user_input)

           
            pred = model.predict(X_new)
            prediction = "Postive" if pred[0] == 1 else "Negative"
        except ValueError:
            prediction = "Invalid input! Please enter numbers."

    return render_template("detection.html", prediction=prediction, feature_names=feature_names)



# ----- Logout -----
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")




    
if __name__ == "__main__":
    app.run(debug=True)
