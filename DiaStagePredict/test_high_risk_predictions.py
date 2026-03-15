"""Test the new model with various high-risk inputs"""
import pickle
import numpy as np

print("="*70)
print("TESTING NEW MODEL WITH HIGH-RISK VALUES")
print("="*70)

# Load the new model
model = pickle.load(open('./static/Models/diabetes_model.pkl', 'rb'))

# Test cases with high-risk values
test_cases = [
    {
        'name': 'Extreme High Risk',
        'values': [15.0, 199.0, 120.0, 99.0, 400.0, 60.0, 2.4, 75.0],
        'description': 'Very high glucose, BMI, age'
    },
    {
        'name': 'High Risk Case 1',
        'values': [10.0, 200.0, 110.0, 50.0, 300.0, 45.0, 1.5, 65.0],
        'description': 'High glucose, BMI, insulin'
    },
    {
        'name': 'High Risk Case 2',
        'values': [8.0, 183.0, 100.0, 40.0, 250.0, 40.5, 1.8, 55.0],
        'description': 'High glucose and BMI'
    },
    {
        'name': 'High Glucose Only',
        'values': [3.0, 190.0, 70.0, 25.0, 100.0, 28.0, 0.5, 35.0],
        'description': 'Very high glucose'
    },
    {
        'name': 'High BMI Only',
        'values': [3.0, 110.0, 70.0, 25.0, 100.0, 55.0, 0.5, 35.0],
        'description': 'Very high BMI'
    },
    {
        'name': 'Low Risk (Control)',
        'values': [1.0, 85.0, 66.0, 29.0, 80.0, 26.6, 0.351, 31.0],
        'description': 'Normal values'
    }
]

print("\nTest Results:")
print("-"*70)

for test in test_cases:
    prediction = model.predict([test['values']])[0]
    result = 'DIABETES' if prediction == 1 else 'NO DIABETES'
    
    print(f"\n{test['name']}:")
    print(f"  Description: {test['description']}")
    print(f"  Input: {test['values']}")
    print(f"  Prediction: {result}")
    
    # Show key features
    glucose = test['values'][1]
    bmi = test['values'][5]
    age = test['values'][7]
    print(f"  Key features: Glucose={glucose}, BMI={bmi}, Age={age}")

print("\n" + "="*70)
print("ANALYSIS")
print("="*70)
print("\nThe model's predictions are based on the training data patterns.")
print("If high-risk values are predicting 'NO DIABETES', it could mean:")
print("1. The model learned that these specific combinations don't always")
print("   indicate diabetes in the training data")
print("2. The model may be conservative (prioritizing precision over recall)")
print("3. The training data may not have enough examples of these patterns")
print("\nModel Performance from Training:")
print("  - Accuracy: 75.32%")
print("  - Precision: 66.67% (when it says diabetes, it's right 67% of time)")
print("  - Recall: 59.26% (catches 59% of actual diabetes cases)")
print("="*70)
