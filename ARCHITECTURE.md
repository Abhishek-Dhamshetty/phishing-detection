# 📐 SYSTEM ARCHITECTURE & DESIGN DOCUMENTATION

## Overview

This document describes the complete architecture of the Phishing Detection System - a machine learning-based web application for identifying fake login pages.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   WEB BROWSER / CLIENT                   │
│              (http://127.0.0.1:5000)                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │           FRONTEND (HTML/CSS/JavaScript)         │  │
│  │  ┌─────────────┬──────────┬────────┬──────────┐ │  │
│  │  │   Single    │  Batch   │Feature │  About   │ │  │
│  │  │ Detection   │Detection │Analysis│          │ │  │
│  │  └─────────────┴──────────┴────────┴──────────┘ │  │
│  └──────────────────────────────────────────────────┘  │
│                      ↕ HTTP/JSON                        │
└─────────────────────────────────────────────────────────┘
                           ↕
                    CORS-enabled
                           ↕
┌─────────────────────────────────────────────────────────┐
│                  FLASK BACKEND SERVER                    │
│              (Python + scikit-learn)                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │              API LAYER (Routes)                   │  │
│  │  • /api/detect              [POST]               │  │
│  │  • /api/batch-detect        [POST]               │  │
│  │  • /api/analyze-features    [POST]               │  │
│  │  • /api/model-info          [GET]                │  │
│  │  • /api/health              [GET]                │  │
│  └──────────────────────────────────────────────────┘  │
│                           ↓                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │        PHISHING DETECTION ENGINE                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Feature Extractor                       │   │  │
│  │  │  • extract_url_features(url)             │   │  │
│  │  │  • extract_html_features(html, url)      │   │  │
│  │  │  • combine_features(url, html)           │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                      ↓                            │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  ML Classification                       │   │  │
│  │  │  • Random Forest Classifier              │   │  │
│  │  │  • Feature Scaling (StandardScaler)      │   │  │
│  │  │  • Confidence Scoring                    │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                      ↓                            │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Risk Analysis                           │   │  │
│  │  │  • Identify suspicious indicators        │   │  │
│  │  │  • Generate risk score (0-100)           │   │  │
│  │  │  • Provide explanations                  │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────┘  │
│                           ↓                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │           MODEL & DATA STORAGE                    │  │
│  │  • phishing_model.pkl (trained model + scaler)   │  │
│  │  • Feature columns metadata                       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Component Details

### 1. Frontend Layer

**Technology Stack:**

- HTML5 (semantic markup)
- CSS3 (responsive design)
- Vanilla JavaScript (ES6+)
- No external dependencies

**Components:**

#### Tab Navigation

- Single URL Detection
- Batch Detection
- Feature Analysis
- About/Information

#### Single Detection Tab

```
┌──────────────────────┐
│ URL Input Field      │
├──────────────────────┤
│ HTML Input Field     │
│ (optional)           │
├──────────────────────┤
│ Detect Button        │
├──────────────────────┤
│ Results Card         │
│ • Risk Label         │
│ • Confidence Score   │
│ • Risk Indicators    │
└──────────────────────┘
```

**Key JavaScript Functions:**

- `detectPhishing()` - Send URL to backend
- `displaySingleResult()` - Show results
- `showToast()` - Notifications
- `switchTab()` - Tab management
- `loadModelInfo()` - Fetch model details

---

### 2. Backend Layer

**Technology Stack:**

- Flask 3.0 (lightweight web framework)
- Python 3.9
- scikit-learn (machine learning)
- BeautifulSoup4 (HTML parsing)
- Requests (HTTP client)

**Application Structure:**

#### app.py (Flask Routes)

```python
@app.route('/api/detect', methods=['POST'])
├─ Validate URL
├─ Fetch HTML (if not provided)
├─ Call detector.detect()
└─ Return JSON response

@app.route('/api/batch-detect', methods=['POST'])
├─ Validate URL list
├─ Loop through URLs
├─ Call detector.detect() for each
└─ Return batch results

@app.route('/api/analyze-features', methods=['POST'])
├─ Extract features from URL
├─ Extract features from HTML
├─ Return feature dictionary

@app.route('/api/model-info', methods=['GET'])
└─ Return model metadata

@app.route('/api/health', methods=['GET'])
└─ Return server status
```

#### phishing_detector.py (Detection Engine)

```python
class PhishingDetector:
    ├─ __init__()
    │  └─ Load trained model from pickle
    ├─ detect(url, html_content)
    │  ├─ Extract features
    │  ├─ Scale features
    │  ├─ Predict with ML model
    │  ├─ Calculate confidence
    │  └─ Identify risk indicators
    ├─ _identify_risk_indicators()
    │  └─ Flag suspicious patterns
    └─ batch_detect(urls_and_html)
       └─ Process multiple URLs
```

#### feature_extractor.py (Feature Engineering)

**URL Features (15):**

1. `url_length` - Total characters
2. `domain_length` - Domain part length
3. `special_chars_in_url` - Count of `-`, `@`, `//`
4. `num_dots_in_domain` - Dots in domain
5. `subdomain_count` - Number of subdomains
6. `has_at_symbol` - Boolean
7. `has_redirect_chars` - `//` in path
8. `has_hyphen_in_domain` - Boolean
9. `has_ip_address` - Boolean
10. `has_https` - Boolean
11. `has_unusual_port` - Boolean
12. `url_entropy` - Randomness score
13. `num_query_params` - Query string parts
14. `common_tld` - Boolean
15. Plus additional metrics

**HTML Features (16):**

1. `num_forms` - Count of form elements
2. `num_input_fields` - Input count
3. `num_password_fields` - Password inputs
4. `has_login_keyword` - Boolean
5. `has_verify_keyword` - Boolean
6. `has_update_keyword` - Boolean
7. `num_links` - Hyperlink count
8. `num_external_links` - External URLs
9. `num_images` - Image count
10. `num_inline_scripts` - Script tags
11. `num_hidden_inputs` - Hidden fields
12. `has_form_action` - Boolean
13. `form_action_diff_domain` - Boolean
14. `suspicious_keyword_count` - Count
15. `form_to_element_ratio` - Float
16. `form_uses_relative_action` - Boolean

#### model_trainer.py (Model Training)

```python
class PhishingModelTrainer:
    ├─ generate_synthetic_data()
    │  ├─ Create legitimate samples
    │  └─ Create phishing samples
    ├─ train_model()
    │  ├─ Split train/test
    │  ├─ Scale features
    │  ├─ Train Random Forest
    │  └─ Evaluate performance
    └─ Save model + scaler
```

---

## 🤖 Machine Learning Pipeline

### Data Flow

```
Raw Input (URL + HTML)
    ↓
┌─────────────────────────────┐
│  Feature Extraction         │
│  • URL parsing             │
│  • HTML parsing            │
│  • Pattern matching        │
│  • Entropy calculation     │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Feature Vector            │
│  [f1, f2, f3, ... f31]     │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Feature Scaling            │
│  StandardScaler            │
│  (normalize to 0-1)        │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  ML Model Prediction        │
│  Random Forest Classifier   │
│  100 decision trees         │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Output Generation          │
│  • Prediction (0 or 1)      │
│  • Probability [P(0), P(1)] │
│  • Risk scanning            │
│  • Indicator identification │
└─────────────────────────────┘
    ↓
Final Output (JSON Response)
```

### Model Specifications

| Parameter         | Value                        |
| ----------------- | ---------------------------- |
| Algorithm         | Random Forest                |
| Trees             | 100                          |
| Max Depth         | 15                           |
| Min Samples Split | 5                            |
| Input Features    | 31                           |
| Output            | Binary (0=Legit, 1=Phishing) |
| Training Samples  | ~2000                        |

### Model Performance Metrics

```
Accuracy:  ~95%
Precision: ~91-93%
Recall:    ~90-92%
ROC-AUC:   ~0.94-0.96
```

---

## 💾 Data Flow in API

### Single Detection Request

```
Client Request (JSON)
{
  "url": "https://example.com",
  "html_content": "<html>...</html>"  // optional
}
    ↓
Flask Route Handler (/api/detect)
    ↓
Fetch HTML from URL (if not provided)
    ↓
PhishingDetector.detect()
    ├─ FeatureExtractor.combine_features()
    │  ├─ extract_url_features()
    │  └─ extract_html_features()
    │
    ├─ Create feature vector
    │
    ├─ Scale with StandardScaler
    │
    ├─ Predict with Random Forest
    │  ├─ classification (0 or 1)
    │  └─ probabilities [P(0), P(1)]
    │
    ├─ Calculate risk score
    │
    └─ Identify risk indicators

    ↓
JSON Response
{
  "success": true,
  "data": {
    "is_phishing": false,
    "confidence": 0.92,
    "risk_score": 8.0,
    "phishing_score": 8.0,
    "legitimate_score": 92.0,
    "risk_indicators": [...],
    "features_extracted": {...}
  }
}
```

---

## 🔄 Processing Pipeline

### Feature Extraction Process

```
URL Input
├─ Parse URL
│  ├─ Extract domain
│  ├─ Check protocol (http/https)
│  ├─ Count special characters
│  └─ Calculate entropy
│
├─ Domain Analysis
│  ├─ Check for hyphens
│  ├─ Count dots
│  ├─ Detect subdomains
│  └─ Identify TLD
│
├─ Security Checks
│  ├─ HTTPS presence
│  ├─ IP address detection
│  ├─ Unusual port detection
│  └─ Redirect patterns
│
└─ Feature Vector [14 features]

HTML Input (if provided)
├─ Parse with BeautifulSoup
│
├─ Form Analysis
│  ├─ Count forms
│  ├─ Find input fields
│  ├─ Detect password fields
│  ├─ Check form actions
│  └─ Identify hidden fields
│
├─ Content Analysis
│  ├─ Search for keywords(login, verify, update)
│  ├─ Count images
│  ├─ Count links
│  ├─ Detect scripts
│  └─ Analyze text
│
└─ Feature Vector [16 features]

Combined Feature Vector [31 features]
```

---

## 🎯 Risk Indicator Detection

The system identifies 15+ suspicious patterns:

```
URL-based Indicators:
├─ IP address instead of domain
├─ @ symbol in URL
├─ // redirect patterns
├─ Missing HTTPS
├─ Hyphen in domain
├─ Unusual port number
└─ Too long URL

HTML-based Indicators:
├─ Multiple password fields
├─ Form action different domain
├─ Verify/Confirm keywords
├─ Update/Upgrade keywords
├─ Too many external links
├─ Excessive scripts
├─ Hidden input fields
└─ Relative form action URL

Behavioral Indicators:
├─ Form to element ratio
├─ Script density
├─ Link composition
└─ Keyword clustering
```

---

## 📊 Request/Response Examples

### Example 1: Legitimate Website

**Request:**

```json
{
  "url": "https://google.com"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "is_phishing": false,
    "confidence": 0.98,
    "risk_score": 2.0,
    "legitimate_score": 98.0,
    "phishing_score": 2.0,
    "risk_indicators": [
      "Multiple inline scripts detected",
      "Form uses relative action URL"
    ],
    "features_extracted": {
      "url_length": 18,
      "has_https": 1,
      "common_tld": 1
    }
  }
}
```

### Example 2: Suspicious Website

**Request:**

```json
{
  "url": "https://g00gl-verify.xyz/login"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "is_phishing": true,
    "confidence": 0.89,
    "risk_score": 89.0,
    "legitimate_score": 11.0,
    "phishing_score": 89.0,
    "risk_indicators": [
      "Domain contains hyphen (common in phishing)",
      "Unusual domain structure",
      "Non-standard TLD"
    ],
    "features_extracted": {
      "url_length": 30,
      "has_hyphen_in_domain": 1,
      "has_https": 1,
      "num_forms": 2
    }
  }
}
```

---

## 🔐 Security Considerations

### Input Validation

- URL format validation
- HTML content size limits
- Timeout protection
- Request rate limiting (future)

### Data Processing

- No data persistence
- No user tracking
- Local processing only
- Stateless API

### Error Handling

- Try-catch blocks
- Graceful degradation
- Safe defaults
- Informative error messages

---

## ⚙️ Configuration

### Model Configuration

```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
```

### Flask Configuration

```python
app.config['JSON_SORT_KEYS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
DEBUG_MODE = True
PORT = 5000
```

### Feature Scaling

```python
StandardScaler()
# Scales features to mean=0, std=1
```

---

## 🚀 Scalability & Performance

### Current Performance

- Single detection: <500ms (URL only)
- With HTML fetch: <2-5 seconds
- Batch (4 URLs): ~8-10 seconds
- Inference: <50ms per URL

### Optimization Opportunities

1. **Caching** - Cache model predictions
2. **Async Processing** - Queue-based batch jobs
3. **Content Delivery** - CDN for static files
4. **Database** - Cache detected URLs
5. **Image Optimization** - Reduce asset sizes

---

## 🧪 Testing Strategy

### Unit Tests

- Feature extraction functions
- URL parsing logic
- Risk indicator identification

### Integration Tests

- API endpoints
- Model predictions
- End-to-end flow

### Performance Tests

- Response time benchmarks
- Concurrent requests
- Memory usage
- Model inference speed

---

## 📈 Future Enhancements

### Short Term

- [ ] Database integration for caching
- [ ] User authentication
- [ ] Detection history
- [ ] Custom model retraining

### Medium Term

- [ ] Deep Learning models (CNN/LSTM)
- [ ] Visual similarity detection
- [ ] WHOIS domain analysis
- [ ] Screenshot-based detection

### Long Term

- [ ] Real-time threat intelligence
- [ ] Browser extension
- [ ] Mobile app
- [ ] Cloud deployment
- [ ] REST API for third parties

---

## 📚 References & Technologies

### Libraries Used

```
Flask 3.0.0          - Web framework
scikit-learn 1.3.0   - Machine learning
numpy 1.24.3         - Numerical computing
pandas 2.0.3         - Data manipulation
beautifulsoup4 4.12.2 - HTML parsing
requests 2.31.0      - HTTP client
```

### Design Patterns

- MVC (Model-View-Controller)
- Factory Pattern (model loading)
- API Gateway Pattern
- Separation of Concerns

---

## 📞 Support & Troubleshooting

See QUICK_START.md for quick setup and common issues.

See README.md for comprehensive documentation.

---

**Architecture Document v1.0**  
_Comprehensive design documentation for the Phishing Detection System_
