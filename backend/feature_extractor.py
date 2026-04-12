import re
import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import socket
from datetime import datetime
import math

class FeatureExtractor:
    """
    Extracts features from URLs and HTML content for phishing detection
    """
    
    @staticmethod
    def extract_url_features(url):
        """Extract features from URL"""
        features = {}
        
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # 1. URL Length: Phishing URLs are typically longer
            features['url_length'] = len(url)
            
            # 2. Domain length
            features['domain_length'] = len(domain)
            
            # 3. Special characters in URL (-, @, //)
            features['special_chars_in_url'] = len(re.findall(r'[-@//]', url))
            
            # 4. Number of dots in domain
            features['num_dots_in_domain'] = domain.count('.')
            
            # 5. Subdomain count
            features['subdomain_count'] = domain.count('.') - 1
            
            # 6. Check for @ symbol (suspicious)
            features['has_at_symbol'] = 1 if '@' in url else 0
            
            # 7. Check for // in URL path (redirect)
            url_after_protocol = url.split('://', 1)[1] if len(url.split('://')) > 1 else url
            features['has_redirect_chars'] = 1 if '//' in url_after_protocol else 0
            
            # 8. Check for hyphen in domain
            features['has_hyphen_in_domain'] = 1 if '-' in domain else 0
            
            # 9. Check for IP address
            features['has_ip_address'] = 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain) else 0
            
            # 10. Check for https
            features['has_https'] = 1 if parsed_url.scheme == 'https' else 0
            
            # 11. Port number
            features['has_unusual_port'] = 1 if ':' in domain else 0
            
            # 12. URL entropy (randomness)
            features['url_entropy'] = FeatureExtractor._calculate_entropy(url)
            
            # 13. Number of query parameters
            features['num_query_params'] = len(parse_qs(parsed_url.query))
            
            # 14. TLD check (common vs uncommon)
            parts = domain.split('.')
            if len(parts) >= 2:
                tld = parts[-1]
                common_tlds = ['com', 'org', 'net', 'edu', 'gov', 'co', 'uk', 'de', 'fr', 'it']
                features['common_tld'] = 1 if tld in common_tlds else 0
            else:
                features['common_tld'] = 0
                
        except Exception as e:
            # Default values if parsing fails
            for key in ['url_length', 'domain_length', 'special_chars_in_url', 
                       'num_dots_in_domain', 'subdomain_count', 'has_at_symbol',
                       'has_redirect_chars', 'has_hyphen_in_domain', 'has_ip_address',
                       'has_https', 'has_unusual_port', 'url_entropy', 'num_query_params',
                       'common_tld']:
                features[key] = 0
                
        return features
    
    @staticmethod
    def extract_html_features(html_content, url=''):
        """Extract features from HTML content"""
        features = {}
        
        try:
            if not html_content or len(html_content.strip()) == 0:
                raise ValueError("Empty HTML content")
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 1. Number of forms
            forms = soup.find_all('form')
            features['num_forms'] = len(forms)
            
            # 2. Number of input fields
            inputs = soup.find_all('input')
            features['num_input_fields'] = len(inputs)
            
            # 3. Number of password fields
            password_inputs = soup.find_all('input', {'type': 'password'})
            features['num_password_fields'] = len(password_inputs)
            
            # 4. Check for login keyword
            page_text = soup.get_text().lower()
            page_html = str(soup).lower()
            features['has_login_keyword'] = 1 if 'login' in page_text or 'login' in page_html else 0
            
            # 5. Check for verify keyword (credential stealing)
            features['has_verify_keyword'] = 1 if 'verify' in page_text or 'confirm' in page_text else 0
            
            # 6. Check for update keyword
            features['has_update_keyword'] = 1 if 'update' in page_text or 'upgrade' in page_text else 0
            
            # 7. Number of links
            features['num_links'] = len(soup.find_all('a'))
            
            # 8. External links count
            external_links = 0
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http') and url:
                    if urlparse(url).netloc not in href:
                        external_links += 1
            features['num_external_links'] = external_links
            
            # 9. Number of images
            features['num_images'] = len(soup.find_all('img'))
            
            # 10. Check for inline scripts
            features['num_inline_scripts'] = len(soup.find_all('script'))
            
            # 11. Number of hidden input fields
            hidden_inputs = soup.find_all('input', {'type': 'hidden'})
            features['num_hidden_inputs'] = len(hidden_inputs)
            
            # 12. Form action URL
            features['has_form_action'] = 0
            features['form_action_diff_domain'] = 0
            if forms:
                for form in forms:
                    action = form.get('action', '')
                    if action:
                        features['has_form_action'] = 1
                        if url:
                            parsed_url = urlparse(url)
                            if action.startswith('http'):
                                action_domain = urlparse(action).netloc
                                if action_domain != parsed_url.netloc:
                                    features['form_action_diff_domain'] = 1
                            elif action.startswith('/') or action.startswith('?'):
                                features['form_action_diff_domain'] = 0
                            else:
                                features['form_action_diff_domain'] = 1
            
            # 13. Check for suspicious keywords
            suspicious_keywords = ['confirm', 'verify', 'validate', 'authenticate', 'secure', 'click', 'urgent']
            suspicious_count = sum(1 for kw in suspicious_keywords if kw in page_text)
            features['suspicious_keyword_count'] = min(suspicious_count, 5)
            
            # 14. Ratio of forms to other elements
            total_elements = len(soup.find_all(['form', 'div', 'section', 'article', 'main']))
            features['form_to_element_ratio'] = len(forms) / total_elements if total_elements > 0 else 0
            
            # 15. SSL check in submission
            if forms:
                for form in forms:
                    action = form.get('action', '')
                    if action and not action.startswith('http'):
                        features['form_uses_relative_action'] = 1
                        break
                else:
                    features['form_uses_relative_action'] = 0
            else:
                features['form_uses_relative_action'] = 0
            
        except Exception as e:
            # Default values
            defaults = {
                'num_forms': 0, 'num_input_fields': 0, 'num_password_fields': 0,
                'has_login_keyword': 0, 'has_verify_keyword': 0, 'has_update_keyword': 0,
                'num_links': 0, 'num_external_links': 0, 'num_images': 0,
                'num_inline_scripts': 0, 'num_hidden_inputs': 0, 'has_form_action': 0,
                'form_action_diff_domain': 0, 'suspicious_keyword_count': 0,
                'form_to_element_ratio': 0, 'form_uses_relative_action': 0
            }
            features.update(defaults)
            
        return features
    
    @staticmethod
    def _calculate_entropy(text):
        """Calculate Shannon entropy of text"""
        char_counts = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        entropy = 0
        text_len = len(text)
        for count in char_counts.values():
            probability = count / text_len
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    @staticmethod
    def combine_features(url, html_content=''):
        """Combine URL and HTML features"""
        features = {}
        
        url_features = FeatureExtractor.extract_url_features(url)
        features.update(url_features)
        
        if html_content:
            html_features = FeatureExtractor.extract_html_features(html_content, url)
            features.update(html_features)
        
        return features
