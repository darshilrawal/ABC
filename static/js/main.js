/**
 * ABC - Atal Bharat Creation
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all features
    initThemeToggle();
    initMobileNav();
    initScrollAnimations();
    initSmoothScroll();
    initFormValidation();
    initNavbarScroll();
    initProfileDropdown();
    initToastNotifications();
    initPasswordToggle();
});

/**
 * Theme Toggle - Dark/Light Mode
 */
function initThemeToggle() {
    const themeToggle = document.querySelector('.theme-toggle');
    const html = document.documentElement;

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);

            // Add animation effect
            this.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.style.transform = '';
            }, 300);
        });
    }
}

/**
 * Mobile Navigation Toggle
 */
function initMobileNav() {
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navbarNav = document.querySelector('.navbar-nav');

    if (!mobileToggle || !navbarNav) return;

    // ── Create backdrop overlay ──────────────────────────────────────────
    // This div blocks ALL underlying page content from receiving taps
    // when the mobile menu is open. Without it, hero buttons / absolutely
    // positioned elements intercept touches meant for the nav buttons.
    const backdrop = document.createElement('div');
    backdrop.id = 'mobile-nav-backdrop';
    backdrop.style.cssText = [
        'display:none',
        'position:fixed',
        'inset:0',
        'z-index:999',       // BELOW navbar (10002) so nav links are never blocked
        'background:rgba(0,0,0,0.55)',
        'touch-action:none',  // prevents scroll-through on iOS
        '-webkit-tap-highlight-color:transparent',
    ].join(';');
    document.body.appendChild(backdrop);

    // ── Hamburger icon animation helper ─────────────────────────────────
    function setHamburger(open) {
        const spans = mobileToggle.querySelectorAll('span');
        if (open) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
        } else {
            spans[0].style.transform = '';
            spans[1].style.opacity = '';
            spans[2].style.transform = '';
        }
    }

    // ── Open / close helpers ─────────────────────────────────────────────
    function openMobileMenu() {
        navbarNav.classList.add('active');
        mobileToggle.classList.add('active');
        backdrop.style.display = 'block';
        setHamburger(true);
        // Visually hide WhatsApp widget while mobile menu is open
        document.body.classList.add('mobile-nav-open');
    }

    function closeMobileMenu() {
        navbarNav.classList.remove('active');
        mobileToggle.classList.remove('active');
        backdrop.style.display = 'none';
        setHamburger(false);
        document.body.classList.remove('mobile-nav-open');
    }

    // ── Toggle on hamburger click ────────────────────────────────────────
    mobileToggle.addEventListener('click', function (e) {
        e.stopPropagation();
        if (navbarNav.classList.contains('active')) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    });

    // ── Tap backdrop → close menu ────────────────────────────────────────
    backdrop.addEventListener('click', closeMobileMenu);

    // ── Nav-links (Home, Products, About, Contact) ───────────────────────
    const navLinks = navbarNav.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // ── Action buttons (Login, Register, Logout, Bulk Inquiry, etc.) ─────
    // Use explicit window.location so tap always navigates on all mobile
    // browsers regardless of stacking context or compositing layer quirks.
    const mobileActionBtns = navbarNav.querySelectorAll('.mobile-menu-actions a');
    mobileActionBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            const href = this.getAttribute('href');
            const target = this.getAttribute('target');
            closeMobileMenu();
            if (!href || href === '#') return;
            if (target === '_blank') {
                window.open(href, '_blank', 'noopener,noreferrer');
            } else {
                // Small tick so closeMobileMenu DOM changes paint before navigation
                requestAnimationFrame(function () {
                    window.location.href = href;
                });
            }
        });
    });
}

/**
 * Scroll Animations
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animatedElements.forEach(el => observer.observe(el));

    // Add stagger effect to grid items
    const gridContainers = document.querySelectorAll('.categories-grid, .products-grid, .highlights-grid, .values-grid');
    gridContainers.forEach(container => {
        const items = container.children;
        Array.from(items).forEach((item, index) => {
            item.style.transitionDelay = `${index * 0.1}s`;
            item.classList.add('animate-on-scroll');
            observer.observe(item);
        });
    });
}

/**
 * Smooth Scroll for Anchor Links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const headerOffset = 80;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}

/**
 * Form Validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            let isValid = true;
            const requiredFields = this.querySelectorAll('[required]');

            requiredFields.forEach(field => {
                removeError(field);

                if (!field.value.trim()) {
                    showError(field, 'This field is required');
                    isValid = false;
                } else if (field.type === 'email' && !isValidEmail(field.value)) {
                    showError(field, 'Please enter a valid email address');
                    isValid = false;
                } else if (field.name === 'phone' && !isValidPhone(field.value)) {
                    showError(field, 'Please enter a valid phone number');
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const firstError = this.querySelector('.form-error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
}

function showError(field, message) {
    field.classList.add('form-error');
    field.style.borderColor = '#ef4444';

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = 'color: #ef4444; font-size: 0.85rem; margin-top: 5px;';
    errorDiv.textContent = message;

    field.parentNode.appendChild(errorDiv);
}

function removeError(field) {
    field.classList.remove('form-error');
    field.style.borderColor = '';

    const errorMessage = field.parentNode.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function isValidPhone(phone) {
    const regex = /^[\d\s+\-()]{10,}$/;
    return regex.test(phone);
}

/**
 * Navbar Scroll Effect
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');

    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.2)';
            } else {
                navbar.style.boxShadow = 'none';
            }
        });
    }
}

/**
 * Profile Dropdown Toggle
 */
function initProfileDropdown() {
    const profileDropdown = document.querySelector('.profile-dropdown');

    if (profileDropdown) {
        const profileToggle = profileDropdown.querySelector('.profile-toggle');

        // Toggle dropdown on button click
        profileToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            profileDropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function (e) {
            if (!profileDropdown.contains(e.target)) {
                profileDropdown.classList.remove('active');
            }
        });

        // Close dropdown when clicking on a dropdown item
        const dropdownItems = profileDropdown.querySelectorAll('.dropdown-item');
        dropdownItems.forEach(item => {
            item.addEventListener('click', function () {
                profileDropdown.classList.remove('active');
            });
        });
    }
}

/**
 * Toast Notifications - Auto dismiss and manual close
 */
function initToastNotifications() {
    const toasts = document.querySelectorAll('.toast');

    toasts.forEach(toast => {
        // Auto dismiss after 3 seconds
        if (toast.getAttribute('data-auto-dismiss') === 'true') {
            setTimeout(() => {
                dismissToast(toast);
            }, 3000);
        }

        // Manual close button
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissToast(toast);
            });
        }
    });
}

function dismissToast(toast) {
    toast.classList.add('toast-exit');
    setTimeout(() => {
        toast.remove();

        // Remove container if no toasts left
        const container = document.querySelector('.toast-container');
        if (container && container.children.length === 0) {
            container.remove();
        }
    }, 300);
}

/**
 * Password Visibility Toggle
 */
function initPasswordToggle() {
    const passwordToggles = document.querySelectorAll('.password-toggle');

    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function () {
            const wrapper = this.closest('.password-input-wrapper');
            const input = wrapper.querySelector('input');

            // Toggle password visibility
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.add('active');
            } else {
                input.type = 'password';
                this.classList.remove('active');
            }
        });
    });
}

/**
 * Category Filter (for Products Page)
 */
function filterProducts(category) {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('category', category);
    window.location.href = currentUrl.toString();
}

/**
 * Utility Functions
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Counter animation for stats
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);

    const updateCounter = () => {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start).toLocaleString();
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target.toLocaleString();
        }
    };

    updateCounter();
}

// Initialize counters when they come into view
function initCounters() {
    const counters = document.querySelectorAll('[data-counter]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-counter'));
                animateCounter(entry.target, target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

// Call initCounters if you have counter elements
if (document.querySelectorAll('[data-counter]').length > 0) {
    initCounters();
}
