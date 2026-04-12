# 🚀 QUICK START GUIDE

## System Overview

A **Machine Learning-based Phishing Detection System** that analyzes webpages to identify fake login pages.

### ✨ Key Features

- ✅ Single URL detection with confidence scoring
- ✅ Batch analysis (up to 10 URLs at once)
- ✅ Detailed feature extraction (31 features)
- ✅ Risk indicator identification
- ✅ HTML content analysis
- ✅ Beautiful web interface

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## 🎯 Fast Setup (< 2 minutes)

### Step 1: Install Dependencies

```bash
cd /Users/abhishekdhamshetty/Desktop/cyber
pip install -r backend/requirements.txt
```

### Step 2: Start the Backend Server

```bash
# Terminal Window 1
cd backend
python app.py
```

You should see:

```
Running on http://127.0.0.1:5000
```

### Step 3: Open the Web Interface

```
http://127.0.0.1:5000
```

Then either:

- Open in your browser: `http://127.0.0.1:5000`
- Or open the HTML file directly: `frontend/index.html`

---

## 🧪 Test the System

### Option 1: Quick Manual Test

1. Go to http://127.0.0.1:5000
2. Paste a URL in the input field
3. Click "🔍 Detect Phishing"
4. View results with confidence scores

**Test URLs:**

- Legitimate: `https://google.com`, `https://amazon.com`
- Phishing: `https://goog1e-secure.xyz`, `https://amaz0n-login.ru`

### Option 2: Run Automated Tests

```bash
python test_api.py
```

Expected output:

```
✨ All tests passed! System is working correctly.
```

---

## 💻 How to Use

### 1️⃣ Single URL Detection

- **Enter URL** → **Click "Detect"** → Get results with risk score

### 2️⃣ Batch Detection

- **Enter multiple URLs** (one per line) → **Click "Check All"** → Get summary

### 3️⃣ Feature Analysis

- **Enter URL** → **Click "Extract"** → View 31 extracted features

### 4️⃣ Learn More

- Click **"About"** tab for system details and technologies

---

## 📊 Understanding Results

### Risk Scoring

- **0-30%**: ✅ Likely Legitimate
- **30-70%**: ⚠️ Suspicious (needs review)
- **70-100%**: 🚨 Likely Phishing

### Confidence Score

- Higher = More certain about classification
- 0.0 to 1.0 scale (0-100%)

### Risk Indicators

Red flags detected:

- ✗ Missing HTTPS
- ✗ IP address in URL
- ✗ Multiple password fields
- ✗ Form submits to different domain
- ✗ Suspicious keywords
- ✗ Hidden input fields

---

## 🔧 API Endpoints

All accessible via `http://127.0.0.1:5000/api`

| Endpoint            | Method | Purpose               |
| ------------------- | ------ | --------------------- |
| `/detect`           | POST   | Analyze single URL    |
| `/batch-detect`     | POST   | Analyze multiple URLs |
| `/analyze-features` | POST   | Extract features      |
| `/model-info`       | GET    | Model details         |
| `/health`           | GET    | Server status         |

### Example API Call

```bash
curl -X POST http://127.0.0.1:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

## 🛠️ Troubleshooting

### "Cannot connect to backend"

```bash
# Make sure Flask server is running in another terminal
cd backend
python app.py
```

### "Port 5000 already in use"

```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### "ModuleNotFoundError"

```bash
# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Slow Response Time

- First detection takes longer (loading HTML from web)
- Subsequent detections are faster
- Feature extraction is the bottleneck

---

## 📁 File Structure

```
cyber/
├── backend/                 # Python backend
│   ├── app.py              # Flask server (START HERE)
│   ├── phishing_detector.py # Detection logic
│   ├── feature_extractor.py # Feature analysis
│   ├── model_trainer.py    # ML model training
│   └── requirements.txt    # Python packages
├── frontend/               # Web interface
│   ├── index.html          # Main page
│   ├── css/style.css       # Styling
│   └── js/app.js           # Frontend logic
├── data/
│   └── phishing_model.pkl  # Trained ML model
├── test_api.py            # Automated tests
└── README.md              # Full documentation
```

---

## 🎓 How It Works

1. **User Input** → URL or HTML content
2. **Feature Extraction** → 31 features calculated
3. **ML Prediction** → Random Forest classifier
4. **Risk Analysis** → Identify suspicious indicators
5. **Results Display** → Confidence + Risk indicators

### Features Analyzed

**URL Features (15):**

- Length, domain structure, special characters
- HTTPS presence, IP addresses, subdomains

**HTML Features (16):**

- Forms, input fields, password fields
- Links, scripts, keywords, form actions

---

## 📊 System Performance

- **Accuracy**: ~95%
- **Inference Time**: <500ms (URL only) | <2s (with HTML)
- **Model Type**: Random Forest (100 trees)
- **Training Data**: ~2000 synthetic samples

---

## 🔐 Security Notes

⚠️ **For Educational Use Only**

- Not a replacement for browser security
- Use with other security tools
- Limited by training data
- Sophisticated attacks may evade detection

---

## 🌟 What Works Well

✅ Common phishing patterns (typosquatting, suspicious domains)  
✅ Login form detection  
✅ HTTPS/SSL analysis  
✅ Domain age and structure  
✅ Form behavior analysis

## ⚠️ Known Limitations

❌ JavaScript-rendered content  
❌ Encrypted form analysis  
❌ Real-time URL geolocation  
❌ WHOIS domain info  
❌ Visual similarity detection

---

## 🚀 Extended Features

Try running tests:

```bash
python test_api.py  # Run all API tests
```

Access model info:

```bash
curl http://127.0.0.1:5000/api/model-info
```

Check server health:

```bash
curl http://127.0.0.1:5000/api/health
```

---

## 💡 Pro Tips

1. **Combine with Browser Tools**: Use alongside uBlock, ScriptSafe
2. **Check Multiple Attributes**: Look at both URL and risk indicators
3. **Be Suspicious of Urgency**: Phishing often requires immediate action
4. **Verify Official Channels**: Always verify through official websites
5. **Enable 2FA**: Protects even if credentials are stolen

---

## 📞 Support

Check **README.md** for detailed documentation.

Common issues resolved in troubleshooting section.

---

## 🎉 You're Ready!

1. ✅ Backend running
2. ✅ Frontend accessible
3. ✅ Tests passing
4. ✅ Start detecting phishing!

**Happy analyzing! 🛡️**

---

_Phishing Detection System v1.0_  
_Built with Flask, scikit-learn, and ❤️_
