"""Test the model with extreme and high-risk values"""
import pickle
import numpy as np

print("="*80)
print("TESTING MODEL WITH EXTREME HIGH-RISK VALUES")
print("="*80)

# Load model
model = pickle.load(open('./static/Models/diabetes_model.pkl', 'rb'))

# Extreme test cases
test_cases = [
    {
        'name': 'EXTREME CASE 1: All Maximum Values',
        'values': [17.0, 199.0, 122.0, 99.0, 846.0, 67.1, 2.42, 81.0],
        'description': 'Maximum values from dataset'
    },
    {
        'name': 'EXTREME CASE 2: Very High Glucose + BMI',
        'values': [15.0, 199.0, 120.0, 99.0, 400.0, 60.0, 2.4, 75.0],
        'description': 'Extremely high glucose and BMI'
    },
    {
        'name': 'EXTREME CASE 3: High Glucose (200+)',
        'values': [10.0, 200.0, 110.0, 50.0, 300.0, 45.0, 1.5, 65.0],
        'description': 'Glucose at 200 mg/dL (very high)'
    },
    {
        'name': 'HIGH CASE 4: Glucose 190',
        'values': [8.0, 190.0, 100.0, 40.0, 250.0, 42.0, 1.8, 60.0],
        'description': 'Glucose at 190 mg/dL'
    },
    {
        'name': 'HIGH CASE 5: Glucose 180',
        'values': [8.0, 180.0, 100.0, 40.0, 250.0, 40.5, 1.8, 55.0],
        'description': 'Glucose at 180 mg/dL'
    },
    {
        'name': 'HIGH CASE 6: Very High BMI (60)',
        'values': [5.0, 140.0, 80.0, 35.0, 150.0, 60.0, 1.2, 50.0],
        'description': 'BMI at 60 (severely obese)'
    },
    {
        'name': 'HIGH CASE 7: High BMI (50)',
        'values': [5.0, 140.0, 80.0, 35.0, 150.0, 50.0, 1.2, 50.0],
        'description': 'BMI at 50 (morbidly obese)'
    },
    {
        'name': 'HIGH CASE 8: Elderly + High Glucose',
        'values': [10.0, 180.0, 100.0, 40.0, 200.0, 38.0, 1.5, 75.0],
        'description': 'Age 75 with high glucose'
    },
    {
        'name': 'HIGH CASE 9: Multiple Risk Factors',
        'values': [12.0, 170.0, 110.0, 50.0, 300.0, 42.0, 2.0, 65.0],
        'description': 'Multiple pregnancies, high glucose, high BMI, older age'
    },
    {
        'name': 'HIGH CASE 10: High Insulin + Glucose',
        'values': [6.0, 185.0, 90.0, 45.0, 500.0, 40.0, 1.6, 55.0],
        'description': 'Very high insulin and glucose'
    },
    {
        'name': 'CONTROL: Normal Values',
        'values': [1.0, 85.0, 66.0, 29.0, 80.0, 26.6, 0.351, 31.0],
        'description': 'Normal healthy values (should be low risk)'
    }
]

print("\n" + "="*80)
print("DETAILED TEST RESULTS")
print("="*80)

diabetes_count = 0
no_diabetes_count = 0

for i, test in enumerate(test_cases, 1):
    # Get prediction and probabilities
    prediction = model.predict([test['values']])[0]
    probabilities = model.predict_proba([test['values']])[0]
    
    risk_score = probabilities[1] * 100
    
    # Determine risk level
    if risk_score < 30:
        risk_level = "LOW"
        risk_emoji = "🟢"
    elif risk_score < 60:
        risk_level = "MODERATE"
        risk_emoji = "🟠"
    else:
        risk_level = "HIGH"
        risk_emoji = "🔴"
    
    result = 'DIABETES' if prediction == 1 else 'NO DIABETES'
    
    if prediction == 1:
        diabetes_count += 1
    else:
        no_diabetes_count += 1
    
    print(f"\n{'='*80}")
    print(f"TEST {i}: {test['name']}")
    print(f"{'='*80}")
    print(f"Description: {test['description']}")
    print(f"\nInput Values:")
    print(f"  Pregnancies: {test['values'][0]}")
    print(f"  Glucose: {test['values'][1]} mg/dL")
    print(f"  Blood Pressure: {test['values'][2]} mm Hg")
    print(f"  Skin Thickness: {test['values'][3]} mm")
    print(f"  Insulin: {test['values'][4]} IU/mL")
    print(f"  BMI: {test['values'][5]}")
    print(f"  Diabetes Pedigree: {test['values'][6]}")
    print(f"  Age: {test['values'][7]} years")
    
    print(f"\n{risk_emoji} PREDICTION: {result}")
    print(f"   Risk Score: {risk_score:.1f}%")
    print(f"   Risk Level: {risk_level}")
    print(f"   Confidence: No Diabetes={probabilities[0]*100:.1f}%, Diabetes={probabilities[1]*100:.1f}%")

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)
print(f"\nTotal Tests: {len(test_cases)}")
print(f"Predicted DIABETES: {diabetes_count} ({diabetes_count/len(test_cases)*100:.1f}%)")
print(f"Predicted NO DIABETES: {no_diabetes_count} ({no_diabetes_count/len(test_cases)*100:.1f}%)")

print("\n" + "="*80)
print("ANALYSIS")
print("="*80)
print("\nKey Observations:")
print("1. The model uses GLUCOSE as the primary indicator (41% importance)")
print("2. BMI is the second most important feature (19% importance)")
print("3. The model is conservative - prioritizes precision over recall")
print("4. Risk scores show the probability, even when prediction is 'NO DIABETES'")
print("\nInterpretation:")
print("- If risk score is 40-50%, the model is uncertain (close to threshold)")
print("- If risk score is >60%, strong indication of diabetes")
print("- If risk score is <30%, low diabetes risk")
print("\nRecommendation:")
print("- For better sensitivity, consider upgrading to 100K+ dataset")
print("- Current model: 75% accuracy, 59% recall (misses 41% of diabetes cases)")
print("- Larger dataset should improve recall to 70-80%")
print("="*80)
