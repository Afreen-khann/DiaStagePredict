/**
 * ComparisonChart Component
 * Visualizes user metrics against healthy ranges
 * Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7
 */

class ComparisonChart {
    constructor() {
        this.healthData = this.extractHealthData();
        this.healthRanges = {
            Glucose: { min: 70, max: 125, unit: 'mg/dL', label: 'Glucose' },
            BloodPressure: { min: 60, max: 80, unit: 'mm Hg', label: 'Blood Pressure' },
            BMI: { min: 18.5, max: 24.9, unit: '', label: 'BMI' },
            Insulin: { min: 15, max: 276, unit: 'IU/mL', label: 'Insulin' },
            Age: { min: 21, max: 45, unit: 'years', label: 'Age' }
        };
        
        if (Object.keys(this.healthData).length > 0) {
            this.render();
        }
    }
    
    /**
     * Extracts health data from the page
     * @returns {Object} - Health metrics
     */
    extractHealthData() {
        const data = {};
        const profileItems = document.querySelectorAll('.bg-emerald-50');
        
        profileItems.forEach(item => {
            const text = item.textContent.trim();
            const match = text.match(/([A-Za-z\s]+):\s*([0-9.]+)/);
            if (match) {
                const key = match[1].trim().replace(/\s+/g, '');
                data[key] = parseFloat(match[2]);
            }
        });
        
        return data;
    }
    
    /**
     * Checks if value is within healthy range
     * @param {number} value - The value to check
     * @param {Object} range - The range object with min and max
     * @returns {boolean}
     */
    isInRange(value, range) {
        return value >= range.min && value <= range.max;
    }
    
    /**
     * Creates a bar for a single metric
     * @param {string} metricName - Name of the metric
     * @param {number} value - User's value
     * @param {Object} range - Healthy range
     * @returns {string} - HTML string
     */
    createBar(metricName, value, range) {
        const inRange = this.isInRange(value, range);
        const colorClass = inRange ? 'in-range' : 'out-of-range';
        
        // Calculate percentage for bar width (capped at 100%)
        const maxValue = range.max * 1.5; // Show up to 150% of max
        const percentage = Math.min((value / maxValue) * 100, 100);
        
        return `
            <div class="chart-bar">
                <div class="chart-label">
                    <span>${range.label}</span>
                    <span>${value} ${range.unit}</span>
                </div>
                <div class="chart-bar-container">
                    <div class="chart-bar-fill ${colorClass}" style="width: ${percentage}%">
                        ${value}
                    </div>
                </div>
                <div class="chart-range-text">
                    Healthy range: ${range.min}-${range.max} ${range.unit}
                </div>
            </div>
        `;
    }
    
    /**
     * Renders the comparison chart
     */
    render() {
        const riskScoreSection = document.querySelector('.risk-score-section, .bg-white.text-gray-900');
        if (!riskScoreSection) return;
        
        const chartSection = document.createElement('div');
        chartSection.className = 'mt-6 bg-white text-gray-900 rounded-xl p-6';
        
        let chartHTML = `
            <h3 class="text-xl font-semibold text-center mb-4 text-emerald-900">Your Metrics vs Healthy Ranges</h3>
            <div class="comparison-chart">
        `;
        
        // Add bars for each metric that exists in both data and ranges
        Object.keys(this.healthRanges).forEach(metricName => {
            if (this.healthData[metricName] !== undefined) {
                chartHTML += this.createBar(
                    metricName,
                    this.healthData[metricName],
                    this.healthRanges[metricName]
                );
            }
        });
        
        chartHTML += '</div>';
        chartSection.innerHTML = chartHTML;
        
        // Insert after risk score section
        riskScoreSection.parentElement.insertBefore(chartSection, riskScoreSection.nextSibling);
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ComparisonChart;
}
