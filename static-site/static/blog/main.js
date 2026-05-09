/* ─────────────────────────────────────────
   main.js — shared scripts for all pages
   ───────────────────────────────────────── */

/* 1. Theme toggle button */
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("theme-toggle");
    if (!btn) return;
    btn.addEventListener("click", () => {
        const root = document.documentElement;
        const nowDark = root.classList.toggle("dark");
        root.classList.toggle("light", !nowDark);
        localStorage.setItem("theme", nowDark ? "dark" : "light");
    });
});

/* 3. Navbar hide-on-scroll */
(function () {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    let lastY = window.scrollY;
    let ticking = false;
    const threshold = 20;
    function isMenuOpen() {
        const menuToggle = document.getElementById('menu-toggle');
        return menuToggle ? menuToggle.checked : false;
    }
    function update() {
        const y = window.scrollY;
        const delta = y - lastY;
        if (Math.abs(delta) > threshold) {
            if (delta > 0 && y > threshold && !isMenuOpen()) {
                navbar.classList.add('hide');
            } else if (delta < 0) {
                navbar.classList.remove('hide');
            }
            lastY = y;
        } else {
            lastY = y;
        }
        ticking = false;
    }
    window.addEventListener('scroll', function () {
        if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
})();

/* 4. Scroll-triggered fade-ins */
(function () {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // fire once
            }
        });
    }, { threshold: 0.12 });

    document.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
    });
})();

/* 5. Page transitions (View Transitions API) */
(function () {
    if (!document.startViewTransition) return; // unsupported browsers fall back gracefully

    document.addEventListener('click', (e) => {
        const anchor = e.target.closest('a');
        if (!anchor) return;
        const href = anchor.getAttribute('href');
        if (!href) return;
        // Only transition internal, same-origin, non-hash page links
        if (href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('http')) return;
        e.preventDefault();
        document.startViewTransition(() => {
            window.location.href = anchor.href;
        });
    });
})();

/* 6. Image lightbox */
(function () {
    document.addEventListener("DOMContentLoaded", () => {
        // Build overlay once
        const overlay = document.createElement('div');
        overlay.className = 'lightbox-overlay';
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('role', 'dialog');

        const img = document.createElement('img');
        const closeBtn = document.createElement('button');
        closeBtn.className = 'lightbox-close';
        closeBtn.setAttribute('aria-label', 'Close image');
        closeBtn.textContent = '×';

        overlay.appendChild(closeBtn);
        overlay.appendChild(img);
        document.body.appendChild(overlay);

        function open(src, alt) {
            img.src = src;
            img.alt = alt || '';
            overlay.classList.add('open');
            document.body.style.overflow = 'hidden';
        }
        function close() {
            overlay.classList.remove('open');
            document.body.style.overflow = '';
            // Clear src after transition
            setTimeout(() => { img.src = ''; }, 260);
        }

        // Attach to eligible images, skipping any already inside a page-specific
        // lightbox grid (e.g. .photo-item on the Italy post)
        document.querySelectorAll('.content-block img, .progress-entry img').forEach(el => {
            if (el.closest('.photo-item')) return;
            el.addEventListener('click', () => open(el.src, el.alt));
        });

        // Close handlers
        closeBtn.addEventListener('click', (e) => { e.stopPropagation(); close(); });
        overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && overlay.classList.contains('open')) close();
        });
    });
})();

/* 7. Typewriter effect on hero subtitle */
(function () {
    document.addEventListener("DOMContentLoaded", () => {
        const heroP = document.querySelector('.hero header p');
        if (!heroP) return;

        // Build: "Right now I'm " + animated link "here"
        const prefix = "Right now I'm ";
        const linkHref = "now.html";
        const linkText = "here";

        heroP.innerHTML = ''; // clear existing content

        // Cursor element
        const cursor = document.createElement('span');
        cursor.className = 'typewriter-cursor';

        // Type the prefix first, then reveal the link
        let i = 0;
        const fullText = prefix + linkText;

        function type() {
            if (i < prefix.length) {
                heroP.appendChild(document.createTextNode(fullText[i]));
                heroP.appendChild(cursor);
                i++;
                setTimeout(type, 55);
            } else if (i < fullText.length) {
                // Build the link character by character
                let link = heroP.querySelector('a.hero-link');
                if (!link) {
                    link = document.createElement('a');
                    link.className = 'hero-link';
                    link.href = linkHref;
                    link.style.cssText = 'color: var(--bg); font-style: italic;';
                    cursor.remove();
                    heroP.appendChild(link);
                    heroP.appendChild(cursor);
                }
                link.textContent += fullText[i];
                i++;
                setTimeout(type, 65);
            } else {
                // Done — remove cursor after a brief pause
                setTimeout(() => cursor.remove(), 900);
            }
        }

        // Short delay before starting so the page feels settled
        setTimeout(type, 480);
    });
})();

/* 8. Navbar logo scramble */
(function () {
    const original = "Eric's Blog";
    const alternate = "思烨的博客";
    let showingOriginal = true;
    let interval;

    function scrambleText(element, text) {
        const chars = "!@#$%^&*()_+=-{}[];:<>?,.";
        let iterations = 0;
        clearInterval(interval);
        interval = setInterval(() => {
            const scrambled = text.split("").map((char, i) => {
                if (i < iterations) return char;
                return chars[Math.floor(Math.random() * chars.length)];
            }).join("");
            element.textContent = scrambled;
            if (iterations >= text.length) clearInterval(interval);
            iterations += 1 / 2;
        }, 50);
    }

    setInterval(() => {
        const nameEl = document.getElementById("scrambleName");
        if (!nameEl) return;
        showingOriginal = !showingOriginal;
        scrambleText(nameEl, showingOriginal ? original : alternate);
    }, 3000);
})();
