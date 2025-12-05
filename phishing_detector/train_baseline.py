import argparse
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import classification_report, precision_recall_fscore_support, confusion_matrix
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib
from utils import load_data, clean_text, extract_numeric_features


def build_pipeline(use_smote=True, use_ensemble=False):
    # Word-level analysis - looking at individual words and phrases
    text_pipe_word = TfidfVectorizer(
        analyzer='word', 
        ngram_range=(1, 3),  # single words + 2-3 word combos
        max_features=80000,  
        min_df=2,  # ignore super rare words
        max_df=0.95,  # ignore super common words like "the", "and"
        sublinear_tf=True,  
        strip_accents='unicode',
        lowercase=True
    )
    
    # Character-level analysis - helps catch misspelled words and weird patterns
    text_pipe_char = TfidfVectorizer(
        analyzer='char',
        ngram_range=(3, 5),  # 3-5 character sequences
        max_features=20000,
        min_df=2,
        sublinear_tf=True
    )
    
    # Combine different types of features
    ct = ColumnTransformer(transformers=[
        ('text_word', text_pipe_word, 'text'),
        ('text_char', text_pipe_char, 'text'),
        ('num', StandardScaler(), ['url_count', 'email_count', 'phone_count', 'exclamation_count', 'question_count', 'dollar_count', 'digit_ratio', 'upper_ratio', 'word_count'])
    ])
    
    if use_ensemble:
        # Try combining two different models - sometimes works better than just one
        if use_smote:
            clf = ImbPipeline([
                ('features', ct),
                ('smote', SMOTE(random_state=42, k_neighbors=5)),
                ('voting', VotingClassifier(
                    estimators=[
                        ('lr', LogisticRegression(class_weight='balanced', solver='saga', max_iter=1000, C=0.3, random_state=42)),
                        ('rf', RandomForestClassifier(n_estimators=200, max_depth=20, min_samples_split=5, class_weight='balanced', random_state=42, n_jobs=-1))
                    ],
                    voting='soft',
                    weights=[1.2, 1.0]  # trust logistic regression a bit more
                ))
            ])
        else:
            clf = Pipeline([
                ('features', ct),
                ('voting', VotingClassifier(
                    estimators=[
                        ('lr', LogisticRegression(class_weight='balanced', solver='saga', max_iter=1000, C=0.3, random_state=42)),
                        ('rf', RandomForestClassifier(n_estimators=200, max_depth=20, min_samples_split=5, class_weight='balanced', random_state=42, n_jobs=-1))
                    ],
                    voting='soft',
                    weights=[1.2, 1.0]
                ))
            ])
    else:
        if use_smote:
            # Just using logistic regression - works pretty well for text classification
            clf = ImbPipeline([
                ('features', ct),
                ('smote', SMOTE(random_state=42, k_neighbors=5)),
                ('clf', LogisticRegression(class_weight='balanced', solver='saga', max_iter=1000, C=0.3, penalty='l2', random_state=42))
            ])
        else:
            clf = Pipeline([
                ('features', ct),
                ('clf', LogisticRegression(class_weight='balanced', solver='saga', max_iter=1000, C=0.3, penalty='l2', random_state=42))
            ])
    return clf


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='Phishing_Email.csv')
    parser.add_argument('--out', type=str, default='baseline_tfidf_lr.pkl')
    parser.add_argument('--test-size', type=float, default=0.2)
    parser.add_argument('--sample-frac', type=float, default=1.0,
                        help='Fraction of the dataset to sample for quick runs (1.0 = all)')
    parser.add_argument('--no-smote', action='store_true',
                        help='Disable SMOTE for class balancing')
    parser.add_argument('--ensemble', action='store_true',
                        help='Use ensemble (LogisticRegression + RandomForest) for better accuracy')
    args = parser.parse_args()

    df = load_data(args.input)
    print(f"Dataset shape: {df.shape}")
    print(f"Class distribution:\n{df['label'].value_counts()}")
    print(f"Class balance: {df['label'].value_counts(normalize=True)}")
    if args.sample_frac < 1.0:
        df = df.sample(frac=args.sample_frac, random_state=42).reset_index(drop=True)
    df['text'] = df['text'].astype(str).apply(clean_text)
    # handle empty texts so we don't crash
    df['text'] = df['text'].replace('', 'empty').fillna('empty')
    numeric = extract_numeric_features(df)
    # put text and numbers together
    X = pd.concat([numeric.reset_index(drop=True), df[['text']].reset_index(drop=True)], axis=1)
    # make sure we don't have any missing text
    X['text'] = X['text'].fillna('empty').astype(str)
    y = df['label'].reset_index(drop=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=args.test_size, random_state=42)
    
    # double check - sometimes the split messes things up
    X_train['text'] = X_train['text'].fillna('empty').astype(str)
    X_test['text'] = X_test['text'].fillna('empty').astype(str)

    use_smote = not args.no_smote
    use_ensemble = args.ensemble
    clf = build_pipeline(use_smote=use_smote, use_ensemble=use_ensemble)
    model_type = 'Ensemble (LR+RF)' if use_ensemble else 'LogisticRegression'
    print(f'\nTraining {model_type} with Enhanced TF-IDF (SMOTE: {use_smote})')
    print('Features: Word trigrams + Character n-grams + Numeric features')
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print('\n' + '='*60)
    print('CLASSIFICATION REPORT')
    print('='*60)
    print(classification_report(y_test, y_pred, target_names=['safe', 'phishing']))
    
    print('\n' + '='*60)
    print('CONFUSION MATRIX')
    print('='*60)
    cm = confusion_matrix(y_test, y_pred)
    print(f"True Negatives (Safe correctly classified): {cm[0,0]}")
    print(f"False Positives (Safe misclassified as Phishing): {cm[0,1]}")
    print(f"False Negatives (Phishing misclassified as Safe): {cm[1,0]}")
    print(f"True Positives (Phishing correctly classified): {cm[1,1]}")
    print('='*60)

    print('Saving model to', args.out)
    joblib.dump(clf, args.out)
