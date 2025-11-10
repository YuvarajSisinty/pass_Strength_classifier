"""
Main Application Script for Password Strength Classification
Interactive CLI tool to classify password strength
"""

import sys
import joblib
import numpy as np
from feature_extractor import PasswordFeatureExtractor


class PasswordStrengthClassifier:
    """Main application for password strength classification"""
    
    def __init__(self, model_path: str = 'password_strength_model.pkl'):
        self.model_path = model_path
        self.model_data = None
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.feature_extractor = PasswordFeatureExtractor()
        
    def load_model(self):
        """Load the trained model"""
        try:
            self.model_data = joblib.load(self.model_path)
            self.model = self.model_data['model']
            self.scaler = self.model_data['scaler']
            self.feature_columns = self.model_data['feature_columns']
            print(f"✓ Model loaded successfully ({self.model_data['model_name']})")
            return True
        except FileNotFoundError:
            print(f"✗ Error: Model file '{self.model_path}' not found.")
            print("  Please train the model first by running: python train_model.py")
            return False
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            return False
    
    def classify(self, password: str) -> dict:
        """Classify password strength"""
        if self.model is None:
            if not self.load_model():
                return None
        
        # Extract features
        features = self.feature_extractor.extract_features(password)
        feature_vector = np.array([[features[col] for col in self.feature_columns]])
        
        # Scale features if needed
        model_name = self.model_data['model_name']
        if model_name == 'SVM' or model_name == 'Logistic Regression':
            feature_vector = self.scaler.transform(feature_vector)
        
        # Predict
        prediction = self.model.predict(feature_vector)[0]
        probabilities = self.model.predict_proba(feature_vector)[0]
        
        strength_map = {0: 'Weak', 1: 'Medium', 2: 'Strong'}
        strength_colors = {'Weak': '🔴', 'Medium': '🟡', 'Strong': '🟢'}
        
        result = {
            'password': password,
            'strength': strength_map[prediction],
            'strength_label': int(prediction),
            'probabilities': {
                'Weak': float(probabilities[0]),
                'Medium': float(probabilities[1]),
                'Strong': float(probabilities[2])
            },
            'icon': strength_colors[strength_map[prediction]]
        }
        
        return result
    
    def display_result(self, result: dict):
        """Display classification result in a formatted way"""
        if result is None:
            return
        
        print("\n" + "="*60)
        print("PASSWORD STRENGTH ANALYSIS")
        print("="*60)
        print(f"\nPassword: {result['password']}")
        print(f"Strength: {result['icon']} {result['strength']}")
        print(f"\nConfidence Probabilities:")
        for strength, prob in result['probabilities'].items():
            bar_length = int(prob * 30)
            bar = '█' * bar_length + '░' * (30 - bar_length)
            print(f"  {strength:8s}: {bar} {prob*100:5.2f}%")
        print("="*60)
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("\n" + "="*60)
        print("Password Strength Classifier")
        print("="*60)
        print("\nEnter passwords to classify their strength.")
        print("Type 'quit' or 'exit' to stop.\n")
        
        if not self.load_model():
            return
        
        while True:
            try:
                password = input("Enter password: ").strip()
                
                if password.lower() in ['quit', 'exit', 'q']:
                    print("\nGoodbye!")
                    break
                
                if not password:
                    print("Please enter a password.")
                    continue
                
                result = self.classify(password)
                self.display_result(result)
                print()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def batch_mode(self, passwords: list):
        """Classify multiple passwords"""
        if not self.load_model():
            return
        
        results = []
        for password in passwords:
            result = self.classify(password)
            if result:
                results.append(result)
                self.display_result(result)
        
        return results


def main():
    """Main entry point"""
    classifier = PasswordStrengthClassifier()
    
    if len(sys.argv) > 1:
        # Command line mode
        passwords = sys.argv[1:]
        classifier.batch_mode(passwords)
    else:
        # Interactive mode
        classifier.interactive_mode()


if __name__ == "__main__":
    main()

