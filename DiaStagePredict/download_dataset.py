"""
Dataset Download Helper Script
This script helps you download a larger diabetes dataset from Kaggle
"""

import os
import sys

def print_instructions():
    print("=" * 80)
    print("DIABETES DATASET UPGRADE - DOWNLOAD INSTRUCTIONS")
    print("=" * 80)
    print()
    print("To get a larger dataset and improve model predictions, follow these steps:")
    print()
    print("OPTION 1: Manual Download (Recommended)")
    print("-" * 80)
    print("1. Go to Kaggle:")
    print("   https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset")
    print()
    print("2. Click 'Download' button (you may need to create a free Kaggle account)")
    print()
    print("3. Extract the ZIP file and find 'diabetes_prediction_dataset.csv'")
    print()
    print("4. Copy it to: DiaStagePredict/static/Models/diabetes.csv")
    print("   (Replace the existing file)")
    print()
    print("5. Run: python train_model.py")
    print()
    print("=" * 80)
    print()
    print("OPTION 2: Using Kaggle API (Advanced)")
    print("-" * 80)
    print("1. Install Kaggle API:")
    print("   pip install kaggle")
    print()
    print("2. Set up Kaggle credentials:")
    print("   - Go to https://www.kaggle.com/settings")
    print("   - Click 'Create New API Token'")
    print("   - Place kaggle.json in: ~/.kaggle/kaggle.json (Linux/Mac)")
    print("     or C:\\Users\\<username>\\.kaggle\\kaggle.json (Windows)")
    print()
    print("3. Run this script with --download flag:")
    print("   python download_dataset.py --download")
    print()
    print("=" * 80)
    print()
    
    choice = input("Do you want to try automatic download now? (yes/no): ").lower()
    if choice in ['yes', 'y']:
        try_automatic_download()
    else:
        print("\nPlease follow Option 1 (Manual Download) above.")
        print("After downloading, run: python train_model.py")

def try_automatic_download():
    print("\nAttempting automatic download...")
    
    try:
        import kaggle
        print("✓ Kaggle API found")
    except ImportError:
        print("✗ Kaggle API not installed")
        print("\nInstalling Kaggle API...")
        os.system(f"{sys.executable} -m pip install kaggle")
        try:
            import kaggle
            print("✓ Kaggle API installed successfully")
        except:
            print("✗ Failed to install Kaggle API")
            print("Please use Option 1 (Manual Download)")
            return
    
    # Check for Kaggle credentials
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    if not os.path.exists(kaggle_json_path):
        kaggle_json_path_win = os.path.expanduser("~/.kaggle/kaggle.json")
        if not os.path.exists(kaggle_json_path_win):
            print("\n✗ Kaggle credentials not found")
            print("Please set up Kaggle API credentials first:")
            print("1. Go to https://www.kaggle.com/settings")
            print("2. Click 'Create New API Token'")
            print("3. Place kaggle.json in ~/.kaggle/ directory")
            return
    
    print("✓ Kaggle credentials found")
    print("\nDownloading dataset...")
    
    try:
        # Download the dataset
        os.system("kaggle datasets download -d iammustafatz/diabetes-prediction-dataset")
        
        print("✓ Dataset downloaded")
        print("\nExtracting...")
        
        import zipfile
        with zipfile.ZipFile("diabetes-prediction-dataset.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        print("✓ Dataset extracted")
        
        # Move to correct location
        if os.path.exists("diabetes_prediction_dataset.csv"):
            # Backup old dataset
            if os.path.exists("./static/Models/diabetes.csv"):
                os.rename("./static/Models/diabetes.csv", "./static/Models/diabetes_old_768.csv")
                print("✓ Old dataset backed up")
            
            # Move new dataset
            os.rename("diabetes_prediction_dataset.csv", "./static/Models/diabetes.csv")
            print("✓ New dataset installed")
            
            # Clean up
            if os.path.exists("diabetes-prediction-dataset.zip"):
                os.remove("diabetes-prediction-dataset.zip")
            
            print("\n" + "=" * 80)
            print("SUCCESS! Dataset upgraded successfully!")
            print("=" * 80)
            print("\nNext step: Retrain the model")
            print("Run: python train_model.py")
            print()
            
        else:
            print("✗ Could not find extracted CSV file")
            print("Please use Option 1 (Manual Download)")
            
    except Exception as e:
        print(f"\n✗ Error during download: {e}")
        print("\nPlease use Option 1 (Manual Download) instead")

if __name__ == "__main__":
    if "--download" in sys.argv:
        try_automatic_download()
    else:
        print_instructions()
