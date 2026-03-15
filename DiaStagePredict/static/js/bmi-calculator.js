/**
 * BMICalculator Component
 * Automatically calculates BMI from height and weight inputs
 * Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7
 */

class BMICalculator {
    constructor() {
        this.heightField = document.getElementById('Height');
        this.weightField = document.getElementById('Weight');
        this.bmiField = document.getElementById('BMI');
        this.manualOverride = false;
        
        if (this.heightField && this.weightField && this.bmiField) {
            this.attachListeners();
        }
    }
    
    /**
     * Calculates BMI from height and weight
     * @returns {Object} - {value: number} or {error: string}
     */
    calculate() {
        const height = parseFloat(this.heightField.value);
        const weight = parseFloat(this.weightField.value);
        
        if (!height || !weight || height <= 0 || weight <= 0) {
            return { error: 'Please enter valid height and weight values' };
        }
        
        if (height < 50 || height > 250) {
            return { error: 'Height must be between 50 and 250 cm' };
        }
        
        if (weight < 20 || weight > 300) {
            return { error: 'Weight must be between 20 and 300 kg' };
        }
        
        const heightInMeters = height / 100;
        const bmi = weight / (heightInMeters * heightInMeters);
        
        if (!isFinite(bmi)) {
            return { error: 'Unable to calculate BMI' };
        }
        
        return { value: Math.round(bmi * 10) / 10 };
    }
    
    /**
     * Updates the BMI field with calculated value
     */
    updateBMI() {
        if (this.manualOverride) {
            return;
        }
        
        const result = this.calculate();
        
        if (result.value) {
            this.bmiField.value = result.value;
            // Trigger input event for validation
            this.bmiField.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
    
    /**
     * Attaches event listeners to height and weight fields
     */
    attachListeners() {
        let debounceTimer;
        
        const debouncedUpdate = () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => this.updateBMI(), 300);
        };
        
        this.heightField.addEventListener('input', debouncedUpdate);
        this.weightField.addEventListener('input', debouncedUpdate);
        
        // Track manual BMI edits
        this.bmiField.addEventListener('input', () => {
            this.manualOverride = true;
        });
        
        // Reset manual override when height/weight changes
        this.heightField.addEventListener('input', () => {
            this.manualOverride = false;
        });
        this.weightField.addEventListener('input', () => {
            this.manualOverride = false;
        });
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = BMICalculator;
}
