import pandas as pd
import pickle
import numpy as np

# Load dataset
df = pd.read_csv('static/Models/diabetes.csv')

print("="*60)
print("DATASET ANALYSIS")
print("="*60)

print('\nZero values per column:')
print((df == 0).sum())

print('\nColumns with suspicious zeros:')
suspicious = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in suspicious:
    zero_count = (df[col] == 0).sum()
    print(f'{col}: {zero_count} zeros ({zero_count/len(df)*100:.1f}%)')

print("\n" + "="*60)
print("MODEL TESTING")
print("="*60)

# Load model
model = pickle.load(open('static/Models/diabetes_model.pkl', 'rb'))
print(f'\nModel type: {type(model).__name__}')

# Test cases
test_cases = [
    {
        'name': 'High Risk Case 1',
        'values': [10, 200, 110, 50, 300, 45.0, 1.5, 65],
        'expected': 'Diabetes'
    },
    {
        'name': 'High Risk Case 2',
        'values': [8, 183, 100, 40, 250, 40.5, 1.8, 55],
        'expected': 'Diabetes'
    },
    {
        'name': 'Low Risk Case',
        'values': [1, 85, 66, 29, 80, 26.6, 0.351, 31],
        'expected': 'No Diabetes'
    },
    {
        'name': 'Extreme High Risk',
        'values': [15, 199, 120, 99, 400, 60.0, 2.4, 75],
        'expected': 'Diabetes'
    }
]

print('\nTest Results:')
for test in test_cases:
    features = np.array([test['values']])
    prediction = model.predict(features)[0]
    result = 'Diabetes' if prediction == 1 else 'No Diabetes'
    status = '✓' if result == test['expected'] else '✗'
    print(f"\n{status} {test['name']}")
    print(f"  Input: {test['values']}")
    print(f"  Predicted: {result}, Expected: {test['expected']}")
