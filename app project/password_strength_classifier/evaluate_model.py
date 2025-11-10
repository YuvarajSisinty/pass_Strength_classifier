"""
Model Evaluation Script with Detailed Metrics
Provides precision, recall, F1-score, and confusion matrix visualization
"""

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, precision_recall_fscore_support
)
from feature_extractor import PasswordFeatureExtractor


class ModelEvaluator:
    """Comprehensive model evaluation with visualization"""
    
    def __init__(self, model_path: str = 'password_strength_model.pkl'):
        self.model_path = model_path
        self.model_data = None
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.feature_extractor = PasswordFeatureExtractor()
        
    def load_model(self):
        """Load the trained model"""
        print(f"Loading model from {self.model_path}...")
        self.model_data = joblib.load(self.model_path)
        self.model = self.model_data['model']
        self.scaler = self.model_data['scaler']
        self.feature_columns = self.model_data['feature_columns']
        print(f"Model loaded: {self.model_data['model_name']}")
    
    def predict_password_strength(self, password: str) -> dict:
        """Predict strength of a single password"""
        if self.model is None:
            self.load_model()
        
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
        
        return {
            'password': password,
            'strength': strength_map[prediction],
            'strength_label': int(prediction),
            'probabilities': {
                'Weak': float(probabilities[0]),
                'Medium': float(probabilities[1]),
                'Strong': float(probabilities[2])
            }
        }
    
    def evaluate_on_dataset(self, dataset_path: str = 'password_dataset.csv'):
        """Evaluate model on full dataset"""
        if self.model is None:
            self.load_model()
        
        print(f"\nEvaluating model on {dataset_path}...")
        df = pd.read_csv(dataset_path)
        
        # Prepare features
        X = df[self.feature_columns].values
        y_true = df['strength_label'].values
        
        # Make predictions
        model_name = self.model_data['model_name']
        if model_name == 'SVM' or model_name == 'Logistic Regression':
            X_scaled = self.scaler.transform(X)
            y_pred = self.model.predict(X_scaled)
        else:
            y_pred = self.model.predict(X)
        
        # Calculate metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average=None)
        recall = recall_score(y_true, y_pred, average=None)
        f1 = f1_score(y_true, y_pred, average=None)
        
        # Per-class metrics
        precision_macro = precision_score(y_true, y_pred, average='macro')
        recall_macro = recall_score(y_true, y_pred, average='macro')
        f1_macro = f1_score(y_true, y_pred, average='macro')
        
        # Weighted averages
        precision_weighted = precision_score(y_true, y_pred, average='weighted')
        recall_weighted = recall_score(y_true, y_pred, average='weighted')
        f1_weighted = f1_score(y_true, y_pred, average='weighted')
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Print results
        print("\n" + "="*60)
        print("MODEL EVALUATION RESULTS")
        print("="*60)
        
        print(f"\nOverall Accuracy: {accuracy:.4f}")
        
        print(f"\n{'='*60}")
        print("Per-Class Metrics")
        print(f"{'='*60}")
        classes = ['Weak', 'Medium', 'Strong']
        metrics_df = pd.DataFrame({
            'Class': classes,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1
        })
        print(metrics_df.to_string(index=False))
        
        print(f"\n{'='*60}")
        print("Average Metrics")
        print(f"{'='*60}")
        print(f"Macro Average:")
        print(f"  Precision: {precision_macro:.4f}")
        print(f"  Recall: {recall_macro:.4f}")
        print(f"  F1-Score: {f1_macro:.4f}")
        
        print(f"\nWeighted Average:")
        print(f"  Precision: {precision_weighted:.4f}")
        print(f"  Recall: {recall_weighted:.4f}")
        print(f"  F1-Score: {f1_weighted:.4f}")
        
        print(f"\n{'='*60}")
        print("Confusion Matrix")
        print(f"{'='*60}")
        print("\nActual vs Predicted:")
        cm_df = pd.DataFrame(cm, 
                            index=[f'Actual {c}' for c in classes],
                            columns=[f'Predicted {c}' for c in classes])
        print(cm_df)
        
        print(f"\n{'='*60}")
        print("Detailed Classification Report")
        print(f"{'='*60}")
        print(classification_report(y_true, y_pred, target_names=classes))
        
        # Visualize confusion matrix
        self.plot_confusion_matrix(cm, classes)
        
        # Create metrics summary
        summary = {
            'accuracy': accuracy,
            'precision_macro': precision_macro,
            'recall_macro': recall_macro,
            'f1_macro': f1_macro,
            'precision_weighted': precision_weighted,
            'recall_weighted': recall_weighted,
            'f1_weighted': f1_weighted,
            'per_class': {
                classes[i]: {
                    'precision': float(precision[i]),
                    'recall': float(recall[i]),
                    'f1': float(f1[i])
                }
                for i in range(len(classes))
            },
            'confusion_matrix': cm.tolist()
        }
        
        return summary
    
    def plot_confusion_matrix(self, cm: np.ndarray, classes: list):
        """Visualize confusion matrix"""
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=classes, yticklabels=classes,
                   cbar_kws={'label': 'Count'})
        plt.title('Confusion Matrix - Password Strength Classification', 
                 fontsize=16, fontweight='bold')
        plt.ylabel('Actual Strength', fontsize=12)
        plt.xlabel('Predicted Strength', fontsize=12)
        plt.tight_layout()
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        print("\nConfusion matrix visualization saved to 'confusion_matrix.png'")
        plt.close()
    
    def test_sample_passwords(self):
        """Test model on sample passwords"""
        if self.model is None:
            self.load_model()
        
        test_passwords = [
            'password',
            '123456',
            'abc123',
            'Password123',
            'MyP@ssw0rd',
            'Tr0ub4dor&3',
            'P@ssw0rd!2024',
            'Kx9#mP2$vL7@nQ5',
            'a',
            'qwerty'
        ]
        
        print("\n" + "="*60)
        print("SAMPLE PASSWORD PREDICTIONS")
        print("="*60)
        
        results = []
        for pwd in test_passwords:
            result = self.predict_password_strength(pwd)
            results.append(result)
            
            print(f"\nPassword: {pwd}")
            print(f"Predicted Strength: {result['strength']}")
            print(f"Probabilities:")
            for strength, prob in result['probabilities'].items():
                print(f"  {strength}: {prob:.4f}")
        
        return results


if __name__ == "__main__":
    evaluator = ModelEvaluator()
    
    # Evaluate on full dataset
    summary = evaluator.evaluate_on_dataset()
    
    # Test sample passwords
    evaluator.test_sample_passwords()

