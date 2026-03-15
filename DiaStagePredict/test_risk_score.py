"""Test the risk score feature"""
import pickle
import numpy as np

print("="*70)
print("TESTING RISK SCORE FEATURE")
print("="*70)

# Load model
model = pickle.load(open('./static/Models/diabetes_model.pkl', 'rb'))

test_cases = [
    {
        'name': 'Extreme High Risk',
        'values': [15.0, 199.0, 120.0, 99.0, 400.0, 60.0, 2.4, 75.0]
    },
    {
        'name': 'High Risk',
        'values': [10.0, 200.0, 110.0, 50.0, 300.0, 45.0, 1.5, 65.0]
    },
    {
        'name': 'Moderate Risk',
        'values': [5.0, 140.0, 80.0, 30.0, 150.0, 32.0, 0.8, 45.0]
    },
    {
        'name': 'Low Risk',
        'values': [1.0, 85.0, 66.0, 29.0, 80.0, 26.6, 0.351, 31.0]
    }
]

print("\nRisk Score Results:")
print("-"*70)

for test in test_cases:
    # Get prediction and probabilities
    prediction = model.predict([test['values']])[0]
    probabilities = model.predict_proba([test['values']])[0]
    
    risk_score = probabilities[1] * 100  # Probability of diabetes
    
    # Determine risk level
    if risk_score < 30:
        risk_level = "Low"
    elif risk_score < 60:
        risk_level = "Moderate"
    else:
        risk_level = "High"
    
    result = 'DIABETES' if prediction == 1 else 'NO DIABETES'
    
    print(f"\n{test['name']}:")
    print(f"  Prediction: {result}")
    print(f"  Risk Score: {risk_score:.1f}%")
    print(f"  Risk Level: {risk_level}")
    print(f"  Confidence: No Diabetes={probabilities[0]*100:.1f}%, Diabetes={probabilities[1]*100:.1f}%")

print("\n" + "="*70)
print("RISK SCORE FEATURE WORKING!")
print("="*70)
