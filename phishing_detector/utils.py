import re
import pandas as pd
import numpy as np
import warnings
from bs4 import BeautifulSoup
from bs4 import MarkupResemblesLocatorWarning

# BeautifulSoup sometimes complains about weird HTML - we don't care
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# Patterns we look for in emails
URL_PATTERN = re.compile(r"http[s]?://|www\.")
EMAIL_PATTERN = re.compile(r"\b[\w.-]+@[\w.-]+\.\w+\b")
PHONE_PATTERN = re.compile(r"\+?\d[\d\s\-()]{7,}\d")


def load_data(csv_path):
    """Load the email dataset and prep it for training"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df[['Email Text', 'Email Type']].dropna()
    df.columns = ['text', 'type']
    # 1 = phishing, 0 = safe
    df['label'] = df['type'].str.lower().str.contains('phishing').astype(int)
    return df


def clean_text(text):
    """Clean up email text - remove HTML and fix spacing"""
    if not isinstance(text, str):
        return ""
    # strip out HTML tags and scripts
    text = BeautifulSoup(text, 'lxml').get_text(separator=' ')
    # fix crazy spacing
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_numeric_features(df, text_col='text'):
    """Extract numbers and patterns that might indicate phishing"""
    text_series = df[text_col].fillna('').astype(str)
    features = pd.DataFrame()
    
    # count suspicious stuff
    features['url_count'] = text_series.str.count(URL_PATTERN)
    features['email_count'] = text_series.str.count(EMAIL_PATTERN) 
    features['phone_count'] = text_series.str.count(PHONE_PATTERN)
    features['exclamation_count'] = text_series.str.count('!')
    features['question_count'] = text_series.str.count(r'\?')
    features['dollar_count'] = text_series.str.count(r'\$')
    
    # ratios that might be weird in phishing emails
    text_length = text_series.str.len().replace(0, 1)  # avoid division by zero
    features['digit_ratio'] = text_series.str.count(r"\d").fillna(0) / text_length
    features['upper_ratio'] = text_series.str.count(r"[A-Z]").fillna(0) / text_length
    features['word_count'] = text_series.str.split().str.len().fillna(0)
    
    return features
