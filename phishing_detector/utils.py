"""
Utilitaires de Traitement de Texte pour la Détection de Phishing
Auteur: Mbula Mboma Jean Gilbert (MikaelX)
Année: 2024-2025
Domaine: Machine Learning & NLP
"""

import re
import pandas as pd
import numpy as np
import warnings
from bs4 import BeautifulSoup
from bs4 import MarkupResemblesLocatorWarning

# Configuration des avertissements : suppression des alertes BeautifulSoup
# pour les structures HTML non conformes
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# Définition des expressions régulières pour la détection de patterns suspects
URL_PATTERN = re.compile(r"http[s]?://|www\.")
EMAIL_PATTERN = re.compile(r"\b[\w.-]+@[\w.-]+\.\w+\b")
PHONE_PATTERN = re.compile(r"\+?\d[\d\s\-()]{7,}\d")


def load_data(csv_path):
    """
    Procédure de chargement et de préparation des données d'entraînement
    
    Cette fonction charge le jeu de données d'emails depuis un fichier CSV
    et effectue les opérations de preprocessing nécessaires pour l'entraînement
    du modèle de machine learning.
    
    Paramètres:
        csv_path (str): Chemin vers le fichier CSV contenant les données
    
    Retourne:
        pandas.DataFrame: Données préparées avec labels encodés
    """
    df = pd.read_csv(csv_path, dtype=str)
    df = df[['Email Text', 'Email Type']].dropna()
    df.columns = ['text', 'type']
    # Encodage binaire : 1 = phishing, 0 = légitime
    df['label'] = df['type'].str.lower().str.contains('phishing').astype(int)
    return df


def clean_text(text):
    """
    Fonction de nettoyage et normalisation du texte
    
    Cette procédure effectue le preprocessing des emails en supprimant
    les balises HTML et en normalisant les espaces pour préparer
    le texte à l'analyse par les algorithmes de machine learning.
    
    Paramètres:
        text (str): Texte brut de l'email à nettoyer
    
    Retourne:
        str: Texte nettoyé et normalisé
    """
    if not isinstance(text, str):
        return ""
    # Suppression des balises HTML et scripts à l'aide de BeautifulSoup
    text = BeautifulSoup(text, 'lxml').get_text(separator=' ')
    # Normalisation des espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_numeric_features(df, text_col='text'):
    """
    Extraction de caractéristiques numériques pour la détection de phishing
    
    Cette fonction analyse le contenu textuel pour extraire des indicateurs
    quantitatifs susceptibles de révéler des tentatives de phishing,
    tels que le nombre d'URLs, de signes d'exclamation, etc.
    
    Paramètres:
        df (pandas.DataFrame): DataFrame contenant les textes à analyser
        text_col (str): Nom de la colonne contenant le texte
    
    Retourne:
        pandas.DataFrame: Caractéristiques numériques extraites
    """
    text_series = df[text_col].fillna('').astype(str)
    features = pd.DataFrame()
    
    # Comptage des éléments suspects
    features['url_count'] = text_series.str.count(URL_PATTERN)
    features['email_count'] = text_series.str.count(EMAIL_PATTERN) 
    features['phone_count'] = text_series.str.count(PHONE_PATTERN)
    features['exclamation_count'] = text_series.str.count('!')
    features['question_count'] = text_series.str.count(r'\?')
    features['dollar_count'] = text_series.str.count(r'\$')
    
    # Calcul des ratios caractéristiques pouvant indiquer des anomalies
    text_length = text_series.str.len().replace(0, 1)  # Éviter la division par zéro
    features['digit_ratio'] = text_series.str.count(r"\d").fillna(0) / text_length
    features['upper_ratio'] = text_series.str.count(r"[A-Z]").fillna(0) / text_length
    features['word_count'] = text_series.str.split().str.len().fillna(0)
    
    return features
