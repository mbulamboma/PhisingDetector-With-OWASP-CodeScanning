# Phishing Detector Training

This folder contains the code to train the phishing detection model.

## What's Here

- `train_baseline.py` - main script that trains the model
- `utils.py` - helper functions for processing text and extracting features  
- `requirements.txt` - list of Python packages you need

## How to Train

Basic usage:
```bash
python train_baseline.py
```

This will:
1. Load the email dataset from `../Phishing_Email.csv`
2. Clean and process the text
3. Extract features (word patterns, URLs, punctuation, etc.)
4. Train a logistic regression model
5. Save the trained model as `baseline_tfidf_lr.pkl`

## Options

You can customize the training with these options:

- `--input path/to/data.csv` - use different data file
- `--out model_name.pkl` - change output filename
- `--sample-frac 0.1` - use only 10% of data (for testing)
- `--ensemble` - use multiple models instead of just one
- `--no-smote` - don't balance the classes
- `--test-size 0.3` - use 30% of data for testing

Examples:
```bash
# Quick test with small data sample
python train_baseline.py --sample-frac 0.1

# Train with multiple models
python train_baseline.py --ensemble

# Use custom data file
python train_baseline.py --input my_emails.csv --out my_model.pkl
```

## What the Script Does

1. **Load Data**: Reads CSV file with email text and labels
2. **Clean Text**: Removes HTML, fixes spacing, etc.
3. **Extract Features**:
   - Word-level TF-IDF (looks at words and phrases)
   - Character-level TF-IDF (catches typos and obfuscation)
   - Numerical features (URL count, punctuation, etc.)
4. **Balance Classes**: Uses SMOTE to create synthetic examples
5. **Train Model**: Fits logistic regression or ensemble
6. **Evaluate**: Shows accuracy, precision, recall on test set
7. **Save Model**: Saves trained model to disk

## Expected Output

When training finishes, you should see something like:

```
Dataset shape: (18000, 3)
Class distribution:
0    10800
1     7200

Training LogisticRegression with Enhanced TF-IDF (SMOTE: True)
Features: Word trigrams + Character n-grams + Numeric features

========================================
CLASSIFICATION REPORT
========================================
              precision    recall  f1-score   support

        safe       0.87      0.89      0.88      2160
    phishing       0.85      0.82      0.84      1440

    accuracy                           0.86      3600
   macro avg       0.86      0.86      0.86      3600
weighted avg       0.86      0.86      0.86      3600

Saving model to baseline_tfidf_lr.pkl
```

## Model Details

The default model uses:
- **Word features**: 1-3 word combinations (unigrams, bigrams, trigrams)
- **Character features**: 3-5 character sequences
- **Numerical features**: counts of URLs, emails, phone numbers, punctuation
- **SMOTE**: synthetic minority oversampling to balance classes
- **Logistic Regression**: simple but effective for text classification

## Troubleshooting

**"ModuleNotFoundError"**: Install requirements first
```bash
pip install -r requirements.txt
```

**"FileNotFoundError"**: Make sure `Phishing_Email.csv` exists in the parent directory, or use `--input` to specify the correct path

**"Memory Error"**: Try using a smaller sample with `--sample-frac 0.5` or reduce `max_features` in the code

**Low accuracy**: The model performance depends on your data quality. Try:
- Using the ensemble option (`--ensemble`)
- Checking that your CSV has the right columns
- Making sure you have enough training examples

# Activate it
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Train the Model
```bash
# Basic training (recommended)
python train_baseline.py --input ../Phishing_Email.csv

# With ensemble for better accuracy
python train_baseline.py --input ../Phishing_Email.csv --ensemble

# Without SMOTE (for comparison)
python train_baseline.py --input ../Phishing_Email.csv --no-smote
```

### Step 3: Check Results
The training script already shows all evaluation metrics. To test the model in action, use the web application:

```bash
cd ../webapp
pip install -r requirements.txt
python app.py
```

---

## 🎯 How It Works (Simple Explanation)

### 1. **Data Loading** 📊
- Reads emails from CSV file
- Labels them as "safe" or "phishing"

### 2. **Feature Extraction** 🔍
The model looks at TWO types of features:

**A. Text Features** (What words are used?)
- Word combinations (n-grams): "verify your account"
- Character patterns: "p4ypal" vs "paypal"
- Word importance (TF-IDF): rare words = more important

**B. Numerical Features** (Suspicious behaviors?)
- How many URLs? (Phishing often has many links)
- How many "!" marks? (Urgency tactics)
- How many CAPITAL LETTERS? (Aggressive tone)
- How many $ signs? (Money-related)

### 3. **Handling Imbalance** ⚖️
Problem: More "safe" emails than "phishing" in dataset
Solution: **SMOTE** creates artificial phishing examples to balance

### 4. **Training** 🎓
The model learns patterns:
- "Free money" + many "!" → probably phishing
- "verify account" + many URLs → probably phishing
- Professional language + few links → probably safe

### 5. **Prediction** 🎯
New email arrives → Extract features → Model decides: Safe or Phishing?

---

## 📚 What Each Script Does

### `train_baseline.py`
**What it does:** Trains the phishing detector

**Key Features:**
- ✅ TF-IDF text analysis (word importance)
- ✅ Character n-grams (detects typos/obfuscation)
- ✅ SMOTE (balances dataset)
- ✅ Logistic Regression (fast & accurate)
- ✅ Optional Ensemble (LR + Random Forest)

**Command Options:**
```bash
--input FILE         # Path to CSV file
--out MODEL.pkl      # Where to save model
--test-size 0.2      # 20% data for testing
--ensemble           # Use ensemble (slower but better)
--no-smote           # Disable SMOTE
```

### `utils.py`
**What it does:** Helper functions

**Contains:**
- `load_data()` - Loads and cleans CSV
- `clean_text()` - Removes HTML, normalizes text
- `extract_numeric_features()` - Counts URLs, !, $, etc.

### `baseline_tfidf_lr.pkl`
**What it is:** Trained model file

**Used by:**
- Web application for real-time detection
- Can be loaded with `joblib.load()` for predictions
- Contains complete pipeline (feature extraction + classifier)

---

## 🧠 Understanding the Model

### Why These Features?

| Feature | Why Important? | Example |
|---------|----------------|---------|
| **URL Count** | Phishing emails have many malicious links | 5+ links suspicious |
| **"!" Count** | Creates false urgency | "ACT NOW!!!" |
| **Capital Ratio** | Aggressive/shouty tone | "URGENT ACTION REQUIRED" |
| **Character n-grams** | Detects deliberate misspellings | "micr0s0ft" vs "microsoft" |
| **Word trigrams** | Understands phrases in context | "verify your account now" |

### What is SMOTE?

**Problem:** Dataset has 60% safe, 40% phishing
**Issue:** Model might ignore phishing patterns
**Solution:** SMOTE creates fake phishing examples

**How?**
1. Take a phishing email
2. Find similar phishing emails
3. Create new examples "between" them
4. Now dataset is balanced 50/50

### What is TF-IDF?

**TF-IDF** = Term Frequency × Inverse Document Frequency

**Simple explanation:**
- Common words everywhere (the, and, is) → Low score
- Rare words in few emails (verify, account, urgent) → High score
- Helps model focus on important words

**Example:**
```
"verify your account immediately" 
- "verify" → rare → HIGH score
- "your" → common → LOW score
- "account" → rare → HIGH score
- "immediately" → medium → MEDIUM score
```

---

## 📊 Model Performance

### Current Results
```
              Precision  Recall  F1-Score
Safe Email       91%      86%     88%
Phishing         80%      87%     83%

Overall Accuracy: 86%
```

### What This Means

✅ **Good News:**
- Catches 87% of phishing emails (high recall)
- When it says "safe", it's right 91% of the time
- Balanced performance on both classes

⚠️ **Trade-offs:**
- 13% of phishing emails slip through (false negatives)
- 14% of safe emails marked suspicious (false positives)

### Confusion Matrix Explained
```
              Predicted
           Safe  Phishing
Actual Safe   1,947    318     ← 318 safe emails wrongly flagged
     Phishing   190  1,272     ← 190 phishing emails missed
```

---

## 🔧 Troubleshooting

### Common Issues

**1. "ModuleNotFoundError"**
```bash
Solution: pip install -r requirements.txt
```

**2. "FileNotFoundError: Phishing_Email.csv"**
```bash
Solution: Check file path with --input ../Phishing_Email.csv
```

**3. Training too slow**
```bash
Solution: Use smaller sample
python train_baseline.py --input ../Phishing_Email.csv --sample-frac 0.1
```

**4. Out of memory**
```bash
Solution: Reduce max_features in TfidfVectorizer
```

---

## 🎓 For Master Students

### Key ML Concepts Demonstrated

1. **Text Classification** - NLP task of categorizing documents
2. **Feature Engineering** - Creating informative features from raw data
3. **Class Imbalance** - Handling unequal class distributions
4. **Regularization** - Preventing overfitting (L2 penalty)
5. **Ensemble Learning** - Combining multiple models
6. **Cross-validation** - Proper train/test splitting
7. **Evaluation Metrics** - Precision, Recall, F1-Score

### Algorithms Used

- **TF-IDF Vectorization** - Text to numerical features
- **Logistic Regression** - Linear classifier with L2 regularization
- **SMOTE** - Synthetic oversampling for minority class
- **Random Forest** - Ensemble of decision trees (optional)

### Good Practices Applied

✅ Stratified train-test split (preserves class distribution)
✅ Pipeline architecture (reproducible workflow)
✅ Class weighting (handles imbalance)
✅ Regularization (prevents overfitting)
✅ Comprehensive evaluation (multiple metrics)

---

## 📝 Summary

This project shows how machine learning can solve real-world cybersecurity problems:

1. **Problem:** Detect phishing emails automatically
2. **Data:** 18,634 emails (60% safe, 40% phishing)
3. **Solution:** ML model with text + numerical features
4. **Result:** 86% accuracy with balanced performance
5. **Demo:** Interactive web application for real-time testing

**Key Takeaway:** Combining domain knowledge (what makes emails suspicious) with ML techniques (TF-IDF, SMOTE, Logistic Regression) creates an effective phishing detector.

**Try it:** See `../webapp/` for an interactive chat application that demonstrates the model in action!

---

## 📖 Further Reading

- **Main Report:** See `../README.md` for full academic report
- **Scikit-learn Docs:** https://scikit-learn.org/
- **SMOTE Paper:** Chawla et al., 2002
- **TF-IDF Explanation:** https://en.wikipedia.org/wiki/Tf%E2%80%93idf

---

**Questions?** Check the main README.md for detailed methodology and results.
