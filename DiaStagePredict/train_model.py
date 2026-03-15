"""
Diabetes Prediction Model Training Pipeline

This script implements a reproducible training pipeline that:
1. Loads and validates the diabetes dataset
2. Handles missing values (zeros) appropriately
3. Trains multiple classification models
4. Evaluates and selects the best model
5. Saves the model for use in the Flask application

Author: DiaStagePredict Team
Date: 2026-03-12
"""

import os
import sys
import logging
import pickle
from datetime import datetime
from typing import Dict, List, Tuple, Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)
from sklearn.pipeline import Pipeline
import sklearn

# Configuration Constants
CONFIG = {
    'data_path': './static/Models/diabetes.csv',
    'model_path': './static/Models/diabetes_model.pkl',
    'scaler_path': './static/Models/scaler.pkl',
    'report_path': './static/Models/model_evaluation_report.txt',
    'random_state': 42,
    'test_size': 0.2,
    'features_with_missing_zeros': [
        'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI'
    ],
    'imputation_strategy': 'median',
    'models': {
        'RandomForestClassifier': {'random_state': 42, 'n_estimators': 100},
        'LogisticRegression': {'random_state': 42, 'max_iter': 1000},
        'GradientBoostingClassifier': {'random_state': 42, 'n_estimators': 100}
    }
}

# Required feature columns
REQUIRED_FEATURES = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'
]

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)



class DataLoader:
    """Handles loading and validation of the diabetes dataset"""
    
    def __init__(self, filepath: str, required_features: List[str]):
        """
        Initialize DataLoader
        
        Args:
            filepath: Path to the CSV file
            required_features: List of required column names
        """
        self.filepath = filepath
        self.required_features = required_features
    
    def load_data(self) -> pd.DataFrame:
        """
        Load CSV and validate required columns
        
        Returns:
            DataFrame with validated data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required columns are missing
            pd.errors.ParserError: If CSV is malformed
        """
        logger.info(f"Loading data from {self.filepath}")
        
        # Check if file exists
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(
                f"Dataset file not found: {self.filepath}. "
                f"Please ensure the file exists at the specified path."
            )
        
        try:
            # Load CSV
            df = pd.read_csv(self.filepath)
            logger.info(f"Successfully loaded {len(df)} rows")
            
            # Validate schema
            self.validate_schema(df)
            
            return df
            
        except pd.errors.ParserError as e:
            raise pd.errors.ParserError(
                f"Failed to parse CSV file {self.filepath}. "
                f"Please ensure the file is a valid CSV format. Error: {str(e)}"
            )
    
    def validate_schema(self, df: pd.DataFrame) -> bool:
        """
        Ensure all required columns are present
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If required columns are missing
        """
        missing_cols = set(self.required_features) - set(df.columns)
        
        if missing_cols:
            raise ValueError(
                f"Missing required columns: {sorted(missing_cols)}. "
                f"Expected columns: {self.required_features}"
            )
        
        logger.info("Schema validation passed - all required columns present")
        return True

    
    def log_statistics(self, df: pd.DataFrame) -> None:
        """
        Log dataset shape and basic statistics
        
        Args:
            df: DataFrame to analyze
        """
        logger.info("="*70)
        logger.info("DATASET STATISTICS")
        logger.info("="*70)
        logger.info(f"Dataset shape: {df.shape}")
        logger.info(f"Total samples: {len(df)}")
        
        # Class distribution
        if 'Outcome' in df.columns:
            class_dist = df['Outcome'].value_counts().to_dict()
            logger.info(f"Class distribution: {class_dist}")
            logger.info(f"  - No diabetes (0): {class_dist.get(0, 0)} ({class_dist.get(0, 0)/len(df)*100:.1f}%)")
            logger.info(f"  - Diabetes (1): {class_dist.get(1, 0)} ({class_dist.get(1, 0)/len(df)*100:.1f}%)")
        
        # Basic statistics for features
        logger.info("\nFeature Statistics:")
        for col in df.columns:
            if col != 'Outcome':
                logger.info(f"  {col}: mean={df[col].mean():.2f}, std={df[col].std():.2f}, "
                          f"min={df[col].min():.2f}, max={df[col].max():.2f}")
        logger.info("="*70)



class DataCleaner:
    """Handles detection and imputation of missing values"""
    
    def __init__(self, features_with_zeros_as_missing: List[str]):
        """
        Initialize DataCleaner
        
        Args:
            features_with_zeros_as_missing: List of features where 0 indicates missing data
        """
        self.features_with_missing = features_with_zeros_as_missing
        self.imputation_values = {}
    
    def detect_missing(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Count zeros in specified features (zeros represent missing values)
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary mapping feature names to count of missing values
        """
        logger.info("="*70)
        logger.info("MISSING VALUE DETECTION")
        logger.info("="*70)
        
        missing_counts = {}
        total_rows = len(df)
        
        for feature in self.features_with_missing:
            if feature in df.columns:
                zero_count = (df[feature] == 0).sum()
                missing_counts[feature] = zero_count
                percentage = (zero_count / total_rows) * 100
                
                logger.info(f"{feature}: {zero_count} zeros ({percentage:.1f}% missing)")
        
        logger.info("="*70)
        return missing_counts

    
    def create_imputer(self, strategy: str = 'median') -> SimpleImputer:
        """
        Create sklearn imputer with specified strategy
        
        Args:
            strategy: Imputation strategy ('median', 'mean', 'most_frequent')
            
        Returns:
            Configured SimpleImputer instance
        """
        return SimpleImputer(strategy=strategy, missing_values=0)
    
    def fit_transform(self, X_train: pd.DataFrame) -> Tuple[np.ndarray, SimpleImputer]:
        """
        Fit imputer on training data and transform
        
        Args:
            X_train: Training features DataFrame
            
        Returns:
            Tuple of (transformed array, fitted imputer)
        """
        logger.info("="*70)
        logger.info("IMPUTATION - TRAINING DATA")
        logger.info("="*70)
        
        # Create imputer
        imputer = self.create_imputer(strategy='median')
        
        # Fit and transform
        X_train_imputed = imputer.fit_transform(X_train)
        
        # Log imputation values
        logger.info("Imputation values (medians from training data):")
        for idx, feature in enumerate(X_train.columns):
            if feature in self.features_with_missing:
                imputed_value = imputer.statistics_[idx]
                self.imputation_values[feature] = imputed_value
                logger.info(f"  {feature}: {imputed_value:.2f}")
        
        logger.info("="*70)
        return X_train_imputed, imputer
    
    def transform(self, X_test: pd.DataFrame, imputer: SimpleImputer) -> np.ndarray:
        """
        Apply fitted imputer to test data
        
        Args:
            X_test: Test features DataFrame
            imputer: Fitted SimpleImputer instance
            
        Returns:
            Transformed array
        """
        logger.info("Applying imputation to test data...")
        X_test_imputed = imputer.transform(X_test)
        return X_test_imputed



def split_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> Tuple:
    """
    Split dataset into training and test sets with stratification
    
    Args:
        df: Complete dataset
        test_size: Proportion of data for testing
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    logger.info("="*70)
    logger.info("TRAIN/TEST SPLIT")
    logger.info("="*70)
    
    # Separate features and target
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    # Stratified split to maintain class distribution
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state,
        stratify=y
    )
    
    logger.info(f"Training samples: {len(X_train)} ({len(X_train)/len(df)*100:.1f}%)")
    logger.info(f"Test samples: {len(X_test)} ({len(X_test)/len(df)*100:.1f}%)")
    logger.info(f"Training class distribution: {y_train.value_counts().to_dict()}")
    logger.info(f"Test class distribution: {y_test.value_counts().to_dict()}")
    logger.info("="*70)
    
    return X_train, X_test, y_train, y_test



def scale_features(X_train: np.ndarray, X_test: np.ndarray) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    """
    Apply feature scaling using StandardScaler
    
    Args:
        X_train: Training features
        X_test: Test features
        
    Returns:
        Tuple of (scaled X_train, scaled X_test, fitted scaler)
    """
    logger.info("="*70)
    logger.info("FEATURE SCALING")
    logger.info("="*70)
    
    # Create and fit scaler on training data only
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Apply same transformation to test data
    X_test_scaled = scaler.transform(X_test)
    
    logger.info("StandardScaler fitted on training data")
    logger.info(f"Training data scaled - mean≈0, std≈1")
    logger.info(f"Test data scaled using training statistics")
    logger.info("="*70)
    
    return X_train_scaled, X_test_scaled, scaler



class ModelTrainer:
    """Handles training of multiple classification models"""
    
    def __init__(self, random_state: int = 42):
        """
        Initialize ModelTrainer
        
        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
    
    def get_candidate_models(self) -> Dict[str, Any]:
        """
        Return dictionary of model name -> instantiated classifier
        
        Returns:
            Dictionary mapping model names to configured classifiers
        """
        models = {
            'RandomForestClassifier': RandomForestClassifier(
                random_state=self.random_state,
                n_estimators=100
            ),
            'LogisticRegression': LogisticRegression(
                random_state=self.random_state,
                max_iter=1000
            ),
            'GradientBoostingClassifier': GradientBoostingClassifier(
                random_state=self.random_state,
                n_estimators=100
            )
        }
        return models
    
    def train_model(self, model: Any, X_train: np.ndarray, y_train: np.ndarray, model_name: str) -> Any:
        """
        Fit a single model
        
        Args:
            model: Classifier instance
            X_train: Training features
            y_train: Training labels
            model_name: Name of the model for logging
            
        Returns:
            Fitted model
        """
        logger.info(f"Training {model_name}...")
        model.fit(X_train, y_train)
        logger.info(f"  [OK] {model_name} training completed")
        return model
    
    def train_all(self, X_train: np.ndarray, y_train: np.ndarray) -> Dict[str, Any]:
        """
        Train all candidate models
        
        Args:
            X_train: Training features
            y_train: Training labels
            
        Returns:
            Dictionary mapping model names to fitted models
        """
        logger.info("="*70)
        logger.info("MODEL TRAINING")
        logger.info("="*70)
        
        models = self.get_candidate_models()
        trained_models = {}
        
        for name, model in models.items():
            trained_models[name] = self.train_model(model, X_train, y_train, name)
        
        logger.info(f"Successfully trained {len(trained_models)} models")
        logger.info("="*70)
        return trained_models



class ModelEvaluator:
    """Handles model evaluation and selection"""
    
    def evaluate_model(self, model: Any, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """
        Calculate accuracy, precision, recall, F1-score
        
        Args:
            model: Trained classifier
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary of metric names to values
        """
        y_pred = model.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, zero_division=0)
        }
        
        return metrics
    
    def get_confusion_matrix(self, model: Any, X_test: np.ndarray, y_test: np.ndarray) -> np.ndarray:
        """
        Generate confusion matrix
        
        Args:
            model: Trained classifier
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Confusion matrix as numpy array
        """
        y_pred = model.predict(X_test)
        return confusion_matrix(y_test, y_pred)
    
    def select_best_model(self, results: Dict[str, Dict[str, float]]) -> str:
        """
        Select model with highest accuracy, F1 as tiebreaker
        
        Args:
            results: Dictionary mapping model names to their metrics
            
        Returns:
            Name of the best model
        """
        # Sort by accuracy (primary), then F1-score (tiebreaker)
        best_model = max(
            results.items(),
            key=lambda x: (x[1]['accuracy'], x[1]['f1_score'])
        )[0]
        
        return best_model
    
    def evaluate_all(self, models: Dict[str, Any], X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Dict[str, float]]:
        """
        Evaluate all models and return results
        
        Args:
            models: Dictionary of model names to trained models
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary mapping model names to their metrics
        """
        logger.info("="*70)
        logger.info("MODEL EVALUATION")
        logger.info("="*70)
        
        results = {}
        for name, model in models.items():
            logger.info(f"Evaluating {name}...")
            results[name] = self.evaluate_model(model, X_test, y_test)
        
        logger.info("="*70)
        return results

    
    def generate_report(self, results: Dict[str, Dict[str, float]], best_model_name: str, 
                       best_model: Any, X_test: np.ndarray, y_test: np.ndarray,
                       imputation_values: Dict[str, float], dataset_info: Dict) -> str:
        """
        Create formatted evaluation report
        
        Args:
            results: Dictionary of model metrics
            best_model_name: Name of the best performing model
            best_model: The best model instance
            X_test: Test features
            y_test: Test labels
            imputation_values: Dictionary of imputed values
            dataset_info: Dataset statistics
            
        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("="*70)
        report_lines.append("MODEL EVALUATION REPORT")
        report_lines.append("="*70)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Scikit-learn version: {sklearn.__version__}")
        report_lines.append(f"Random seed: {CONFIG['random_state']}")
        report_lines.append("")
        
        # Dataset statistics
        report_lines.append("Dataset Statistics:")
        report_lines.append(f"  Total samples: {dataset_info['total_samples']}")
        report_lines.append(f"  Training samples: {dataset_info['train_samples']}")
        report_lines.append(f"  Test samples: {dataset_info['test_samples']}")
        report_lines.append(f"  Class distribution: {dataset_info['class_distribution']}")
        report_lines.append("")
        
        # Missing value imputation
        report_lines.append("Missing Value Imputation:")
        for feature, value in imputation_values.items():
            report_lines.append(f"  {feature}: zeros replaced with median {value:.2f}")
        report_lines.append("")
        
        # Model performance
        report_lines.append("Model Performance:")
        report_lines.append(f"{'Model':<30} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10}")
        report_lines.append("-"*70)
        
        for model_name, metrics in results.items():
            marker = " <- BEST" if model_name == best_model_name else ""
            report_lines.append(
                f"{model_name:<30} "
                f"{metrics['accuracy']:<10.4f} "
                f"{metrics['precision']:<10.4f} "
                f"{metrics['recall']:<10.4f} "
                f"{metrics['f1_score']:<10.4f}{marker}"
            )
        
        report_lines.append("")
        report_lines.append(f"Best Model: {best_model_name}")
        report_lines.append("")
        
        # Confusion matrix
        cm = self.get_confusion_matrix(best_model, X_test, y_test)
        report_lines.append("Confusion Matrix (Best Model):")
        report_lines.append("              Predicted")
        report_lines.append("              0    1")
        report_lines.append(f"Actual  0   [{cm[0][0]:>4} {cm[0][1]:>4}]")
        report_lines.append(f"        1   [{cm[1][0]:>4} {cm[1][1]:>4}]")
        report_lines.append("")
        
        # Feature importance (if available)
        if hasattr(best_model, 'feature_importances_'):
            report_lines.append(f"Feature Importance ({best_model_name}):")
            feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                           'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
            importances = list(zip(feature_names, best_model.feature_importances_))
            importances.sort(key=lambda x: x[1], reverse=True)
            
            for idx, (feature, importance) in enumerate(importances, 1):
                report_lines.append(f"  {idx}. {feature}: {importance:.4f}")
        
        report_lines.append("="*70)
        
        return "\n".join(report_lines)



class ModelPersister:
    """Handles saving of trained models and artifacts"""
    
    def __init__(self, model_dir: str = './static/Models'):
        """
        Initialize ModelPersister
        
        Args:
            model_dir: Directory for model artifacts
        """
        self.model_dir = model_dir
    
    def backup_existing_model(self, filepath: str) -> None:
        """
        Create timestamped backup of existing model
        
        Args:
            filepath: Path to existing model file
        """
        if os.path.exists(filepath):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = filepath.replace('.pkl', f'_backup_{timestamp}.pkl')
            
            try:
                import shutil
                shutil.copy2(filepath, backup_path)
                logger.info(f"Created backup: {backup_path}")
            except Exception as e:
                logger.warning(f"Failed to create backup: {str(e)}")
    
    def save_model(self, model: Any, filepath: str) -> None:
        """
        Serialize model using pickle
        
        Args:
            model: Trained model to save
            filepath: Destination file path
        """
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Model saved to: {filepath}")
    
    def save_scaler(self, scaler: StandardScaler, filepath: str) -> None:
        """
        Serialize scaler using pickle
        
        Args:
            scaler: Fitted scaler to save
            filepath: Destination file path
        """
        with open(filepath, 'wb') as f:
            pickle.dump(scaler, f)
        logger.info(f"Scaler saved to: {filepath}")
    
    def save_report(self, report: str, filepath: str) -> None:
        """
        Write evaluation report to text file
        
        Args:
            report: Report content
            filepath: Destination file path
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"Report saved to: {filepath}")
    
    def verify_model_loads(self, filepath: str) -> bool:
        """
        Attempt to load saved model
        
        Args:
            filepath: Path to model file
            
        Returns:
            True if model loads successfully
        """
        try:
            with open(filepath, 'rb') as f:
                model = pickle.load(f)
            logger.info("[OK] Model verification: Successfully loaded saved model")
            return True
        except Exception as e:
            logger.error(f"[FAIL] Model verification failed: {str(e)}")
            return False



def main():
    """Main pipeline orchestration function"""
    try:
        logger.info("="*70)
        logger.info("DIABETES PREDICTION MODEL TRAINING PIPELINE")
        logger.info("="*70)
        logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Scikit-learn version: {sklearn.__version__}")
        logger.info(f"Random seed: {CONFIG['random_state']}")
        logger.info("="*70)
        
        # Step 1: Load data
        data_loader = DataLoader(CONFIG['data_path'], REQUIRED_FEATURES)
        df = data_loader.load_data()
        data_loader.log_statistics(df)
        
        # Step 2: Detect missing values
        data_cleaner = DataCleaner(CONFIG['features_with_missing_zeros'])
        missing_counts = data_cleaner.detect_missing(df)
        
        # Step 3: Split data
        X_train, X_test, y_train, y_test = split_data(
            df, 
            test_size=CONFIG['test_size'],
            random_state=CONFIG['random_state']
        )
        
        # Step 4: Impute missing values
        X_train_imputed, imputer = data_cleaner.fit_transform(X_train)
        X_test_imputed = data_cleaner.transform(X_test, imputer)
        
        # Step 5: Scale features
        X_train_scaled, X_test_scaled, scaler = scale_features(X_train_imputed, X_test_imputed)
        
        # Step 6: Train models
        trainer = ModelTrainer(random_state=CONFIG['random_state'])
        trained_models = trainer.train_all(X_train_scaled, y_train)
        
        # Step 7: Evaluate models
        evaluator = ModelEvaluator()
        results = evaluator.evaluate_all(trained_models, X_test_scaled, y_test)
        
        # Step 8: Select best model
        best_model_name = evaluator.select_best_model(results)
        best_model = trained_models[best_model_name]
        
        logger.info("="*70)
        logger.info(f"BEST MODEL SELECTED: {best_model_name}")
        logger.info(f"  Accuracy: {results[best_model_name]['accuracy']:.4f}")
        logger.info(f"  F1-Score: {results[best_model_name]['f1_score']:.4f}")
        logger.info("="*70)
        
        # Step 9: Create Pipeline (scaler + model) for Flask compatibility
        model_pipeline = Pipeline([
            ('scaler', scaler),
            ('classifier', best_model)
        ])
        
        # Step 10: Generate report
        dataset_info = {
            'total_samples': len(df),
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'class_distribution': df['Outcome'].value_counts().to_dict()
        }
        
        report = evaluator.generate_report(
            results, best_model_name, best_model,
            X_test_scaled, y_test,
            data_cleaner.imputation_values,
            dataset_info
        )
        
        # Display report
        print("\n" + report + "\n")
        
        # Step 11: Save artifacts
        persister = ModelPersister()
        
        # Backup existing model
        persister.backup_existing_model(CONFIG['model_path'])
        
        # Save new model pipeline
        persister.save_model(model_pipeline, CONFIG['model_path'])
        
        # Save report
        persister.save_report(report, CONFIG['report_path'])
        
        # Verify model loads
        persister.verify_model_loads(CONFIG['model_path'])
        
        logger.info("="*70)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*70)
        
        return True
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        return False
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
