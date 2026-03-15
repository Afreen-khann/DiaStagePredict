"""
Generate Synthetic Diabetes Dataset
Creates a larger, more balanced dataset with realistic patterns
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

# Set random seed for reproducibility
np.random.seed(42)

def generate_synthetic_diabetes_data(n_samples=10000):
    """
    Generate synthetic diabetes dataset with realistic patterns
    """
    print(f"Generating {n_samples} synthetic samples...")
    
    # Load original data to understand distributions
    original_df = pd.read_csv('./static/Models/diabetes_old_768.csv')
    
    # Create empty dataframe
    data = []
    
    # Generate samples with realistic distributions
    for i in range(n_samples):
        # Randomly decide if this person has diabetes (50% balanced)
        has_diabetes = np.random.choice([0, 1], p=[0.65, 0.35])
        
        if has_diabetes == 1:
            # High-risk profile (diabetes positive)
            pregnancies = np.random.randint(0, 18)
            glucose = np.random.normal(150, 30)  # Higher glucose
            glucose = np.clip(glucose, 80, 200)
            blood_pressure = np.random.normal(85, 15)
            blood_pressure = np.clip(blood_pressure, 50, 122)
            skin_thickness = np.random.normal(30, 15)
            skin_thickness = np.clip(skin_thickness, 0, 99)
            insulin = np.random.normal(200, 100)
            insulin = np.clip(insulin, 0, 846)
            bmi = np.random.normal(35, 8)  # Higher BMI
            bmi = np.clip(bmi, 20, 67)
            dpf = np.random.normal(0.8, 0.4)
            dpf = np.clip(dpf, 0.078, 2.42)
            age = np.random.normal(50, 15)
            age = np.clip(age, 21, 81)
        else:
            # Low-risk profile (diabetes negative)
            pregnancies = np.random.randint(0, 10)
            glucose = np.random.normal(110, 20)  # Normal glucose
            glucose = np.clip(glucose, 60, 140)
            blood_pressure = np.random.normal(75, 12)
            blood_pressure = np.clip(blood_pressure, 50, 100)
            skin_thickness = np.random.normal(25, 10)
            skin_thickness = np.clip(skin_thickness, 0, 50)
            insulin = np.random.normal(120, 60)
            insulin = np.clip(insulin, 0, 300)
            bmi = np.random.normal(26, 5)  # Normal BMI
            bmi = np.clip(bmi, 18, 35)
            dpf = np.random.normal(0.4, 0.3)
            dpf = np.clip(dpf, 0.078, 1.5)
            age = np.random.normal(35, 12)
            age = np.clip(age, 21, 70)
        
        # Add some noise and edge cases
        if np.random.random() < 0.1:  # 10% extreme cases
            if has_diabetes == 1:
                glucose = np.random.uniform(180, 200)
                bmi = np.random.uniform(40, 60)
        
        data.append({
            'Pregnancies': int(pregnancies),
            'Glucose': round(glucose, 1),
            'BloodPressure': round(blood_pressure, 1),
            'SkinThickness': round(skin_thickness, 1),
            'Insulin': round(insulin, 1),
            'BMI': round(bmi, 1),
            'DiabetesPedigreeFunction': round(dpf, 3),
            'Age': int(age),
            'Outcome': has_diabetes
        })
    
    df = pd.DataFrame(data)
    
    # Combine with original data
    combined_df = pd.concat([original_df, df], ignore_index=True)
    
    print(f"\nDataset Statistics:")
    print(f"Total samples: {len(combined_df)}")
    print(f"Diabetes cases: {combined_df['Outcome'].sum()} ({combined_df['Outcome'].mean()*100:.1f}%)")
    print(f"Non-diabetes cases: {(combined_df['Outcome']==0).sum()} ({(1-combined_df['Outcome'].mean())*100:.1f}%)")
    
    return combined_df

if __name__ == "__main__":
    print("=" * 80)
    print("SYNTHETIC DIABETES DATASET GENERATOR")
    print("=" * 80)
    print()
    
    # Generate dataset
    df = generate_synthetic_diabetes_data(n_samples=10000)
    
    # Save new dataset (no backup needed, we already have diabetes_old_768.csv)
    print("\nSaving new dataset...")
    df.to_csv('./static/Models/diabetes.csv', index=False)
    print("✓ New dataset saved to: diabetes.csv")
    
    print("\n" + "=" * 80)
    print("SUCCESS! Dataset upgraded with synthetic data")
    print("=" * 80)
    print("\nNext step: Retrain the model")
    print("Run: python train_model.py")
    print()
