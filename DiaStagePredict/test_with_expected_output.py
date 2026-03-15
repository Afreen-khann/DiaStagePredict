"""
Test Model with Expected Outputs
Shows exact values to enter and what the prediction should be
"""

import pickle
import numpy as np

# Load the trained model
print("Loading model...")
with open('./static/Models/diabetes_model.pkl', 'rb') as f:
    model = f.read()
    model = pickle.loads(model)

print("Model loaded successfully!")
print("=" * 80)

# Test cases with expected outputs
test_cases = [
    {
        "name": "TEST 1: EXTREME HIGH RISK",
        "values": {
            "Height (cm)": 160,
            "Weight (kg)": 154,
            "Pregnancies": 15,
            "Glucose": 200,
            "Blood Pressure": 120,
            "Skin Thickness": 99,
            "Insulin": 400,
            "BMI": 60.2,
            "Diabetes Pedigree": 2.4,
            "Age": 75
        },
        "expected": "DIABETES (90-100% risk)"
    },
    {
        "name": "TEST 2: HIGH GLUCOSE",
        "values": {
            "Height (cm)": 165,
            "Weight (kg)": 114,
            "Pregnancies": 10,
            "Glucose": 190,
            "Blood Pressure": 100,
            "Skin Thickness": 40,
            "Insulin": 250,
            "BMI": 41.9,
            "Diabetes Pedigree": 1.8,
            "Age": 60
        },
        "expected": "DIABETES (95-100% risk)"
    },
    {
        "name": "TEST 3: MORBID OBESITY",
        "values": {
            "Height (cm)": 160,
            "Weight (kg)": 128,
            "Pregnancies": 5,
            "Glucose": 140,
            "Blood Pressure": 80,
            "Skin Thickness": 35,
            "Insulin": 150,
            "BMI": 50.0,
            "Diabetes Pedigree": 1.2,
            "Age": 50
        },
        "expected": "DIABETES (90-95% risk)"
    },
    {
        "name": "TEST 4: NORMAL HEALTHY",
        "values": {
            "Height (cm)": 165,
            "Weight (kg)": 72,
            "Pregnancies": 1,
            "Glucose": 85,
            "Blood Pressure": 66,
            "Skin Thickness": 29,
            "Insulin": 80,
            "BMI": 26.4,
            "Diabetes Pedigree": 0.351,
            "Age": 31
        },
        "expected": "NO DIABETES (0-10% risk)"
    },
    {
        "name": "TEST 5: MODERATE RISK",
        "values": {
            "Height (cm)": 170,
            "Weight (kg)": 92,
            "Pregnancies": 3,
            "Glucose": 130,
            "Blood Pressure": 85,
            "Skin Thickness": 30,
            "Insulin": 120,
            "BMI": 31.8,
            "Diabetes Pedigree": 0.8,
            "Age": 45
        },
        "expected": "MODERATE RISK (40-60%)"
    }
]

# Run predictions
for i, test in enumerate(test_cases, 1):
    print(f"\n{'=' * 80}")
    print(f"{test['name']}")
    print(f"{'=' * 80}")
    
    # Extract features (model only uses these 8 features)
    features = [
        test['values']['Pregnancies'],
        test['values']['Glucose'],
        test['values']['Blood Pressure'],
        test['values']['Skin Thickness'],
        test['values']['Insulin'],
        test['values']['BMI'],
        test['values']['Diabetes Pedigree'],
        test['values']['Age']
    ]
    
    # Print input values
    print("\n📋 INPUT VALUES TO ENTER IN FORM:")
    print("-" * 80)
    for key, value in test['values'].items():
        print(f"  {key:25s}: {value}")
    
    # Make prediction
    features_array = np.array([features])
    prediction = model.predict(features_array)[0]
    probability = model.predict_proba(features_array)[0]
    
    risk_score = probability[1] * 100  # Probability of diabetes
    
    # Determine result
    if prediction == 1:
        result = "🔴 DIABETES"
    else:
        result = "🟢 NO DIABETES"
    
    # Determine risk level
    if risk_score < 30:
        risk_level = "LOW"
    elif risk_score < 60:
        risk_level = "MODERATE"
    else:
        risk_level = "HIGH"
    
    print("\n" + "=" * 80)
    print("✅ EXPECTED OUTPUT:")
    print(f"  {test['expected']}")
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("🤖 ACTUAL MODEL PREDICTION:")
    print(f"  Prediction: {result}")
    print(f"  Risk Score: {risk_score:.1f}%")
    print(f"  Risk Level: {risk_level}")
    print(f"  Confidence: No Diabetes={probability[0]*100:.1f}%, Diabetes={probability[1]*100:.1f}%")
    print("=" * 80)
    
    # Check if matches expected
    if prediction == 1 and "DIABETES" in test['expected']:
        print("✅ CORRECT - Matches expected output!")
    elif prediction == 0 and "NO DIABETES" in test['expected']:
        print("✅ CORRECT - Matches expected output!")
    else:
        print("❌ MISMATCH - Does not match expected output!")
    
    print()

print("\n" + "=" * 80)
print("TESTING COMPLETE")
print("=" * 80)
print("\nNOTE: If you see mismatches, restart your Flask app:")
print("  1. Press Ctrl+C to stop the app")
print("  2. Run: python app.py")
print("  3. Refresh your browser")
print("  4. Try the test values again")
print()
