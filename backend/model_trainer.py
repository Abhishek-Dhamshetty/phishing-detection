import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
import pickle
import os
from feature_extractor import FeatureExtractor

class PhishingModelTrainer:
    """
    Trains and saves phishing detection model
    """
    
    @staticmethod
    def generate_synthetic_data(num_samples=1000):
        """
        Generate synthetic training data
        In production, this would use real labeled phishing/legitimate datasets
        """
        data = []
        
        # Legitimate websites
        legitimate_urls = [
            'https://www.google.com',
            'https://www.facebook.com',
            'https://www.twitter.com',
            'https://www.amazon.com',
            'https://www.apple.com',
            'https://www.microsoft.com',
            'https://www.github.com',
            'https://www.linkedin.com',
            'https://www.instagram.com',
            'https://www.youtube.com'
        ]
        
        phishing_urls = [
            'https://goog1e.com/login',
            'https://fb-secure.com/verify',
            'https://twitter-confirm.net/',
            'https://amazon-account.ru/login',
            'http://apple-verify.cn/',
            'https://micros0ft.com/update',
            'https://github-login.tk/',
            'https://linked-in.com/signin',
            'http://192.168.1.1/login',
            'https://g00gle.com'
        ]
        
        # Generate legitimate samples
        for i in range(num_samples // 2):
            url = np.random.choice(legitimate_urls)
            features = FeatureExtractor.extract_url_features(url)
            # Add some HTML features
            features['num_forms'] = np.random.randint(0, 3)
            features['num_password_fields'] = np.random.randint(0, 2)
            features['has_login_keyword'] = 1
            features['form_action_diff_domain'] = 0
            features['has_https'] = 1
            features['label'] = 0  # Legitimate
            data.append(features)
        
        # Generate phishing samples
        for i in range(num_samples // 2):
            url = np.random.choice(phishing_urls)
            features = FeatureExtractor.extract_url_features(url)
            # Modify for phishing characteristics
            features['num_forms'] = np.random.randint(1, 4)
            features['num_password_fields'] = np.random.randint(1, 3)
            features['has_login_keyword'] = 1
            features['form_action_diff_domain'] = np.random.choice([0, 1])
            features['has_https'] = np.random.choice([0, 1])
            features['has_hyphen_in_domain'] = np.random.choice([0, 1])
            features['num_dots_in_domain'] = np.random.randint(2, 5)
            features['url_length'] = np.random.randint(30, 100)
            features['label'] = 1  # Phishing
            data.append(features)
        
        return pd.DataFrame(data)
    
    @staticmethod
    def train_model(output_path='../data/phishing_model.pkl'):
        """Train the phishing detection model"""
        
        print("Generating training data...")
        df = PhishingModelTrainer.generate_synthetic_data(2000)
        
        # Feature columns (excluding target)
        feature_columns = [col for col in df.columns if col != 'label']
        
        # Handle missing values
        df = df.fillna(0)
        
        X = df[feature_columns]
        y = df['label']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        print("Training Random Forest model...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        print("\n" + "="*50)
        print("MODEL EVALUATION")
        print("="*50)
        
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
        print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                    target_names=['Legitimate', 'Phishing']))
        print(f"\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Feature importance
        print(f"\nTop 10 Important Features:")
        importance_df = pd.DataFrame({
            'feature': feature_columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(importance_df.head(10).to_string(index=False))
        print("="*50)
        
        # Save model and scaler
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        with open(output_path, 'wb') as f:
            pickle.dump({
                'model': model,
                'scaler': scaler,
                'feature_columns': feature_columns
            }, f)
        
        print(f"\nModel saved to {output_path}")
        
        return model, scaler, feature_columns

if __name__ == '__main__':
    PhishingModelTrainer.train_model()
