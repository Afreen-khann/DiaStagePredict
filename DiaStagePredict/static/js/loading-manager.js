/**
 * LoadingManager Component
 * Displays loading animation during form submission
 * Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 10.8
 */

class LoadingManager {
    constructor(formElement) {
        this.form = formElement;
        this.overlay = null;
        this.attachSubmitListener();
    }
    
    /**
     * Creates loading overlay element
     * @returns {HTMLElement} - The overlay element
     */
    createOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.setAttribute('aria-live', 'polite');
        overlay.setAttribute('aria-busy', 'true');
        
        overlay.innerHTML = `
            <div class="loading-spinner" role="status"></div>
            <p class="loading-message">Analyzing your health data...</p>
        `;
        
        return overlay;
    }
    
    /**
     * Shows the loading overlay
     * @param {string} message - Optional custom message
     */
    show(message = 'Analyzing your health data...') {
        if (!this.overlay) {
            this.overlay = this.createOverlay();
            document.body.appendChild(this.overlay);
        }
        
        const messageElement = this.overlay.querySelector('.loading-message');
        if (messageElement) {
            messageElement.textContent = message;
        }
        
        // Only disable buttons to prevent double submission
        // DO NOT disable input fields - disabled inputs don't submit their values!
        const buttons = this.form.querySelectorAll('button, input[type="submit"]');
        buttons.forEach(button => {
            button.setAttribute('disabled', 'disabled');
        });
    }
    
    /**
     * Hides the loading overlay
     */
    hide() {
        if (this.overlay && this.overlay.parentNode) {
            this.overlay.parentNode.removeChild(this.overlay);
            this.overlay = null;
        }
        
        // Re-enable buttons
        const buttons = this.form.querySelectorAll('button, input[type="submit"]');
        buttons.forEach(button => {
            button.removeAttribute('disabled');
        });
    }
    
    /**
     * Attaches submit event listener to form
     */
    attachSubmitListener() {
        this.form.addEventListener('submit', (e) => {
            this.show();
        });
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = LoadingManager;
}
