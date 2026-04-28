import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'cms.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Analyse automatique de l'IMC
def interpreter_imc(imc):
    if imc < 18.5: return "Insuffisance pondérale"
    elif 18.5 <= imc < 25: return "Corpulence normale"
    elif 25 <= imc < 30: return "Surpoids"
    else: return "Obésité"

@app.route('/')
def index():
    return render_template('formulaire.html')

@app.route('/enregistrer', methods=['POST'])
def enregistrer():
    nom = request.form['nom']
    sexe = request.form['sexe']
    taille = float(request.form['taille'])
    poids = float(request.form['poids'])
    
    imc = round(poids / (taille * taille), 2)
    diagnostic = interpreter_imc(imc)
    
    conn = get_db_connection()
    conn.execute('INSERT INTO Etudiant (nom, sexe, imc, diagnostic) VALUES (?, ?, ?, ?)',
                 (nom, sexe, imc, diagnostic))
    conn.commit()
    conn.close()
    
    return render_template('resultat.html', nom=nom, imc=imc, diag=diagnostic)

# Route pour les Diagrammes (Analyse Visuelle)
@app.route('/stats')
def stats():
    conn = get_db_connection()
    # Données pour le Camembert (Sexe)
    sexe_data = conn.execute("SELECT sexe, COUNT(*) as count FROM Etudiant GROUP BY sexe").fetchall()
    # Données pour l'Histogramme (Diagnostic)
    diag_data = conn.execute("SELECT diagnostic, COUNT(*) as count FROM Etudiant GROUP BY diagnostic").fetchall()
    conn.close()
    return render_template('stats.html', sexe_data=sexe_data, diag_data=diag_data)

if __name__ == '__main__':
    app.run(debug=True)