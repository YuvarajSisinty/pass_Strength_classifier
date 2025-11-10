"""
Dataset Generator for Password Strength Classification
Generates labeled password datasets for training ML models
"""

import random
import string
import pandas as pd
from feature_extractor import PasswordFeatureExtractor


class PasswordDatasetGenerator:
    """Generates labeled password datasets with different strength levels"""
    
    def __init__(self):
        self.feature_extractor = PasswordFeatureExtractor()
        self.common_passwords = [
            'password', '123456', '123456789', 'password123', 'admin',
            'qwerty', 'abc123', 'letmein', 'welcome', 'monkey'
        ]
    
    def generate_weak_passwords(self, count: int) -> list:
        """Generate weak passwords (short, simple, common)"""
        passwords = []
        
        # Common passwords
        for _ in range(count // 3):
            passwords.append(random.choice(self.common_passwords))
        
        # Short passwords
        for _ in range(count // 3):
            length = random.randint(4, 6)
            password = ''.join(random.choices(string.ascii_lowercase, k=length))
            passwords.append(password)
        
        # Simple numeric passwords
        for _ in range(count - len(passwords)):
            length = random.randint(4, 6)
            password = ''.join(random.choices(string.digits, k=length))
            passwords.append(password)
        
        return passwords[:count]
    
    def generate_medium_passwords(self, count: int) -> list:
        """Generate medium strength passwords"""
        passwords = []
        
        # Mixed case, some digits
        for _ in range(count // 2):
            length = random.randint(7, 10)
            chars = string.ascii_letters + string.digits
            password = ''.join(random.choices(chars, k=length))
            # Ensure at least one uppercase and one digit
            if not any(c.isupper() for c in password):
                password = password[0].upper() + password[1:]
            if not any(c.isdigit() for c in password):
                password = password[:-1] + str(random.randint(0, 9))
            passwords.append(password)
        
        # Lowercase with digits
        for _ in range(count - len(passwords)):
            length = random.randint(8, 12)
            chars = string.ascii_lowercase + string.digits
            password = ''.join(random.choices(chars, k=length))
            passwords.append(password)
        
        return passwords[:count]
    
    def generate_strong_passwords(self, count: int) -> list:
        """Generate strong passwords (long, complex, high entropy)"""
        passwords = []
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Full complexity passwords
        for _ in range(count):
            length = random.randint(12, 20)
            chars = string.ascii_letters + string.digits + special_chars
            password = ''.join(random.choices(chars, k=length))
            
            # Ensure all character types are present
            if not any(c.isupper() for c in password):
                idx = random.randint(0, len(password) - 1)
                password = password[:idx] + random.choice(string.ascii_uppercase) + password[idx+1:]
            if not any(c.islower() for c in password):
                idx = random.randint(0, len(password) - 1)
                password = password[:idx] + random.choice(string.ascii_lowercase) + password[idx+1:]
            if not any(c.isdigit() for c in password):
                idx = random.randint(0, len(password) - 1)
                password = password[:idx] + random.choice(string.digits) + password[idx+1:]
            if not any(c in special_chars for c in password):
                idx = random.randint(0, len(password) - 1)
                password = password[:idx] + random.choice(special_chars) + password[idx+1:]
            
            passwords.append(password)
        
        return passwords[:count]
    
    def generate_dataset(self, samples_per_class: int = 1000) -> pd.DataFrame:
        """
        Generate a complete labeled dataset
        
        Args:
            samples_per_class: Number of samples for each strength class
            
        Returns:
            DataFrame with passwords and labels
        """
        print("Generating password dataset...")
        
        # Generate passwords for each class
        weak_passwords = self.generate_weak_passwords(samples_per_class)
        medium_passwords = self.generate_medium_passwords(samples_per_class)
        strong_passwords = self.generate_strong_passwords(samples_per_class)
        
        # Create labels (0: Weak, 1: Medium, 2: Strong)
        passwords = weak_passwords + medium_passwords + strong_passwords
        labels = [0] * len(weak_passwords) + [1] * len(medium_passwords) + [2] * len(strong_passwords)
        
        # Extract features
        print("Extracting features...")
        features_list = []
        for password in passwords:
            features = self.feature_extractor.extract_features(password)
            features_list.append(features)
        
        # Create DataFrame
        df = pd.DataFrame(features_list)
        df['password'] = passwords
        df['strength_label'] = labels
        df['strength_name'] = df['strength_label'].map({0: 'Weak', 1: 'Medium', 2: 'Strong'})
        
        # Shuffle the dataset
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        print(f"Dataset generated: {len(df)} samples")
        print(f"Class distribution:")
        print(df['strength_name'].value_counts())
        
        return df
    
    def save_dataset(self, df: pd.DataFrame, filename: str = 'password_dataset.csv'):
        """Save dataset to CSV file"""
        df.to_csv(filename, index=False)
        print(f"Dataset saved to {filename}")


if __name__ == "__main__":
    generator = PasswordDatasetGenerator()
    dataset = generator.generate_dataset(samples_per_class=1000)
    generator.save_dataset(dataset, 'password_dataset.csv')

