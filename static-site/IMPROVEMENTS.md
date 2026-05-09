# claeryc.com — Improvement Plan

> Planning document for design, UX, code quality, and content improvements.
> Generated from a full audit of the static site on 2026-05-09.

---

## Site Overview

**claeryc.com** is a pure static HTML/CSS/JS personal blog. No build tools, no framework.

| Page | Status |
|---|---|
| `index.html` | Home — hero, project cards, intro, recent posts |
| `blog.html` | Full post listing with client-side search |
| `now.html` | /now timeline page |
| `recs.html` | Recommendations — placeholder only |
| `chinese.html` | Mandarin study project page |
| `posts/` | Individual blog posts |
| `404.html` | Error page |

**What's working well:**
- Strong visual personality — scramble logo, 3D tilt cards, parallax hero
- Consistent CSS custom property system (`--bg`, `--fg`, `--bnb`, etc.)
- Light/dark theme toggle with `localStorage` persistence
- Responsive hamburger nav
- `/now` timeline design is clean and distinctive
- OG meta tags and `loading="lazy"` on images

---

## Improvement Areas

### 1. Code Quality & Maintainability

The same JavaScript blocks (theme toggle, navbar hide-on-scroll, logo scramble) are copy-pasted into every HTML file. This makes updates fragile — changing one means updating all of them.

**Key issues:**
- No shared `main.js` — scripts duplicated across all pages
- Heavy inline styles in `index.html` (the personal intro section)
- `post_listing_layout.css` exists but may be partially redundant with `styles.css`
- No build pipeline — no minification, bundling, or image optimization

---

### 2. Dark Mode Gaps

Several components break in dark mode because they use hardcoded light-only colors.

**Key issues:**
- `.p_card` background is hardcoded `#f8f8f8` — renders as a bright white card in dark mode
- `.callout` uses hardcoded `#fff8e5` and `#f39c12` — ignores dark theme
- `details` element uses `#fafafa` / `#fff8e5` backgrounds — same problem
- `footer::after` is hardcoded `#0a0a23` — fine for light mode but should use `var(--bnb)`

---

### 3. Design & UX

**Homepage:**
- Hero title "Welcome to My Blog" is generic — something more personal/branded would fit better
- The personal intro section has a lot of scattered inline `style=""` attributes — good candidate to extract into a CSS class

**Blog page:**
- No header or hero — jumps straight into a search box after a gap; feels abrupt
- Blog cards show only 3 posts on the homepage but 5 on `blog.html` — inconsistency worth clarifying (intentional "latest 3" or oversight?)

**Navigation / Dead ends:**
- Footer links (About, Contact, Privacy) are all `href="#"` — non-functional
- "Travel Journey" and "Mini Projects" project cards say "Coming Soon" but link to `#` — users hit dead ends
- Recs page is a placeholder with no content

**Visual consistency:**
- `now.html` has Playfair Display headings but the font isn't imported via a `<link>` tag in `styles.css` — relies on system fallback (will look different across devices unless the font is loaded)
- Copyright in footer reads "© 2025" but the site has April 2026 content

---

### 4. Potential Bug — Vanilla Tilt

The project cards in `index.html` use `data-tilt`, `data-tilt-max`, `data-tilt-glare` etc. but there is no `<script src="...vanilla-tilt...">` import visible in the page. If Vanilla Tilt is not loaded, the tilt effect silently fails. Worth verifying the script is included (possibly in a `<head>` link that was missed, or needs to be added).

---

### 5. Performance

- No image dimensions (`width`/`height`) on `<img>` tags — causes Cumulative Layout Shift (CLS)
- `background-attachment: fixed` (parallax) on the hero is known to trigger slow paint on iOS Safari — already has a mobile override (`background-attachment: initial`) but only below 600px
- No preloading for critical images (e.g., the hero background `thailand.jpg`)
- Images are large JPEGs/PNGs — no WebP conversion or responsive `srcset`
- Scripts are not deferred (most are at bottom of `<body>`, which is fine, but no `defer` attribute)

---

### 6. SEO & Discoverability

- No `sitemap.xml`
- No `robots.txt`
- OG image (`og:image`) defaults to `thailand.jpg` on almost all pages — individual post pages should use their own banner image
- No JSON-LD structured data (Article, Person, BreadcrumbList)
- No canonical `<link>` tags

---

### 7. Accessibility

- Theme toggle `<button id="theme-toggle">` has no `aria-label` — screen readers just hear "Theme"
- Hamburger `<label for="menu-toggle">` has no text or `aria-label`
- Search `<label for="search">` on homepage is empty (just a space)
- CSS-only checkbox-based mobile menu may have screen reader / keyboard focus issues
- No skip-to-main-content link
- Low-opacity text (`opacity: 0.45` on `--fg`) may fail WCAG AA contrast ratio (4.5:1) depending on theme

---

### 8. Content Gaps

- No About page (linked in footer but page doesn't exist)
- No tags or categories — no way to filter posts by topic (travel, language, AI, etc.)
- No reading time estimate on post cards
- No RSS/Atom feed — no way for readers to subscribe
- `recs.html` is a great page idea but completely empty

---

## Prioritised Improvement Checklist

Items are grouped by effort and impact. High priority items are things that are broken or actively hurt UX. Medium are meaningful enhancements. Low are polish / nice-to-haves.

### 🔴 High Priority (Fix These First)

**Bugs & broken things:**
- [x] Verify Vanilla Tilt script is properly imported in `index.html` — added CDN import
- [x] Fix all `href="#"` footer links — About → `about.html`, Contact → mailto, Privacy removed
- [x] Fix `.p_card` background: now uses `--card-bg` CSS variable (dark-mode aware)
- [x] Fix `.callout`, `details`: now use `--callout-bg` / `--callout-border` variables

**Content correctness:**
- [x] Update copyright year — updated to © 2026 across all 12 HTML files
- [ ] Update OG image per-page so individual posts use their own banner image

---

### 🟡 Medium Priority (Next Iteration)

**Code quality:**
- [x] Extract shared JS (theme toggle, navbar hide-on-scroll, logo scramble) into `static/blog/main.js`
- [ ] Extract the personal intro section's inline styles in `index.html` into a CSS class in `styles.css`
- [x] Add Google Fonts `@import` for Playfair Display in `styles.css`

**UX / design:**
- [ ] Replace "Welcome to My Blog" hero title with something more personal and on-brand
- [x] Add a proper header/intro to `blog.html`
- [x] Add content to `recs.html` — books, Mandarin resources, tools
- [ ] Replace "Coming Soon" project card links with something less dead-end

**SEO / discoverability:**
- [x] Add `sitemap.xml`
- [x] Add `robots.txt`
- [ ] Add JSON-LD Person/Blog structured data to `index.html`

**Performance:**
- [ ] Add explicit `width` and `height` attributes to `<img>` tags to prevent layout shift
- [ ] Preload the hero background image (`<link rel="preload" as="image">`)
- [ ] Convert large images to WebP format for better compression

---

### 🟢 Low Priority (Polish & Future Features)

**Accessibility:**
- [ ] Add `aria-label="Toggle theme"` to the theme button
- [ ] Add `aria-label="Open menu"` to the hamburger label
- [ ] Fix empty search form label (`<label for="search">`)
- [ ] Add a skip-to-main-content link at the top of each page
- [ ] Audit low-opacity text for WCAG AA contrast compliance

**Content & features:**
- [ ] Create an About page (`about.html`) and wire it up in the footer
- [ ] Add post tags/categories and filter UI on `blog.html`
- [ ] Add reading time estimate to post cards
- [ ] Add RSS/Atom feed (`feed.xml`)
- [ ] Consider an email subscribe option (e.g., a simple mailto link or Buttondown integration)

**Code architecture:**
- [ ] Consider a lightweight HTML partial system (or a minimal SSG like Eleventy/Astro) to eliminate repeated navbar/footer/scripts across files — this becomes more valuable as the post count grows
- [ ] Add post count badge or "X posts" indicator on the blog page

---

## Notes on Future Tech Direction

The current pure-HTML approach is refreshingly simple and fast, but copy-pasting the navbar, footer, and 4 JS blocks into every new page will become painful at scale. Options to consider when the time feels right:

- **Lightweight SSG** — Eleventy (11ty) would preserve the current HTML/CSS workflow almost exactly but add partials, templates, and automatic RSS generation
- **Shared JS bundle** — even without a build tool, extracting the shared scripts into `main.js` and using a single `<script src="...">` would be a big win with minimal disruption
- **Image pipeline** — a simple script (sharp/imagemagick) to batch-convert images to WebP and generate `srcset` would meaningfully improve load times

---

*Last updated: 2026-05-09*
