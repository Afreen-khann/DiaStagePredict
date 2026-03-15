/**
 * DiaStagePredict - Pro Portfolio Animations
 * Glassmorphism · Typing · Particles · 3D Tilt · Liquid · Accuracy Bars
 * ZERO content hiding - all above-fold content always visible
 */

(function () {

    /* ── Cursor glow ring ── */
    const glow = document.createElement('div');
    glow.id = 'cursor-glow';
    document.body.appendChild(glow);
    document.addEventListener('mousemove', (e) => {
        glow.style.left = e.clientX + 'px';
        glow.style.top  = e.clientY + 'px';
    });

    /* ── Mouse parallax on hero image ── */
    const heroImg = document.querySelector('.hero-parallax');
    if (heroImg) {
        document.addEventListener('mousemove', (e) => {
            const cx = window.innerWidth  / 2;
            const cy = window.innerHeight / 2;
            const dx = (e.clientX - cx) / cx;
            const dy = (e.clientY - cy) / cy;
            heroImg.style.transform = `translate(${dx * 12}px, ${dy * 8}px) scale(1.02)`;
        });
    }

    /* ── Typing effect for hero h1 ── */
    const typingEl = document.getElementById('typing-text');
    if (typingEl) {
        const fullText = typingEl.getAttribute('data-text') || typingEl.textContent.trim();
        typingEl.textContent = '';

        // Add cursor
        const cursor = document.createElement('span');
        cursor.className = 'typing-cursor';
        typingEl.parentNode.insertBefore(cursor, typingEl.nextSibling);

        let i = 0;
        const speed = 38;
        function type() {
            if (i < fullText.length) {
                typingEl.textContent += fullText.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        // Small delay so page is rendered first
        setTimeout(type, 400);
    }

    /* ── Particle orbit system around hero image ── */
    const orbitContainer = document.querySelector('.orbit-container');
    if (orbitContainer) {
        const COUNT = 18;
        const particles = [];

        for (let i = 0; i < COUNT; i++) {
            const p = document.createElement('div');
            p.className = 'orbit-particle';

            // Vary size and opacity
            const size = 4 + Math.random() * 5;
            p.style.width  = size + 'px';
            p.style.height = size + 'px';
            p.style.opacity = (0.4 + Math.random() * 0.6).toFixed(2);

            orbitContainer.appendChild(p);

            particles.push({
                el: p,
                angle: (i / COUNT) * Math.PI * 2,
                speed: 0.004 + Math.random() * 0.006,
                rx: 0,   // set after layout
                ry: 0,
                size: size
            });
        }

        function animateParticles() {
            const rect = orbitContainer.getBoundingClientRect();
            const cx = orbitContainer.offsetWidth  / 2;
            const cy = orbitContainer.offsetHeight / 2;
            const rx = cx * 0.88;
            const ry = cy * 0.88;

            particles.forEach(p => {
                p.angle += p.speed;
                const x = cx + rx * Math.cos(p.angle) - p.size / 2;
                const y = cy + ry * Math.sin(p.angle) - p.size / 2;
                p.el.style.left = x + 'px';
                p.el.style.top  = y + 'px';
            });

            requestAnimationFrame(animateParticles);
        }
        animateParticles();
    }

    /* ── 3D Tilt on cards ── */
    document.querySelectorAll('.card-hover').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const cx = rect.width  / 2;
            const cy = rect.height / 2;
            const rotX = ((y - cy) / cy) * -8;
            const rotY = ((x - cx) / cx) *  8;
            card.style.transform = `perspective(600px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-6px)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });

    /* ── Scroll reveal (IntersectionObserver) ── */
    const srObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('sr-visible');
                srObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.sr').forEach(el => srObserver.observe(el));

    /* ── Accuracy bars (model.html) ── */
    const accObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const fill  = entry.target.querySelector('.acc-bar-fill');
                const label = entry.target.querySelector('.acc-label');
                if (fill) {
                    const target = fill.getAttribute('data-acc');
                    setTimeout(() => {
                        fill.style.width = target + '%';
                        fill.classList.add('animated');
                        if (label) label.classList.add('visible');
                    }, 150);
                }
                accObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    document.querySelectorAll('.acc-card').forEach(el => accObserver.observe(el));

    /* ── Navbar shadow on scroll ── */
    const navbar = document.querySelector('nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.style.boxShadow = window.scrollY > 20
                ? '0 8px 32px rgba(0,0,0,0.3)'
                : '';
        }, { passive: true });
    }

    /* ── Smooth scroll for anchor links ── */
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const target = document.querySelector(a.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

})();
