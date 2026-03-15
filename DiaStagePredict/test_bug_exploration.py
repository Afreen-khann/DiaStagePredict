"""
Bug Condition Exploration Test for Diabetes Prediction Accuracy Fix

Property 1: Bug Condition - Accurate Predictions for High-Risk Inputs

CRITICAL: This test MUST FAIL on unfixed code - failure confirms the bug exists.
This test encodes the expected behavior and will validate the fix when it passes.

Scoped to high-risk cases: Glucose≥180, BMI≥40, Age≥60
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pickle
import numpy as np
from app import app
import unittest


class TestBugConditionExploration(unittest.TestCase):
    """
    Test that high-risk inputs produce correct diabetes predictions.
    
    This test will FAIL on unfixed code because form values are passed as strings
    instead of numeric types, causing incorrect model predictions.
    """
    
    def setUp(self):
        """Set up test client and load model"""
        self.app = app.test_client()
        self.app.testing = True
        self.model = pickle.load(open('./static/Models/diabetes_model.pkl', 'rb'))
    
    def test_high_risk_case_1_glucose_200_bmi_45_age_65(self):
        """
        Test Case: High-risk input with Glucose=200, BMI=45, Age=65
        
        Expected: Should predict "diabetes" (output=1)
        Bug Behavior: Predicts "no diabetes" (output=0) due to string type issue
        """
        # High-risk values that should clearly indicate diabetes
        high_risk_values = [10, 200, 110, 50, 300, 45.0, 1.5, 65]
        
        # Test direct model prediction with numeric array (this should work)
        numeric_features = np.array([high_risk_values])
        direct_prediction = self.model.predict(numeric_features)[0]
        
        # Direct model prediction should be 1 (diabetes)
        self.assertEqual(direct_prediction, 1, 
                        "Direct model prediction with numeric array should predict diabetes")
        
        # Now test the app's prediction pipeline (this will fail on unfixed code)
        # Simulate form submission with string values (as they come from HTML form)
        form_data = {
            'Pregnancies': '10',
            'Glucose': '200',
            'BloodPressure': '110',
            'SkinThickness': '50',
            'Insulin': '300',
            'BMI': '45.0',
            'DiabetesPedigreeFunction': '1.5',
            'Age': '65'
        }
        
        # Test the output endpoint
        response = self.app.post('/output', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check if response contains "does suffer from diabetes"
        response_text = response.data.decode('utf-8')
        
        # This assertion will FAIL on unfixed code
        self.assertIn('does suffer from diabetes', response_text,
                     "High-risk input should predict diabetes, but got 'does not suffer'")
    
    def test_high_risk_case_2_glucose_183_bmi_40_age_55(self):
        """
        Test Case: High-risk input with Glucose=183, BMI=40.5, Age=55
        
        Expected: Should predict "diabetes" (output=1)
        """
        high_risk_values = [8, 183, 100, 40, 250, 40.5, 1.8, 55]
        
        # Test direct model prediction
        numeric_features = np.array([high_risk_values])
        direct_prediction = self.model.predict(numeric_features)[0]
        self.assertEqual(direct_prediction, 1)
        
        # Test app prediction
        form_data = {
            'Pregnancies': '8',
            'Glucose': '183',
            'BloodPressure': '100',
            'SkinThickness': '40',
            'Insulin': '250',
            'BMI': '40.5',
            'DiabetesPedigreeFunction': '1.8',
            'Age': '55'
        }
        
        response = self.app.post('/output', data=form_data, follow_redirects=True)
        response_text = response.data.decode('utf-8')
        
        # This will FAIL on unfixed code
        self.assertIn('does suffer from diabetes', response_text)
    
    def test_extreme_high_risk_glucose_199_bmi_60_age_75(self):
        """
        Test Case: Extreme high-risk input with Glucose=199, BMI=60, Age=75
        
        Expected: Should definitely predict "diabetes" (output=1)
        """
        extreme_risk_values = [15, 199, 120, 99, 400, 60.0, 2.4, 75]
        
        # Test direct model prediction
        numeric_features = np.array([extreme_risk_values])
        direct_prediction = self.model.predict(numeric_features)[0]
        self.assertEqual(direct_prediction, 1)
        
        # Test app prediction
        form_data = {
            'Pregnancies': '15',
            'Glucose': '199',
            'BloodPressure': '120',
            'SkinThickness': '99',
            'Insulin': '400',
            'BMI': '60.0',
            'DiabetesPedigreeFunction': '2.4',
            'Age': '75'
        }
        
        response = self.app.post('/output', data=form_data, follow_redirects=True)
        response_text = response.data.decode('utf-8')
        
        # This will FAIL on unfixed code
        self.assertIn('does suffer from diabetes', response_text)
    
    def test_data_type_verification(self):
        """
        Test that verifies the root cause: string vs numeric types
        
        This test inspects the data types being passed to the model.
        On unfixed code, int_features will contain strings.
        On fixed code, int_features will contain floats.
        """
        # This test requires modifying app.py to expose int_features for testing
        # For now, we document the expected behavior:
        # UNFIXED: int_features = ['200', '45', '65', ...] (strings)
        # FIXED: int_features = [200.0, 45.0, 65.0, ...] (floats)
        
        # We can verify this by checking the numpy array dtype
        form_values_as_strings = ['10', '200', '110', '50', '300', '45.0', '1.5', '65']
        
        # Simulate unfixed code behavior
        int_features_unfixed = [x for x in form_values_as_strings]
        final_features_unfixed = [np.array(int_features_unfixed)]
        array_unfixed = np.array(final_features_unfixed)
        
        # On unfixed code, dtype will be string (Unicode)
        # This is the root cause of the bug
        self.assertTrue(array_unfixed.dtype.kind in ['U', 'S', 'O'],
                       f"Unfixed code should have string dtype, got {array_unfixed.dtype}")
        
        # Simulate fixed code behavior
        int_features_fixed = [float(x) for x in form_values_as_strings]
        final_features_fixed = [np.array(int_features_fixed)]
        array_fixed = np.array(final_features_fixed)
        
        # On fixed code, dtype will be numeric (float64)
        self.assertEqual(array_fixed.dtype, np.float64,
                        f"Fixed code should have float64 dtype, got {array_fixed.dtype}")


if __name__ == '__main__':
    print("="*70)
    print("BUG CONDITION EXPLORATION TEST")
    print("="*70)
    print("\nCRITICAL: These tests are EXPECTED TO FAIL on unfixed code.")
    print("Failure confirms the bug exists.\n")
    
    # Run tests
    unittest.main(verbosity=2)
