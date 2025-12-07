"""
Système de Détection de Phishing - Interface Web
Auteur: Mbula Mboma Jean Gilbert (MikaelX)
Année: 2024-2025
Domaine: Machine Learning & Cybersécurité
"""

from flask import Flask, render_template, request, jsonify, session
import sqlite3
import joblib
import os
from datetime import datetime
import sys


# Configuration du système : importation des modules de traitement de texte
# depuis le répertoire phishing_detector pour assurer la cohérence du pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'phishing_detector'))
from utils import clean_text, extract_numeric_features
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # NOTE: à modifier en production

# Chargement du modèle de machine learning pré-entraîné
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'phishing_detector', 'baseline_tfidf_lr.pkl')
model = joblib.load(MODEL_PATH)

# Configuration de la base de données pour le stockage des messages
DB_PATH = 'chat.db'

def init_db():
    """Procédure d'initialisation de la base de données
    
    Cette fonction configure la structure de la base de données SQLite
    en créant la table des messages si elle n'existe pas déjà.
    Les champs incluent l'identifiant, le nom d'utilisateur, le message,
    les indicateurs de phishing et l'horodatage.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            is_phishing INTEGER DEFAULT 0,
            phishing_probability REAL DEFAULT 0.0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def predict_phishing(message):
    """Fonction de détection de phishing
    
    Cette fonction applique le modèle de machine learning pour évaluer
    la probabilité qu'un message donné soit de nature malveillante.
    
    Paramètres:
        message (str): Le texte à analyser
    
    Retourne:
        tuple: (probabilité, classification binaire)
    """
    # Étape 1: Préprocessing du texte d'entrée
    cleaned = clean_text(message)
    if not cleaned:
        cleaned = 'empty'  # Gestion des cas de messages vides
    
    # Étape 2: Transformation en format compatible avec le modèle
    df = pd.DataFrame({'text': [cleaned]})
    
    # Étape 3: Extraction des caractéristiques numériques (URLs, signes d'exclamation, etc.)
    numeric = extract_numeric_features(df)
    
    # Étape 4: Concaténation des données textuelles et numériques
    X = pd.concat([numeric.reset_index(drop=True), df[['text']].reset_index(drop=True)], axis=1)
    X['text'] = X['text'].fillna('empty').astype(str)
    
    # Étape 5: Application du modèle de classification
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]  # Calcul de la probabilité de phishing
    
    return int(prediction), float(probability)

@app.route('/')
def index():
    """Route principale de l'interface de chat
    
    Cette fonction gère l'affichage de la page principale et
    assure l'attribution automatique d'un nom d'utilisateur
    si aucun n'est défini dans la session.
    """
    if 'username' not in session:
        session['username'] = f"User{datetime.now().strftime('%H%M%S')}"
    return render_template('chat.html', username=session['username'])

@app.route('/set_username', methods=['POST'])
def set_username():
    """Procédure de définition du nom d'utilisateur
    
    Cette fonction traite les requêtes de modification
    du nom d'utilisateur et valide les données d'entrée.
    """
    data = request.json
    username = data.get('username', '').strip()
    if username:
        session['username'] = username
        return jsonify({'success': True, 'username': username})
    return jsonify({'success': False, 'error': 'Nom d\'utilisateur invalide'})

@app.route('/send_message', methods=['POST'])
def send_message():
    """Procédure d'envoi et d'analyse des messages
    
    Cette fonction traite l'envoi d'un nouveau message, applique
    l'algorithme de détection de phishing et stocke les résultats
    dans la base de données.
    """
    data = request.json
    message = data.get('message', '').strip()
    username = session.get('username', 'Anonyme')
    
    if not message:
        return jsonify({'success': False, 'error': 'Message vide'})
    
    # Application de l'algorithme de détection
    is_phishing, probability = predict_phishing(message)
    
    # Application du seuil de confiance (>73% pour minimiser les faux positifs)
    is_high_confidence_phishing = is_phishing and probability > 0.73
    
    # Sauvegarde dans la base de données
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (username, message, is_phishing, phishing_probability)
        VALUES (?, ?, ?, ?)
    ''', (username, message, int(is_high_confidence_phishing), probability))
    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'success': True,
        'message_id': message_id,
        'is_phishing': bool(is_high_confidence_phishing),
        'probability': probability
    })

@app.route('/get_messages', methods=['GET'])
def get_messages():
    """Procédure de récupération des messages
    
    Cette fonction retourne l'ensemble des messages stockés
    avec leurs métadonnées d'analyse de sécurité.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, message, is_phishing, phishing_probability, timestamp
        FROM messages
        ORDER BY timestamp ASC
    ''')
    messages = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'messages': [
            {
                'id': msg[0],
                'username': msg[1],
                'message': msg[2],
                'is_phishing': bool(msg[3]),
                'probability': msg[4],
                'timestamp': msg[5]
            }
            for msg in messages
        ]
    })

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    """Procédure de remise à zéro de la conversation
    
    Cette fonction supprime l'ensemble des messages
    de la base de données pour démarrer une nouvelle session.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    # Initialisation du système au démarrage
    init_db()
    print("\n" + "="*60)
    print("Détecteur de Phishing - Interface Web")
    print("="*60)
    print("Application démarrée sur http://localhost:5000")
    print("Utilisez Ctrl+C pour arrêter le serveur")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
