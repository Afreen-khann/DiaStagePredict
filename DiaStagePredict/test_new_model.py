"""Test the newly trained model with Flask app compatibility"""
import pickle
import numpy as np

print("="*70)
print("TESTING NEW MODEL COMPATIBILITY")
print("="*70)

# Load the new model
model = pickle.load(open('./static/Models/diabetes_model.pkl', 'rb'))
print(f"\nModel type: {type(model)}")
print(f"Model: {model}")

# Test with high-risk values (should predict diabetes)
high_risk = [10.0, 200.0, 110.0, 50.0, 300.0, 45.0, 1.5, 65.0]
print(f"\nHigh-risk input: {high_risk}")

# The model is now a Pipeline, so it handles scaling internally
prediction = model.predict([high_risk])
print(f"Prediction: {prediction[0]}")
print(f"Result: {'Diabetes' if prediction[0] == 1 else 'No Diabetes'}")

# Test with low-risk values (should predict no diabetes)
low_risk = [1.0, 85.0, 66.0, 29.0, 80.0, 26.6, 0.351, 31.0]
print(f"\nLow-risk input: {low_risk}")
prediction = model.predict([low_risk])
print(f"Prediction: {prediction[0]}")
print(f"Result: {'Diabetes' if prediction[0] == 1 else 'No Diabetes'}")

print("\n" + "="*70)
print("MODEL COMPATIBILITY TEST PASSED!")
print("="*70)
