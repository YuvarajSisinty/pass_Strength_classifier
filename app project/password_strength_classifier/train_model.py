"""
Model Training Script for Password Strength Classification
Trains multiple ML models and selects the best one
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os


class PasswordStrengthTrainer:
    """Trains and evaluates multiple ML models for password strength classification"""
    
    def __init__(self, dataset_path: str = 'password_dataset.csv'):
        self.dataset_path = dataset_path
        self.models = {}
        self.scaler = StandardScaler()
        self.best_model = None
        self.best_model_name = None
        self.feature_columns = None
        
    def load_data(self) -> tuple:
        """Load and prepare data for training"""
        print(f"Loading dataset from {self.dataset_path}...")
        
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset file {self.dataset_path} not found. "
                                  f"Please run dataset_generator.py first.")
        
        df = pd.read_csv(self.dataset_path)
        
        # Separate features and labels
        feature_columns = [col for col in df.columns 
                          if col not in ['password', 'strength_label', 'strength_name']]
        self.feature_columns = feature_columns
        
        X = df[feature_columns].values
        y = df['strength_label'].values
        
        print(f"Loaded {len(df)} samples with {len(feature_columns)} features")
        print(f"Feature columns: {', '.join(feature_columns[:5])}... ({len(feature_columns)} total)")
        
        return X, y
    
    def train_models(self, X_train: np.ndarray, y_train: np.ndarray, 
                     X_val: np.ndarray, y_val: np.ndarray):
        """Train multiple models and select the best one"""
        print("\n" + "="*60)
        print("Training Multiple Models")
        print("="*60)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # Define models to train
        model_configs = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=42,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42,
                learning_rate=0.1
            ),
            'SVM': SVC(
                kernel='rbf',
                C=1.0,
                gamma='scale',
                random_state=42,
                probability=True
            ),
            'Logistic Regression': LogisticRegression(
                max_iter=1000,
                random_state=42,
                multi_class='multinomial',
                solver='lbfgs'
            )
        }
        
        best_accuracy = 0
        
        for name, model in model_configs.items():
            print(f"\nTraining {name}...")
            
            # Train model
            if name == 'SVM' or name == 'Logistic Regression':
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_val_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_val)
            
            # Evaluate
            accuracy = accuracy_score(y_val, y_pred)
            print(f"{name} Validation Accuracy: {accuracy:.4f}")
            
            self.models[name] = {
                'model': model,
                'accuracy': accuracy,
                'predictions': y_pred
            }
            
            # Track best model
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                self.best_model = model
                self.best_model_name = name
        
        print(f"\n{'='*60}")
        print(f"Best Model: {self.best_model_name} (Accuracy: {best_accuracy:.4f})")
        print(f"{'='*60}")
        
        return self.best_model_name
    
    def evaluate_best_model(self, X_test: np.ndarray, y_test: np.ndarray):
        """Evaluate the best model on test set"""
        print(f"\nEvaluating {self.best_model_name} on test set...")
        
        # Scale test data if needed
        if self.best_model_name == 'SVM' or self.best_model_name == 'Logistic Regression':
            X_test_scaled = self.scaler.transform(X_test)
            y_pred = self.best_model.predict(X_test_scaled)
        else:
            y_pred = self.best_model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nTest Set Results:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                  target_names=['Weak', 'Medium', 'Strong']))
        
        print(f"\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        
        return {
            'accuracy': accuracy,
            'predictions': y_pred,
            'confusion_matrix': cm
        }
    
    def save_model(self, filename: str = 'password_strength_model.pkl'):
        """Save the best model and scaler"""
        if self.best_model is None:
            raise ValueError("No model trained yet. Call train_models() first.")
        
        model_data = {
            'model': self.best_model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'model_name': self.best_model_name
        }
        
        joblib.dump(model_data, filename)
        print(f"\nModel saved to {filename}")
    
    def run_training_pipeline(self):
        """Run the complete training pipeline"""
        # Load data
        X, y = self.load_data()
        
        # Split data: 60% train, 20% validation, 20% test
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.4, random_state=42, stratify=y
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
        )
        
        print(f"\nData Split:")
        print(f"Training set: {len(X_train)} samples")
        print(f"Validation set: {len(X_val)} samples")
        print(f"Test set: {len(X_test)} samples")
        
        # Train models
        self.train_models(X_train, y_train, X_val, y_val)
        
        # Evaluate best model
        results = self.evaluate_best_model(X_test, y_test)
        
        # Save model
        self.save_model()
        
        return results


if __name__ == "__main__":
    trainer = PasswordStrengthTrainer()
    results = trainer.run_training_pipeline()

