# Kwiktow NQ — Townsville Towing Website

Static, SEO-optimised marketing site for **Kwiktow NQ**, a 24/7 towing &amp; recovery business serving Townsville and North Queensland.

## Stack
- Plain HTML5, CSS3, vanilla JS — no build step, deploy anywhere (Netlify, Vercel, S3, GitHub Pages, cPanel).
- Mobile-first responsive design.
- JSON-LD structured data (LocalBusiness / AutomotiveBusiness, Service, FAQPage) for rich Google results.
- `llms.txt` included for LLM/AI assistant discoverability.

## Pages
| File | Purpose |
|---|---|
| `index.html` | Home — hero, carousel, services overview, USPs, testimonials, FAQ teaser |
| `services.html` | Detailed service pages with anchor sections |
| `service-areas.html` | Suburb &amp; regional coverage (Townsville, Thuringowa, Magnetic Is., Ayr, Ingham, Charters Towers) |
| `about.html` | Company story, values, fleet |
| `faq.html` | Frequently asked questions (with FAQPage schema) |
| `contact.html` | Contact details + quote form + depot map placeholder |
| `404.html` | Custom not-found page |

## Replacing placeholders before launch

### 1. Phone number
Replace `0400 000 000` and `+61400000000` everywhere:

```bash
grep -rl '0400 000 000\|+61400000000' . --include='*.html'
```

### 2. Images
The site uses dashed-border placeholders. Replace with real photos:

| Placeholder location | Suggested filename |
|---|---|
| Home carousel (5 slides) | `assets/images/slide-1.jpg` … `slide-5.jpg` |
| Home "Why us" split | `assets/images/why-us.jpg` |
| Services page sections | `tilt-tray.jpg`, `accident.jpg`, `breakdown.jpg`, `heavy.jpg`, `4wd.jpg`, `machinery.jpg`, `roadside.jpg`, `long-distance.jpg` |
| About page | `about-team.jpg` |
| Service Areas + Contact maps | embed `<iframe>` from Google Maps |

To swap a placeholder, replace the `<div class="placeholder">…</div>` or `<div class="img-placeholder">…</div>` block with `<img src="assets/images/your-photo.jpg" alt="descriptive alt text">`.

### 3. Domain
Sitemap, canonical tags and OG URLs use `https://kwiktownq.com.au/`. Update if the domain differs.

### 4. Social links
Update `sameAs` URLs in the home-page JSON-LD (currently placeholder Facebook/Instagram handles).

### 5. Map embeds
Two locations expect a Google Maps `<iframe>`:
- `service-areas.html` (top)
- `contact.html` (bottom)

## SEO highlights
- Title tags &amp; meta descriptions tuned for **"towing Townsville"**, **"tow truck Townsville"**, **"24 hour towing North Queensland"**, **"tilt tray Townsville"** and related long-tail variants.
- LocalBusiness schema with geo coordinates (Townsville), opening hours, area served, aggregate rating placeholder.
- FAQPage schema for rich result eligibility.
- Service schema with offer catalog.
- Suburb-rich content (every Townsville suburb mentioned) for local search.
- Canonical tags, OpenGraph, Twitter cards.
- Sitemap + robots.txt.
- `llms.txt` for AI assistant context.

## Local preview
Just open `index.html` in a browser, or:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```
