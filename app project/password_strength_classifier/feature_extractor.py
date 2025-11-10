"""
Feature Extraction Module for Password Strength Classification
Extracts features like length, entropy, complexity metrics from passwords
"""

import re
import math
from typing import Dict


class PasswordFeatureExtractor:
    """Extracts various features from passwords for ML model training"""
    
    def __init__(self):
        self.common_passwords = {
            'password', '123456', '123456789', '12345678', '12345',
            '1234567', '1234567890', 'qwerty', 'abc123', 'password1',
            'admin', 'letmein', 'welcome', 'monkey', '1234567890'
        }
    
    def extract_features(self, password: str) -> Dict[str, float]:
        """
        Extract all features from a password
        
        Args:
            password: The password string to analyze
            
        Returns:
            Dictionary of feature names and values
        """
        features = {}
        
        # Basic length features
        features['length'] = len(password)
        features['log_length'] = math.log(len(password) + 1)
        
        # Character type counts
        features['num_uppercase'] = sum(1 for c in password if c.isupper())
        features['num_lowercase'] = sum(1 for c in password if c.islower())
        features['num_digits'] = sum(1 for c in password if c.isdigit())
        features['num_special'] = sum(1 for c in password if not c.isalnum())
        
        # Character type ratios
        features['ratio_uppercase'] = features['num_uppercase'] / max(len(password), 1)
        features['ratio_lowercase'] = features['num_lowercase'] / max(len(password), 1)
        features['ratio_digits'] = features['num_digits'] / max(len(password), 1)
        features['ratio_special'] = features['num_special'] / max(len(password), 1)
        
        # Character type diversity
        features['has_uppercase'] = 1.0 if features['num_uppercase'] > 0 else 0.0
        features['has_lowercase'] = 1.0 if features['num_lowercase'] > 0 else 0.0
        features['has_digits'] = 1.0 if features['num_digits'] > 0 else 0.0
        features['has_special'] = 1.0 if features['num_special'] > 0 else 0.0
        
        # Character type count (how many different types)
        char_types = sum([
            features['has_uppercase'],
            features['has_lowercase'],
            features['has_digits'],
            features['has_special']
        ])
        features['char_type_count'] = char_types
        
        # Entropy calculation (Shannon entropy)
        features['entropy'] = self._calculate_entropy(password)
        features['normalized_entropy'] = features['entropy'] / max(len(password), 1)
        
        # Complexity features
        features['complexity_score'] = self._calculate_complexity(password)
        features['sequential_chars'] = self._count_sequential_chars(password)
        features['repeated_chars'] = self._count_repeated_chars(password)
        features['keyboard_patterns'] = self._detect_keyboard_patterns(password)
        
        # Common password check
        features['is_common'] = 1.0 if password.lower() in self.common_passwords else 0.0
        
        # Pattern detection
        features['has_sequence'] = 1.0 if self._has_sequence(password) else 0.0
        features['has_repetition'] = 1.0 if self._has_repetition(password) else 0.0
        
        # Position-based features
        features['starts_with_uppercase'] = 1.0 if password and password[0].isupper() else 0.0
        features['ends_with_digit'] = 1.0 if password and password[-1].isdigit() else 0.0
        
        return features
    
    def _calculate_entropy(self, password: str) -> float:
        """Calculate Shannon entropy of the password"""
        if not password:
            return 0.0
        
        # Count character frequencies
        char_counts = {}
        for char in password:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0.0
        length = len(password)
        for count in char_counts.values():
            probability = count / length
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _calculate_complexity(self, password: str) -> float:
        """Calculate a complexity score based on various factors"""
        score = 0.0
        
        # Length bonus
        score += min(len(password) * 0.5, 10)
        
        # Character variety bonus
        unique_chars = len(set(password))
        score += unique_chars * 0.3
        
        # Character type bonus
        if any(c.isupper() for c in password):
            score += 2
        if any(c.islower() for c in password):
            score += 2
        if any(c.isdigit() for c in password):
            score += 2
        if any(not c.isalnum() for c in password):
            score += 3
        
        # Penalties
        if self._has_sequence(password):
            score -= 3
        if self._has_repetition(password):
            score -= 2
        if password.lower() in self.common_passwords:
            score -= 10
        
        return max(score, 0)
    
    def _count_sequential_chars(self, password: str) -> int:
        """Count sequential character patterns (e.g., abc, 123)"""
        count = 0
        for i in range(len(password) - 2):
            if password[i].isdigit() and password[i+1].isdigit() and password[i+2].isdigit():
                if ord(password[i+1]) == ord(password[i]) + 1 and ord(password[i+2]) == ord(password[i+1]) + 1:
                    count += 1
            elif password[i].isalpha() and password[i+1].isalpha() and password[i+2].isalpha():
                if ord(password[i+1].lower()) == ord(password[i].lower()) + 1 and ord(password[i+2].lower()) == ord(password[i+1].lower()) + 1:
                    count += 1
        return count
    
    def _count_repeated_chars(self, password: str) -> int:
        """Count repeated character patterns"""
        count = 0
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                count += 1
        return count
    
    def _detect_keyboard_patterns(self, password: str) -> int:
        """Detect common keyboard patterns (qwerty, asdf, etc.)"""
        keyboard_rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', '1234567890']
        count = 0
        password_lower = password.lower()
        
        for row in keyboard_rows:
            for i in range(len(row) - 2):
                pattern = row[i:i+3]
                if pattern in password_lower:
                    count += 1
        
        return count
    
    def _has_sequence(self, password: str) -> bool:
        """Check if password contains sequential characters"""
        return self._count_sequential_chars(password) > 0
    
    def _has_repetition(self, password: str) -> bool:
        """Check if password contains repeated characters"""
        return self._count_repeated_chars(password) > 0
    
    def get_feature_names(self) -> list:
        """Return list of all feature names"""
        # Use a sample password to get feature names
        sample_features = self.extract_features("Sample1!")
        return list(sample_features.keys())

