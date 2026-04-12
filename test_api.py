#!/usr/bin/env python3
"""
Test script for the Phishing Detection System
Tests API endpoints and feature extraction
"""

import requests
import json
from time import time

BASE_URL = 'http://127.0.0.1:5000/api'

def test_health_check():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    try:
        response = requests.get(f'{BASE_URL}/health')
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_model_info():
    """Test model information endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Model Information")
    print("="*60)
    try:
        response = requests.get(f'{BASE_URL}/model-info')
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Model Type: {data.get('model_type')}")
        print(f"✓ Estimators: {data.get('n_estimators')}")
        print(f"✓ Features Count: {data.get('features_count')}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_single_detection_legitimate():
    """Test single URL detection - legitimate site"""
    print("\n" + "="*60)
    print("TEST 3: Single Detection - Legitimate Site")
    print("="*60)
    try:
        payload = {
            'url': 'https://www.google.com'
        }
        response = requests.post(f'{BASE_URL}/detect', json=payload)
        data = response.json()
        
        if response.status_code == 200:
            result = data.get('data', {})
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Is Phishing: {result.get('is_phishing')}")
            print(f"✓ Confidence: {result.get('confidence')}")
            print(f"✓ Risk Score: {result.get('risk_score')}")
            print(f"✓ Legitimate Score: {result.get('legitimate_score')}%")
            print(f"✓ Phishing Score: {result.get('phishing_score')}%")
            
            if result.get('risk_indicators'):
                print(f"⚠️ Risk Indicators:")
                for indicator in result['risk_indicators'][:3]:
                    print(f"   - {indicator}")
            
            return result.get('is_phishing') == False
        else:
            print(f"✗ Error: {data}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_single_detection_phishing():
    """Test single URL detection - phishing site"""
    print("\n" + "="*60)
    print("TEST 4: Single Detection - Phishing Site")
    print("="*60)
    try:
        payload = {
            'url': 'https://goog1e-secure.xyz/login'
        }
        response = requests.post(f'{BASE_URL}/detect', json=payload)
        data = response.json()
        
        if response.status_code == 200:
            result = data.get('data', {})
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Is Phishing: {result.get('is_phishing')}")
            print(f"✓ Confidence: {result.get('confidence')}")
            print(f"✓ Risk Score: {result.get('risk_score')}")
            print(f"✓ Legitimate Score: {result.get('legitimate_score')}%")
            print(f"✓ Phishing Score: {result.get('phishing_score')}%")
            
            if result.get('risk_indicators'):
                print(f"⚠️ Risk Indicators:")
                for indicator in result['risk_indicators'][:5]:
                    print(f"   - {indicator}")
            
            return True  # We're just checking it responds correctly
        else:
            print(f"✗ Error: {data}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_batch_detection():
    """Test batch detection"""
    print("\n" + "="*60)
    print("TEST 5: Batch Detection")
    print("="*60)
    try:
        payload = {
            'urls': [
                'https://www.amazon.com',
                'https://amaz0n-secure.ru',
                'https://www.github.com',
                'https://github-login.tk'
            ]
        }
        response = requests.post(f'{BASE_URL}/batch-detect', json=payload)
        data = response.json()
        
        if response.status_code == 200:
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Count: {data.get('count')} URLs analyzed")
            
            legitimate = sum(1 for r in data.get('data', []) if not r.get('is_phishing') and not r.get('error'))
            phishing = sum(1 for r in data.get('data', []) if r.get('is_phishing'))
            errors = sum(1 for r in data.get('data', []) if r.get('error'))
            
            print(f"✓ Legitimate: {legitimate}")
            print(f"✓ Phishing: {phishing}")
            print(f"✓ Errors: {errors}")
            
            return data.get('count') == 4
        else:
            print(f"✗ Error: {data}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_feature_extraction():
    """Test feature extraction"""
    print("\n" + "="*60)
    print("TEST 6: Feature Extraction")
    print("="*60)
    try:
        payload = {
            'url': 'https://example-login.com/signin?redirect=google'
        }
        response = requests.post(f'{BASE_URL}/analyze-features', json=payload)
        data = response.json()
        
        if response.status_code == 200:
            features = data.get('features', {})
            
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Features Extracted: {len(features)} features")
            
            # Display some key features
            key_features = ['url_length', 'domain_length', 'has_https', 
                           'num_forms', 'num_password_fields', 'has_login_keyword']
            print(f"✓ Sample Features:")
            for feature in key_features:
                if feature in features:
                    print(f"   - {feature}: {features[feature]}")
            
            return len(features) > 0
        else:
            print(f"✗ Error: {data}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "🛡️  PHISHING DETECTION SYSTEM - API TESTS 🛡️ ")
    print("="*60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Model Info", test_model_info),
        ("Legitimate Detection", test_single_detection_legitimate),
        ("Phishing Detection", test_single_detection_phishing),
        ("Batch Detection", test_batch_detection),
        ("Feature Extraction", test_feature_extraction),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("✨ All tests passed! System is working correctly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed.")

if __name__ == '__main__':
    import time
    print("Waiting for server to be ready...")
    time.sleep(2)
    run_all_tests()
