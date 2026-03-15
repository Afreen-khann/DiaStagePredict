/**
 * TooltipManager Component
 * Manages informational tooltips for form fields
 * 
 * Validates: Requirements 2.1, 2.2, 2.3, 2.6, 2.7, 10.7
 */

class TooltipManager {
    constructor(containerElement) {
        this.container = containerElement;
        this.tooltipContent = {
            Pregnancies: {
                title: "Number of Pregnancies",
                description: "Total number of times pregnant. Gestational diabetes during pregnancy increases future diabetes risk.",
                range: "Typical: 0-17"
            },
            Glucose: {
                title: "Plasma Glucose Concentration",
                description: "Blood sugar level measured 2 hours after oral glucose tolerance test. Higher levels indicate impaired glucose metabolism.",
                range: "Normal: 70-125 mg/dL"
            },
            BloodPressure: {
                title: "Diastolic Blood Pressure",
                description: "The pressure in arteries when the heart rests between beats. High blood pressure is associated with increased diabetes risk.",
                range: "Normal: 60-80 mm Hg"
            },
            SkinThickness: {
                title: "Triceps Skin Fold Thickness",
                description: "Measurement of subcutaneous fat at the back of the upper arm. Used as an indicator of body fat percentage.",
                range: "Typical: 7-99 mm"
            },
            Insulin: {
                title: "2-Hour Serum Insulin",
                description: "Insulin level measured 2 hours after glucose tolerance test. Indicates how well your body produces insulin.",
                range: "Typical: 15-276 IU/mL"
            },
            BMI: {
                title: "Body Mass Index",
                description: "A measure of body fat based on height and weight. Higher BMI is associated with increased diabetes risk.",
                range: "Healthy: 18.5-24.9"
            },
            DiabetesPedigreeFunction: {
                title: "Diabetes Pedigree Function",
                description: "A function that scores likelihood of diabetes based on family history. Higher values indicate stronger genetic predisposition.",
                range: "Typical: 0.078-2.42"
            },
            Age: {
                title: "Age",
                description: "Age in years. Diabetes risk increases with age, particularly after 45.",
                range: "Typical: 21-81 years"
            },
            Height: {
                title: "Height",
                description: "Your height in centimeters. Used to calculate Body Mass Index (BMI).",
                range: "Typical: 50-250 cm"
            },
            Weight: {
                title: "Weight",
                description: "Your weight in kilograms. Used to calculate Body Mass Index (BMI).",
                range: "Typical: 20-300 kg"
            }
        };
        
        this.addTooltips();
    }
    
    /**
     * Adds tooltips to all form fields
     */
    addTooltips() {
        const labels = this.container.querySelectorAll('label');
        
        labels.forEach(label => {
            const forAttr = label.getAttribute('for');
            const field = this.container.querySelector(`#${forAttr}, [name="${forAttr}"]`);
            
            if (field && this.tooltipContent[forAttr]) {
                this.createTooltipElement(label, forAttr, this.tooltipContent[forAttr]);
            }
        });
    }
    
    /**
     * Creates tooltip element with info icon
     * @param {HTMLElement} label - The label element
     * @param {string} fieldName - Name of the field
     * @param {Object} content - Tooltip content
     */
    createTooltipElement(label, fieldName, content) {
        // Create tooltip container
        const tooltipContainer = document.createElement('span');
        tooltipContainer.className = 'tooltip-container';
        
        // Create info icon
        const infoIcon = document.createElement('span');
        infoIcon.className = 'info-icon';
        infoIcon.textContent = 'i';
        infoIcon.setAttribute('tabindex', '0');
        infoIcon.setAttribute('role', 'button');
        infoIcon.setAttribute('aria-label', `Information about ${content.title}`);
        
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.id = `tooltip-${fieldName}`;
        tooltip.setAttribute('role', 'tooltip');
        
        tooltip.innerHTML = `
            <div class="tooltip-title">${content.title}</div>
            <div class="tooltip-description">${content.description}</div>
            <div class="tooltip-range">${content.range}</div>
        `;
        
        // Add event listeners
        infoIcon.addEventListener('mouseenter', () => this.show(tooltip.id));
        infoIcon.addEventListener('mouseleave', () => this.hide(tooltip.id));
        infoIcon.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggle(tooltip.id);
        });
        
        // Keyboard accessibility
        infoIcon.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.toggle(tooltip.id);
            }
        });
        
        // Assemble tooltip
        tooltipContainer.appendChild(infoIcon);
        tooltipContainer.appendChild(tooltip);
        label.appendChild(tooltipContainer);
    }
    
    /**
     * Shows a tooltip
     * @param {string} tooltipId - ID of the tooltip to show
     */
    show(tooltipId) {
        const tooltip = document.getElementById(tooltipId);
        if (tooltip) {
            tooltip.classList.add('show');
        }
    }
    
    /**
     * Hides a tooltip
     * @param {string} tooltipId - ID of the tooltip to hide
     */
    hide(tooltipId) {
        const tooltip = document.getElementById(tooltipId);
        if (tooltip) {
            tooltip.classList.remove('show');
        }
    }
    
    /**
     * Toggles a tooltip
     * @param {string} tooltipId - ID of the tooltip to toggle
     */
    toggle(tooltipId) {
        const tooltip = document.getElementById(tooltipId);
        if (tooltip) {
            tooltip.classList.toggle('show');
        }
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = TooltipManager;
}
