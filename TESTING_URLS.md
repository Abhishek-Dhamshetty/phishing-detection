# 🧪 PHISHING DETECTION TESTING GUIDE

## ⚠️ IMPORTANT: Safe Testing Only

**DO NOT** test with real active phishing URLs as they:

- May be malicious
- Could trigger antivirus warnings
- May contain actually harmful code
- Could get your IP flagged

Instead, use these **educational/safe testing URLs**:

---

## ✅ TEST LEGITIMATE WEBSITES

```
https://www.google.com
https://www.amazon.com
https://www.github.com
https://www.linkedin.com
https://www.facebook.com
https://www.apple.com
https://www.microsoft.com
https://www.netflix.com
https://www.instagram.com
https://www.twitter.com
https://www.youtube.com
https://www.reddit.com
https://www.wikipedia.org
https://www.stackoverflow.com
https://www.dropbox.com
```

**Expected Result:** ✅ LEGITIMATE (Low risk score, 90%+ confidence)

---

## ⚠️ TEST PHISHING PATTERNS (Safe Variants)

These are **fake URLs** that mimic phishing patterns but are controlled/safe:

### Pattern 1: Domain Typosquatting

```
https://goog1e.com                    (0=O, 1=L)
https://amaz0n-login.com              (0=O)
https://faceboo-k.com                 (split domain)
https://gogle123.ru                   (wrong TLD + typo)
```

### Pattern 2: Subdomain Obfuscation

```
https://google.secure-verify.com
https://amazon-login-verify.net
https://paypal-update.xyz
https://apple-confirm.tk
```

### Pattern 3: IP Address Usage

```
http://192.168.1.1/login
http://10.0.0.1/verify
http://172.16.0.1/secure
```

### Pattern 4: Suspicious TLDs

```
https://google-login.ru
https://amazon-verify.tk
https://paypal-confirm.xyz
https://bank-secure.info
```

### Pattern 5: Redirect Characters

```
https://google.com@phishing.com
https://amazon.com//verify
https://paypal..com/login
```

### Pattern 6: URL Encoding Tricks

```
https://goo%67le.com
https://ama%7aon.com
https://pay%70al.com
```

**Expected Result:** ⚠️ PHISHING (High risk score, 80%+ confidence)

---

## 📊 BATCH TEST SCRIPT

Run all at once in **Batch Detection** tab:

```
https://www.google.com
https://goog1e-login.xyz
https://www.amazon.com
https://amaz0n-verify.ru
https://github.com
https://github-secure.net
https://paypal.com
https://paypa1-confirm.com
https://apple.com
https://apple-update.tk
```

**Expected Result:**

- Legitimate: 5 ✅
- Phishing: 5 ⚠️

---

## 🔬 REAL-WORLD PHISHING SIMULATORS (Educational)

### Phishtank - Educational Database

```
https://www.phishtank.com/
```

Get test URLs from their educational section

### APWG (Anti-Phishing Working Group)

```
https://www.apwg.org/
```

Research organization for phishing studies

### Testsites for Security Testing

```
https://www.eicar.org/
https://www.phishery.com/
```

---

## 🧩 CUSTOM TEST CASES

Create your own test patterns:

### Format: [Legitimate_Domain]\_[Phishing_TLD/Pattern]

```
Bank Phishing:
https://bank-verify.ru
https://banking-secure.xyz
https://bankofamerica-login.tk

Email Phishing:
https://gmail-security.com
https://outlook-verify.net
https://mail-confirm.xyz

Payment Phishing:
https://stripe-update.ru
https://paypal-confirm.xyz
https://square-verify.tk
```

---

## 🎯 QUICK TEST (5 minutes)

### Test Set 1: Obviously Legitimate

```
https://www.google.com
https://www.github.com
https://www.wikipedia.org
```

**Should be detected as:** ✅ ALL LEGITIMATE

### Test Set 2: Obviously Phishing

```
https://g00gl3-login.ru
https://gith0b-security.xyz
https://wikip3edia-verify.tk
```

**Should be detected as:** ⚠️ ALL PHISHING

### Test Set 3: Edge Cases

```
https://google.secure-login.com
https://github-auth.net
https://wikipedia.verify.org
```

**Should be detected as:** Mixed results (some questionable)

---

## 🚀 RUN AUTOMATED TESTS

The system already has built-in tests:

```bash
cd /Users/abhishekdhamshetty/Desktop/cyber
./.venv/bin/python test_api.py
```

**Output:**

```
✓ PASSED: Health Check
✓ PASSED: Model Info
✓ PASSED: Legitimate Detection
✓ PASSED: Phishing Detection
✓ PASSED: Batch Detection
✓ PASSED: Feature Extraction
```

---

## 📈 ACCURACY VALIDATION

### Expected Performance

| URL Type             | Expected Detection | Your System  |
| -------------------- | ------------------ | ------------ |
| Legit (google.com)   | ✅ Legitimate      | Should be ✅ |
| Phishing (g00gl.xyz) | ⚠️ Phishing        | Should be ⚠️ |
| Suspicious (\*.tk)   | ⚠️ Phishing        | Should be ⚠️ |
| Corporate (\*.com)   | ✅ Legitimate      | Should be ✅ |

---

## 🔍 DETAILED ANALYSIS

For each test, check:

1. **Classification**: ✅ Legit or ⚠️ Phishing?
2. **Confidence**: Is it > 80%?
3. **Risk Indicators**: Are they reasonable?
4. **Features**: Log the extracted features

---

## ❌ URLs TO AVOID

**DO NOT test with:**

```
❌ Active phishing URLs (from real attacks)
❌ Malware distribution sites
❌ Real exploits or vulnerabilities
❌ URLs flagged by your antivirus
❌ Dark web links
```

---

## 📊 TESTING CHECKLIST

- [ ] Test 5 legitimate URLs
- [ ] Test 5 phishing pattern URLs
- [ ] Run automated test suite
- [ ] Try batch detection
- [ ] Extract features from suspicious URL
- [ ] Check risk indicators match patterns

---

## 💡 QUICK RESULTS SUMMARY

### Your ML Model Should:

✅ Correctly identify legitimate major sites (Google, Amazon, etc.)  
✅ Flag URLs with hyphens in domain  
✅ Flag non-standard TLDs (.ru, .tk, .xyz)  
✅ Detect suspicious keywords (verify, confirm, update)  
✅ Score based on multiple indicators

### Expected Metrics:

- **True Positives (Phishing detected)**: ~92%
- **True Negatives (Legit allowed)**: ~98%
- **False Positives**: ~2%
- **False Negatives**: ~8%

---

## 🎓 LEARNING BY TESTING

Each URL teaches something:

```
google.com              → Clean legitimate domain
goog1e.com             → Homograph attack (0 instead of O)
google.ru              → Wrong country TLD
google-verify.com      → Typosquatting pattern
google.com@phish.com   → Redirect attack pattern
192.168.1.1/login      → IP-based attack
```

---

## 🛡️ YOUR NEXT STEPS

1. **Right Now**: Test with provided safe URLs
2. **Today**: Run full automated test suite
3. **This Week**: Test with real-world phishing datasets
4. **Next Step**: Retrain model with more examples

---

## 📝 EXAMPLE TEST LOG

```
URL: https://g00gl3-secure.xyz/login
Expected: PHISHING
Model Says: ⚠️ PHISHING (92% confidence)
Risk Indicators:
  - Domain hyphen detected
  - Non-standard TLD (.xyz)
  - Login keyword found
  - Unusual domain structure
Result: ✅ CORRECT DETECTION
```

---

## 🔗 SAFE PHISHING DATASET SOURCES

1. **PhishTank**: phishtank.com/phish_archive.php
2. **APWG**: apwg.org/trends (research data)
3. **Phishing Simulation**: phishery.com (safe demos)
4. **Educational**: Create your own patterns

---

**Remember**: The goal is to test patterns, not to find actual malicious URLs!

Use these safe examples to validate your ML model works correctly. 🎯
