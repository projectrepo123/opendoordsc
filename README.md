# New Beginnings DSC — Website

Short-term / vacation property rental site for **New Beginnings DSC** (host: **Nichole**).
Built by **JB Web Co.** Light, warm hospitality theme: clay + teal + sun on warm paper.

- **Static site, no build step.** Plain HTML + inline CSS + vanilla JS.
- **Hosting:** Cloudflare Pages (assets served from `public/`).
- **Forms:** Formspree.
- **Listings are data-driven** from `public/data/properties.json` and rendered client-side,
  so the catalog is easy to edit now and **CMS-ready** for Nichole's self-serve admin later
  (see _Phase 2_).
- **Availability** is shown via a mock per-stay calendar driven by `unavailableDates` in
  `properties.json`. The data shape maps cleanly to iCal sync or a booking platform when
  Nichole picks one.

> This is a **template / placeholder** build. Logo, photos, real copy, the Formspree ID,
> the booking provider, and the live domain are all swapped in later. Search the code for
> `__SWAP__` to find every spot that needs a real value.

---

## Project structure

```
NewBeginningsDSC/
├── wrangler.jsonc              # Cloudflare Pages config (project name: jbwebcoclientsnewbeginningsdsc)
├── .gitignore
├── scripts/
│   └── make_placeholders.py    # regenerates placeholder brand + property images (Pillow)
└── public/                     # everything served lives here
    ├── index.html              # homepage (hero, JS-rendered listings, why-us, about, FAQ, inquiry form)
    ├── stay/index.html         # per-property page: /stay/?id=<slug> with availability calendar
    ├── privacy.html
    ├── 404.html
    ├── _headers                # security headers + CSP + cache rules
    ├── robots.txt
    ├── sitemap.xml
    ├── favicon.svg, favicon.png, apple-touch-icon.png, og-share.png
    ├── data/properties.json    # the listings + availability (edit this to manage stays)
    └── images/properties/      # per-property photos (slug-prefixed)
```

## Brand basics

- **Type:** Fraunces (display, variable optical-size serif) + Inter (body).
- **Palette:** clay `#d96b4a`, teal `#0e8f7c`, sun `#f4c95a`, warm paper `#faf5ea`, ink `#1c2422`.
- **Voice:** brand "we / our" for marketing copy; Nichole speaks in first person ("I / my") inside About and FAQ.

---

## Local preview

`fetch()` needs HTTP. Opening the files via `file://` will not load the listings.

```bash
# Option A. Quick, does NOT apply _headers/CSP:
cd public
python -m http.server 8000
#   open http://localhost:8000/

# Option B. Closest to production, applies _headers, CSP, 404:
npx wrangler pages dev public
```

Check: homepage grid renders, `/stay/?id=sunny-cottage` loads with its availability
calendar, a bad id shows the "couldn't find that stay" page, the inquiry form validates,
the sticky mobile booking bar appears on narrow widths, and the layout is responsive.

---

## Managing the listings (`public/data/properties.json`)

Each entry under `"properties"`:

| Field | Notes |
|---|---|
| `id` | URL slug, lowercase-with-hyphens, **unique**. Used in `/stay/?id=<id>`. |
| `name`, `tagline` | Display title plus a one-liner. |
| `status` | `available` (shown), `coming-soon` (hidden from grid), `draft` (hidden everywhere). |
| `featured` | `true` floats it to the front of the grid and adds a "Featured" badge. On desktop the first featured card spans two columns. |
| `location.label` | e.g. `"Lake Saint Louis, MO"`. |
| `capacity` | `guests`, `bedrooms`, `beds`, `baths` (numbers). |
| `price` | `amount` (number), `unit` (`"night"`), `currency`, optional `note` (e.g. minimum nights). |
| `description` | Use a blank line (`\n\n`) to separate paragraphs. |
| `amenities` | List of strings, shown as a checklist. |
| `images` | List of `{ "src": "images/properties/<file>", "alt": "...", "featured": true }`. Store `src` **without** a leading slash. The first/`featured` image is the thumbnail. |
| `unavailableDates` | List of `{ "from": "YYYY-MM-DD", "to": "YYYY-MM-DD" }` ranges. These dates render as booked on the stay-page calendar. |
| `booking` | `type` = `"inquiry"` (use the request form, default), `"external"` (link out, set `url`), or `"iframe"` (Phase 2). |

**To add a stay:** copy an entry, give it a new `id`, drop photos into `images/properties/`
(named `<id>-1.jpg`, `-2.jpg`, ...), and list them in `images`.
**To hide a stay:** set `status` to `coming-soon` or `draft`.
**To mark booked dates:** add the date range(s) to `unavailableDates`.
**Valid JSON only.** No trailing commas, straight quotes. If the file is broken the site
shows a friendly fallback and logs a warning to the console.

### Placeholder images

`python scripts/make_placeholders.py` regenerates the favicon, social card, and the labeled
property tiles. When real photos arrive, just drop them in at the same paths (overwriting
the placeholders) and update the `images` entries.

---

## Swap-in checklist (before launch)

Search the codebase for `__SWAP__`. In order of importance:

1. **Formspree ID** in `public/index.html`. Replace `__SWAP_FORMSPREE_ID__` in the
   inquiry `fetch()` with the real form ID.
2. **Logo.** Replace the inline `.brand-mark` SVG and the wordmark with Nichole's logo
   `<img>` in the nav, mobile menu, and footer of both HTML pages. Regenerate favicons
   and the OG card.
3. **Photos.** Real JPGs into `images/properties/`. Update `images[]` in `properties.json`.
4. **Real copy.** Hero, About-Nichole bio, FAQ, and each listing's text.
5. **Domain.** Set the real domain in the `canonical` and `og:url` tags (both HTML pages),
   `robots.txt`, and `sitemap.xml` (currently `https://newbeginningsdsc.com/`).
6. **Contact.** Email and phone in the footers, privacy page, and the `LodgingBusiness`
   JSON-LD.

---

## Deploy (Cloudflare Pages)

- **GitHub repo:** `jbwebco_clients_NewBeginningsDSC` (matches JB Web Co. convention).
- **Cloudflare Pages project / wrangler name:** `jbwebcoclientsnewbeginningsdsc`.
- Build command: _none_. Output directory: `public`.
- Or `npx wrangler pages deploy public`.

---

## Phase 2 (planned, not built yet)

1. **Nichole's self-serve admin.** Add a Git-based CMS (Sveltia or Decap) at `/admin` that
   edits `data/properties.json` and commits to GitHub, triggering a Pages rebuild. Auth via
   GitHub OAuth through a small Cloudflare Worker. Scope any CSP relaxations to `/admin/*`
   in `_headers` so the public site stays locked down.

2. **Real booking platform.** The mock calendar's `unavailableDates` field is the seam.
   Three good options for Nichole, in order of how much she wants to take on:

   | Platform | Price | Best for |
   |---|---|---|
   | **iCal feeds from Airbnb / Vrbo** | Free | Already listing on Airbnb/Vrbo, wants one-way sync (booked dates flow into our calendar). No payment processing on our site. |
   | **Lodgify** | ~$24/mo | Wants a full booking flow on her own site with payment, owns the customer relationship. Easy to embed. |
   | **Hospitable** | ~$40/mo | Multi-channel automation. Smart messaging. Strong if she lists across Airbnb + Vrbo + direct. |
   | **OwnerRez** | $36–$95/mo | Most powerful and customizable. Worth it once she has 5+ properties or wants serious automation. |

   When a platform is picked: flip each listing's `booking.type` to `"external"` (link out)
   or `"iframe"` (embed), drop the provider widget into the booking-widget placeholder in
   `index.html`, and add the provider origin to `frame-src` in **both** `_headers` and the
   meta CSP. The Formspree inquiry form stays as a fallback.

3. **Optional SEO pre-render** of static `/stay/<slug>/` pages if social unfurls or SEO
   become a priority (see Social link previews below).

### Social link previews

`/stay/?id=…` pages render their content with JavaScript, so link-unfurl bots that don't
run JS (iMessage, Facebook, Slack, SMS) show the **generic** site share card, not a
per-property image. Links still unfurl cleanly. If per-property previews ever matter, add
a small pre-render script (like `make_placeholders.py`) that writes a static
`/stay/<slug>/index.html` per listing with baked-in OG tags.
