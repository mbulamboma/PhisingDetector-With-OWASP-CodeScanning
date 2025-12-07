# Copilot Instructions for PhishingDetector-With-OWASP-CodeScanning

These instructions orient AI coding agents to be productive immediately in this repo.

## Big Picture
- **Components:**
  - `phishing_detector/`: ML training pipeline (TF‑IDF + numeric features + SMOTE) and text utilities.
  - `webapp/`: Flask app serving a chat UI and using the trained model (`baseline_tfidf_lr.pkl`) for live phishing classification.
  - `security/`: OWASP Dependency-Check script and generated reports.
- **Data Flow:** CSV (`Phishing_Email.csv`) → preprocessing + feature extraction → model `.pkl` → loaded by Flask → classify chat messages; security scans audit `webapp` dependencies and store reports in `security/security-reports`.
- **Why this structure:** Keep ML training decoupled from the runtime app but reuse common preprocessing via `phishing_detector/utils.py`. Security tooling is isolated to keep scan artifacts out of app directories.

## Training Workflow
- **Entry point:** `phishing_detector/train_baseline.py`.
- **Dataset expectations:** CSV columns `Email Text`, `Email Type` → mapped to `text` and `type`; `label` is `1` if `type` contains "phishing" (case-insensitive), else `0`.
- **Pipeline:**
  - Word TF‑IDF (1–3 grams, `max_features=80000`, `min_df=2`, `max_df=0.95`, `sublinear_tf=True`).
  - Character TF‑IDF (3–5 grams, `max_features=20000`).
  - Numeric features from `utils.extract_numeric_features`: `url_count`, `email_count`, `phone_count`, `exclamation_count`, `question_count`, `dollar_count`, `digit_ratio`, `upper_ratio`, `word_count` (with safe division).
  - Classifier: LogisticRegression (`saga`, `C=0.3`, `penalty='l2'`, `class_weight='balanced'`, `max_iter=1000`). Optional ensemble adds RandomForest via `VotingClassifier`.
  - Class balancing: `SMOTE` enabled by default.
- **CLI args:**
  - `--input` CSV path (default `Phishing_Email.csv`).
  - `--out` model path (default `baseline_tfidf_lr.pkl`).
  - `--test-size` fraction (default `0.2`).
  - `--sample-frac` for quick runs (default `1.0`).
  - `--no-smote` to disable SMOTE; `--ensemble` to enable LR+RF voting.
- **Conventions:** Replace empty text with `'empty'` before vectorization. Always concatenate numeric + text features columns into a single `X` dataframe with a `text` column.

## Web App Workflow
- **Entry point:** `webapp/app.py`.
- **Model path:** `../phishing_detector/baseline_tfidf_lr.pkl` relative to `webapp`.
- **Preprocessing reuse:** Imports `clean_text` and `extract_numeric_features` from `phishing_detector/utils.py`; mirror training features exactly.
- **Classification:** `predict_phishing(message)` returns `(is_phishing, probability)`. A message is flagged only if `is_phishing` is `True` AND `probability > 0.73` (project-specific threshold to reduce false positives).
- **Persistence:** SQLite `chat.db` with table `messages (id, username, message, is_phishing, phishing_probability, timestamp)`; initialized via `init_db()` at app start.
- **Routes:**
  - `/` renders `templates/chat.html` and assigns session username.
  - `POST /set_username` sets session `username`.
  - `POST /send_message` analyzes and stores message.
  - `GET /get_messages` returns all messages.
  - `POST /clear_chat` truncates table.
- **Run locally:**
  - From `webapp/`: `pip install -r requirements.txt`; then `python app.py` → `http://localhost:5000`.

## Security Scans
- **Dependency audit:** `security/Run-SecurityScan.ps1` (Windows PowerShell v5.1). Requires Docker Desktop.
  - Scans `webapp/` dependencies using `owasp/dependency-check:latest`.
  - Outputs reports to `security/security-reports/` (`html`, `json`, `xml`, `sarif`, etc.) and opens the HTML report if present.
  - Usage:
    - From `security/`: `./Run-SecurityScan.ps1`.
- **Stored reports:** See `security/security-reports/` for prior results across formats.

## Patterns & Gotchas
- **Text cleaning:** Always sanitize via `clean_text()` (BeautifulSoup `lxml`) and normalize whitespace. Non-string inputs must return `""` and later be converted to `'empty'`.
- **Feature parity:** Keep webapp `predict_phishing` feature columns aligned with training pipeline; missing or reordered columns will break the model.
- **Model updates:** When retraining, ensure the webapp points to the new `.pkl` path and restart the server.
- **Session key:** `app.secret_key` is hardcoded for dev; do not commit production secrets.
- **Dependencies:** Large TF‑IDF `max_features` can increase memory; adjust only with corresponding training and webapp updates.

## Examples
- **Train with ensemble, no SMOTE:**
  - From repo root:
    - `cd phishing_detector`
    - `pip install -r requirements.txt`
    - `python train_baseline.py --ensemble --no-smote --out baseline_tfidf_ens.pkl`
- **Use new model in webapp:** Place `.pkl` under `phishing_detector/` and update `MODEL_PATH` in `webapp/app.py` accordingly.
- **Run security scan:**
  - `cd security`; `./Run-SecurityScan.ps1`

## File References
- `phishing_detector/train_baseline.py`: Training CLI and pipeline (TF‑IDF + numeric + SMOTE/ensemble).
- `phishing_detector/utils.py`: Cleaning, numeric feature extraction, CSV loading.
- `webapp/app.py`: Flask server, SQLite persistence, model inference, routes.
- `security/Run-SecurityScan.ps1`: OWASP Dependency-Check with Docker; outputs to `security/security-reports/`.
