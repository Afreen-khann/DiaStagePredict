/**
 * Form Enhancements Main Orchestrator
 * Initializes and coordinates all UX enhancement components
 */

// Logger utility for consistent error handling
const logger = {
    error: (component, message, error) => {
        console.error(`[${component}] ${message}`, error);
    },
    warn: (component, message) => {
        console.warn(`[${component}] ${message}`);
    },
    info: (component, message) => {
        console.info(`[${component}] ${message}`);
    }
};

// Main initialization function
function initializeEnhancements() {
    logger.info('FormEnhancements', 'Initializing UX enhancements...');
    
    try {
        // Initialize page transitions
        if (typeof TransitionManager !== 'undefined') {
            const transitionManager = new TransitionManager();
            logger.info('FormEnhancements', 'TransitionManager initialized');
        }
        
        // Initialize form-specific enhancements on predict page
        const form = document.querySelector('form[action="/output"]');
        if (form) {
            initializeFormEnhancements(form);
        }
        
        // Initialize results page enhancements
        const resultsPage = document.querySelector('.risk-score-section');
        if (resultsPage) {
            initializeResultsEnhancements();
        }
        
        logger.info('FormEnhancements', 'All enhancements initialized successfully');
    } catch (error) {
        logger.error('FormEnhancements', 'Failed to initialize enhancements', error);
        // Graceful degradation - form still works without enhancements
    }
}

// Initialize form-specific enhancements
function initializeFormEnhancements(form) {
    try {
        // Initialize FormValidator
        if (typeof FormValidator !== 'undefined') {
            const validator = new FormValidator(form);
            logger.info('FormEnhancements', 'FormValidator initialized');
        }
        
        // Initialize TooltipManager
        if (typeof TooltipManager !== 'undefined') {
            const tooltipManager = new TooltipManager(form);
            logger.info('FormEnhancements', 'TooltipManager initialized');
        }
        
        // Initialize BMICalculator
        if (typeof BMICalculator !== 'undefined') {
            const bmiCalculator = new BMICalculator();
            logger.info('FormEnhancements', 'BMICalculator initialized');
        }
        
        // Initialize ProgressTracker
        if (typeof ProgressTracker !== 'undefined') {
            const progressTracker = new ProgressTracker(form);
            logger.info('FormEnhancements', 'ProgressTracker initialized');
        }
        
        // Initialize LoadingManager
        if (typeof LoadingManager !== 'undefined') {
            const loadingManager = new LoadingManager(form);
            logger.info('FormEnhancements', 'LoadingManager initialized');
        }
    } catch (error) {
        logger.error('FormEnhancements', 'Failed to initialize form enhancements', error);
    }
}

// Initialize results page enhancements
function initializeResultsEnhancements() {
    try {
        // Initialize RecommendationEngine
        if (typeof RecommendationEngine !== 'undefined') {
            const recommendationEngine = new RecommendationEngine();
            logger.info('FormEnhancements', 'RecommendationEngine initialized');
        }
        
        // Initialize ComparisonChart
        if (typeof ComparisonChart !== 'undefined') {
            const comparisonChart = new ComparisonChart();
            logger.info('FormEnhancements', 'ComparisonChart initialized');
        }
    } catch (error) {
        logger.error('FormEnhancements', 'Failed to initialize results enhancements', error);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeEnhancements);
} else {
    initializeEnhancements();
}
