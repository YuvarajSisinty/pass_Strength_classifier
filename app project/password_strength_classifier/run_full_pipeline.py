"""
Quick Start Script - Runs the complete pipeline
Generates dataset, trains model, and evaluates it
"""

import os
import sys

def main():
    print("="*60)
    print("Password Strength Classifier - Full Pipeline")
    print("="*60)
    
    # Step 1: Generate dataset
    print("\n[Step 1/3] Generating password dataset...")
    print("-" * 60)
    from dataset_generator import PasswordDatasetGenerator
    generator = PasswordDatasetGenerator()
    dataset = generator.generate_dataset(samples_per_class=1000)
    generator.save_dataset(dataset, 'password_dataset.csv')
    
    # Step 2: Train model
    print("\n[Step 2/3] Training ML models...")
    print("-" * 60)
    from train_model import PasswordStrengthTrainer
    trainer = PasswordStrengthTrainer()
    results = trainer.run_training_pipeline()
    
    # Step 3: Evaluate model
    print("\n[Step 3/3] Evaluating model...")
    print("-" * 60)
    from evaluate_model import ModelEvaluator
    evaluator = ModelEvaluator()
    summary = evaluator.evaluate_on_dataset()
    
    # Test sample passwords
    print("\n" + "="*60)
    print("Testing on Sample Passwords")
    print("="*60)
    evaluator.test_sample_passwords()
    
    print("\n" + "="*60)
    print("Pipeline Complete! ✓")
    print("="*60)
    print("\nYou can now use the classifier:")
    print("  python password_classifier.py")
    print("\nOr test specific passwords:")
    print('  python password_classifier.py "password123" "MyP@ssw0rd!2024"')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

