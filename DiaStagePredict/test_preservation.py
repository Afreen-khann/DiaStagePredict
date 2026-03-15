"""
Preservation Property Tests for Diabetes Prediction Accuracy Fix

Property 2: Preservation - Unchanged Application Behavior

These tests capture the baseline behavior on UNFIXED code that must be preserved.
Tests should PASS on both unfixed and fixed code.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pickle
import numpy as np
from app import app
from profiler import generateOutput, generateProfile
import unittest


class TestPreservation(unittest.TestCase):
    """
    Test that existing correct behavior is preserved after the fix.
    
    These tests observe behavior on UNFIXED code and verify it remains unchanged.
    """
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_low_risk_prediction_preserved(self):
        """
        Test Case: Low-risk input should continue to predict "no diabetes"
        
        Observe on UNFIXED code: Glucose=85, BMI=26.6, Age=31 predicts "no diabetes"
        Preserve: This behavior must remain unchanged after fix
        """
        form_data = {
            'Pregnancies': '1',
            'Glucose': '85',
            'BloodPressure': '66',
            'SkinThickness': '29',
            'Insulin': '80',
            'BMI': '26.6',
            'DiabetesPedigreeFunction': '0.351',
            'Age': '31'
        }
        
        response = self.app.post('/output', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        response_text = response.data.decode('utf-8')
        
        # Low-risk should predict "no diabetes"
        self.assertIn('does not suffer from diabetes', response_text,
                     "Low-risk input should continue to predict no diabetes")

    def test_output_formatting_preserved(self):
        """
        Test Case: generateOutput() formatting must remain unchanged
        
        Observe: Output format is "From the given profile our model has predicted : ..."
        Preserve: This exact format must remain after fix
        """
        # Test prediction 0 (no diabetes)
        output_0 = generateOutput(0)
        self.assertEqual(output_0, 
                        'From the given profile our model has predicted : The person does not suffer from diabetes.',
                        "Output format for prediction 0 must be preserved")
        
        # Test prediction 1 (diabetes)
        output_1 = generateOutput(1)
        self.assertEqual(output_1,
                        'From the given profile our model has predicted : The person does suffer from diabetes.',
                        "Output format for prediction 1 must be preserved")
    
    def test_profile_formatting_preserved(self):
        """
        Test Case: generateProfile() formatting must remain unchanged
        
        Observe: Profile format is "FieldName  :  value"
        Preserve: This exact format must remain after fix
        """
        test_data = {
            'Pregnancies': '5',
            'Glucose': '120',
            'BMI': '30.5'
        }
        
        profile = generateProfile(test_data)
        
        # Check that profile is a list
        self.assertIsInstance(profile, list)
        
        # Check format of each item
        self.assertIn('Pregnancies  :  5', profile)
        self.assertIn('Glucose  :  120', profile)
        self.assertIn('BMI  :  30.5', profile)
    
    def test_form_interface_preserved(self):
        """
        Test Case: Form accepts same input fields with same names
        
        Observe: Form accepts 8 fields with specific names
        Preserve: Field names and structure must remain unchanged
        """
        # All 8 required fields
        form_data = {
            'Pregnancies': '3',
            'Glucose': '100',
            'BloodPressure': '70',
            'SkinThickness': '25',
            'Insulin': '100',
            'BMI': '28.0',
            'DiabetesPedigreeFunction': '0.5',
            'Age': '35'
        }
        
        response = self.app.post('/output', data=form_data, follow_redirects=True)
        
        # Should successfully process the form
        self.assertEqual(response.status_code, 200)
        
        # Should contain prediction result
        response_text = response.data.decode('utf-8')
        self.assertIn('From the given profile our model has predicted', response_text)
    
    def test_multiple_low_risk_cases_preserved(self):
        """
        Test Case: Multiple low-risk cases should all predict "no diabetes"
        
        Property-based approach: Test several low-risk profiles
        """
        low_risk_cases = [
            {
                'Pregnancies': '0', 'Glucose': '90', 'BloodPressure': '70',
                'SkinThickness': '20', 'Insulin': '90', 'BMI': '22.0',
                'DiabetesPedigreeFunction': '0.3', 'Age': '25'
            },
            {
                'Pregnancies': '2', 'Glucose': '100', 'BloodPressure': '75',
                'SkinThickness': '25', 'Insulin': '100', 'BMI': '24.5',
                'DiabetesPedigreeFunction': '0.4', 'Age': '30'
            },
            {
                'Pregnancies': '1', 'Glucose': '95', 'BloodPressure': '68',
                'SkinThickness': '22', 'Insulin': '85', 'BMI': '23.0',
                'DiabetesPedigreeFunction': '0.35', 'Age': '28'
            }
        ]
        
        for case in low_risk_cases:
            response = self.app.post('/output', data=case, follow_redirects=True)
            response_text = response.data.decode('utf-8')
            
            # All low-risk cases should predict no diabetes
            self.assertIn('does not suffer from diabetes', response_text,
                         f"Low-risk case {case} should predict no diabetes")


if __name__ == '__main__':
    print("="*70)
    print("PRESERVATION PROPERTY TESTS")
    print("="*70)
    print("\nThese tests capture baseline behavior that must be preserved.")
    print("Tests should PASS on both unfixed and fixed code.\n")
    
    # Run tests
    unittest.main(verbosity=2)
