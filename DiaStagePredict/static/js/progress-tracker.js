/**
 * ProgressTracker Component
 * Displays form completion progress
 * Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7
 */

class ProgressTracker {
    constructor(formElement) {
        this.form = formElement;
        this.requiredFields = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                               'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'];
        this.createProgressBar();
        this.attachListeners();
        this.updateDisplay();
    }
    
    /**
     * Creates progress bar HTML element
     */
    createProgressBar() {
        const progressContainer = document.createElement('div');
        progressContainer.className = 'progress-container';
        progressContainer.innerHTML = `
            <div class="progress-bar-wrapper">
                <div class="progress-bar-fill" id="progress-bar-fill">
                    <span class="progress-text" id="progress-text">0%</span>
                </div>
            </div>
            <div class="progress-message" id="progress-message"></div>
        `;
        
        // Insert at the top of the form
        this.form.insertBefore(progressContainer, this.form.firstChild);
        
        this.progressFill = document.getElementById('progress-bar-fill');
        this.progressText = document.getElementById('progress-text');
        this.progressMessage = document.getElementById('progress-message');
    }
    
    /**
     * Calculates progress percentage
     * @returns {number} - Progress percentage (0-100)
     */
    calculateProgress() {
        let filledCount = 0;
        
        this.requiredFields.forEach(fieldName => {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            if (field && field.value && field.value.trim() !== '') {
                filledCount++;
            }
        });
        
        return Math.round((filledCount / this.requiredFields.length) * 100);
    }
    
    /**
     * Updates progress bar display
     */
    updateDisplay() {
        const progress = this.calculateProgress();
        
        this.progressFill.style.width = `${progress}%`;
        this.progressText.textContent = `${progress}%`;
        
        if (progress === 100) {
            this.progressMessage.textContent = 'Ready to Submit ✓';
            this.progressMessage.style.color = '#059669';
        } else {
            this.progressMessage.textContent = `${progress}% Complete`;
            this.progressMessage.style.color = '#6b7280';
        }
    }
    
    /**
     * Attaches event listeners to form fields
     */
    attachListeners() {
        this.requiredFields.forEach(fieldName => {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.addEventListener('input', () => this.updateDisplay());
            }
        });
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProgressTracker;
}
