import pickle
import numpy as np

# Simulate the exact code from app.py output() function
model = pickle.load(open('./static/Models/diabetes_model.pkl', 'rb'))

# Simulate form data - this is what request.form.values() returns
# High risk values
form_values = ['10', '200', '110', '50', '300', '45.0', '1.5', '65']

print("="*60)
print("SIMULATING APP.PY BUG")
print("="*60)

print("\nForm values (as strings):", form_values)

# This is the EXACT code from app.py lines 62-63
int_features = [x for x in form_values]
final_features = [np.array(int_features)]

print("\nint_features:", int_features)
print("Type of int_features[0]:", type(int_features[0]))
print("\nfinal_features shape:", np.array(final_features).shape)
print("final_features dtype:", np.array(final_features).dtype)

try:
    prediction = model.predict(final_features)
    output = prediction[0]
    print("\n✓ Prediction successful:", output)
    print("Result:", "Diabetes" if output == 1 else "No Diabetes")
except Exception as e:
    print("\n✗ Prediction failed:", str(e))

print("\n" + "="*60)
print("CORRECT APPROACH")
print("="*60)

# Correct approach - convert strings to floats
int_features_correct = [float(x) for x in form_values]
final_features_correct = [np.array(int_features_correct)]

print("\nint_features_correct:", int_features_correct)
print("Type of int_features_correct[0]:", type(int_features_correct[0]))
print("\nfinal_features_correct shape:", np.array(final_features_correct).shape)
print("final_features_correct dtype:", np.array(final_features_correct).dtype)

prediction_correct = model.predict(final_features_correct)
output_correct = prediction_correct[0]
print("\n✓ Prediction:", output_correct)
print("Result:", "Diabetes" if output_correct == 1 else "No Diabetes")
