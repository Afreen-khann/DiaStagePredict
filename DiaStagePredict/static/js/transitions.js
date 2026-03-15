/**
 * TransitionManager Component
 * Handles smooth page transitions and scroll animations
 * Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 11.7
 */

class TransitionManager {
    constructor() {
        this.fadeInPage();
        this.attachNavigationListeners();
        this.initScrollAnimations();
        this.addParallaxEffect();
    }
    
    /**
     * Fades in page content on load
     * @param {HTMLElement} element - Element to fade in (defaults to body)
     * @param {number} duration - Duration in ms (defaults to 300)
     * @returns {Promise}
     */
    fadeIn(element = document.body, duration = 300) {
        return new Promise((resolve) => {
            element.style.opacity = '0';
            element.style.transition = `opacity ${duration}ms ease-in-out`;
            
            setTimeout(() => {
                element.style.opacity = '1';
                setTimeout(resolve, duration);
            }, 10);
        });
    }
    
    /**
     * Fades out page content before navigation
     * @param {HTMLElement} element - Element to fade out (defaults to body)
     * @param {number} duration - Duration in ms (defaults to 200)
     * @returns {Promise}
     */
    fadeOut(element = document.body, duration = 200) {
        return new Promise((resolve) => {
            element.style.transition = `opacity ${duration}ms ease-in-out`;
            element.style.opacity = '0';
            setTimeout(resolve, duration);
        });
    }
    
    /**
     * Fades in the page on load
     */
    fadeInPage() {
        const mainContent = document.querySelector('section, main, .page-content') || document.body;
        this.fadeIn(mainContent);
        window.scrollTo(0, 0);
    }
    
    /**
     * Attaches listeners to navigation links
     */
    attachNavigationListeners() {
        const navLinks = document.querySelectorAll('nav a');
        
        navLinks.forEach(link => {
            // Skip external links and anchors
            if (link.hostname === window.location.hostname && !link.hash) {
                link.addEventListener('click', (e) => {
                    const href = link.getAttribute('href');
                    
                    // Only intercept if it's a regular navigation
                    if (href && !href.startsWith('#') && !href.startsWith('javascript:')) {
                        e.preventDefault();
                        
                        const mainContent = document.querySelector('section, main, .page-content') || document.body;
                        this.fadeOut(mainContent).then(() => {
                            window.location.href = href;
                        });
                    }
                });
            }
        });
    }
    
    /**
     * Initialize scroll-triggered animations
     */
    initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        // Observe elements that should animate on scroll
        const animateOnScroll = document.querySelectorAll('.animate-on-scroll');
        animateOnScroll.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
            observer.observe(el);
        });
    }
    
    /**
     * Add subtle parallax effect to header sections
     */
    addParallaxEffect() {
        const headers = document.querySelectorAll('.bg-emerald-900');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            
            headers.forEach(header => {
                const rect = header.getBoundingClientRect();
                if (rect.top < window.innerHeight && rect.bottom > 0) {
                    header.style.transform = `translateY(${scrolled * 0.3}px)`;
                }
            });
        });
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = TransitionManager;
}
