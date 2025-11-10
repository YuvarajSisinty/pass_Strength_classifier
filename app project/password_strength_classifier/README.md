# Password Strength Classifier 🔐

A machine learning-based password strength classification system that evaluates passwords and categorizes them into **Weak**, **Medium**, or **Strong** strength levels. This project combines cybersecurity principles with machine learning techniques to provide accurate password strength assessment.

## Features

- 🤖 **Machine Learning Models**: Trains multiple ML algorithms (Random Forest, Gradient Boosting, SVM, Logistic Regression) and selects the best performer
- 📊 **Comprehensive Feature Engineering**: Extracts 30+ features including:
  - Length metrics (length, log length)
  - Character type analysis (uppercase, lowercase, digits, special characters)
  - Entropy calculation (Shannon entropy)
  - Complexity scoring
  - Pattern detection (sequential chars, repetitions, keyboard patterns)
- 📈 **Detailed Evaluation**: 
  - Precision, Recall, and F1-score metrics
  - Confusion matrix analysis
  - Per-class and macro/weighted averages
  - Visual confusion matrix plots
- 🎯 **Easy-to-Use Interface**: Interactive CLI tool for password classification
- 📦 **Complete Pipeline**: Dataset generation, model training, and evaluation scripts

## Project Structure

```
password_strength_classifier/
├── feature_extractor.py      # Feature engineering module
├── dataset_generator.py      # Generates labeled password datasets
├── train_model.py            # Model training script
├── evaluate_model.py         # Comprehensive model evaluation
├── password_classifier.py    # Main application (interactive CLI)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd password_strength_classifier
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Generate Training Dataset

First, generate a labeled dataset of passwords:

```bash
python dataset_generator.py
```

This creates `password_dataset.csv` with 3000 samples (1000 per class: Weak, Medium, Strong).

### Step 2: Train the Model

Train multiple ML models and select the best one:

```bash
python train_model.py
```

This will:
- Load the dataset
- Split into train/validation/test sets
- Train 4 different models
- Select the best performing model
- Save the model to `password_strength_model.pkl`

### Step 3: Evaluate the Model

Run comprehensive evaluation with detailed metrics:

```bash
python evaluate_model.py
```

This provides:
- Overall accuracy
- Per-class precision, recall, and F1-scores
- Macro and weighted averages
- Confusion matrix (printed and visualized)
- Classification report
- Sample password predictions

### Step 4: Use the Classifier

**Interactive Mode:**
```bash
python password_classifier.py
```

Then enter passwords one by one to get strength classifications.

**Command Line Mode:**
```bash
python password_classifier.py "password123" "MyP@ssw0rd!2024" "abc"
```

## Features Extracted

The model uses 30+ features to assess password strength:

### Length Features
- Password length
- Logarithmic length

### Character Type Features
- Count of uppercase, lowercase, digits, special characters
- Ratios of each character type
- Presence flags for each character type
- Character type diversity count

### Entropy Features
- Shannon entropy (measures randomness)
- Normalized entropy

### Complexity Features
- Complexity score (based on multiple factors)
- Sequential character patterns
- Repeated character patterns
- Keyboard pattern detection

### Pattern Detection
- Common password detection
- Sequence detection
- Repetition detection
- Position-based features

## Model Performance

The training script evaluates multiple algorithms:
- **Random Forest**: Ensemble method with high accuracy
- **Gradient Boosting**: Sequential ensemble learning
- **SVM**: Support Vector Machine with RBF kernel
- **Logistic Regression**: Linear classification model

The best model is automatically selected based on validation accuracy.

## Evaluation Metrics

The evaluation script provides:

1. **Accuracy**: Overall classification accuracy
2. **Precision**: Per-class and average precision scores
3. **Recall**: Per-class and average recall scores
4. **F1-Score**: Harmonic mean of precision and recall
5. **Confusion Matrix**: Visual representation of classification results

### Example Output

```
MODEL EVALUATION RESULTS
============================================================

Overall Accuracy: 0.9542

Per-Class Metrics
============================================================
Class     Precision    Recall    F1-Score
Weak      0.9650       0.9420    0.9534
Medium    0.9234       0.9512    0.9371
Strong    0.9742       0.9695    0.9718

Average Metrics
============================================================
Macro Average:
  Precision: 0.9542
  Recall: 0.9542
  F1-Score: 0.9541
```

## Example Classifications

```
Password: password123
Strength: 🟡 Medium
Confidence: Weak: 15%, Medium: 75%, Strong: 10%

Password: Kx9#mP2$vL7@nQ5
Strength: 🟢 Strong
Confidence: Weak: 2%, Medium: 8%, Strong: 90%

Password: 123456
Strength: 🔴 Weak
Confidence: Weak: 95%, Medium: 5%, Strong: 0%
```

## Technical Details

### Machine Learning Approach
- **Supervised Learning**: Classification problem with 3 classes
- **Feature Scaling**: StandardScaler for SVM and Logistic Regression
- **Model Selection**: Best model chosen based on validation set performance
- **Evaluation**: Train/Validation/Test split (60/20/20)

### Cybersecurity Principles
- **Entropy Calculation**: Measures password randomness
- **Pattern Detection**: Identifies common weak patterns
- **Complexity Scoring**: Multi-factor complexity assessment
- **Common Password Detection**: Flags known weak passwords

## Requirements

- Python 3.8+
- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn
- joblib

## Future Enhancements

- Integration with password breach databases (Have I Been Pwned API)
- Real-time password strength feedback
- Web API interface
- Additional ML models (Neural Networks, XGBoost)
- Customizable strength thresholds
- Password generation suggestions

## License

This project is for educational and demonstration purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Disclaimer

This tool is designed for educational purposes and password strength assessment. Always follow best security practices and use strong, unique passwords for important accounts.

