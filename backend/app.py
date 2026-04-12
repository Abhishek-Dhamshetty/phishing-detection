from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from phishing_detector import PhishingDetector
from feature_extractor import FeatureExtractor
import requests
from bs4 import BeautifulSoup
import os
import sys

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Initialize detector
detector = None

def init_detector():
    """Initialize phishing detector"""
    global detector
    model_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'phishing_model.pkl')
    try:
        detector = PhishingDetector(model_path)
        print("✓ Phishing detector initialized successfully")
    except FileNotFoundError:
        print("✗ Model not found. Training new model...")
        from model_trainer import PhishingModelTrainer
        PhishingModelTrainer.train_model(model_path)
        detector = PhishingDetector(model_path)
        print("✓ Model trained and detector initialized")

@app.before_request
def before_request():
    """Initialize detector on first request"""
    global detector
    if detector is None:
        init_detector()

@app.route('/')
def index():
    """Serve main page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/detect', methods=['POST'])
def detect_phishing():
    """
    API endpoint to detect phishing
    Expects JSON: {
        'url': 'https://example.com',
        'html_content': '<html>...</html>' (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'URL is required',
                'code': 'MISSING_URL'
            }), 400
        
        url = data['url'].strip()
        html_content = data.get('html_content', '').strip()
        
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # If no HTML provided, try to fetch it
        if not html_content:
            try:
                print(f"Fetching HTML from {url}...")
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                html_content = response.text
            except Exception as e:
                print(f"Could not fetch HTML: {str(e)}")
                # Continue without HTML content
                html_content = ''
        
        # Detect phishing
        result = detector.detect(url, html_content)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 'DETECTION_ERROR'
        }), 500

@app.route('/api/batch-detect', methods=['POST'])
def batch_detect():
    """
    API endpoint for batch detection
    Expects JSON: {
        'urls': ['url1', 'url2', ...]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({
                'error': 'URLs array is required',
                'code': 'MISSING_URLS'
            }), 400
        
        urls = data['urls']
        if not isinstance(urls, list) or len(urls) == 0:
            return jsonify({
                'error': 'URLs must be non-empty array',
                'code': 'INVALID_URLS'
            }), 400
        
        results = []
        for url in urls[:10]:  # Limit to 10 URLs
            try:
                url = url.strip()
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                result = detector.detect(url)
                result['url'] = url
                results.append(result)
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'count': len(results),
            'data': results
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 'BATCH_DETECTION_ERROR'
        }), 500

@app.route('/api/analyze-features', methods=['POST'])
def analyze_features():
    """
    API endpoint to analyze and return extracted features
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'URL is required',
                'code': 'MISSING_URL'
            }), 400
        
        url = data['url'].strip()
        html_content = data.get('html_content', '').strip()
        
        # Extract features
        if html_content:
            features = FeatureExtractor.combine_features(url, html_content)
        else:
            features = FeatureExtractor.extract_url_features(url)
        
        return jsonify({
            'success': True,
            'url': url,
            'features': features
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 'FEATURE_EXTRACTION_ERROR'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'detector_initialized': detector is not None
    }), 200

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    if detector is None or detector.model is None:
        return jsonify({
            'error': 'Model not initialized'
        }), 500
    
    return jsonify({
        'model_type': 'Random Forest Classifier',
        'n_estimators': detector.model.n_estimators,
        'features_count': len(detector.feature_columns),
        'features': detector.feature_columns
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    # Try to serve files from frontend folder
    return send_from_directory('../frontend', 'index.html'), 200

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'code': 'INTERNAL_SERVER_ERROR'
    }), 500

if __name__ == '__main__':
    print("="*60)
    print("PHISHING DETECTION SYSTEM - BACKEND SERVER")
    print("="*60)
    
    # Initialize detector and train if needed
    init_detector()
    
    print("\nStarting Flask server...")
    print("Server running at: http://127.0.0.1:5000")
    print("="*60)
    
    app.run(debug=True, port=5000, use_reloader=False)
