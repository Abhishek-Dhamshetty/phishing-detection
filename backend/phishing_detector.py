import pickle
import numpy as np
import pandas as pd
from feature_extractor import FeatureExtractor
import os

class PhishingDetector:
    """
    Detects phishing pages using trained ML model
    """
    
    def __init__(self, model_path='../data/phishing_model.pkl'):
        """Initialize detector with trained model"""
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load trained model"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_columns = model_data['feature_columns']
    
    def detect(self, url, html_content=''):
        """
        Detect if a webpage is phishing
        Returns: {
            'is_phishing': bool,
            'confidence': float (0-1),
            'risk_score': float (0-100),
            'features_extracted': dict,
            'risk_indicators': list
        }
        """
        try:
            # Extract features
            features_dict = FeatureExtractor.combine_features(url, html_content)
            
            # Create feature vector in correct order
            feature_vector = []
            for col in self.feature_columns:
                feature_vector.append(features_dict.get(col, 0))
            
            feature_vector = np.array(feature_vector).reshape(1, -1)
            
            # Handle NaN values
            feature_vector = np.nan_to_num(feature_vector)
            
            # Scale features
            feature_vector_scaled = self.scaler.transform(feature_vector)
            
            # Predict
            prediction = self.model.predict(feature_vector_scaled)[0]
            probability = self.model.predict_proba(feature_vector_scaled)[0]
            
            is_phishing = bool(prediction)
            confidence = float(probability[prediction])
            risk_score = confidence * 100
            
            # Identify risk indicators
            risk_indicators = self._identify_risk_indicators(features_dict)
            
            return {
                'is_phishing': is_phishing,
                'prediction': int(prediction),
                'confidence': round(confidence, 4),
                'risk_score': round(risk_score, 2),
                'legitimate_score': round(probability[0] * 100, 2),
                'phishing_score': round(probability[1] * 100, 2),
                'features_extracted': {k: v for k, v in features_dict.items() if k in self.feature_columns},
                'risk_indicators': risk_indicators
            }
        
        except Exception as e:
            return {
                'is_phishing': None,
                'error': str(e),
                'confidence': 0.0,
                'risk_score': 0
            }
    
    @staticmethod
    def _identify_risk_indicators(features):
        """Identify suspicious features"""
        indicators = []
        
        # URL-based indicators
        if features.get('has_ip_address'):
            indicators.append('URL contains IP address instead of domain')
        
        if features.get('has_at_symbol'):
            indicators.append('URL contains @ symbol (redirection attack)')
        
        if features.get('has_redirect_chars'):
            indicators.append('URL contains // redirection characters')
        
        if not features.get('has_https'):
            indicators.append('No HTTPS - connection not secure')
        
        if features.get('has_hyphen_in_domain'):
            indicators.append('Domain contains hyphen (common in phishing)')
        
        if features.get('url_length', 0) > 75:
            indicators.append('Unusually long URL')
        
        if features.get('has_unusual_port'):
            indicators.append('Non-standard port used')
        
        # HTML-based indicators
        if features.get('form_action_diff_domain'):
            indicators.append('Form submits to different domain')
        
        if features.get('num_password_fields', 0) > 1:
            indicators.append('Multiple password fields detected')
        
        if features.get('has_verify_keyword'):
            indicators.append('Page contains "verify" or "confirm" keyword')
        
        if features.get('has_update_keyword'):
            indicators.append('Page contains "update" or "upgrade" keyword')
        
        if features.get('num_external_links', 0) > 10:
            indicators.append('Excessive external links detected')
        
        if features.get('num_inline_scripts', 0) > 5:
            indicators.append('Multiple inline scripts detected')
        
        if features.get('suspicious_keyword_count', 0) >= 2:
            indicators.append(f'Multiple suspicious keywords found')
        
        if features.get('form_uses_relative_action'):
            indicators.append('Form uses relative action URL')
        
        return indicators
    
    def batch_detect(self, urls_and_html):
        """
        Detect multiple websites
        urls_and_html: list of tuples (url, html_content)
        """
        results = []
        for url, html_content in urls_and_html:
            result = self.detect(url, html_content)
            result['url'] = url
            results.append(result)
        return results
