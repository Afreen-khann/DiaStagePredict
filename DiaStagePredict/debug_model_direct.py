"""
Debug: Test the model file directly with exact values
"""

import pickle
import numpy as np

print("=" * 80)
print("DIRECT MODEL FILE TEST")
print("=" * 80)

# Load model
print("\nLoading model from: ./static/Models/diabetes_model.pkl")
with open('./static/Models/diabetes_model.pkl', 'rb') as f:
    model = pickle.load(f)

print(f"Model type: {type(model)}")
print(f"Model: {model}")

# Test with extreme high-risk values
print("\n" + "=" * 80)
print("TEST: Extreme High Risk Values")
print("=" * 80)

test_values = {
    'Pregnancies': 15,
    'Glucose': 200,
    'BloodPressure': 120,
    'SkinThickness': 99,
    'Insulin': 400,
    'BMI': 60.2,
    'DiabetesPedigreeFunction': 2.4,
    'Age': 75
}

print("\nInput Values:")
for key, value in test_values.items():
    print(f"  {key}: {value}")

# Create feature array in correct order
features = [
    test_values['Pregnancies'],
    test_values['Glucose'],
    test_values['BloodPressure'],
    test_values['SkinThickness'],
    test_values['Insulin'],
    test_values['BMI'],
    test_values['DiabetesPedigreeFunction'],
    test_values['Age']
]

print(f"\nFeature array: {features}")

# Make prediction
features_array = np.array([features])
print(f"Features shape: {features_array.shape}")

prediction = model.predict(features_array)[0]
probabilities = model.predict_proba(features_array)[0]
risk_score = probabilities[1] * 100

print("\n" + "=" * 80)
print("PREDICTION RESULT:")
print("=" * 80)
print(f"Prediction: {prediction} ({'DIABETES' if prediction == 1 else 'NO DIABETES'})")
print(f"Probabilities: No Diabetes={probabilities[0]*100:.1f}%, Diabetes={probabilities[1]*100:.1f}%")
print(f"Risk Score: {risk_score:.1f}%")

if risk_score >= 80:
    print("\n✅ CORRECT! Model predicts high risk as expected")
else:
    print(f"\n❌ WRONG! Model predicts {risk_score:.1f}% but should predict ~90%")
    print("\nThis means the model file is the OLD model!")
    print("The training might have failed or the file wasn't saved correctly.")

print("\n" + "=" * 80)
