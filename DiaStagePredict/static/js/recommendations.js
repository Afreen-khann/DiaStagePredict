/**
 * RecommendationEngine Component
 * Generates personalized health recommendations based on risk score and metrics
 * Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8
 */

class RecommendationEngine {
    constructor() {
        this.riskScore = this.extractRiskScore();
        this.healthData = this.extractHealthData();
        this.recommendations = [];
        
        if (this.riskScore !== null) {
            this.generateRecommendations();
            this.renderRecommendations();
        }
    }
    
    /**
     * Extracts risk score from the page
     * @returns {number|null} - Risk score percentage
     */
    extractRiskScore() {
        const riskScoreElement = document.querySelector('[data-risk-score]');
        if (riskScoreElement) {
            return parseFloat(riskScoreElement.getAttribute('data-risk-score'));
        }
        
        // Fallback: try to extract from text
        const riskText = document.body.textContent;
        const match = riskText.match(/(\d+(?:\.\d+)?)\s*%/);
        if (match) {
            return parseFloat(match[1]);
        }
        
        return null;
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
     * Generates recommendations based on risk level and metrics
     */
    generateRecommendations() {
        // Get risk-level specific recommendations
        this.recommendations = this.getRiskLevelRecommendations();
        
        // Add metric-specific recommendations
        const metricRecs = this.getMetricBasedRecommendations();
        this.recommendations.push(...metricRecs);
        
        // Limit to appropriate count
        const targetCount = this.riskScore < 30 ? 4 : (this.riskScore < 60 ? 5 : 6);
        this.recommendations = this.recommendations.slice(0, targetCount);
    }
    
    /**
     * Gets recommendations based on risk level
     * @returns {Array} - Array of recommendation objects
     */
    getRiskLevelRecommendations() {
        if (this.riskScore < 30) {
            return [
                { icon: '🥗', category: 'Diet', text: 'Continue eating a balanced diet rich in vegetables, whole grains, and lean proteins' },
                { icon: '🏃', category: 'Exercise', text: 'Maintain at least 150 minutes of moderate aerobic activity per week' },
                { icon: '⚖️', category: 'Weight', text: 'Keep your weight within a healthy BMI range (18.5-24.9)' },
                { icon: '🩺', category: 'Screening', text: 'Continue regular health checkups and diabetes screening every 3 years' }
            ];
        } else if (this.riskScore < 60) {
            return [
                { icon: '🥗', category: 'Diet', text: 'Reduce sugar and refined carbohydrate intake; focus on low glycemic index foods' },
                { icon: '🏃', category: 'Exercise', text: 'Increase physical activity to 200+ minutes per week with both cardio and strength training' },
                { icon: '⚖️', category: 'Weight', text: 'Work towards losing 5-10% of body weight if overweight' },
                { icon: '🩺', category: 'Screening', text: 'Schedule diabetes screening annually and monitor blood glucose levels' },
                { icon: '😴', category: 'Lifestyle', text: 'Ensure 7-9 hours of quality sleep per night and manage stress levels' }
            ];
        } else {
            return [
                { icon: '👨‍⚕️', category: 'Medical', text: 'Consult a healthcare professional immediately for comprehensive diabetes evaluation', priority: 'high' },
                { icon: '🩸', category: 'Monitoring', text: 'Begin regular blood glucose monitoring as recommended by your doctor', priority: 'high' },
                { icon: '🥗', category: 'Diet', text: 'Work with a registered dietitian to create a diabetes prevention meal plan', priority: 'high' },
                { icon: '🏃', category: 'Exercise', text: 'Start a supervised exercise program with medical clearance' },
                { icon: '💊', category: 'Medication', text: 'Discuss preventive medication options (like metformin) with your doctor' },
                { icon: '📊', category: 'Tracking', text: 'Keep a daily log of diet, exercise, and blood sugar readings' }
            ];
        }
    }
    
    /**
     * Gets metric-specific recommendations
     * @returns {Array} - Array of recommendation objects
     */
    getMetricBasedRecommendations() {
        const recs = [];
        
        // BMI recommendations
        if (this.healthData.BMI && (this.healthData.BMI < 18.5 || this.healthData.BMI > 24.9)) {
            if (this.healthData.BMI > 24.9) {
                recs.push({ 
                    icon: '⚖️', 
                    category: 'Weight', 
                    text: 'Your BMI is above the healthy range. Consider a weight management program with professional guidance' 
                });
            }
        }
        
        // Glucose recommendations
        if (this.healthData.Glucose && this.healthData.Glucose > 125) {
            recs.push({ 
                icon: '🍬', 
                category: 'Blood Sugar', 
                text: 'Your glucose level is elevated. Reduce sugar intake and increase fiber consumption' 
            });
        }
        
        // Age recommendations
        if (this.healthData.Age && this.healthData.Age > 45) {
            recs.push({ 
                icon: '🩺', 
                category: 'Screening', 
                text: 'At your age, annual diabetes screening is recommended even with low risk' 
            });
        }
        
        return recs;
    }
    
    /**
     * Renders recommendations to the page
     */
    renderRecommendations() {
        const riskScoreSection = document.querySelector('.risk-score-section, .bg-white.text-gray-900');
        if (!riskScoreSection) return;
        
        const recommendationsSection = document.createElement('div');
        recommendationsSection.className = 'mt-6 bg-white text-gray-900 rounded-xl p-6';
        recommendationsSection.innerHTML = `
            <h3 class="text-xl font-semibold text-center mb-4 text-emerald-900">Personalized Health Recommendations</h3>
            <ul class="recommendations-list">
                ${this.recommendations.map(rec => `
                    <li class="recommendation-item ${rec.priority === 'high' ? 'border-red-500' : ''}">
                        <span class="recommendation-icon">${rec.icon}</span>
                        <div class="recommendation-text">
                            <div class="recommendation-category">${rec.category}</div>
                            <div>${rec.text}</div>
                        </div>
                    </li>
                `).join('')}
            </ul>
        `;
        
        riskScoreSection.parentElement.insertBefore(recommendationsSection, riskScoreSection.nextSibling);
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = RecommendationEngine;
}
