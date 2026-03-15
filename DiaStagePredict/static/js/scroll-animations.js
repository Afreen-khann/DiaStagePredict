/**
 * Scroll-triggered animations - inspired by modern portfolio sites
 * Elements fade + slide in as they enter the viewport
 */

(function () {
    const selectors = [
        '.animate-section',
        '.animate-card',
        '.animate-item'
    ];

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // animate once
            }
        });
    }, {
        threshold: 0.08,
        rootMargin: '0px 0px -30px 0px'
    });

    function init() {
        selectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => observer.observe(el));
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
