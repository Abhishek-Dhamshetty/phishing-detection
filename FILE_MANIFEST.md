# 📂 PROJECT FILE STRUCTURE & DESCRIPTIONS

## Complete Directory Tree

```
/Users/abhishekdhamshetty/Desktop/cyber/
│
├── 📄 README.md                    # Main documentation (comprehensive)
├── 📄 QUICK_START.md               # Quick setup guide (< 5 min)
├── 📄 ARCHITECTURE.md              # System design documentation
├── 📄 FILE_MANIFEST.md             # This file
├── 🐍 test_api.py                  # Automated API tests
│
├── 📁 backend/                     # Python Flask Application
│   ├── 🐍 app.py                   # Flask server & routes (MAIN ENTRY)
│   ├── 🐍 phishing_detector.py      # ML detection logic
│   ├── 🐍 feature_extractor.py      # Feature extraction
│   ├── 🐍 model_trainer.py          # Model training script
│   └── 📋 requirements.txt          # Python dependencies
│
├── 📁 frontend/                    # Web Interface
│   ├── 📄 index.html               # Main HTML page
│   ├── 📁 css/
│   │   └── 🎨 style.css            # Complete styling (responsive)
│   └── 📁 js/
│       └── 📜 app.js               # Frontend logic (vanilla JS)
│
├── 📁 data/                        # ML Model & Data
│   └── 🗂️  phishing_model.pkl      # Trained model (auto-generated)
│
└── 📁 .venv/                       # Python virtual environment (auto-created)
    └── [Python packages]           # All installed dependencies
```

---

## 📋 File Descriptions

### 📄 Documentation Files

#### `README.md` (5,000+ words)

**Purpose:** Comprehensive project documentation  
**Contains:**

- Project overview
- Features and capabilities
- Installation instructions
- API documentation
- Usage examples
- Troubleshooting guide
- Technologies used
- Future improvements

**When to read:** For complete understanding of the system

#### `QUICK_START.md`

**Purpose:** Fast setup guide for quick testing  
**Contains:**

- Fast 2-minute setup
- Manual testing steps
- Automated test instructions
- API endpoint examples
- Troubleshooting quick fixes
- Pro tips

**When to read:** To get running quickly

#### `ARCHITECTURE.md`

**Purpose:** Technical design and system architecture  
**Contains:**

- System architecture diagrams
- Component details
- ML pipeline explanation
- Data flow diagrams
- Feature descriptions
- Performance metrics
- Future enhancements

**When to read:** To understand how system works internally

#### `FILE_MANIFEST.md`

**Purpose:** File listing and descriptions  
**Contains:** This documentation

---

### 🐍 Python Backend Files

#### `backend/requirements.txt`

**Purpose:** List of Python dependencies  
**Important Packages:**

```
Flask==3.0.0              - Web framework
Flask-CORS==4.0.0         - Cross-origin requests
scikit-learn==1.3.0       - Machine learning
numpy==1.24.3             - Numerical arrays
pandas==2.0.3             - Data manipulation
beautifulsoup4==4.12.2    - HTML parsing
requests==2.31.0          - HTTP requests
```

**Usage:** `pip install -r backend/requirements.txt`

---

#### `backend/app.py` (200+ lines)

**Purpose:** Flask web server and API routes

**Key Routes:**

```python
GET  /                      # Serve frontend
POST /api/detect            # Single URL detection
POST /api/batch-detect      # Multiple URL detection
POST /api/analyze-features  # Feature extraction
GET  /api/model-info        # Model details
GET  /api/health            # Server health check
```

**Key Functions:**

- `init_detector()` - Initialize ML model
- `detect_phishing()` - Process single URL
- `batch_detect()` - Process multiple URLs
- `analyze_features()` - Extract features
- `before_request()` - Initialization handler

**How to run:**

```bash
cd backend
python app.py
```

Server starts on `http://127.0.0.1:5000`

---

#### `backend/phishing_detector.py` (200+ lines)

**Purpose:** ML-based phishing detection engine

**Key Class:** `PhishingDetector`

**Methods:**

```python
__init__(model_path)                # Load model
load_model(path)                    # Load from pickle
detect(url, html_content)           # Analyze URL
batch_detect(urls_and_html)         # Batch analysis
_identify_risk_indicators(features) # Find red flags
```

**Output Includes:**

- Phishing prediction (True/False)
- Confidence score (0-1)
- Risk score (0-100)
- Risk indicators (descriptive)
- Extracted features

---

#### `backend/feature_extractor.py` (300+ lines)

**Purpose:** Extract 31 features from URLs and HTML

**Key Class:** `FeatureExtractor`

**Methods:**

```python
extract_url_features(url)           # 15 URL features
extract_html_features(html, url)    # 16 HTML features
combine_features(url, html)         # Both + combined
_calculate_entropy(text)            # Randomness score
```

**URL Features (15):**

- url_length, domain_length
- special_chars, dots_count, subdomains
- has_at_symbol, has_redirect_chars
- has_hyphen, has_ip_address
- has_https, has_unusual_port
- url_entropy, num_query_params
- common_tld

**HTML Features (16):**

- num_forms, num_input_fields
- num_password_fields
- has_login_keyword, has_verify_keyword
- has_update_keyword
- num_links, num_external_links
- num_images, num_inline_scripts
- num_hidden_inputs
- has_form_action, form_action_diff_domain
- suspicious_keyword_count
- form_to_element_ratio
- form_uses_relative_action

---

#### `backend/model_trainer.py` (200+ lines)

**Purpose:** Train and save the ML model

**Key Class:** `PhishingModelTrainer`

**Methods:**

```python
generate_synthetic_data(num_samples)  # Create training data
train_model(output_path)              # Train Random Forest
```

**Produces:**

- `phishing_model.pkl` - Saved model
- Contains model + scaler + feature columns
- Auto-triggered on first run if model missing

**Running manually:**

```bash
cd backend
python model_trainer.py
```

---

### 🌐 Frontend Files

#### `frontend/index.html` (300+ lines)

**Purpose:** Main web interface

**Structure:**

```html
<header>
  <!-- Title & branding -->
  <nav>
    <!-- Tab navigation -->
    <main>
      <!-- Tab content -->
      ├─ Single URL Detection ├─ Batch Detection ├─ Feature Analysis └─
      About/Info
      <footer><!-- Footer --></footer>
    </main>
  </nav>
</header>
```

**Key Elements:**

- Input fields (URL, HTML, batch)
- Result displays
- Loading spinners
- Toast notifications
- Model information section

**No external libraries** - Pure HTML5

---

#### `frontend/css/style.css` (800+ lines)

**Purpose:** Complete responsive styling

**Features:**

- Mobile-responsive design
- Color-coded results (phishing/legitimate)
- Smooth animations
- Professional UI/UX
- Dark/light compatible
- Accessibility features

**CSS Variables:**

```css
--primary-color: #2563eb /* Blue */ --danger-color: #dc2626 /* Red */
  --success-color: #16a34a /* Green */ --warning-color: #ea580c /* Orange */;
```

**Responsive Breakpoints:**

- Desktop: 1024px+
- Tablet: 768px - 1024px
- Mobile: < 768px

---

#### `frontend/js/app.js` (500+ lines)

**Purpose:** Frontend logic and API communication

**Key Functions:**

```javascript
switchTab(tabName); // Switch tabs
showToast(message, type); // Notifications
detectPhishing(url, html); // Single detection
displaySingleResult(result); // Show results
performBatchDetection(urls); // Batch detection
extractFeatures(url); // Feature analysis
loadModelInfo(); // Load model details
```

**No External Dependencies** - Vanilla JavaScript ES6+

**Features:**

- Fetch API calls
- Error handling
- Toast notifications
- Tab management
- Result formatting
- Form validation

---

### 🧪 Testing File

#### `test_api.py` (200+ lines)

**Purpose:** Automated API testing

**Test Cases:**

1. Health check
2. Model information
3. Single legitimate detection
4. Single phishing detection
5. Batch detection
6. Feature extraction

**Usage:**

```bash
python test_api.py
```

**Expected Output:**

```
✨ All tests passed! System is working correctly.
Total: 6/6 tests passed
```

---

### 💾 Data Files

#### `data/phishing_model.pkl`

**Purpose:** Trained ML model

**Contents:**

- Random Forest Classifier (100 trees)
- StandardScaler (feature normalization)
- Feature column names (metadata)

**Generated by:** `model_trainer.py` (first run)

**Size:** ~5-10 MB

**Format:** Python pickle binary

---

## 🔄 Data Flow Diagram

```
User Input (Browser)
    ↓
Frontend (HTML/CSS/JS)
    ├─ Validate input
    ├─ Show loading spinner
    └─ Make Fetch API call
    ↓
Backend (Flask app.py)
    ├─ Receive JSON request
    ├─ Validate parameters
    └─ Route to appropriate handler
    ↓
Feature Extraction (feature_extractor.py)
    ├─ Parse URL
    ├─ Fetch/Parse HTML
    ├─ Extract 31 features
    └─ Return feature vector
    ↓
ML Detection (phishing_detector.py)
    ├─ Load trained model
    ├─ Scale features
    ├─ Predict class
    ├─ Calculate confidence
    └─ Identify risk indicators
    ↓
Backend Response (JSON)
    ├─ is_phishing: boolean
    ├─ confidence: float
    ├─ risk_score: float
    ├─ risk_indicators: array
    └─ features_extracted: dict
    ↓
Frontend Display
    ├─ Hide loading
    ├─ Show results card
    ├─ Format confidence
    ├─ Display indicators
    └─ Highlight result type
    ↓
User sees phishing detection result ✓
```

---

## 🚀 Typical Workflow

### First Time Setup

```bash
1. cd /Users/abhishekdhamshetty/Desktop/cyber
2. pip install -r backend/requirements.txt
3. cd backend
4. python app.py
   → Trains model (~30 seconds)
   → Starts server on port 5000
5. Open http://127.0.0.1:5000
6. Test detection
```

### Regular Usage

```bash
1. Start backend:
   cd backend && python app.py

2. Open frontend:
   http://127.0.0.1:5000

3. Enter URL or HTML

4. View results

5. Stop with Ctrl+C
```

---

## 📊 File Size Summary

| File                 | Lines     | Size      | Purpose             |
| -------------------- | --------- | --------- | ------------------- |
| app.py               | 200+      | 8KB       | Flask server        |
| phishing_detector.py | 200+      | 9KB       | ML detection        |
| feature_extractor.py | 320+      | 14KB      | Features            |
| model_trainer.py     | 180+      | 7KB       | Training            |
| index.html           | 250+      | 12KB      | Web UI              |
| style.css            | 800+      | 28KB      | Styling             |
| app.js               | 500+      | 18KB      | JS logic            |
| test_api.py          | 200+      | 8KB       | Tests               |
| phishing_model.pkl   | -         | 8MB       | ML model            |
| **Total**            | **2500+** | **112KB** | **Complete system** |

---

## 🔑 Key Configuration Files

### Flask Configuration (in app.py)

```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.run(debug=True, port=5000, use_reloader=False)
```

### Feature Configuration (in feature_extractor.py)

```python
# URL parsing
common_tlds = ['com', 'org', 'net', 'edu', 'gov', 'co', 'uk', 'de', 'fr', 'it']

# Suspicious keywords
suspicious_keywords = ['confirm', 'verify', 'validate', 'authenticate', 'secure', ...]
```

### Model Configuration (in model_trainer.py)

```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)
```

---

## 🎯 Quick File Navigation

**Want to:**

- **Start the server?** → Run `backend/app.py`
- **Add new features?** → Edit `backend/feature_extractor.py`
- **Modify ML model?** → Edit `backend/model_trainer.py`
- **Change detection logic?** → Edit `backend/phishing_detector.py`
- **Modify UI?** → Edit `frontend/index.html` or `frontend/css/style.css`
- **Fix frontend bugs?** → Edit `frontend/js/app.js`
- **Run tests?** → Execute `test_api.py`
- **Deploy?** → See deployment section in README.md

---

## 💻 Environment Details

### Python Version

```bash
Python 3.9.6 (minimum 3.8)
```

### Virtual Environment

```bash
Location: /Users/abhishekdhamshetty/Desktop/cyber/.venv
Type: venv (built-in)
```

### Package Versions

See `backend/requirements.txt` for exact versions

### Node/npm

Not required - no frontend build process needed!

---

## 🔒 Important Files to Backup

1. `backend/phishing_model.pkl` - The trained model
2. `backend/feature_extractor.py` - Core feature logic
3. `frontend/index.html` - Main interface
4. `README.md` - Documentation

---

## 📝 File Modification Guidelines

**Safe to modify:**

- CSS stylesheets
- Frontend HTML
- Configuration values
- API routes

**Careful with:**

- Feature extraction logic
- Model training code
- Feature column names
- Database operations (when added)

**Should not modify:**

- Pickle model file directly
- Python module imports (unless updating deps)

---

## 🚀 File Dependencies

```
app.py
├─ phishing_detector.py
│  └─ feature_extractor.py
├─ model_trainer.py
│  └─ feature_extractor.py
└─ Flask, CORS, requests

Frontend
├─ index.html
│  ├─ css/style.css
│  └─ js/app.js
└─ No external libraries

test_api.py
├─ requests library
└─ api routes (Flask)
```

---

## 📚 Learning Path

**For Beginners:**

1. Read QUICK_START.md (5 min)
2. Run the system locally (5 min)
3. Test with examples (10 min)
4. Read README.md (20 min)

**For Developers:**

1. Read ARCHITECTURE.md (15 min)
2. Study `feature_extractor.py` (20 min)
3. Review `phishing_detector.py` (15 min)
4. Understand `app.py` routes (15 min)
5. Explore `app.js` (15 min)

**For Data Scientists:**

1. Study `model_trainer.py` (20 min)
2. Review feature engineering (30 min)
3. Analyze training data (20 min)
4. Experiment with parameters (varies)

---

**File Manifest v1.0**  
_Complete documentation of all project files and their purposes_
