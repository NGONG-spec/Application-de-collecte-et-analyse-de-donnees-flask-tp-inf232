from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        prenom TEXT,
        sexe TEXT,
        date_naissance TEXT,
        telephone TEXT,
        taille REAL,
        poids REAL,
        imc REAL,
        tension TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def accueil():
    return render_template("accueil.html")

@app.route("/formulaire", methods=["GET", "POST"])
def formulaire():
    if request.method == "POST":
        data = request.form

        taille = float(data["taille"]) / 100  # cm -> m
        poids = float(data["poids"])
        imc = poids / (taille ** 2)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users (nom, prenom, sexe, date_naissance, telephone, taille, poids, imc, tension)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["nom"],
            data["prenom"],
            data["sexe"],
            data["date_naissance"],
            data["telephone"],
            data["taille"],
            data["poids"],
            imc,
            data["tension"]
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("merci"))

    return render_template("formulaire.html")

@app.route("/merci")
def merci():
    return render_template("merci.html")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT sexe, imc FROM users")
    data = cursor.fetchall()

    conn.close()

    hommes = sum(1 for d in data if d[0] == "Homme")
    femmes = sum(1 for d in data if d[0] == "Femme")

    imc_values = [d[1] for d in data]

    return render_template(
        "dashboard.html",
        hommes=hommes,
        femmes=femmes,
        imc_values=imc_values
    )

if __name__ == "__main__":
    app.run(debug=True)