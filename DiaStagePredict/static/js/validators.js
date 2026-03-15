/**
 * FormValidator Component
 * Provides real-time validation for form inputs with visual feedback
 * 
 * Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 1.6
 */

class FormValidator {
    constructor(formElement) {
        this.form = formElement;
        this.validationRules = {
            Pregnancies: { min: 0, max: 17, required: true, type: 'integer' },
            Glucose: { min: 0, max: 200, required: true, type: 'number' },
            BloodPressure: { min: 0, max: 122, required: true, type: 'number' },
            SkinThickness: { min: 0, max: 99, required: true, type: 'number' },
            Insulin: { min: 0, max: 846, required: true, type: 'number' },
            BMI: { min: 0, max: 67.1, required: true, type: 'decimal' },
            DiabetesPedigreeFunction: { min: 0.078, max: 2.42, required: true, type: 'decimal' },
            Age: { min: 21, max: 81, required: true, type: 'integer' }
        };
        
        this.lastButtonState = null; // Track last button state to prevent unnecessary updates
        this.updateTimeout = null; // Debounce timeout
        
        this.attachValidators();
        // REMOVED: this.updateSubmitButton() - button is always enabled now
    }
    
    /**
     * Validates a single field against its rules
     * @param {string} fieldName - Name of the field to validate
     * @param {string|number} value - Value to validate
     * @returns {Object} - {isValid: boolean, message: string}
     */
    validateField(fieldName, value) {
        const rules = this.validationRules[fieldName];
        
        if (!rules) {
            return { isValid: true, message: '' };
        }
        
        // Check if field is required and empty
        if (rules.required && (value === '' || value === null || value === undefined)) {
            return { 
                isValid: false, 
                message: 'This field is required' 
            };
        }
        
        // If empty and not required, it's valid
        if (value === '' || value === null || value === undefined) {
            return { isValid: true, message: '' };
        }
        
        // Check if value is numeric
        const numValue = parseFloat(value);
        if (isNaN(numValue)) {
            return { 
                isValid: false, 
                message: 'Please enter a numeric value' 
            };
        }
        
        // Check if integer type and value has decimals
        if (rules.type === 'integer' && !Number.isInteger(numValue)) {
            return { 
                isValid: false, 
                message: 'Please enter a whole number (no decimals)' 
            };
        }
        
        // Check range
        if (numValue < rules.min || numValue > rules.max) {
            return { 
                isValid: false, 
                message: `Value must be between ${rules.min} and ${rules.max}` 
            };
        }
        
        return { isValid: true, message: '' };
    }
    
    /**
     * Attaches event listeners (blur, input) to all form fields
     */
    attachValidators() {
        const fields = this.form.querySelectorAll('input[name]');
        
        fields.forEach(field => {
            const fieldName = field.getAttribute('name');
            
            if (this.validationRules[fieldName]) {
                // Validate on blur (when user leaves the field)
                field.addEventListener('blur', () => {
                    this.validateAndShowFeedback(field);
                });
                
                // Clear error on input (when user starts typing)
                field.addEventListener('input', () => {
                    const result = this.validateField(fieldName, field.value);
                    if (result.isValid) {
                        this.clearError(field);
                    }
                    // REMOVED: this.updateSubmitButton() - no more button state changes
                });
            }
        });
    }
    
    /**
     * Validates a field and shows/clears feedback
     * @param {HTMLElement} fieldElement - The field element to validate
     */
    validateAndShowFeedback(fieldElement) {
        const fieldName = fieldElement.getAttribute('name');
        const value = fieldElement.value;
        const result = this.validateField(fieldName, value);
        
        if (!result.isValid) {
            this.showError(fieldElement, result.message);
        } else {
            this.clearError(fieldElement);
        }
        
        // REMOVED: this.updateSubmitButton() - no more button state changes
    }
    
    /**
     * Displays validation message and error styling
     * @param {HTMLElement} fieldElement - The field element
     * @param {string} message - The error message to display
     */
    showError(fieldElement, message) {
        // Add error class to field
        fieldElement.classList.add('validation-error');
        fieldElement.setAttribute('aria-invalid', 'true');
        
        // Find or create error message container
        let errorContainer = fieldElement.parentElement.querySelector('.validation-message');
        
        if (!errorContainer) {
            errorContainer = document.createElement('div');
            errorContainer.className = 'validation-message';
            errorContainer.setAttribute('role', 'alert');
            errorContainer.setAttribute('aria-live', 'polite');
            
            // Insert after the field
            fieldElement.parentElement.appendChild(errorContainer);
            
            // Link error message to field for screen readers
            const errorId = `${fieldElement.id || fieldElement.name}-error`;
            errorContainer.id = errorId;
            fieldElement.setAttribute('aria-describedby', errorId);
        }
        
        errorContainer.textContent = message;
    }
    
    /**
     * Removes validation message and error styling
     * @param {HTMLElement} fieldElement - The field element
     */
    clearError(fieldElement) {
        // Remove error class from field
        fieldElement.classList.remove('validation-error');
        fieldElement.setAttribute('aria-invalid', 'false');
        
        // Remove error message
        const errorContainer = fieldElement.parentElement.querySelector('.validation-message');
        if (errorContainer) {
            errorContainer.remove();
            fieldElement.removeAttribute('aria-describedby');
        }
    }
    
    /**
     * Checks if all fields pass validation
     * @returns {boolean} - True if form is valid
     */
    isFormValid() {
        const fields = this.form.querySelectorAll('input[name]');
        let allValid = true;
        
        fields.forEach(field => {
            const fieldName = field.getAttribute('name');
            
            if (this.validationRules[fieldName]) {
                const result = this.validateField(fieldName, field.value);
                if (!result.isValid) {
                    allValid = false;
                }
            }
        });
        
        return allValid;
    }
    
    /**
     * Updates submit button state based on form validity
     */
    updateSubmitButton() {
        // Debounce to prevent rapid updates
        if (this.updateTimeout) {
            clearTimeout(this.updateTimeout);
        }
        
        this.updateTimeout = setTimeout(() => {
            const submitButton = this.form.querySelector('button[type="submit"], input[type="submit"]');
            
            if (submitButton) {
                const isValid = this.isFormValid();
                
                // Only update if state actually changed
                if (this.lastButtonState !== isValid) {
                    this.lastButtonState = isValid;
                    
                    if (isValid) {
                        submitButton.removeAttribute('disabled');
                        submitButton.setAttribute('aria-disabled', 'false');
                        submitButton.style.opacity = '1';
                        submitButton.style.cursor = 'pointer';
                    } else {
                        submitButton.setAttribute('disabled', 'disabled');
                        submitButton.setAttribute('aria-disabled', 'true');
                        submitButton.style.opacity = '0.6';
                        submitButton.style.cursor = 'not-allowed';
                    }
                }
            }
        }, 100); // 100ms debounce
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FormValidator;
}
