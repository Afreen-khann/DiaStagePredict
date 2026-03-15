# Implementation Plan: Model Retraining with Data Cleaning

## Overview

This plan implements a reproducible training pipeline for the diabetes prediction model that addresses data quality issues (missing values represented as zeros) and version compatibility problems. The pipeline will load data, clean it, train multiple models, evaluate performance, and save the best model in a format compatible with the existing Flask application.

## Tasks

- [x] 1. Set up project structure and configuration
  - Create `train_model.py` script in DiaStagePredict directory
  - Define configuration constants (file paths, random seeds, hyperparameters)
  - Set up logging configuration for pipeline execution
  - _Requirements: 9.1, 9.3, 10.2_

- [ ] 2. Implement DataLoader component
  - [x] 2.1 Create DataLoader class with load_data method
    - Implement CSV loading from DiaStagePredict/static/Models/diabetes.csv
    - Add schema validation to check for required columns
    - Add error handling for file not found and invalid CSV format
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [x] 2.2 Add logging and statistics methods
    - Implement log_statistics method to display dataset shape and class distribution
    - Log basic statistics (mean, std, min, max) for each feature
    - _Requirements: 1.4_
  
  - [ ]* 2.3 Write property test for schema validation
    - **Property 1: Schema Validation**
    - **Validates: Requirements 1.2, 1.3**
    - Generate random dataframes with missing columns and verify ValueError is raised

- [ ] 3. Implement DataCleaner component
  - [x] 3.1 Create DataCleaner class with missing value detection
    - Initialize with list of features where zeros represent missing values
    - Implement detect_missing method to count zeros in specified features
    - Calculate and log percentage of missing values per feature
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  
  - [x] 3.2 Implement imputation functionality
    - Create create_imputer method using sklearn SimpleImputer with median strategy
    - Implement fit_transform method for training data
    - Implement transform method for test data
    - Log imputation values used for each feature
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  
  - [ ]* 3.3 Write property tests for missing value handling
    - **Property 2: Missing Value Identification**
    - **Validates: Requirements 2.1, 2.4**
    - Generate data with zeros in various columns and verify correct identification
  
  - [ ]* 3.4 Write property test for missing value percentage
    - **Property 3: Missing Value Percentage Calculation**
    - **Validates: Requirements 2.2**
    - Generate data with known zero counts and verify percentage calculation
  
  - [ ]* 3.5 Write property test for median imputation
    - **Property 4: Median Imputation**
    - **Validates: Requirements 3.1**
    - Generate data with missing values and verify imputed values equal training median

- [ ] 4. Implement data preprocessing pipeline
  - [x] 4.1 Create train/test split functionality
    - Implement stratified split with 80/20 ratio using sklearn train_test_split
    - Use fixed random seed (42) for reproducibility
    - Separate features (X) from target (y)
    - _Requirements: 4.1, 4.5_
  
  - [ ] 4.2 Implement feature scaling
    - Create StandardScaler instance
    - Fit scaler on training data only
    - Transform both training and test data
    - _Requirements: 4.2, 4.3_
  
  - [ ]* 4.3 Write property test for data leakage prevention
    - **Property 5: Data Leakage Prevention**
    - **Validates: Requirements 3.2, 3.3, 4.3**
    - Verify imputer and scaler fit only on training data
  
  - [ ]* 4.4 Write property test for feature scaling correctness
    - **Property 6: Feature Scaling Correctness**
    - **Validates: Requirements 4.2**
    - Verify scaled training data has mean≈0 and std≈1
  
  - [ ]* 4.5 Write property test for reproducible splits
    - **Property 7: Reproducible Splits**
    - **Validates: Requirements 4.5, 10.1**
    - Verify same seed produces identical train/test splits

- [x] 5. Checkpoint - Verify data pipeline
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement ModelTrainer component
  - [x] 6.1 Create ModelTrainer class with candidate models
    - Initialize with random seed for reproducibility
    - Implement get_candidate_models method returning RandomForestClassifier, LogisticRegression, and GradientBoostingClassifier
    - Configure all models with fixed random_state
    - _Requirements: 5.1, 5.2, 10.1_
  
  - [x] 6.2 Implement model training methods
    - Create train_model method to fit a single model
    - Create train_all method to train all candidate models
    - Add logging for training start/completion for each model
    - _Requirements: 5.1, 9.3_

- [ ] 7. Implement ModelEvaluator component
  - [x] 7.1 Create ModelEvaluator class with evaluation methods
    - Implement evaluate_model method to calculate accuracy, precision, recall, F1-score
    - Implement get_confusion_matrix method
    - Use sklearn metrics (accuracy_score, precision_score, recall_score, f1_score)
    - _Requirements: 5.3, 5.4, 7.2_
  
  - [x] 7.2 Implement model selection logic
    - Create select_best_model method using accuracy as primary criterion
    - Implement F1-score as tiebreaker for equal accuracy
    - _Requirements: 5.5, 5.6_
  
  - [x] 7.3 Implement report generation
    - Create generate_report method to format evaluation results
    - Include all model metrics in tabular format
    - Add confusion matrix for best model
    - Add feature importance scores if available
    - _Requirements: 7.1, 7.2, 7.5_
  
  - [ ]* 7.4 Write property test for model evaluation completeness
    - **Property 8: Model Evaluation Completeness**
    - **Validates: Requirements 5.3, 5.4**
    - Verify all four metrics present and in valid range [0,1]
  
  - [ ]* 7.5 Write property test for best model selection
    - **Property 9: Best Model Selection**
    - **Validates: Requirements 5.5, 5.6**
    - Verify correct model selected based on accuracy and F1-score tiebreaker

- [ ] 8. Implement ModelPersister component
  - [x] 8.1 Create ModelPersister class with backup functionality
    - Initialize with model directory path
    - Implement backup_existing_model method to create timestamped backup
    - _Requirements: 6.4_
  
  - [x] 8.2 Implement model and scaler saving
    - Create save_model method using pickle
    - Create save_scaler method using pickle
    - Save to DiaStagePredict/static/Models/diabetes_model.pkl and scaler.pkl
    - _Requirements: 6.1, 6.2, 6.3_
  
  - [x] 8.3 Implement report saving and verification
    - Create save_report method to write evaluation report to text file
    - Implement verify_model_loads method to test loading saved model
    - Save report to DiaStagePredict/static/Models/model_evaluation_report.txt
    - _Requirements: 6.5, 7.3, 7.4_
  
  - [ ]* 8.4 Write property test for model persistence round-trip
    - **Property 10: Model Persistence Round-Trip**
    - **Validates: Requirements 6.5**
    - Verify predictions identical before and after save/load

- [x] 9. Checkpoint - Verify training and evaluation pipeline
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Implement main pipeline orchestration
  - [x] 10.1 Create main function to orchestrate pipeline
    - Initialize all components (DataLoader, DataCleaner, ModelTrainer, ModelEvaluator, ModelPersister)
    - Execute pipeline steps in sequence: load → clean → split → scale → train → evaluate → save
    - Add comprehensive error handling with descriptive messages
    - _Requirements: 9.1, 9.2, 9.4_
  
  - [x] 10.2 Add logging and progress tracking
    - Log each major step with timestamp
    - Log configuration parameters (random seed, scikit-learn version)
    - Display final evaluation report to console
    - _Requirements: 9.3, 10.2, 10.3_
  
  - [x] 10.3 Add script entry point
    - Add if __name__ == "__main__" block to make script executable
    - _Requirements: 9.1_

- [ ] 11. Implement Flask compatibility wrapper
  - [x] 11.1 Create Pipeline or wrapper for model
    - Decide between sklearn Pipeline (scaler + model) or separate files
    - Ensure model accepts 8 features in correct order
    - Ensure model returns predictions in {0, 1} format
    - _Requirements: 8.1, 8.2, 8.4_
  
  - [x] 11.2 Test compatibility with existing Flask app
    - Load saved model in format expected by app.py
    - Verify no version compatibility warnings
    - Test with sample input matching Flask app format
    - _Requirements: 8.3_
  
  - [ ]* 11.3 Write property test for input format compatibility
    - **Property 11: Input Format Compatibility**
    - **Validates: Requirements 8.1, 8.2, 8.4**
    - Generate random valid inputs and verify model accepts them

- [ ] 12. Implement comprehensive error handling
  - [x] 12.1 Add error handling for data loading
    - Handle FileNotFoundError with descriptive path
    - Handle pd.errors.ParserError for invalid CSV
    - Handle ValueError for missing columns
    - _Requirements: 1.3, 9.4_
  
  - [x] 12.2 Add error handling for training and persistence
    - Handle convergence warnings (log and continue)
    - Handle MemoryError with suggestions
    - Handle OSError and PermissionError for file operations
    - _Requirements: 9.4_
  
  - [ ]* 12.3 Write property test for error handling
    - **Property 12: Error Handling**
    - **Validates: Requirements 9.4**
    - Generate invalid inputs and verify appropriate exceptions raised

- [ ] 13. Final integration and reproducibility testing
  - [x] 13.1 Run complete pipeline end-to-end
    - Execute train_model.py on actual diabetes.csv dataset
    - Verify all output files created in correct locations
    - Verify execution completes within 5 minutes
    - _Requirements: 9.2, 9.5_
  
  - [x] 13.2 Test reproducibility
    - Run pipeline twice with same configuration
    - Compare performance metrics from both runs
    - Verify metrics are identical
    - _Requirements: 10.4_
  
  - [ ]* 13.3 Write property test for end-to-end reproducibility
    - **Property 13: End-to-End Reproducibility**
    - **Validates: Requirements 10.4**
    - Run pipeline multiple times and verify identical metrics

- [x] 14. Final checkpoint - Complete validation
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties from the design document
- The pipeline maintains full compatibility with the existing Flask application
- All stochastic operations use fixed random seeds for reproducibility
- Checkpoints ensure incremental validation at key milestones
