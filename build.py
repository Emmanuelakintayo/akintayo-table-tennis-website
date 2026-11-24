#!/usr/bin/env python3
"""
AKINTAYO — static site generator.

Emits plain HTML into this folder. There is no build step at deploy time:
GitHub serves the .html files this script writes. The script exists only so the
header, CTA block and footer are authored once instead of thirteen times; the
markup is written into every page, so SEO and no-JS visitors get everything.

    python3 build.py
"""
import os, html

OUT    = os.path.dirname(os.path.abspath(__file__))
EMAIL  = "akintayo@akintayoakingbehin.com"
DOMAIN = "https://akintayoakingbehin.com"
YEAR   = "2026"

def mail(subject="Website project enquiry"):
    from urllib.parse import quote
    return f"mailto:{EMAIL}?subject={quote(subject)}"

ARROW = ('<svg width="16" height="12" viewBox="0 0 16 12" fill="none" aria-hidden="true">'
         '<path d="M10 1l5 5-5 5M15 6H0" stroke="currentColor" stroke-width="1.6"/></svg>')
ARROW_S = ('<svg width="14" height="11" viewBox="0 0 16 12" fill="none" aria-hidden="true">'
           '<path d="M10 1l5 5-5 5M15 6H0" stroke="currentColor" stroke-width="1.6"/></svg>')

NAV = [("Work", "work.html"), ("Sports", "sports.html"), ("Services", "services.html"),
       ("About", "about.html"), ("Contact", "contact.html")]

SPORTS = [
    ("table-tennis", "Table tennis", "Equipment stores, club and coaching sites"),
    ("football",     "Football",     "Club and academy sites, retail stores"),
    ("cricket",      "Cricket",      "Club and league sites, kit stores"),
    ("volleyball",   "Volleyball",   "Team, tournament and school sites"),
    ("field-hockey", "Field hockey", "Club sites, fixtures, stick and kit stores"),
    ("ice-hockey",   "Ice hockey",   "Team, rink and league sites, jersey stores"),
]

# Faint line icons for the image placeholder, one per sport.
SPORT_ICON = {
    "table-tennis": '<circle cx="34" cy="30" r="16"/><path d="M26 44l-10 18 8 5 12-17"/><circle cx="62" cy="54" r="6"/>',
    "football":     '<circle cx="40" cy="40" r="26"/><path d="M40 22l10 8-4 13H34l-4-13z"/><path d="M40 14v8M18 34l12 4M62 34l-12 4M26 60l8-7M54 60l-8-7"/>',
    "cricket":      '<path d="M22 58L46 20l8 6-24 38z"/><path d="M20 56l-6 10 10-6z"/><circle cx="62" cy="52" r="9"/>',
    "volleyball":   '<circle cx="40" cy="40" r="26"/><path d="M40 14c-8 14-8 38 0 52M14 40c14-8 38-8 52 0M22 20c6 16 22 28 40 30"/>',
    "field-hockey": '<path d="M26 16v30c0 10 8 16 16 16s14-6 14-14"/><circle cx="60" cy="58" r="6"/>',
    "ice-hockey":   '<path d="M20 18v32c0 6 4 10 10 10h30"/><ellipse cx="58" cy="62" rx="12" ry="5"/>',
}

# ---------------------------------------------------------------- components
def btn(label, href, kind="", attrs=""):
    cls = "btn" + (f" btn--{kind}" if kind else "")
    return f'<a class="{cls}" href="{href}"{attrs}><span>{label}</span>{ARROW}</a>'

def tlink(label, href, attrs=""):
    return f'<a class="tlink" href="{href}"{attrs}>{label}{ARROW_S}</a>'

def circ():
    return f'<span class="circ" aria-hidden="true">{ARROW_S}</span>'

def slot(filename, sport="table-tennis", ratio="4/3"):
    """The styled placeholder. Used wherever a photograph has not been
    supplied yet, so a missing file never leaves a broken page."""
    icon = SPORT_ICON.get(sport, SPORT_ICON["table-tennis"])
    return (f'<div class="slot" style="aspect-ratio:{ratio}" role="img" '
            f'aria-label="Placeholder for {filename}">'
            f'<svg viewBox="0 0 80 80" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icon}</svg>'
            f'<span class="slot__l">Image &middot; {filename}</span></div>')

def img(src, alt, w, h, cls="", eager=False, style=""):
    ld = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    s = f' style="{style}"' if style else ""
    return (f'<img src="{src}" alt="{html.escape(alt, quote=True)}" '
            f'width="{w}" height="{h}" {ld} decoding="async"{c}{s}>')

def shot(src, alt, cap, w, h):
    return (f'<figure class="shot" data-reveal>{img(src, alt, w, h)}'
            f'<figcaption>{cap}</figcaption></figure>')

def phone(src, alt, w=780, h=1688):
    return (f'<div class="phone"><div class="phone__d">{img(src, alt, w, h)}</div></div>')

GRIP = ('<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" '
        'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M9.5 6l-5 6 5 6M14.5 6l5 6-5 6"/></svg>')


def compare(bsrc, balt, bw, bh, asrc, aalt, aw, ah, label):
    """Drag-to-compare slider. Before fills the left of the frame, after the
    right. The range input is the whole control surface, so pointer, touch
    and keyboard all work without any custom event handling."""
    return f"""<div class="ba" data-reveal>
  <div class="ba__frame">
    <img class="ba__img" src="{asrc}" alt="{html.escape(aalt, quote=True)}" width="{aw}" height="{ah}" loading="lazy" decoding="async">
    <div class="ba__clip"><img class="ba__img" src="{bsrc}" alt="{html.escape(balt, quote=True)}" width="{bw}" height="{bh}" loading="lazy" decoding="async"></div>
    <span class="ba__tag ba__tag--l">Before</span>
    <span class="ba__tag ba__tag--r">After</span>
    <input class="ba__range" type="range" min="0" max="100" value="50" step="0.1"
           aria-label="Drag to compare {label}">
    <span class="ba__bar" aria-hidden="true"><span class="ba__grip">{GRIP}</span></span>
  </div>
  <p class="ba__cap">Drag the handle &middot; before on the left, after on the right</p>
</div>"""


def ashot(src, alt, cap, w, h, kicker):
    """A dashboard screenshot shown large, never upscaled past its own pixels,
    pannable on a narrow screen rather than shrunk to nothing."""
    return f"""<figure class="ashot" data-reveal>
  <p class="ashot__k">{kicker}</p>
  <div class="ashot__s"><img src="{src}" alt="{html.escape(alt, quote=True)}" width="{w}" height="{h}" loading="lazy" decoding="async" style="max-width:{w}px"></div>
  <figcaption>{cap}<span class="ashot__hint">Swipe the panel to see all of it</span></figcaption>
</figure>"""

def meta_row(items):
    cells = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in items)
    return f'<dl class="meta" data-reveal>{cells}</dl>'

def shead(label, title_html, aside="", link=None):
    a = f'<p class="lead body" style="max-width:48ch">{aside}</p>' if aside else ""
    l = ""
    if link:
        l = f'<div>{tlink(link[0], link[1])}</div>'
    row = f'<div class="shead__row"><div>{title_html}</div>{l}</div>' if link else title_html
    return (f'<div class="shead" data-reveal><p class="label">{label}</p>{row}{a}</div>')

# -------------------------------------------------------------------- chrome
def header(current, over_hero=False):
    links = ""
    for i, (label, href) in enumerate(NAV, 1):
        cur = ' aria-current="page"' if href == current else ""
        links += f'<a href="{href}"{cur}>{label}<sup>0{i}</sup></a>'
    menu_links = "".join(f'<a href="{h}">{l}</a>' for l, h in NAV)
    cls = "hdr" + ("" if over_hero else " hdr--static")
    dark = ' style="color:#fff"' if over_hero else ""
    return f"""<header class="{cls}"{dark}>
  <div class="wrap hdr__in">
    <a class="mark" href="index.html" aria-label="Akintayo, home">AKINTAYO<i></i></a>
    <nav class="nav" aria-label="Primary">{links}</nav>
    <div class="hdr__cta">{btn("Start a project", mail(), "primary" if not over_hero else "pear")}</div>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<div class="menu" id="menu" aria-label="Menu">
  <button class="menu__close" type="button" aria-label="Close menu">&times;</button>
  {menu_links}
  <p class="menu__mail"><a href="{mail()}" style="color:inherit">{EMAIL}</a></p>
</div>"""

def cta():
    return f"""<section class="cta">
  <div class="wrap">
    <p class="label" data-reveal style="color:var(--pear)">Have a project?</p>
    <h2 class="cta__h" data-reveal>LET&rsquo;S <em class="it">play.</em></h2>
    <a class="cta__mail" href="{mail()}" data-reveal>{EMAIL}</a>
    <div class="cta__row" data-reveal>
      <p>Tell me about your team, club or store. I&rsquo;ll look properly and reply with scope and price in writing.</p>
      {btn("Start a project", mail(), "light")}
    </div>
  </div>
</section>"""

def footer():
    pages = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in NAV)
    sports = "".join(f'<li><a href="sports.html#{sid}">{name}</a></li>'
                     for sid, name, _ in SPORTS[:4])
    sports += '<li><a href="sports.html#field-hockey">Field &amp; ice hockey</a></li>'
    return f"""<footer class="ftr">
  <div class="wrap">
    <div class="ftr__top">
      <div><span class="mark" aria-hidden="true">AKINTAYO<i></i></span></div>
      <div><h3>Pages</h3><ul>{pages}</ul></div>
      <div><h3>Sports</h3><ul>{sports}</ul></div>
      <div><h3>Contact</h3><ul>
        <li><a href="{mail()}">{EMAIL}</a></li>
        <li>Osun State, Nigeria</li>
        <li>Working worldwide</li>
      </ul></div>
    </div>
    <div class="ftr__bot">
      <span>&copy; {YEAR} Akingbehin Akintayo</span>
      <span>Sports web design</span>
      <span data-clock>03:16 AM GMT+1</span>
    </div>
  </div>
</footer>
<div class="sticky" aria-hidden="false">
  <span style="font-size:.9rem">Have a project?</span>
  {btn("Start", mail(), "light")}
</div>"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wght@400;500;600;700;800&'
         'family=Instrument+Serif:ital@1&'
         'family=Martian+Mono:wght@400;500&display=swap">')

def page(fname, title, desc, current, body, og="og-default.jpg", jsonld="", over_hero=False):
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="canonical" href="{DOMAIN}/{fname}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:url" content="{DOMAIN}/{fname}">
<meta property="og:image" content="{DOMAIN}/{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title, quote=True)}">
<meta name="twitter:description" content="{html.escape(desc, quote=True)}">
<meta name="twitter:image" content="{DOMAIN}/{og}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="site.css">
{jsonld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(current, over_hero)}
<main id="main">
{body}
</main>
{footer()}
<script src="site.js" defer></script>
</body>
</html>
"""
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(doc)
    return fname


# ===================================================================== HOME ==
def build_home():
    sports_rows = ""
    for i, (sid, name, desc) in enumerate(SPORTS, 1):
        sports_rows += f"""<a class="srow" href="sports.html#{sid}">
  <span class="srow__n">0{i}</span>
  <span class="srow__b"><span class="srow__t">{name}</span><span class="srow__d">{desc}</span></span>
  {slot_prev(sid)}
  {circ()}
</a>"""

    mq = ('<span>TABLE TENNIS</span><em>football</em><span>CRICKET</span>'
          '<em>volleyball</em><span>FIELD HOCKEY</span><em>ice hockey</em>')

    services = [
        ("01", "Website design from scratch", "New clubs, academies, coaches and brands launching direct."),
        ("02", "Ecommerce website design", "Stores for equipment, kits and gear that make buying easy."),
        ("03", "Website redesign", "A new look and a clearer path, without losing your content."),
        ("04", "Conversion optimisation", "More sign-ups and sales from the traffic you already have."),
    ]
    scols = "".join(f'<div class="scol" data-reveal><p class="scol__n">{n}</p>'
                    f'<h3 class="scol__t">{t}</h3><p class="scol__d">{d}</p></div>'
                    for n, t, d in services)

    jsonld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Akingbehin Akintayo",
"alternateName":"Akintayo","jobTitle":"Web designer and developer",
"email":"mailto:akintayo@akintayoakingbehin.com","url":"https://akintayoakingbehin.com",
"address":{"@type":"PostalAddress","addressRegion":"Osun State","addressCountry":"NG"},
"knowsAbout":["Sports web design","Shopify","Ecommerce UX","Conversion optimisation"]}
</script>"""

    body = f"""
<section class="hero">
  <div class="hero__panel">{img("akintayo-cutout.png","Akingbehin Akintayo",850,1194,eager=True)}</div>
  <div class="hero__strip" aria-hidden="true">
    <div class="mqv"><div class="mqv__t">AKINTAYO &copy; SPORTS WEB DESIGN &copy; AKINTAYO &copy; SPORTS WEB DESIGN &copy;</div></div>
  </div>
  <a class="hero__badge" href="contact.html" aria-label="Available for projects worldwide. Get in touch.">
    <svg viewBox="0 0 158 158" aria-hidden="true">
      <defs><path id="bcirc" d="M79,79 m-58,0 a58,58 0 1,1 116,0 a58,58 0 1,1 -116,0"/></defs>
      <g class="spin"><text font-family="Martian Mono, monospace" font-size="11" letter-spacing="2.2" fill="currentColor">
        <textPath href="#bcirc">AVAILABLE FOR PROJECTS &#8226; WORLDWIDE &#8226; </textPath>
      </text></g>
    </svg>
    <span class="mid" aria-hidden="true">{ARROW}</span>
  </a>
  <div class="wrap hero__in">
    <h1 class="xl hero__h"><span class="ln"><span>WEBSITES</span></span><span class="ln"><span>BUILT FOR</span></span><span class="ln"><span>THE <em class="it">game.</em></span></span></h1>
    <p class="hero__lead">Websites for clubs, academies, brands and stores in table tennis, football, cricket, volleyball and hockey.</p>
    <div class="hero__btns">
      {btn("See the work", "work.html", "light")}
      {btn("Start a project", mail(), "outline")}
    </div>
    <div class="hero__micro">
      <span>Osun State, Nigeria &mdash; <span data-clock>03:16 AM GMT+1</span></span>
      <span>Sports web design</span>
      <span>Scroll &darr;</span>
    </div>
  </div>
</section>

<div class="mq mq--sports" aria-hidden="true"><div class="mq__t">{mq}</div></div>

<section class="sect">
  <div class="wrap">
    <p class="label" data-reveal>( 01 ) &mdash; Studio</p>
    <p class="statement" data-reveal style="margin-top:1.6rem">I design and build websites for sports <em class="it">clubs, academies, brands and stores</em> &mdash; so players, parents and fans find what they need in seconds.</p>
    <div class="stats">
      <div class="stat" data-reveal><p class="stat__v" data-count="163" data-pre="+" data-post="%">+163%</p><p class="stat__l">completed orders a month at TableTennisStore.us</p></div>
      <div class="stat" data-reveal><p class="stat__v" data-count="93" data-post="%">93%</p><p class="stat__l">of carts reached checkout, up from 52% before the redesign</p></div>
      <div class="stat" data-reveal><p class="stat__v" data-count="6">6</p><p class="stat__l">sports I design for &mdash; one designer, start to finish</p></div>
    </div>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    {shead("( 02 ) &mdash; Top projects", '<h2 class="tl">TWO FLAGSHIP<br><em class="it">sites.</em></h2>', link=("All work (5)", "work.html"))}
    <div class="pcards">
      <a class="pcard" href="fremont-table-tennis.html" data-reveal>
        <span class="pcard__img">{img("fremont-home-desktop.jpg","Fremont Table Tennis Academy homepage after the redesign",1365,1238)}</span>
        <span class="pcard__meta"><span>
          <span class="label">01 &mdash; Table tennis &middot; Club &amp; academy</span>
          <span class="ts pcard__t" style="display:block">Fremont Table Tennis Academy</span>
          <span class="pcard__d">A full redesign built around one question: which class is right for me?</span>
        </span>{circ()}</span>
      </a>
      <a class="pcard" href="table-tennis-usa.html" data-reveal>
        <span class="pcard__img">{img("tts-desk-c.jpg","TableTennisStore.us homepage",1364,1098)}</span>
        <span class="pcard__meta"><span>
          <span class="label">02 &mdash; Table tennis &middot; Ecommerce</span>
          <span class="ts pcard__t" style="display:block">TableTennisStore.us</span>
          <span class="pcard__d">Shopify redesign and conversion work. Completed orders up 163%.</span>
        </span>{circ()}</span>
      </a>
    </div>
  </div>
</section>

<section class="sect moon">
  <div class="wrap">
    {shead("( 03 ) &mdash; Sports", '<h2 class="tl">ONE DESIGNER.<br><em class="it">Six sports.</em></h2>')}
    <div>{sports_rows}</div>
  </div>
</section>

<section class="sect">
  <div class="wrap">
    {shead("( 04 ) &mdash; Services", '<h2 class="tl">WHAT I<br><em class="it">do.</em></h2>', link=("All services", "services.html"))}
    <div class="grid g-4">{scols}</div>
  </div>
</section>

<section class="sect dark">
  <div class="wrap">
    <div class="split--41 split">
      <div>
        <p class="label" data-reveal>( 05 ) &mdash; Client story</p>
        <h2 class="tm" data-reveal style="margin-top:1.2rem;font-size:clamp(2rem,4vw,3.25rem)">IN THEIR<br><em class="it" style="color:var(--pear);white-space:nowrap">own words.</em></h2>
        <p class="body" data-reveal style="margin-top:1.4rem;max-width:34ch">A short video from a client I&rsquo;ve worked with.</p>
      </div>
      <div>
        <figure class="testimonial tvid" data-reveal>
          <button class="tvid__poster" type="button" data-video aria-label="Play the client testimonial video">
            {img("testimonial-poster.jpg","Still from the client testimonial video",720,1280,style="object-fit:contain;background:var(--royal)")}
            <span class="play" aria-hidden="true"><svg width="22" height="26" viewBox="0 0 22 26" fill="currentColor"><path d="M22 13 0 26V0z"/></svg></span>
            <span class="tvid__tag">Video &middot; testimonial.mp4</span>
            <span class="tvid__dur">1:16</span>
          </button>
          <figcaption class="tvid__cap">
            <span class="tvid__av" aria-hidden="true"></span>
            <span>
              <strong style="display:block">Ben Nisbet</strong>
              <span class="body" style="font-size:.85rem">CEO &amp; founder &middot; Table Tennis Store USA and GEWO USA</span>
            </span>
            <span class="tvid__sport">Table tennis</span>
          </figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>

<dialog class="lbx" id="videoDialog" aria-label="Client testimonial video">
  <button class="lbx__x" type="button" aria-label="Close the video">&times;</button>
  <video controls playsinline preload="metadata" poster="testimonial-poster.jpg" style="aspect-ratio:9/16;max-height:82vh;width:auto;margin-inline:auto">
    <source src="testimonial.mp4" type="video/mp4">
    <a href="testimonial.mp4">Download the testimonial video</a>
  </video>
</dialog>

{cta()}
"""
    return page("index.html", "Akintayo — Sports Web Design for Clubs, Brands & Stores",
                "Websites for sports clubs, academies, brands and stores — table tennis, football, "
                "cricket, volleyball and hockey. Designed and built by Akintayo.",
                "index.html", body, jsonld=jsonld, over_hero=True)


def slot_prev(sid):
    """Hover preview on the home sports rows. Falls back to the styled
    placeholder when the sport photo has not been supplied."""
    import os as _os
    f = f"sport-{sid}.jpg"
    if _os.path.exists(_os.path.join(OUT, f)):
        return (f'<img class="srow__prev" src="{f}" alt="" aria-hidden="true" '
                f'width="300" height="190" loading="lazy">')
    return ""


# ===================================================================== WORK ==
PROJECTS = [
    dict(href="fremont-table-tennis.html", sport="table-tennis", pill="Top project",
         label="Table tennis &middot; Club &amp; academy", name="Fremont Table Tennis Academy",
         line="Redesign", im=("fremont-home-desktop.jpg", 1365, 1238),
         alt="Fremont Table Tennis Academy homepage after the redesign"),
    dict(href="table-tennis-usa.html", sport="table-tennis", pill="Top project",
         label="Table tennis &middot; Ecommerce", name="TableTennisStore.us",
         line="Shopify &middot; +163% completed orders", im=("tts-desk-c.jpg", 1364, 1098),
         alt="TableTennisStore.us homepage"),
    dict(href="gewo-usa.html", sport="table-tennis", pill=None,
         label="Table tennis &middot; Manufacturer store", name="GEWO USA",
         line="Shopify &middot; 1.2s largest paint, zero layout shift", im=("gewo-home.jpg", 1365, 1180),
         alt="GEWO USA homepage"),
    dict(href="octagon.html", sport="football", pill=None,
         label="Football &middot; Sports marketing", name="Octagon",
         line="Website design", im=("octagon-home.jpg", 1440, 900),
         alt="Octagon website"),
    dict(href="starting-eleven.html", sport="football", pill=None,
         label="Football &middot; Retail store", name="Starting Eleven",
         line="Shopify &middot; Lexington, KY", im=("starting-eleven-home.jpg", 1440, 640),
         alt="Starting Eleven online store"),
]

def project_card(p):
    pill = f'<span class="pcard__pill">{p["pill"]}</span>' if p["pill"] else ""
    src, w, h = p["im"]
    return f"""<a class="pcard" href="{p['href']}" data-sport="{p['sport']}" data-reveal>
  {pill}
  <span class="pcard__img">{img(src, p['alt'], w, h)}</span>
  <span class="pcard__meta"><span>
    <span class="label">{p['label']}</span>
    <span class="ts pcard__t" style="display:block">{p['name']}</span>
    <span class="pcard__d">{p['line']}</span>
  </span>{circ()}</span>
</a>"""

def build_work():
    cards = "".join(project_card(p) for p in PROJECTS)
    tile = f"""<div class="ctatile" data-reveal>
  <p class="label" style="color:var(--pear)">Your project next</p>
  <h3>GOT A TEAM, CLUB OR <em class="it">store?</em></h3>
  <div>{btn("Start a project", mail(), "light")}</div>
</div>"""
    body = f"""
<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal>( Work ) &mdash; Five projects</p>
    <h1 class="xl" data-reveal style="margin-top:1.4rem">SELECTED<br><em class="it">work.</em></h1>
    <div class="filters" style="margin-top:clamp(2.4rem,6vw,4rem)" role="group" aria-label="Filter projects by sport">
      <button type="button" data-filter="all" aria-pressed="true">All &mdash; 5</button>
      <button type="button" data-filter="table-tennis" aria-pressed="false">Table tennis &mdash; 3</button>
      <button type="button" data-filter="football" aria-pressed="false">Football &mdash; 2</button>
    </div>
    <div class="pcards">{cards}{tile}</div>
  </div>
</section>
"""
    return page("work.html", "Selected Work — Akintayo",
                "Five sports website projects: Fremont Table Tennis Academy, TableTennisStore.us, "
                "GEWO USA, Octagon and Starting Eleven.",
                "work.html", body, og="og-fremont.jpg")


# =================================================================== SPORTS ==
SPORT_PAGE = [
    ("table-tennis", "Table tennis", "Specialist", "01",
     "My home sport. I know how a player chooses a blade, a rubber and a sponge thickness "
     "&mdash; and how a club fills its classes.",
     ["Equipment stores for blades, rubbers, tables", "Club, academy and coaching websites",
      "Class booking, leagues and tournaments"]),
    ("football", "Football", "Proven", "02",
     "Clubs, academies and retail stores that need to be clear about fixtures, trials, kits "
     "and where to buy.",
     ["Club and academy websites", "Trial, camp and team registration",
      "Fan shops, kits and fixtures"]),
    ("cricket", "Cricket", "Now open", "03",
     "Clubs and leagues live on fixtures, scorecards and results. I make them easy to find on a phone.",
     ["Club and league websites", "Fixtures, scorecards and results",
      "Bat and kit stores, coaching bookings"]),
    ("volleyball", "Volleyball", "Now open", "04",
     "Club, beach and school teams that need sign-ups, schedules and tournament brackets in one place.",
     ["Club, beach and school team sites", "Tournament schedules and brackets",
      "Team sign-up and payments"]),
    ("field-hockey", "Field hockey", "Now open", "05",
     "Clubs that want fixtures, tables and results to be clear, and sticks and kit to be easy to buy.",
     ["Club and academy websites", "Fixtures, tables and results", "Stick and kit stores"]),
    ("ice-hockey", "Ice hockey", "Now open", "06",
     "Teams, rinks and leagues that need game schedules, standings and a jersey store fans actually use.",
     ["Team, rink and league websites", "Game schedules and standings", "Jersey and merch stores"]),
]

def build_sports():
    blocks = ""
    for i, (sid, name, chip, num, para, items) in enumerate(SPORT_PAGE):
        chipcls = "chip chip--solid" if chip in ("Specialist", "Proven") else "chip"
        lis = "".join(f"<li>{x}</li>" for x in items)
        f = f"sport-{sid}.jpg"
        media = (f'<div>{img(f, name + " website work", 1600, 1200)}</div>'
                 if os.path.exists(os.path.join(OUT, f))
                 else f'<div>{slot(f, sid)}</div>')
        rev = " sblock--rev" if i % 2 else ""
        blocks += f"""<section class="sblock{rev}" id="{sid}" data-reveal>
  <div class="sblock__t">
    <span class="{chipcls}">{chip}</span>
    <p class="label" style="margin-top:1rem">{num}</p>
    <h2>{name}</h2>
    <p>{para}</p>
    <ul>{lis}</ul>
    {tlink(f"Start a {name.lower()} project", mail(f"{name} website project"))}
  </div>
  {media}
</section>"""

    built = ["Clubs", "Academies", "Equipment brands", "Online stores",
             "Distributors", "Coaches", "Leagues &amp; tournaments"]
    chips = "".join(f'<span class="chip">{b}</span>' for b in built)

    body = f"""
<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal>( Sports ) &mdash; Six of them</p>
    <h1 class="xl" data-reveal style="margin-top:1.4rem">ONE DESIGNER.<br><em class="it">Six sports.</em></h1>
    <p class="lead body" data-reveal style="margin-top:1.8rem;max-width:52ch">Every sport has its own buyers, fans and habits. A rubber is specified, a class is booked, a fixture is checked, a jersey is browsed. I design around what your audience actually does.</p>
  </div>
</section>

<section class="sect" style="padding-top:0">
  <div class="wrap">{blocks}</div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <div class="builtfor" data-reveal>
      <span class="label" style="margin-right:1rem">Built for</span>{chips}
    </div>
  </div>
</section>

{cta()}
"""
    return page("sports.html", "Sports — Akintayo",
                "Websites for table tennis, football, cricket, volleyball, field hockey and ice "
                "hockey — clubs, academies, brands, stores, coaches and leagues.",
                "sports.html", body)


# ================================================================= SERVICES ==
SERVICES = [
  ("01", "Website design from scratch",
   "New clubs and academies, coaches, event organisers, distributors and brands launching direct.",
   ["Page structure", "Visual design and design system", "Full build and launch",
    "Mobile and performance", "Domain and DNS setup, handover"]),
  ("02", "Ecommerce website design",
   "Equipment brands, sports retailers, manufacturer-owned stores, distributors and clubs with a pro shop.",
   ["Catalogue and collection structure", "Product pages built for specs and sizes",
    "Filtering and search", "Cart and checkout flow", "Shopify and Liquid customisation"]),
  ("03", "Website redesign",
   "Sites that outgrew their design, teams after a rebrand, and sites whose builder is gone.",
   ["Audit of what works and what doesn&rsquo;t", "Redesign around your audience&rsquo;s path",
    "URL and content preserved", "Safe migration, no lost product data",
    "Before-and-after measurement"]),
  ("04", "Conversion optimisation",
   "Sports businesses with real traffic and a sign-up or sales rate that has stalled.",
   ["Journey mapping: browse &rarr; buy, book or join", "Product and collection page work",
    "Cart and checkout friction removed", "Trust, shipping and returns clarity",
    "Analytics and monthly reporting"]),
]

def build_services():
    rows = ""
    for n, title, who, items in SERVICES:
        lis = "".join(f"<li>{x}</li>" for x in items)
        rows += f"""<div class="srv" data-reveal>
  <div><p class="srv__n">{n}</p><h2 class="tm">{title}</h2></div>
  <div><p class="label">For</p><p class="srv__for" style="margin-top:.8rem">{who}</p></div>
  <ul>{lis}</ul>
</div>"""

    steps = [("1", "Learn your game", "Your sport, your audience, your catalogue or class list."),
             ("2", "Map the journey", "How a visitor goes from landing to buying, booking or joining."),
             ("3", "Design and build", "Pages designed and coded by the same person."),
             ("4", "Measure and refine", "Real numbers, reported month over month.")]
    stepsh = "".join(f'<div class="step" data-reveal><p class="step__n">{n}</p>'
                     f'<h3 class="step__t">{t}</h3><p class="step__d">{d}</p></div>'
                     for n, t, d in steps)

    incl = ["Mobile-ready", "Fast loading", "SEO structure",
            "Analytics and conversion tracking", "Meta Business integration", "You stay in control"]
    inclh = "".join(f'<div class="scol" data-reveal style="padding-top:1rem">'
                    f'<p style="font-weight:500">{x}</p></div>' for x in incl)

    body = f"""
<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal>( Services ) &mdash; Four, and only four</p>
    <h1 class="xl" data-reveal style="margin-top:1.4rem">WHAT I<br><em class="it">do.</em></h1>
    <p class="lead body" data-reveal style="margin-top:1.8rem;max-width:50ch">Four focused services, each shaped around how a club, coach, brand or store really earns &mdash; signing up players, selling gear, filling classes.</p>
  </div>
</section>

<section class="sect" style="padding-top:0"><div class="wrap">{rows}</div></section>

<section class="sect moon">
  <div class="wrap">
    <p class="label" data-reveal>How it works</p>
    <h2 class="tl" data-reveal style="margin-top:1.2rem;margin-bottom:clamp(2.4rem,5vw,4rem)">FOUR <em class="it">steps.</em></h2>
    <div class="steps">{stepsh}</div>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal style="margin-bottom:1.6rem">Every site includes</p>
    <div class="grid g-3">{inclh}</div>
  </div>
</section>

{cta()}
"""
    return page("services.html", "Services — Akintayo",
                "Website design from scratch, ecommerce design, website redesign and conversion "
                "optimisation for sports clubs, academies, brands and stores.",
                "services.html", body)


# ==================================================================== ABOUT ==
def build_about():
    how = [("Proof over adjectives", "Real numbers from real stores, not vague promises."),
           ("Audience first", "Players, parents and fans come before decoration."),
           ("Build it, don&rsquo;t just draw it", "Every design ships as working, fast code."),
           ("You stay in control", "A clean handover &mdash; your site, your keys.")]
    howh = "".join(f'<div class="scol" data-reveal><h3 class="scol__t">{t}</h3>'
                   f'<p class="scol__d">{d}</p></div>' for t, d in how)
    tools = ["Shopify &amp; Liquid", "Ecommerce UX &amp; CRO", "SEO structure",
             "Custom CSS &amp; JavaScript", "Analytics &amp; tracking", "Meta Business"]
    toolsh = "".join(f'<span class="chip chip--out">{t}</span>' for t in tools)

    body = f"""
<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal>( About ) &mdash; A designer who picked sport on purpose</p>
    <h1 class="xl" data-reveal style="margin-top:1.4rem">HI, I&rsquo;M<br><em class="it">Akintayo.</em></h1>
  </div>
</section>

<section class="sect" style="padding-top:0">
  <div class="wrap">
    <div class="split">
      <div data-reveal style="position:relative">
        <div style="overflow:hidden;aspect-ratio:5/7;background:var(--porcelain)">
          <!-- scaled from the bottom-right so the photographer's watermark in the
               top-left corner falls outside the frame -->
          {img("akintayo-seated.jpg","Akingbehin Akintayo",1200,1800,style="width:100%;height:100%;object-fit:cover;object-position:100% 100%;transform:scale(1.14);transform-origin:100% 100%")}
        </div>
        <div style="background:var(--pear);padding:14px 18px;display:inline-block;margin-top:-62px;position:relative;z-index:2">
          <p class="label" style="color:var(--royal)">Web designer &amp; developer</p>
          <p style="font-weight:800;text-transform:uppercase;letter-spacing:-.02em;margin-top:.3rem">Akingbehin Akintayo</p>
        </div>
      </div>
      <div>
        <p class="lead" data-reveal style="font-size:clamp(1.2rem,2.1vw,1.875rem);line-height:1.35">I&rsquo;m a web designer and developer from Osun State, Nigeria, building websites for sports businesses around the world.</p>
        <div class="body" data-reveal style="margin-top:2rem;display:grid;gap:1.2rem;max-width:58ch">
          <p>I started in table tennis &mdash; stores, clubs and coaches &mdash; and learned how players actually choose a blade, a class or a coach. Now I bring that same care to football, cricket, volleyball and hockey.</p>
          <p>When you work with me you work with one person: I read your email, go through your site, design the pages and write the code. No account managers, no hand-offs.</p>
        </div>
        <hr class="rule" style="margin:2.4rem 0 1.6rem">
        <p class="label" data-reveal>Off the clock</p>
        <p class="body" data-reveal style="margin-top:1rem;max-width:58ch">I&rsquo;m a Doctor of Pharmacy candidate at Obafemi Awolowo University. I play chess, collect gadgets and enjoy books, restaurants and travel. Beyond sport, I&rsquo;ve also built the Shopify store for ORIMI, a fine jewellery house shipping to more than 25 countries.</p>
      </div>
    </div>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal style="margin-bottom:2rem">How I work</p>
    <div class="grid g-2">{howh}</div>
    <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(2.4rem,5vw,3.6rem)" data-reveal>{toolsh}</div>
  </div>
</section>

{cta()}
"""
    return page("about.html", "About — Akintayo",
                "Akingbehin Akintayo, a web designer and developer in Osun State, Nigeria, "
                "building websites for sports clubs, academies, brands and stores worldwide.",
                "about.html", body, og="akintayo-seated.jpg")


# ================================================================== CONTACT ==
def build_contact():
    steps = [("01", "You email", "A few lines about your site and the problem."),
             ("02", "I look properly", "I go through your site before I reply."),
             ("03", "Scope and price", "In writing, with no surprises.")]
    stepsh = "".join(f'<div class="step" data-reveal><p class="step__n">{n}</p>'
                     f'<h3 class="step__t">{t}</h3><p class="step__d">{d}</p></div>'
                     for n, t, d in steps)
    body = f"""
<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal>( Contact ) &mdash; Email only, no forms to lose</p>
    <h1 class="xl" data-reveal style="margin-top:1.4rem">LET&rsquo;S<br><em class="it">connect.</em></h1>
  </div>
</section>

<section class="sect" style="padding-top:0">
  <div class="wrap">
    <div class="split" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr)">
      <div data-reveal>
        <p class="lead">Tell me about your team, club or store and what isn&rsquo;t working. I&rsquo;ll look properly and reply with scope and price in writing.</p>
        <dl class="dl" style="margin-top:clamp(2rem,4vw,3.4rem)">
          <dt>Email</dt><dd><a href="{mail()}" style="text-decoration:none;border-bottom:1px solid var(--line)">{EMAIL}</a></dd>
          <dt>Based in</dt><dd>Osun State, Nigeria<br>Working worldwide</dd>
          <dt>Local time</dt><dd data-clock>03:16 AM GMT+1</dd>
        </dl>
      </div>
      <div class="fcard" data-reveal>
        <p class="label">Start a project &mdash; opens an email</p>
        <form id="projectForm" action="{mail()}" method="get" style="margin-top:1.8rem">
          <label for="f-site">My website</label>
          <input id="f-site" name="site" type="text" placeholder="https://" autocomplete="url">
          <label for="f-biz">My sport and business</label>
          <input id="f-biz" name="biz" type="text" placeholder="Club, academy, brand or store">
          <label for="f-prob">What is not working</label>
          <textarea id="f-prob" name="problem" rows="3" placeholder="Tell me about the problem..."></textarea>
          <label for="f-when">Timeline</label>
          <input id="f-when" name="when" type="text" placeholder="When would you like to launch?">
          <button class="btn" type="submit"><span>Send email</span>{ARROW}</button>
          <p class="fcard__note">This opens your email app.</p>
        </form>
      </div>
    </div>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap"><div class="steps" style="grid-template-columns:repeat(3,minmax(0,1fr))">{stepsh}</div></div>
</section>
"""
    return page("contact.html", "Contact — Akintayo",
                "Email Akintayo about your sports website. No forms to lose, no calls to book — "
                "one email and a reply with scope and price in writing.",
                "contact.html", body)


# ---------------------------------------------------------- case templates
def case_head(label, title_html, meta, hero_html):
    return f"""
<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal>{label}</p>
    <h1 class="xl" data-reveal style="margin-top:1.4rem;font-size:clamp(2.9rem,8.6vw,7.75rem)">{title_html}</h1>
    {meta_row(meta)}
    <div class="casehero" data-reveal>{hero_html}</div>
  </div>
</section>"""

def next_project(title_html, href, label="Next project", cta_label="View case"):
    return f"""
<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal>{label}</p>
    <div class="nextp" data-reveal style="margin-top:1rem">
      <h2>{title_html}</h2>
      {btn(cta_label, href, "primary")}
    </div>
  </div>
</section>"""


# ================================================= CASE: FREMONT (new page) ==
def build_fremont():
    feats = [("01", "Find a class, fast", "Clear paths for kids, adults, camps and private lessons."),
             ("02", "Camps up front", "Camp registration promoted at the top of every page."),
             ("03", "One tap to act", "Call, text and register buttons always within reach.")]
    featsh = "".join(f'<div class="scol" data-reveal><p class="scol__n">{n}</p>'
                     f'<h3 class="scol__t">{t}</h3><p class="scol__d">{d}</p></div>'
                     for n, t, d in feats)

    body = case_head(
        "( Case study 01 ) &mdash; Table tennis &middot; Top project",
        'FREMONT TABLE TENNIS <em class="it">Academy.</em>',
        [("Client", "Fremont Table Tennis Academy"),
         ("Location", "Fremont &amp; San Ramon, CA"),
         ("Role", "UX &amp; UI redesign, build"),
         ("Live site", '<a href="https://fremonttabletennis.com" target="_blank" rel="noopener">fremonttabletennis.com &#8599;</a>')],
        img("fremont-home-desktop.jpg", "Fremont Table Tennis Academy homepage after the redesign",
            1365, 1238, style="max-height:760px")
    ) + f"""
<section class="sect">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="label" data-reveal>The brief</p>
        <h2 class="tm" data-reveal style="margin-top:1rem">WHICH CLASS IS <em class="it">right for me?</em></h2>
      </div>
      <div data-reveal>
        <p class="lead body">An award-winning academy with two locations, classes for ages 3 to adult, camps, weekly leagues and a pro shop. Every visitor arrives with the same question &mdash; so the redesign answers it first.</p>
      </div>
    </div>
    <div class="grid g-3" style="margin-top:clamp(2.6rem,6vw,4.6rem)">{featsh}</div>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal style="margin-bottom:1.6rem">Before and after</p>
    {compare("fremont-before.jpg", "The Fremont Table Tennis Academy site before the redesign", 1091, 682,
             "fremont-home-desktop.jpg", "The Fremont Table Tennis Academy homepage after the redesign", 1365, 1238,
             "the Fremont Table Tennis Academy site before and after the redesign")}
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <div class="grid g-2">
      <div data-reveal>
        <p class="label" style="margin-bottom:1rem">On a phone</p>
        <p class="body">Most parents book from the sideline or the car. The redesign was laid out phone-first: one column, the class finder at the top, and call, text and register buttons that stay in reach the whole way down.</p>
      </div>
      {phone("fremont-mobile.jpg", "The redesigned Fremont Table Tennis Academy site on a phone", 1080, 1931)}
    </div>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <div class="result-box" data-reveal>
      <div>
        <p class="label">Result</p>
        <h2 class="ts" style="margin-top:.8rem">The before and after are both on this page.</h2>
      </div>
      <div>
        <p class="body">A parent landing on the old site had to work out where to go. On the new one the classes, the camps and the phone number are the first things on the screen, and the academy finally reads the way it talks about itself.</p>
        <p class="body" style="margin-top:1rem">No sign-up figure is published here. The academy&rsquo;s numbers are theirs, not mine &mdash; so drag the slider above and judge this one on the work.</p>
      </div>
    </div>
  </div>
</section>
""" + next_project('TABLETENNIS<br>STORE.US', "table-tennis-usa.html")

    return page("fremont-table-tennis.html", "Fremont Table Tennis Academy — Case Study",
                "A full redesign for Fremont Table Tennis Academy, built around the question every "
                "visitor arrives with: which class is right for me?",
                "work.html", body, og="og-fremont.jpg")


# ====================================================== CASE: TTS (rebuild) ==
TTS_PROBLEMS = [
    "No conversion-focused homepage layout",
    "Weak product discovery for brand-loyal players",
    "Thin trust signals on the pages that needed them",
    "Unclear variant selection on equipment",
    "Shipping cost arriving as a surprise at checkout",
    "Broken breadcrumbs and SEO heading structure",
    "Product pages inconsistent from one to the next",
    "Video content sending visitors away from the store",
    "Email address exposed in markup, inviting spam",
]

def build_ttusa():
    rows = [("July", "16,349", "899", "466", "234", "1.43%"),
            ("August", "43,520", "1,076", "608", "296", "0.68%"),
            ("September", "18,037", "1,084", "719", "353", "1.95%"),
            ("5 Oct &ndash; 4 Nov", "15,516", "1,194", "1,113", "615", "3.96%")]
    trows = "".join(
        f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>"
        for a, b, c, d, e, f in rows)

    changes = [("01", "Homepage", "Rebuilt around brand discovery &mdash; Butterfly, GEWO, Stiga, Victas."),
               ("02", "Trust", "Trust signals added where shoppers hesitate."),
               ("03", "Product pages", "Reworked so variants are clear."),
               ("04", "Shipping", "Options rebuilt, plus a free-shipping bar at $75.")]
    ch = "".join(f'<div class="scol" data-reveal><p class="scol__n">{n}</p>'
                 f'<h3 class="scol__t">{t}</h3><p class="scol__d">{d}</p></div>'
                 for n, t, d in changes)
    probs = "".join(f"<li>{p}</li>" for p in TTS_PROBLEMS)

    body = case_head(
        "( Case study 02 ) &mdash; Table tennis &middot; Top project",
        'TABLETENNIS <em class="it">Store.us</em>',
        [("Client", "Table Tennis USA"), ("Platform", "Shopify"),
         ("Role", "UX design, theme customisation, CRO, SEO"),
         ("Live site", '<a href="https://tabletennisstore.us" target="_blank" rel="noopener">tabletennisstore.us &#8599;</a>')],
        img("tts-desk-c.jpg", "TableTennisStore.us homepage", 1364, 1098, style="max-height:650px")
    ) + f"""
<section class="sect">
  <div class="wrap">
    <p class="label" data-reveal>The result</p>
    <div class="bignum" data-reveal style="margin-top:1.4rem">
      <p class="bignum__v" data-count="163" data-pre="+" data-post="%">+163%</p>
      <p class="bignum__d">more completed orders a month &mdash; from 234 in July to 615 in the 30 days to 4 November 2026.</p>
    </div>

    <div class="dtable-wrap" data-reveal>
      <table class="dtable">
        <thead><tr><th>Period</th><th>Sessions</th><th>Carts</th><th>Checkouts</th><th>Orders</th><th>Conv. rate</th></tr></thead>
        <tbody>{trows}</tbody>
      </table>
    </div>
    <p class="foot-note" data-reveal>Source: Shopify Analytics, July&ndash;4 Nov 2026. August&rsquo;s session spike came mostly from Singapore. Shopify changed its session definition on 21 Sept 2026. Revenue is deliberately not published. <a href="proof.html" style="color:var(--royal)">See the proof log</a>.</p>
  </div>
</section>

<section class="sect sect--tight moon">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="label" data-reveal>What I found</p>
        <h2 class="tm" data-reveal style="margin-top:1rem">HALF OF CHECKOUTS WERE<br><em class="it">abandoned.</em></h2>
      </div>
      <div data-reveal>
        <p class="lead body">Only 5.5% of July sessions reached a cart, and about half of the checkouts that started were never finished. Weak product discovery, thin trust signals, unclear variants and shipping costs that appeared too late.</p>
        <details class="more">
          <summary>All nine problems found in the audit</summary>
          <ul>{probs}</ul>
        </details>
      </div>
    </div>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal style="margin-bottom:1.6rem">What changed</p>
    <div class="grid g-4">{ch}</div>
    <p class="body" data-reveal style="margin-top:2rem"><strong>93% of carts reached checkout</strong>, against 52% in July.</p>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <div class="grid g-2">
      {shot("tts-cart-unlocked.jpg","The side cart on tabletennisstore.us showing a full progress bar reading: you have unlocked free shipping","Live store &middot; free-shipping bar cleared at $75",1354,675)}
      {phone("tts-mobile.jpg","TableTennisStore.us on a phone")}
    </div>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal style="margin-bottom:1.6rem">Straight from the Shopify dashboard</p>
    <div class="astack">
      {ashot("tts-jul.jpg","Shopify Analytics for July 2026: 16,349 sessions, 899 added to cart, 466 reached checkout, 234 completed checkout, 1.43% conversion rate","Shopify Analytics &middot; 1&ndash;31 July 2026",934,492,"Where it started")}
      {ashot("tts-nov-funnel.jpg","Shopify Analytics for 5 October to 4 November 2026: 15,516 sessions, 1,194 added to cart, 1,113 reached checkout, 615 completed checkout, 3.96% conversion rate","Shopify Analytics &middot; 5 Oct &ndash; 4 Nov 2026",1163,280,"Where it is now")}
      {ashot("tts-sep-location.jpg","Shopify sessions by location for September 2026 against August: Singapore down 96% from 21,500 to 789","Sessions by location &middot; Sept vs Aug 2026",754,330,"Why August is discounted")}
    </div>
    <div class="askbox" data-reveal>
      <div>
        <p class="label">The part I cannot publish</p>
        <h3 class="ts" style="margin-top:.8rem">What did that do to <em class="it">revenue?</em></h3>
      </div>
      <div>
        <p class="body">The conversion rate moved from 1.43% to 3.96% on a store that was already taking orders every day. The sales figures behind that are the client&rsquo;s, not mine, so I am not putting them on a public page.</p>
        <p class="body" style="margin-top:1rem">If that is the number you actually care about, book a short call. I will open the real dashboard on screen and walk you through what the increase was worth.</p>
        {btn("Book a call to see the figures", mail("Table Tennis USA results — can we do a live call?"), "primary")}
      </div>
    </div>
  </div>
</section>
""" + next_project('ALL <em class="it">work.</em>', "work.html",
                   label="Back to", cta_label="See all five projects")

    return page("table-tennis-usa.html", "TableTennisStore.us — Case Study",
                "Shopify UX and conversion work for Table Tennis USA. Completed orders from 234 in "
                "July 2026 to 615 in the 30 days to 4 November, with the analytics attached.",
                "work.html", body, og="og-ttusa.jpg")


# =============================================== PROJECT PAGES (3 + extras) ==
def build_gewo():
    body = case_head(
        "( Project 03 ) &mdash; Table tennis &middot; Manufacturer store",
        'GEWO <em class="it">USA.</em>',
        [("Client", "GEWO USA"), ("Sector", "Manufacturer-owned ecommerce"),
         ("Role", "Website design"),
         ("Live site", '<a href="https://www.gewousa.com" target="_blank" rel="noopener">gewousa.com &#8599;</a>')],
        img("gewo-home.jpg", "GEWO USA homepage", 1365, 1180, style="max-height:700px")
    ) + f"""
<section class="sect">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="label" data-reveal>The brief</p>
        <h2 class="tm" data-reveal style="margin-top:1rem">BE THE BRAND AND <em class="it">the shop.</em></h2>
      </div>
      <div data-reveal>
        <p class="lead body">The US store of a table tennis equipment manufacturer. The catalogue runs from shakehand and penhold blades through four categories of rubber, indoor and outdoor tables, balls, apparel, footwear and maintenance items down to edge tape and glue.</p>
        <p class="body" style="margin-top:1.2rem">Those are not one kind of purchase. Apparel is browsed, rubber is specified, a table is researched, edge tape is re-ordered. The store has to let all four happen without the brand story blocking someone who came to buy glue.</p>
      </div>
    </div>

    <div class="grid g-3" style="margin-top:clamp(2.6rem,6vw,4.6rem)">
      <div class="scol" data-reveal><p class="scol__n">01</p><h3 class="scol__t">1.2s largest paint</h3><p class="scol__d">Largest Contentful Paint at the 75th percentile. Google calls anything under 2.5s good.</p></div>
      <div class="scol" data-reveal><p class="scol__n">02</p><h3 class="scol__t">56ms interaction</h3><p class="scol__d">Interaction to Next Paint, against a 200ms threshold.</p></div>
      <div class="scol" data-reveal><p class="scol__n">03</p><h3 class="scol__t">Zero layout shift</h3><p class="scol__d">Nothing on the page moves while it loads. Not low &mdash; zero.</p></div>
    </div>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <div class="grid g-2">
      {shot("gewo-pdp.jpg","A GEWO USA product page","Product page &middot; price, variant, stock and both buy paths above the fold",1366,1180)}
      {shot("gewo-pdp-bands.jpg","The who-it-is-for and performance bands below a GEWO USA product","Below every product &mdash; who it is for, a performance read, and the sponsored players",1366,1250)}
    </div>
    <div style="margin-top:clamp(1.6rem,4vw,3rem)">
      {shot("gewo-vitals.jpg","Shopify Core Web Vitals for GEWO USA: LCP 1201ms, INP 56ms, CLS 0, all rated good","Core Web Vitals &middot; 30 days, as Shopify recorded them",688,76)}
    </div>
    <p class="foot-note" data-reveal style="margin-top:1.6rem">The speed figures above are measured. There is no conversion or revenue data I can publish for this store, so none appears here.</p>
  </div>
</section>
""" + next_project('OCTAGON.', "octagon.html")
    return page("gewo-usa.html", "GEWO USA — Project",
                "Website design for GEWO USA, the US store of a table tennis equipment "
                "manufacturer. 1.2s largest contentful paint and zero layout shift.",
                "work.html", body, og="og-gewo.jpg")


def build_short(fname, num, label_bits, title_html, meta, hero, nxt, og, title, desc,
                head_html="", paras=()):
    """A short project page: label, title, meta, hero, a two-column description
    and the live-site button. Deliberately claims no results — neither project
    has published figures."""
    live = [v for k, v in meta if k == "Live site"][0]
    import re as _re
    url = _re.search(r'href="([^"]+)"', live).group(1)
    ps = "".join(f'<p class="body" style="margin-top:1.1rem">{x}</p>' for x in paras[1:])
    lead = f'<p class="lead body">{paras[0]}</p>' if paras else ""
    body = case_head(f"( Project {num} ) &mdash; {label_bits}", title_html, meta, hero) + f"""
<section class="sect">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="label" data-reveal>The project</p>
        <h2 class="tm" data-reveal style="margin-top:1rem">{head_html}</h2>
      </div>
      <div data-reveal>
        {lead}{ps}
        <div style="margin-top:2rem">{btn("Visit the live site", url, "primary", ' target="_blank" rel="noopener"')}</div>
      </div>
    </div>
  </div>
</section>
""" + nxt
    return page(fname, title, desc, "work.html", body, og=og)


def build_octagon():
    return build_short(
        "octagon.html", "04", "Football &middot; Sports marketing",
        'OCTAGON.', [("Client", "Octagon"), ("Sector", "Football &middot; sports marketing"),
                     ("Role", "Website design"),
                     ("Live site", '<a href="https://www.octagon.com" target="_blank" rel="noopener">octagon.com &#8599;</a>')],
        img("octagon-home.jpg", "Octagon website", 1440, 900, style="max-height:700px"),
        next_project('STARTING <em class="it">Eleven.</em>', "starting-eleven.html"),
        "octagon-home.jpg", "Octagon — Project",
        "Website design for Octagon, a sports and entertainment marketing business working "
        "across brands, talent and campaigns.",
        head_html='THREE AUDIENCES, <em class="it">one site.</em>',
        paras=(
            "Octagon works in sports and entertainment marketing, so the site has to serve three "
            "very different visitors at once: brands looking for a partner, athletes looking for "
            "representation, and people looking for a job.",
            "The design keeps those paths apart and obvious from the first screen, and lets the "
            "campaign work carry the visual weight rather than the copy. Everything else gets out "
            "of the way of the thing a visitor actually came to look at.",
        ))


def build_starting_eleven():
    return build_short(
        "starting-eleven.html", "05", "Football &middot; Retail store",
        'STARTING <em class="it">Eleven.</em>',
        [("Client", "Starting Eleven"), ("Sector", "Football retail &middot; Lexington, KY"),
         ("Role", "Website design &middot; Shopify"),
         ("Live site", '<a href="https://startingxi.com" target="_blank" rel="noopener">startingxi.com &#8599;</a>')],
        img("starting-eleven-home.jpg", "Starting Eleven online store", 1440, 640, style="max-height:700px"),
        next_project('ALL <em class="it">work.</em>', "work.html",
                     label="Back to", cta_label="See all five projects"),
        "starting-eleven-home.jpg", "Starting Eleven — Project",
        "Shopify website design for Starting Eleven, a football retail store in Lexington, "
        "Kentucky, selling boots, fanwear, goalkeeper kit and a monthly mystery kit.",
        head_html='A SHOP AND A <em class="it">subscription.</em>',
        paras=(
            "A football store in Lexington, Kentucky, selling boots, fanwear, balls, goalkeeper "
            "kit and team orders &mdash; with a monthly mystery kit running alongside the usual "
            "catalogue.",
            "Those are two different shoppers. One is replacing a pair of boots and knows exactly "
            "what they want; the other is buying a surprise every month. The storefront leads with "
            "the subscription, because that is the harder sell, and keeps the full catalogue one "
            "tap away for everyone else.",
        ))


# ================================================================== PROOF ====
def build_proof():
    rows = [("1&ndash;31 Jul 2026", "16,349", "899", "466", "234", "1.43%"),
            ("1&ndash;31 Aug 2026", "43,520", "1,076", "608", "296", "0.68%"),
            ("1&ndash;30 Sep 2026", "18,037", "1,084", "719", "353", "1.95%"),
            ("5 Oct&ndash;4 Nov 2026", "15,516", "1,194", "1,113", "615", "3.96%")]
    trows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>"
                    for a, b, c, d, e, f in rows)
    body = f"""
<section class="sect sect--tight">
  <div class="wrap">
    <p class="label" data-reveal>( Proof log ) &mdash; Where every number comes from</p>
    <h1 class="xl" data-reveal style="margin-top:1.4rem;font-size:clamp(2.6rem,7.4vw,6.5rem)">THE <em class="it">receipts.</em></h1>
    <p class="lead body" data-reveal style="margin-top:1.8rem;max-width:52ch">Every figure on this site traces to a dated screenshot of the client&rsquo;s own Shopify Analytics. Nothing is estimated, rounded up or recalled from memory.</p>
    {meta_row([("Store", "Table Tennis USA"), ("Source", "Shopify Analytics"),
               ("Currency", "USD, human sessions"), ("Captured", "4 November 2026")])}
  </div>
</section>

<section class="sect" style="padding-top:0">
  <div class="wrap">
    <div class="dtable-wrap" data-reveal>
      <table class="dtable">
        <thead><tr><th>Period</th><th>Sessions</th><th>Carts</th><th>Checkouts</th><th>Orders</th><th>Conv. rate</th></tr></thead>
        <tbody>{trows}</tbody>
      </table>
    </div>
    <div class="grid g-2" style="margin-top:clamp(2rem,5vw,3.4rem)">
      {shot("tts-nov-funnel.jpg","Shopify Analytics for 5 October to 4 November 2026","Conversion rate breakdown &middot; 5 Oct&ndash;4 Nov 2026 vs 4 Sept&ndash;4 Oct 2026",1163,280)}
      {shot("tts-aug-funnel.jpg","Shopify Analytics for August 2026","Conversion rate breakdown &middot; 1&ndash;31 Aug 2026 vs 1&ndash;31 Jul 2026",1163,262)}
      {shot("tts-sep-funnel.jpg","Shopify Analytics for September 2026","Conversion rate breakdown &middot; 1&ndash;30 Sept 2026 vs 2&ndash;31 Aug 2026",1163,262)}
      {shot("tts-jul.jpg","Shopify Analytics for July 2026","Conversion rate breakdown &middot; 1&ndash;31 July 2026",934,492)}
    </div>
  </div>
</section>

<section class="sect sect--tight moon">
  <div class="wrap">
    <p class="label" data-reveal>Known distortions</p>
    <h2 class="tm" data-reveal style="margin-top:1rem;margin-bottom:2rem">TWO REASONS THE RATE<br><em class="it">lies.</em></h2>
    <div class="grid g-2">
      <div class="scol" data-reveal>
        <h3 class="scol__t">August&rsquo;s traffic was not real</h3>
        <p class="scol__d">43,520 sessions against July&rsquo;s 16,349, almost all of it Singapore going from a handful to 21,500. By September it was back to 789. Roughly 25,000 sessions that were never going to buy pushed August down to 0.68%.</p>
      </div>
      <div class="scol" data-reveal>
        <h3 class="scol__t">Shopify changed how it counts sessions</h3>
        <p class="scol__d">A notice on the analytics page says sessions and related metrics may shift from 21 September 2026. Any rate spanning that date is not like-for-like. Order counts are unaffected, which is why they are the headline.</p>
      </div>
    </div>
    <div style="margin-top:clamp(2rem,4vw,3rem);max-width:620px">
      {shot("tts-sep-location.jpg","Shopify sessions by location, September against August 2026","Sessions by location &middot; the pale bar behind each is August",754,330)}
    </div>
  </div>
</section>

<section class="sect sect--tight">
  <div class="wrap">
    <div class="split">
      <div><p class="label" data-reveal>Deliberately absent</p>
        <h2 class="tm" data-reveal style="margin-top:1rem">NO REVENUE. NO CUSTOMER <em class="it">data.</em></h2></div>
      <div data-reveal>
        <p class="body">The store&rsquo;s sales figures exist and I have seen them. They are the client&rsquo;s to publish, not mine, so no dollar amount appears anywhere on this site. Nor does anything that could identify a customer.</p>
        <p class="body" style="margin-top:1.2rem"><strong>Nothing here is a projection of what your store would do.</strong> It is a record of what one store did, with the parts that are not flattering left in.</p>
      </div>
    </div>
  </div>
</section>

{cta()}
"""
    return page("proof.html", "Proof log — Akintayo",
                "Where every figure on akintayoakingbehin.com comes from: dated Shopify Analytics "
                "screenshots, with the two known distortions stated plainly.",
                "work.html", body, og="og-ttusa.jpg")


def build_404():
    body = f"""
<section class="sect" style="min-height:52vh">
  <div class="wrap">
    <p class="label" data-reveal>( 404 ) &mdash; Off the table</p>
    <h1 class="xl" data-reveal style="margin-top:1.4rem">PAGE NOT<br><em class="it">found.</em></h1>
    <p class="lead body" data-reveal style="margin-top:1.8rem;max-width:44ch">That link has gone. The work, the sports and the services are all still here.</p>
    <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:2.4rem" data-reveal>
      {btn("See the work", "work.html", "primary")}
      {btn("Go home", "index.html", "outline")}
    </div>
  </div>
</section>
"""
    return page("404.html", "Page not found — Akintayo",
                "That page could not be found.", "", body)


# ================================================================== EXTRAS ==
PUBLIC = ["index.html", "work.html", "sports.html", "services.html", "about.html",
          "contact.html", "fremont-table-tennis.html", "table-tennis-usa.html",
          "gewo-usa.html", "octagon.html", "starting-eleven.html", "proof.html"]

def build_extras():
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /paul-david.html\n\nSitemap: {DOMAIN}/sitemap.xml\n")

    urls = ""
    for p in PUBLIC:
        pr = "1.0" if p == "index.html" else ("0.9" if p in ("work.html", "sports.html", "services.html") else "0.8")
        urls += f"  <url><loc>{DOMAIN}/{p}</loc><priority>{pr}</priority></url>\n"
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')

    open(os.path.join(OUT, ".nojekyll"), "w").write("")

    # paul-david.html stays on disk but leaves the index and every link list.
    pd = os.path.join(OUT, "paul-david.html")
    if os.path.exists(pd):
        s = open(pd, encoding="utf-8").read()
        if 'name="robots"' not in s:
            s = s.replace("</title>", '</title>\n<meta name="robots" content="noindex, nofollow">', 1)
            open(pd, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    built = [build_home(), build_work(), build_sports(), build_services(), build_about(),
             build_contact(), build_fremont(), build_ttusa(), build_gewo(), build_octagon(),
             build_starting_eleven(), build_proof(), build_404()]
    build_extras()
    print("Built " + str(len(built)) + ": " + ", ".join(built))
