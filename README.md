# AKINTAYO — akintayoakingbehin.com

A static, multi-page portfolio site positioning **AKINTAYO** as a specialist
website designer for the table tennis industry. No framework, no build step
required to deploy, no dependencies. Plain HTML, one CSS file, one JS file.

---

## 1. Deploy it

**Every file sits in the root of this folder. There are no subfolders, and that is
deliberate** — see section 3. Upload the *contents* of this folder, not the folder
itself.

**GitHub Pages**
Put all these files at the root of the repository (or in `/docs` if you set Pages to
serve from there). `index.html`, `site.css`, `site.js`, the four `og-*.jpg` files,
`favicon.svg` and `.nojekyll` all sit side by side. Settings → Pages → Deploy from a
branch → root. It works both at `https://<user>.github.io/<repo>/` and at a custom
domain, because every path in the HTML is relative.

`.nojekyll` is an empty file that tells GitHub Pages not to run the files through
Jekyll first. Keep it — it is invisible in the file list on most systems but it must
be committed.

**Netlify / Vercel / Cloudflare Pages**
Drag this folder onto the deploy area. No build command, no output directory.

**Any normal host (cPanel, Hostinger, shared hosting)**
Upload the contents into `public_html`. `index.html` must sit at the top level.

**Check after deploying:** the page has a near-black background with blue accents.
If it looks like plain unstyled text, `site.css` is not being found — open the
browser console, look for a 404, and check the file is really at the same level as
`index.html`.

### Pointing akintayoakingbehin.com at it
`<link rel="canonical">`, `og:url` and `og:image` in every page are absolute and
point at `https://akintayoakingbehin.com`. That is correct once the domain is live.
While you are testing on a `github.io` URL the link-preview image will not resolve,
because it is being fetched from a domain that is not serving the site yet. Nothing
is broken — it fixes itself when DNS points at the deployment. If you want the
GitHub Pages URL to be canonical in the meantime, change one line in `build.py`:

```python
DOMAIN = "https://<user>.github.io/<repo>"
```

and rebuild.

## 2. Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `work.html` | Work — all three projects |
| `table-tennis-usa.html` | Case study 01 — the flagship, with the conversion data |
| `gewo-usa.html` | Case study 02 |
| `paul-david.html` | Case study 03 |
| `services.html` | Services in detail + process |
| `about.html` | About, principles, stack |
| `contact.html` | Contact — email only |
| `404.html` | Not-found page |

`robots.txt` and `sitemap.xml` are included and already point at
`akintayoakingbehin.com`.

---

## 3. Images and file layout

**The case studies carry no screenshots.** They are text, data and diagrams — the
conversion chart, the traffic/orders comparison, the four-month table, the GEWO
navigation tree and catalogue-depth chart, and the two Paul David flow diagrams.
All of it is drawn in HTML and CSS, so there is nothing to produce, nothing to
keep up to date, and nothing that can break.

Each case study instead opens with a prominent **"Open the live store"** button.
With no screenshots, the live sites are the visual proof — and a real site a
prospect can click through is stronger evidence than a screenshot anyway.

The entire image set is seven files, already built and sitting beside the HTML:

| File | What it is |
|---|---|
| `og-default.jpg` | Link preview card for Home, Work, Services, About, Contact |
| `og-ttusa.jpg` | Link preview card for the Table Tennis USA case study |
| `og-gewo.jpg` | Link preview card for the GEWO USA case study |
| `og-paul.jpg` | Link preview card for the Paul David case study |
| `favicon.svg` | Browser tab icon |
| `akintayo.jpg` | Your portrait — the "Built by a real person" section on the home page |
| `akintayo-seated.jpg` | Your portrait — the personal block on the contact page |

The preview cards are what appear when you paste a link into an email, a message,
LinkedIn or X. A link with a proper card gets opened noticeably more often than a
bare URL, which matters when the site's main job is cold outreach.

### Why everything is flat

`site.css`, `site.js` and the images live in the same folder as the HTML, and the
HTML refers to them by plain filename — `href="site.css"`, not `/site.css` and not
`assets/css/site.css`. A leading slash breaks on GitHub Pages project sites (it
resolves to the domain root, above your repository). A subfolder breaks the moment
the folder does not survive an upload. A plain relative filename survives both.

**If you ever move a file into a subfolder, you must update the reference in all
nine HTML files to match.** Keeping them flat is what makes that impossible to get
wrong.

## 4. Editing text

Two ways, pick whichever suits you.

**A. Edit the HTML directly.** Open the `.html` file, find the text, change it.
It is normal HTML with no templating. This is fine for small fixes.

**B. Edit `build.py` and rebuild.** All copy lives in `build.py`, and the header,
footer and navigation are defined once there instead of nine times. Change the
text, then run:

```bash
python3 build.py
```

That regenerates every `.html` file. Use this route for anything that appears on
more than one page — the email address, the nav, the footer. **Note: rebuilding
overwrites the HTML files**, so don't mix the two methods.

Key values at the top of `build.py`:

```python
EMAIL  = "akintayo@akintayoakingbehin.com"
DOMAIN = "https://akintayoakingbehin.com"
```

---

## 5. Where the content came from, and what to check

The case studies are built from primary sources, not invention:

- **Table Tennis USA** — your own *TTS CVR Presentation* deck (all 14 slides): the
  nine-item problem list, your seven-item role list, the homepage/trust/product-page
  solutions, and all four months of analytics.
- **GEWO USA** — the live site: navigation structure, the eight collection tiles and
  their product counts, the four trust claims, the six named sponsored players, the
  combo-specials architecture, and the company background (Ben Nisbet, the Mishel
  Levinski partnership, the "eyes of a player" philosophy).
- **Paul David** — the live site: the four services with exact durations, prices and
  descriptions, the per-service booking emails, and the Recommended Equipment page
  with the three GEWO setups and the `PDCGEWO` code.

**Three things to check before you send this anywhere:**

1. **"Chess grandmaster"** (About page, "Off the clock"). Worth a hard look. If you
   hold the formal FIDE Grandmaster title, leave it — it's remarkable and it will get
   remembered. If you mean you're a very strong player rather than titled, change it,
   because a prospect who checks and finds no FIDE record will discount everything
   else on the site, including the numbers. "Serious chess player" or a rating costs
   you almost nothing and carries no risk. Your call — edit the `human` list in
   `build.py` or the card in `about.html`.
2. **"I read and reply to every email myself"** (About and Contact). True today;
   remove it if volume ever makes it untrue.
3. **"Available for projects"** — the green status dot in the home page hero. To
   turn it off, delete the `<span class="status">…</span>` block in `index.html`.

### What the site deliberately does *not* claim
- No revenue figures anywhere.
- No invented client logos, testimonials, awards or statistics.
- No performance data for GEWO USA or Paul David — both case studies say plainly
  that none is published, which is what makes the Table Tennis USA numbers
  believable.
- **The traffic decline is shown, not hidden.** Visitors fell from 36.8k to 20.5k
  between December and January. The case study puts that in the table and then makes
  the argument it supports: orders held at 686 → 669, so the store converted the
  traffic it had far more efficiently. Leave this in. A prospect who spots a hidden
  decline stops believing the rest; a portfolio that volunteers it reads as someone
  who understands their own data.
- The qualifying note on the conversion figures stays for the same reason.

---

## 6. Design notes

- **Colour** — the whole identity lives in one block at the top of `site.css`.
  Change those eight values and the site re-colours:

  ```css
  --bg: #070B0D;  --bg-secondary: #0D1417;
  --blue: #155EEF;  --blue-bright: #2563EB;
  --green: #19D37A; --teal: #08B8A6;
  --white: #F5F7F6; --muted: #A7B0B0;
  ```

  Blue is the primary identity: logo dot, section numbers, eyebrows, links,
  borders, focus rings, the primary CTA. **Green is reserved for growth and
  results** — the "after" bars on the conversion chart, the delta figures, the
  live status dot. Teal bridges them and carries button hover states. The
  gradient `--gradient` is used sparingly: the page-transition wipe, the scroll
  progress bar, and the hairline edge on the portrait frames.

  One note on contrast: `#155EEF` is 3.6:1 on the dark ground, which is below
  the 4.5:1 readability threshold for text. So there is a second token,
  `--accent-text: #5B8DFF` (6.3:1), used **only** where blue becomes type. Fills,
  bars, borders and buttons still use the exact `#155EEF` you specified.

- **Photographs** — `akintayo.jpg` (home) and `akintayo-seated.jpg` (contact) are
  your supplied files, downscaled to 1200 × 1800 and nothing else. No filter, no
  retouching, no overlay sits on either image. The blue-green treatment is
  entirely on the frame *around* the photo: a soft glow behind it and a hairline
  gradient border on the edge. Framing is handled by `object-position` in CSS, so
  changing the crop never means re-exporting the file.

- **Type** — unchanged. Archivo for display and body, Instrument Serif italic as a
  rare accent, Martian Mono for labels and data.
- **Charts** — still plain HTML and CSS. No library, no images, no SVG to maintain.
- **Motion** — unchanged: custom cursor, magnetic buttons, cursor-following stat
  card, line-by-line headline reveals, page-transition wipe, hero trajectory,
  charts drawing on scroll.
- **Everything degrades safely.** All motion is off under `prefers-reduced-motion`,
  and charts render at full value rather than empty. If JavaScript fails entirely,
  nothing is hidden.

## 7. Suggested next steps

1. Confirm the three copy items in section 5 — particularly the chess line.
2. Deploy and check on your own phone.
3. For cold email, link to the case study rather than the home page when the
   prospect runs an ecommerce store: `akintayoakingbehin.com/table-tennis-usa.html`
   opens on the number, which is the strongest thing you have.
4. Later, when a fourth project lands: copy the structure of `gewo-usa.html` in
   `build.py`, add an entry to the `PROJECTS` list near the top, and rebuild.
