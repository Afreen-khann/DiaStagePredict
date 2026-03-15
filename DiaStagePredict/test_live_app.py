"""
Test the live Flask app to see what it's actually predicting
"""

import requests

# Test case 1: Extreme high risk
test_data = {
    'height': '160',
    'weight': '154',
    'pregnancies': '15',
    'glucose': '200',
    'bloodpressure': '120',
    'skinthickness': '99',
    'insulin': '400',
    'bmi': '60.2',
    'dpf': '2.4',
    'age': '75'
}

print("=" * 80)
print("TESTING LIVE FLASK APP")
print("=" * 80)
print("\nSending POST request to http://127.0.0.1:5000/output")
print("\nTest Data (Extreme High Risk):")
for key, value in test_data.items():
    print(f"  {key}: {value}")

try:
    response = requests.post('http://127.0.0.1:5000/output', data=test_data)
    
    if response.status_code == 200:
        print("\n" + "=" * 80)
        print("✅ REQUEST SUCCESSFUL")
        print("=" * 80)
        
        # Try to extract prediction from HTML
        html = response.text
        
        if "does not suffer from diabetes" in html.lower():
            print("\n🟢 PREDICTION: NO DIABETES")
            print("❌ WRONG! Should predict DIABETES with 90% risk")
        elif "suffer from diabetes" in html.lower() or "diabetes" in html.lower():
            print("\n🔴 PREDICTION: DIABETES")
            print("✅ CORRECT!")
        
        # Try to find risk score
        if "Risk Probability" in html or "risk" in html.lower():
            # Extract risk percentage
            import re
            risk_match = re.search(r'(\d+\.?\d*)%', html)
            if risk_match:
                risk = risk_match.group(1)
                print(f"📊 Risk Score: {risk}%")
                
                risk_float = float(risk)
                if risk_float >= 80:
                    print("✅ Risk score is correct (should be 90%)")
                else:
                    print(f"❌ Risk score is WRONG! Got {risk}%, expected 90%")
    else:
        print(f"\n❌ REQUEST FAILED")
        print(f"Status Code: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Could not connect to Flask app")
    print("Make sure the Flask app is running:")
    print("  cd DiaStagePredict")
    print("  python app.py")
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 80)
