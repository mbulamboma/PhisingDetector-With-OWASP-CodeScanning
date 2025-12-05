# Email Phishing Detector

A machine learning project that automatically detects phishing emails using text analysis.

**Project Info:**
- Author: MikaelX  
- Academic Year: 2024-2025  
- Field: Machine Learning & NLP
- Started: December 2024

## What This Does

This project trains a machine learning model to spot phishing emails by looking at patterns in the text. It can catch things like:

- Suspicious URLs and email addresses
- Weird punctuation usage (too many !!! or ???)
- Common phishing phrases
- Unusual writing patterns

## Quick Start

1. **Train the model:**
   ```bash
   cd phishing_detector
   python train_baseline.py
   ```

2. **Run the web demo:**
   ```bash
   cd webapp  
   python app.py
   ```
   Then go to http://localhost:5000

## How It Works

The system uses two main approaches:

1. **Text Analysis**: Looks at words, phrases, and writing patterns using TF-IDF
2. **Pattern Detection**: Counts suspicious elements like URLs, phone numbers, excessive punctuation

### The Model

- **Main algorithm**: Logistic Regression (good for text classification)
- **Features**: Word combinations + character patterns + suspicious element counts  
- **Class balancing**: Uses SMOTE to handle uneven data
- **Ensemble option**: Can combine multiple models for better accuracy

## Project Structure

```
phishing_detector/
├── train_baseline.py    # main training script
├── utils.py            # text processing functions
└── requirements.txt    # dependencies

webapp/
├── app.py             # flask web app
├── templates/         # web interface
└── chat.db           # stores messages

Phishing_Email.csv     # training data
```

## Features

**Text Processing:**
- Removes HTML tags and weird formatting
- Analyzes word combinations (1-3 words)
- Looks at character patterns (catches typos/obfuscation)

**Suspicious Element Detection:**
- URL count
- Email address count  
- Phone number count
- Exclamation marks and question marks
- Dollar signs
- Ratio of UPPERCASE letters
- Ratio of numbers vs letters

## Results

With the current setup, the model typically achieves:
- **Accuracy**: ~85-90%
- **Precision**: ~85% (few false alarms)
- **Recall**: ~90% (catches most phishing)

The web app flags messages as suspicious only when confidence > 73% to reduce false positives.

## File Details

### train_baseline.py
Main training script with options:
- `--input`: path to CSV file
- `--sample-frac`: use portion of data (for testing)
- `--ensemble`: use multiple models
- `--no-smote`: disable class balancing

### utils.py  
Helper functions for:
- Loading and cleaning email data
- Extracting numerical features
- Text preprocessing

### webapp/app.py
Flask web application that:
- Provides chat interface
- Runs phishing detection on messages
- Stores results in SQLite database

## Dataset

The training data (`Phishing_Email.csv`) contains:
- Email text content
- Labels (Safe Email / Phishing Email)
- Various email types and phishing techniques

## Dependencies

Main libraries used:
- scikit-learn (machine learning)
- pandas (data handling)
- beautifulsoup4 (HTML processing)
- imbalanced-learn (SMOTE)
- flask (web app)

## Future Improvements

Some ideas for making it better:
- Add more sophisticated text features
- Try deep learning approaches (BERT, etc.)
- Include email metadata (headers, sender info)
- Implement real-time learning from user feedback
- Add support for other languages

## Notes

- The model works best on English emails
- Performance depends on training data quality
- Web app is for demo purposes (don't use in production without security review)
- Model files can be large depending on feature count

## Getting Help

If something doesn't work:
1. Check that all dependencies are installed
2. Make sure the CSV file exists and has the right columns
3. Try with a smaller data sample first (`--sample-frac 0.1`)
4. Check the console output for error messages

Phishing attacks represent one of the most prevalent cybersecurity threats in the digital age. These attacks use fraudulent emails to deceive recipients into revealing sensitive information, downloading malware, or performing unauthorized actions. According to recent studies, phishing attacks account for over 80% of reported security incidents.

### Objectives

This project aims to:
1. Develop an automated system for detecting phishing emails
2. Apply machine learning techniques to text classification
3. Handle class imbalance in cybersecurity datasets
4. Evaluate and optimize model performance
5. Create a production-ready solution with comprehensive documentation

### Scope

The project encompasses:
- Exploratory Data Analysis (EDA)
- Feature engineering and text preprocessing
- Model training with multiple algorithms
- Performance evaluation and optimization
- Deployment-ready implementation

---

## Problem Statement

### Challenge

Traditional rule-based email filters struggle to keep pace with evolving phishing techniques. Attackers continuously develop new strategies to bypass detection systems, making static rules ineffective.

### Proposed Solution

We propose a machine learning approach that:
- **Learns patterns** from historical phishing and legitimate emails
- **Adapts automatically** to new phishing techniques
- **Combines multiple features** (text, numerical, behavioral)
- **Handles imbalanced data** using SMOTE
- **Provides probabilistic predictions** for risk assessment

### Success Criteria

- Accuracy: ≥ 85%
- Recall (Phishing detection): ≥ 85%
- Precision (Safe classification): ≥ 90%
- Low false negative rate (missed phishing emails)

---

## Dataset Description

### Source

**File:** `Phishing_Email.csv`  
**Total Samples:** 18,634 emails  
**Features:** Email text content and email type labels

### Class Distribution

| Class | Count | Percentage |
|-------|-------|------------|
| Safe (Legitimate) | 11,322 | 60.76% |
| Phishing | 7,312 | 39.24% |

### Class Imbalance

The dataset exhibits moderate class imbalance with a ratio of approximately 3:2 (safe:phishing). This imbalance is addressed through:
- Class weighting in the classifier
- SMOTE (Synthetic Minority Over-sampling Technique)
- Stratified train-test splitting

### Data Characteristics

- **Language:** Primarily English
- **Format:** Plain text and HTML emails
- **Content:** Headers, body text, URLs, and metadata
- **Quality:** Some emails contain HTML tags, special characters, and formatting

---

## Methodology

### 1. Data Preprocessing Pipeline

#### Text Cleaning
```python
- HTML tag removal using BeautifulSoup
- Whitespace normalization
- Text lowercasing
- Empty string handling
```

#### Feature Extraction

**A. Numerical Features (9 dimensions)**
- URL count: Number of hyperlinks
- Email address count: Email mentions in content
- Phone number count: Phone number occurrences
- Exclamation marks: Urgency indicators
- Question marks: Query patterns
- Dollar signs: Financial references
- Digit ratio: Proportion of numeric characters
- Uppercase ratio: Shouting/emphasis detection
- Word count: Email length metric

**B. Text Features (100,000 dimensions)**
- **Word n-grams (1-3):** Captures single words, bigrams, and trigrams
- **Character n-grams (3-5):** Detects obfuscation and typos
- **TF-IDF weighting:** Term Frequency-Inverse Document Frequency
- **Sublinear TF scaling:** Logarithmic term frequency scaling
- **Document frequency filtering:** Removes very common/rare terms

### 2. Feature Engineering Rationale

| Feature Type | Purpose | Example |
|--------------|---------|---------|
| URL Count | Phishing emails often contain multiple malicious links | 5+ URLs suspicious |
| Exclamation Count | Urgency creation tactics | "ACT NOW!!!" |
| Character n-grams | Detect obfuscated words | "p4ypal" instead of "paypal" |
| Word trigrams | Context understanding | "verify your account" |
| Uppercase Ratio | Aggressive tone detection | "URGENT ACTION REQUIRED" |

### 3. Machine Learning Models

#### Primary Model: Enhanced Logistic Regression
- **Algorithm:** L2-regularized Logistic Regression
- **Solver:** SAGA (Stochastic Average Gradient Descent)
- **Regularization:** C = 0.3 (strong regularization)
- **Class Weighting:** Balanced
- **Max Iterations:** 1,000

#### Advanced Option: Ensemble Model
- **Composition:** Logistic Regression + Random Forest
- **Voting Strategy:** Soft voting with probability averaging
- **Weights:** LR (1.2) : RF (1.0)
- **Random Forest Config:** 200 trees, max depth 20

### 4. Handling Class Imbalance

#### SMOTE (Synthetic Minority Over-sampling Technique)
- Generates synthetic samples for minority class (phishing)
- K-nearest neighbors: 5
- Applied after feature extraction, before training
- Balances training set to 1:1 ratio

#### Class Weighting
- Automatically adjusts loss function
- Penalizes misclassification of minority class more heavily
- Formula: `weight = n_samples / (n_classes * n_samples_per_class)`

### 5. Model Training Strategy

```
1. Load and clean data
2. Extract numerical features
3. Split data (80% train, 20% test) - stratified
4. Build feature transformation pipeline
5. Apply SMOTE to training data
6. Train classifier
7. Evaluate on test set
```

---

## System Architecture

### Project Structure

```
Megane/
│
├── Phishing_Email.csv           # Dataset
│
├── phishing_detector/           # Main package
│   ├── utils.py                 # Utility functions
│   ├── train_baseline.py        # Training script
│   ├── baseline_tfidf_lr.pkl    # Trained model (generated)
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # Technical documentation
│
├── webapp/                      # Web application
│   ├── app.py                   # Flask server
│   ├── templates/
│   │   └── chat.html           # Chat interface
│   ├── requirements.txt         # Web app dependencies
│   ├── chat.db                  # SQLite database (auto-generated)
│   └── README.md                # Web app documentation
│
└── README.md                    # This academic report
```

### Component Descriptions

#### `utils.py`
Core utility functions for data processing:
- `load_data()`: CSV loading and label encoding
- `clean_text()`: HTML removal and text normalization
- `extract_numeric_features()`: Behavioral feature extraction

#### `train_baseline.py`
Main training script with options:
- Standard training: TF-IDF + Logistic Regression + SMOTE
- Ensemble training: LR + Random Forest combination
- Configurable hyperparameters
- Comprehensive performance reporting
- Integrated evaluation (metrics and confusion matrix)

#### `webapp/`
Web-based demonstration application:
- Flask server with REST API
- Real-time phishing detection
- SQLite database for message storage
- Interactive chat interface
- Visual alerts for detected phishing

---

## Implementation Details

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.13+ |
| ML Framework | scikit-learn | 1.7+ |
| NLP | TfidfVectorizer | - |
| Imbalanced Learning | imbalanced-learn | 0.14+ |
| Data Processing | pandas, numpy | Latest |
| Text Parsing | BeautifulSoup4 | Latest |

### Key Algorithms

#### TF-IDF (Term Frequency-Inverse Document Frequency)

**Formula:**
```
TF-IDF(t, d) = TF(t, d) × IDF(t)

where:
TF(t, d) = log(1 + freq(t, d))  [sublinear scaling]
IDF(t) = log(N / df(t))

t = term
d = document
N = total documents
df(t) = document frequency of term t
```

**Purpose:** Identifies important words while reducing weight of common terms.

#### SMOTE Algorithm

**Process:**
```
For each minority sample:
  1. Find k nearest neighbors (k=5)
  2. Select random neighbor
  3. Generate synthetic sample:
     new_sample = sample + λ × (neighbor - sample)
     where λ ∈ [0, 1] is random
```

**Purpose:** Creates realistic synthetic phishing emails to balance training data.

#### Logistic Regression with L2 Regularization

**Optimization:**
```
min_w { -log P(y|X,w) + α||w||² }

where:
w = model weights
α = 1/C = regularization strength
C = 0.3 (strong regularization)
```

**Purpose:** Prevents overfitting while learning discriminative patterns.

---

## Experimental Results

### Training Configuration

```bash
# Standard Training (Recommended)
python train_baseline.py --input ../Phishing_Email.csv

# With Ensemble (Higher Accuracy)
python train_baseline.py --input ../Phishing_Email.csv --ensemble

# Without SMOTE (Baseline Comparison)
python train_baseline.py --input ../Phishing_Email.csv --no-smote
```

### Performance Metrics

#### Standard Model (TF-IDF + LR + SMOTE)

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Safe | 0.91 | 0.86 | 0.88 | 2,265 |
| Phishing | 0.80 | 0.87 | 0.83 | 1,462 |
| **Overall Accuracy** | | | **0.86** | **3,727** |

#### Confusion Matrix

```
                 Predicted
              Safe  Phishing
Actual Safe   1,947    318
    Phishing   190  1,272
```

**Interpretation:**
- **True Negatives (TN):** 1,947 - Correctly identified safe emails
- **False Positives (FP):** 318 - Safe emails marked as phishing (acceptable)
- **False Negatives (FN):** 190 - Missed phishing emails (minimize this)
- **True Positives (TP):** 1,272 - Correctly detected phishing

### Key Observations

1. **High Recall for Phishing (87%):** Successfully detects most phishing attempts
2. **Good Precision for Safe (91%):** Minimizes false alarms for users
3. **Balanced Performance:** SMOTE effectively addressed class imbalance
4. **Trade-off:** Slightly lower precision for phishing acceptable to minimize missed attacks

### Comparison: With vs Without SMOTE

| Metric | Without SMOTE | With SMOTE | Improvement |
|--------|---------------|------------|-------------|
| Phishing Recall | ~78% | ~87% | +9% |
| Overall F1-Score | ~0.82 | ~0.86 | +4.8% |
| Class Balance | Biased | Balanced | ✓ |

### Error Analysis

**False Positives (Safe → Phishing):**
- Legitimate marketing emails with multiple URLs
- Professional emails with urgent language
- Newsletters with promotional content

**False Negatives (Phishing → Safe):**
- Sophisticated phishing with minimal red flags
- Well-crafted social engineering
- Emails mimicking internal communication

---

## Model Performance

### Strengths

1. **Robust to Variations**
   - Character n-grams detect obfuscated text
   - Handles typos and intentional misspellings

2. **Efficient Processing**
   - Fast inference (~milliseconds per email)
   - Suitable for real-time filtering

3. **Interpretable Features**
   - Numerical features provide explainability
   - TF-IDF weights show important terms

4. **Adaptive Learning**
   - Can be retrained with new phishing examples
   - Incremental learning possible

### Limitations

1. **Context Understanding**
   - Limited semantic understanding
   - May miss context-dependent phishing

2. **Adversarial Robustness**
   - Vulnerable to deliberate evasion techniques
   - Requires periodic retraining

3. **Language Dependency**
   - Optimized for English emails
   - Performance may vary for other languages

4. **Feature Engineering**
   - Manual feature design required
   - Domain knowledge dependent

---

## Usage Instructions

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/MikaelX/Megane.git
cd Megane
```

#### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

#### 3. Install Dependencies
```bash
cd phishing_detector
pip install -r requirements.txt
```

### Training the Model

#### Basic Training
```bash
python train_baseline.py --input ../Phishing_Email.csv
```

**Output:**
- Trained model: `baseline_tfidf_lr.pkl`
- Training metrics printed to console
- Confusion matrix and classification report

#### Advanced Options

```bash
# Use ensemble model for higher accuracy
python train_baseline.py --input ../Phishing_Email.csv --ensemble

# Disable SMOTE (for comparison)
python train_baseline.py --input ../Phishing_Email.csv --no-smote

# Custom test split
python train_baseline.py --input ../Phishing_Email.csv --test-size 0.3

# Quick test with sample
python train_baseline.py --input ../Phishing_Email.csv --sample-frac 0.1
```

### Evaluating the Model

```bash
python evaluate_baseline.py --model baseline_tfidf_lr.pkl --input ../Phishing_Email.csv
```

### Web Application Demo

```bash
cd ../webapp
pip install -r requirements.txt
python app.py
```

**Open browser:** http://localhost:5000

**Features:**
- Interactive chat interface
- Real-time phishing detection
- Visual alerts and statistics
- Message history with predictions
- No authentication required (demo purposes)

---

## Conclusion

### Summary of Achievements

This project successfully demonstrates the application of machine learning to cybersecurity, specifically phishing email detection. Key accomplishments include:

1. **High Performance:** Achieved 86% accuracy with balanced precision and recall
2. **Bias Mitigation:** Effectively addressed class imbalance using SMOTE
3. **Feature Innovation:** Combined traditional NLP with behavioral features
4. **Production Ready:** Created deployable model with comprehensive documentation
5. **Scalability:** Efficient architecture suitable for real-time applications
6. **Practical Demonstration:** Built interactive web application showcasing real-time detection

### Scientific Contributions

- **Methodology:** Demonstrated effectiveness of SMOTE in cybersecurity datasets
- **Feature Engineering:** Combined word/character n-grams with numerical features
- **Practical Application:** Created usable tool for email security

### Future Work

#### Short-term Improvements
1. **Advanced NLP Models**
   - Implement BERT/RoBERTa for better semantic understanding
   - Use transformers for context-aware classification

2. **Feature Enhancement**
   - Add sender reputation scores
   - Include email header analysis (SPF, DKIM, DMARC)
   - Integrate URL reputation services

3. **Active Learning**
   - Implement feedback loop for model updates
   - Human-in-the-loop validation for uncertain predictions

#### Long-term Research Directions
1. **Multi-modal Learning**
   - Analyze email attachments
   - Image-based phishing detection
   - Combined text + image analysis

2. **Adversarial Robustness**
   - Test against adversarial examples
   - Develop robust training strategies
   - Implement detection of evasion attempts

3. **Cross-lingual Detection**
   - Extend to multiple languages
   - Multilingual transformer models
   - Transfer learning across languages

4. **Real-time System**
   - Deploy as email server plugin
   - Implement API service
   - Create browser extension

### Lessons Learned

1. **Data Quality:** Clean, well-labeled data is crucial for model performance
2. **Class Imbalance:** Cannot be ignored; SMOTE significantly improved results
3. **Feature Engineering:** Domain knowledge enhances model effectiveness
4. **Regularization:** Essential to prevent overfitting in high-dimensional spaces
5. **Evaluation:** Multiple metrics needed to assess security applications

### Personal Reflection

This Master 1 project provided invaluable experience in:
- Applying theoretical machine learning to practical problems
- Understanding the challenges of real-world data
- Balancing model complexity with performance
- Creating production-quality code and documentation
- Thinking critically about model limitations and ethics

The intersection of machine learning and cybersecurity presents fascinating challenges and opportunities. This project reinforced the importance of rigorous methodology, comprehensive evaluation, and ethical considerations in AI development.

---

## References

### Academic Papers

1. **Phishing Detection:**
   - Abu-Nimeh, S., et al. (2007). "A comparison of machine learning techniques for phishing detection." *Proceedings of the Anti-phishing Working Groups 2nd Annual eCrime Researchers Summit*.

2. **SMOTE Algorithm:**
   - Chawla, N. V., et al. (2002). "SMOTE: Synthetic Minority Over-sampling Technique." *Journal of Artificial Intelligence Research*, 16, 321-357.

3. **Text Classification:**
   - Joachims, T. (1998). "Text categorization with support vector machines: Learning with many relevant features." *European Conference on Machine Learning*.

4. **TF-IDF:**
   - Salton, G., & Buckley, C. (1988). "Term-weighting approaches in automatic text retrieval." *Information Processing & Management*, 24(5), 513-523.

### Technical Documentation

5. **Scikit-learn:** Pedregosa, F., et al. (2011). "Scikit-learn: Machine Learning in Python." *JMLR*, 12, 2825-2830.

6. **Imbalanced-learn:** Lemaître, G., et al. (2017). "Imbalanced-learn: A Python Toolbox to Tackle the Curse of Imbalanced Datasets in Machine Learning." *JMLR*, 18(17), 1-5.

### Online Resources

7. **Anti-Phishing Working Group (APWG):** https://apwg.org/
8. **Phishing.org:** Education and awareness resources
9. **Scikit-learn Documentation:** https://scikit-learn.org/

### Datasets

10. **Phishing Email Dataset:** Custom curated dataset for academic purposes

---

## Appendix

### A. Hyperparameter Tuning Details

| Parameter | Values Tested | Selected | Justification |
|-----------|---------------|----------|---------------|
| C (Regularization) | [0.1, 0.3, 0.5, 1.0] | 0.3 | Best validation accuracy |
| N-gram range (word) | [(1,1), (1,2), (1,3)] | (1,3) | Captures more context |
| N-gram range (char) | [(2,4), (3,5), (4,6)] | (3,5) | Balance coverage/sparsity |
| Max features | [50k, 80k, 100k] | 100k | Richer representation |
| SMOTE k-neighbors | [3, 5, 7] | 5 | Standard practice |

### B. System Requirements

**Minimum:**
- CPU: Intel i5 or equivalent
- RAM: 8 GB
- Storage: 5 GB free space
- OS: Windows 10/11, Linux, macOS

**Recommended:**
- CPU: Intel i7 or equivalent
- RAM: 16 GB
- Storage: 10 GB free space
- GPU: Optional, not required

### C. Troubleshooting

**Issue:** "ModuleNotFoundError: No module named 'imblearn'"
**Solution:** `pip install imbalanced-learn`

**Issue:** "ValueError: np.nan is an invalid document"
**Solution:** Already handled in code with `.fillna('empty')`

**Issue:** Training too slow
**Solution:** Use `--sample-frac 0.1` for quick testing

### D. Contact Information

**Author:** MikaelX  
**Institution:** [Your University Name]  
**Program:** Master 1 - Machine Learning  
**Email:** [Your Email]  
**GitHub:** https://github.com/MikaelX/Megane

---

## Acknowledgments

I would like to express my gratitude to:
- My academic advisor for guidance throughout this project
- The cybersecurity research community for datasets and inspiration
- The open-source community for excellent ML tools
- My peers for valuable feedback and discussions

---

**End of Report**

*This document serves as both the project README and academic report for the Master 1 Machine Learning project on Phishing Email Detection.*

**Last Updated:** December 2, 2025  
**Version:** 1.0
