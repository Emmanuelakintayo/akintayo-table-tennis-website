#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static builder for the AKINTAYO site. Emits plain HTML files — no runtime
dependency, no framework. Run: python3 build.py"""

import os, re, html

OUT = os.path.dirname(os.path.abspath(__file__))

EMAIL  = "akintayo@akintayoakingbehin.com"
DOMAIN = "https://akintayoakingbehin.com"
BRAND  = "AKINTAYO"

def mail(subject="Website project enquiry", body=None):
    q = "?subject=" + subject.replace(" ", "%20")
    if body:
        q += "&body=" + body.replace(" ", "%20").replace("\n", "%0D%0A")
    return "mailto:" + EMAIL + q

ARROW = ('<svg class="btn__arrow" viewBox="0 0 10 10" fill="none" aria-hidden="true">'
         '<path d="M1 9L9 1M9 1H2.5M9 1v6.5" stroke="currentColor" stroke-width="1.4" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')

BIGARROW = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            '<path d="M4 20L20 4M20 4H8M20 4v12" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')

NAV = [("Work", "work.html"), ("Services", "services.html"),
       ("About", "about.html"), ("Contact", "contact.html")]

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Archivo:wght@400;500;600;700;800&"
         "family=Instrument+Serif:ital@1&"
         "family=Martian+Mono:wght@400;500&display=swap")


# --------------------------------------------------------------------- chrome
def header(current):
    links = "".join(
        '<a class="nav__link" href="{h}"{c}>{t}</a>'.format(
            h=h, t=t, c=' aria-current="page"' if h == current else "")
        for t, h in NAV)
    menu = "".join(
        '<a class="menu__link" href="{h}"><span>{n:02d}</span>{t}</a>'.format(
            h=h, t=t, n=i + 1)
        for i, (t, h) in enumerate(NAV))
    home_cur = ' aria-current="page"' if current == "index.html" else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="grain" aria-hidden="true"></div>
<div class="curtain" aria-hidden="true"></div>
<div class="progress" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"><span class="cursor__label"></span></div>
<div class="cursor-dot" aria-hidden="true"></div>
<div class="peek" aria-hidden="true"></div>

<header class="nav">
  <div class="nav__inner">
    <a class="logo" href="index.html" aria-label="AKINTAYO — home"{home_cur}><span class="logo__ball"></span>AKINTAYO</a>
    <nav class="nav__links" aria-label="Primary">{links}</nav>
    <a class="btn nav__cta" href="{mail()}" data-magnet="0.2"><span>Start a project</span>{ARROW}</a>
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<div class="menu" id="mobile-menu" aria-hidden="true">
  <nav class="menu__list" aria-label="Mobile">{menu}</nav>
  <div class="menu__foot">
    <p class="mono">Email only — no forms, no calls to book.</p>
    <a class="cta__mail" style="font-size:clamp(1.1rem,5vw,1.7rem)" href="{mail()}">{EMAIL}</a>
  </div>
</div>"""


def cta_block(title, sub, sub2=None):
    extra = f'<p class="mono" style="margin-top:1.6rem">{sub2}</p>' if sub2 else ""
    return f"""<section class="cta section">
  <div class="aura" aria-hidden="true"></div>
  <div class="wrap" style="position:relative;z-index:2">
    <p class="mono eyebrow" data-reveal="fade">Contact</p>
    <h2 class="display h2" data-reveal style="margin-top:1.4rem;max-width:18ch">{title}</h2>
    <p class="lead lead--wide" data-reveal style="margin-top:1.4rem">{sub}</p>
    <div style="margin-top:clamp(2.2rem,5vw,3.6rem)" data-reveal>
      <a class="cta__mail" href="{mail()}">{EMAIL}</a>
    </div>
    {extra}
  </div>
</section>"""


def footer():
    cols = ""
    for title, items in [
        ("Site", NAV),
        ("Work", [("Table Tennis USA", "table-tennis-usa.html"),
                  ("GEWO USA", "gewo-usa.html"),
                  ("Paul David", "paul-david.html")]),
    ]:
        li = "".join(f'<a class="foot__link" href="{h}">{t}</a>' for t, h in items)
        cols += f'<nav class="foot__col" aria-label="{title}"><p class="mono">{title}</p>{li}</nav>'
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div class="foot__brand">
        <a class="logo" href="index.html"><span class="logo__ball"></span>AKINTAYO</a>
        <p style="color:var(--fg-2);max-width:30ch">Website design, ecommerce and conversion work for the table tennis industry.</p>
        <p class="mono">Akingbehin Akintayo — working with clients internationally from Nigeria</p>
      </div>
      {cols}
      <div class="foot__mail">
        <p class="mono">Email</p>
        <a class="foot__link" href="{mail()}" style="word-break:break-word">{EMAIL}</a>
        <p class="mono" style="margin-top:.4rem">Email is the only contact method.</p>
      </div>
    </div>
    <div class="foot__wordmark" aria-hidden="true">AKINTAYO</div>
    <div class="foot__bar">
      <p class="mono">&copy; <span data-year>2026</span> Akingbehin Akintayo</p>
      <p class="mono">akintayoakingbehin.com</p>
    </div>
  </div>
</footer>"""


def page(fname, title, desc, current, body, og_img="og-default.jpg"):
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}/{fname}">
<meta name="theme-color" content="#08090b">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AKINTAYO">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}/{fname}">
<meta property="og:image" content="{DOMAIN}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="site.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
</head>
<body>
{header(current)}
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


# ------------------------------------------------------------------ fragments
def lines(*rows, cls="display hero__title", onload=False):
    inner = "".join(f'<span class="line"><span>{r}</span></span>' for r in rows)
    ol = ' data-onload' if onload else ''
    return f'<h1 class="{cls} lines"{ol}>{inner}</h1>'

def h2lines(*rows, cls="display h2"):
    inner = "".join(f'<span class="line"><span>{r}</span></span>' for r in rows)
    return f'<h2 class="{cls} lines">{inner}</h2>'

def shead(no, kicker, title, aside=""):
    a = f'<div class="shead__aside" data-reveal><p>{aside}</p></div>' if aside else ""
    return f"""<div class="shead">
  <div class="shead__no" data-reveal="fade"><p class="mono mono--accent">{no}</p><p class="mono">{kicker}</p></div>
  <div class="shead__title">{h2lines(*title)}</div>
  {a}
</div>"""


def portrait(src, alt, tag=None, cls="", eager=False):
    """The supplied photograph, unmodified. All blue/green treatment sits on
    the frame around it — never a filter or overlay on the image itself."""
    t = (f'<span class="portrait__tag"><i></i>{tag}</span>') if tag else ""
    # Above the fold the photograph must not lazy-load, or the page opens on a hole.
    ld = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    rv = '' if eager else ' data-reveal'
    return f"""<div class="portrait-wrap{(' ' + cls) if cls else ''}"{rv}>
  <figure class="portrait">
    <img src="{src}" alt="{alt}" width="1200" height="1800" {ld}>
    {t}
  </figure>
</div>"""


def shot(src, cap, w, h, url=None, cls=""):
    """A real screenshot, presented as evidence. The brand treatment is on the
    frame only; the image itself is never filtered, tinted or overlaid, so what
    a visitor sees is what the client's analytics or storefront actually showed.
    A chrome bar is added only for captures of live websites."""
    bar = ('<div class="shot__bar"><span class="shot__dots"><i></i><i></i><i></i></span>'
           f'<span class="shot__url">{url}</span></div>') if url else ""
    c = (" " + cls) if cls else ""
    return f"""<figure class="shot{c}" data-reveal>
  <div class="shot__frame">{bar}<img src="{src}" alt="{cap}" width="{w}" height="{h}" loading="lazy" decoding="async"></div>
  <figcaption class="shot__cap">{cap}</figcaption>
</figure>"""

def shotgrid(*shots, cls=""):
    c = (" " + cls) if cls else ""
    return f'<div class="shotgrid{c}" data-stagger>{"".join(shots)}</div>'

def receipts(*shots):
    return f'<div class="receipts" data-stagger>{"".join(shots)}</div>'

def funnel(rows):
    """rows = [(stage, value, note, pct_of_sessions, is_final), ...]"""
    out = ""
    for i, (k, v, note, pct, end) in enumerate(rows):
        cls = " funnel__row--end" if end else ""
        out += (f'<div class="funnel__row{cls}"><p class="funnel__k">{k}</p>'
                f'<div class="funnel__track"><span class="funnel__fill" '
                f'style="--w:{pct}%;--d:{i * .12:.2f}s"></span></div>'
                f'<p class="funnel__v">{v}<small>{note}</small></p></div>')
    return f'<div class="funnel" data-reveal>{out}</div>'


PROJECTS = [
    dict(no="01", name="Table Tennis USA", href="table-tennis-usa.html",
         tags=["Ecommerce", "Shopify", "Redesign &amp; CRO"],
         res="0.68% &rarr; 2.24% conversion rate",
         stat="2.24%", sub="Conversion rate, latest 30 days — from 0.68% at the August low", live="tabletennisstore.us"),
    dict(no="02", name="GEWO USA", href="gewo-usa.html",
         tags=["Ecommerce", "Shopify", "Manufacturer store"],
         res="1.2s largest paint, zero layout shift",
         stat="1201ms", sub="Largest Contentful Paint, 75th percentile — rated Good", live="gewousa.com"),
    dict(no="03", name="Paul David", href="paul-david.html",
         tags=["Coaching practice", "Services &amp; booking"],
         res="Four services, one booking path",
         stat="4", sub="Services, each with its own one-click booking email", live="pauldavidcoach.com"),
]

def worklist(show_live=False):
    rows = ""
    for p in PROJECTS:
        tags = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
        res = p["res"] if not show_live else f'{p["res"]}'
        rows += f"""<a class="workrow" href="{p['href']}" data-cursor="View case"
   data-peek-stat="{p['stat']}" data-peek-sub="{p['sub']}" data-reveal>
  <div class="workrow__in">
    <p class="workrow__no mono mono--accent">{p['no']}</p>
    <div class="workrow__name"><h3 class="workrow__title">{p['name']}</h3></div>
    <div class="workrow__tags">{tags}</div>
    <p class="workrow__res mono mono--fg">{res}</p>
    <span class="workrow__go">{BIGARROW}</span>
  </div>
</a>"""
    return f'<div class="worklist" data-stagger>{rows}</div>'


def meta_rail(items):
    dl = "".join(f'<div class="meta__item"><dt class="mono">{k}</dt><dd>{v}</dd></div>' for k, v in items)
    return f'<dl class="meta" data-reveal="fade">{dl}</dl>'

def beat(no, title, paras):
    ps = "".join(f"<p>{p}</p>" for p in paras)
    return f"""<div class="beat" data-reveal>
  <h3 class="beat__h"><i>{no}</i><span>{title}</span></h3>
  <div class="prose">{ps}</div>
</div>"""

ARC = """<div class="arc" aria-hidden="true">
  <svg viewBox="0 0 820 470" fill="none" preserveAspectRatio="xMidYMid meet">
    <path d="M-10 462 C 150 110, 300 30, 418 206 S 655 438, 806 126"/>
    <circle cx="806" cy="126" r="8"/>
  </svg>
</div>"""


# ===================================================================== HOME ==
def build_home():
    services = [
        ("01", "Website design from scratch",
         "A complete site for a business that has never had one, or one that has outgrown what it has. Structure, design, build, launch."),
        ("02", "Ecommerce website design",
         "Catalogue architecture, collection pages, product pages, filtering, cart and checkout — built for people buying equipment."),
        ("03", "Website redesign",
         "Rebuilding an existing store without losing what already works: rankings, product data, URLs and the habits of returning customers."),
        ("04", "Conversion-focused optimisation",
         "Working on a site that already exists, on the path from arrival to completed order. Fewer dead ends, fewer reasons to leave."),
    ]
    cards = "".join(f"""<article class="card card--quarter" data-reveal>
  <p class="card__no mono">{n}</p>
  <h3 class="h4">{t}</h3>
  <p class="card__body">{d}</p>
</article>""" for n, t, d in services)

    segments = [
        ("Equipment brands", "Manufacturers and brands selling direct."),
        ("Online &amp; retail stores", "Multi-brand shops with deep catalogues."),
        ("Distributors", "Wholesale and regional supply businesses."),
        ("Coaches &amp; academies", "Lessons, camps and clinics — no cart required."),
        ("Clubs &amp; organisations", "Memberships, leagues, facilities and fixtures."),
        ("Tournaments &amp; events", "Entries, schedules, results and sponsors."),
    ]
    segs = "".join(f"""<div class="seg" data-reveal>
  <span class="seg__i">{i+1:02d}</span>
  <div><h3 class="seg__t">{t}</h3><p class="seg__d">{d}</p></div>
</div>""" for i, (t, d) in enumerate(segments))

    steps = [
        ("01", "Learn the catalogue", "What you sell and how it is organised: brands, categories, specifications, price bands."),
        ("02", "Map the buying path", "Landing page to completed order, written out, with the stalling points marked."),
        ("03", "Design and build", "A working site, not a concept file for someone else to interpret."),
        ("04", "Measure and refine", "Changes made on what the numbers show rather than what looks better."),
    ]
    steplist = "".join(f"""<div class="step" data-reveal>
  <p class="step__no mono mono--accent">{n}</p>
  <h3 class="step__t">{t}</h3>
  <p class="step__d">{d}</p>
</div>""" for n, t, d in steps)

    marquee_items = ["Ecommerce design", "Website redesign", "Conversion optimisation",
                     "Shopify builds", "Product page design", "Catalogue architecture",
                     "Checkout flow", "Coaching &amp; club sites"]
    mset = "".join(f'<span class="marquee__item"><i></i>{m}</span>' for m in marquee_items)

    body = f"""
<section class="hero">
  <div class="aura" aria-hidden="true"></div>
  {ARC}
  <div class="wrap hero__inner">
    <div class="hero__top">
      <p class="mono eyebrow" data-reveal="fade" data-onload>Website design &mdash; table tennis industry</p>
      <span class="status" data-reveal="fade" data-onload><span class="status__dot"></span>Available for projects</span>
    </div>
    {lines('Websites for', 'the <span class="accent">table tennis</span>', 'industry.', onload=True)}
    <div class="hero__body">
      <div class="hero__lead">
        <p class="lead lead--wide" data-reveal data-onload>I design and build ecommerce stores, new sites, redesigns and conversion
        work for table tennis brands, retailers, distributors, clubs and coaches &mdash; around how players
        actually choose a blade, a rubber and a sponge thickness.</p>
      </div>
      <div class="hero__actions" data-reveal data-onload>
        <a class="btn btn--ghost" href="work.html" data-magnet="0.22"><span>See the work</span>{ARROW}</a>
        <a class="btn btn--primary" href="{mail()}" data-magnet="0.22"><span>Start a project</span>{ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="proof">
  <div class="wrap">
    <a class="proof__link" href="table-tennis-usa.html" data-cursor="Case study">
      <div class="proof__k">
        <p class="mono mono--accent">Flagship project</p>
        <p class="mono">Table Tennis Store &mdash; conversion rate, August to October 2026</p>
      </div>
      <div class="proof__figs">
        <span class="fig">0.68%</span><span class="fig fig__sep">&rarr;</span>
        <span class="fig">1.95%</span><span class="fig fig__sep">&rarr;</span>
        <span class="fig fig--now">2.24%</span>
      </div>
      <p class="proof__go mono mono--fg">Screenshots attached<br>&mdash; read it &rarr;</p>
    </a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("01", "Positioning",
           ["A generalist spends your first", "month learning this market.", "I already know it."],
           "A specialist catalogue sold to specialist buyers.")}
    <div class="split">
      <div class="split__l prose" data-reveal>
        <p>Someone buying rubber is choosing between inverted, short pips, long pips and anti-spin, then sponge
        thickness, then ITTF approval. A coach is not selling a product at all, but a time slot.</p>
        <p><strong>That detail is the whole job.</strong> It decides how a catalogue is structured, which filters
        matter, and where a buyer hesitates.</p>
      </div>
      <div class="split__r" data-reveal data-delay="120">
        <p class="mono" style="margin-bottom:1.2rem">What that changes in practice</p>
        <ul class="checklist">
          <li>Category structure that follows how players shop, not by brand alone.</li>
          <li>Product pages built around the specifications buyers compare.</li>
          <li>Filtering that survives pips, sponge thickness and speed ratings without dead ends.</li>
          <li>Booking paths for coaches and clubs, where there is no cart and never should be.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee__track">
    <div class="marquee__set">{mset}</div>
    <div class="marquee__set">{mset}</div>
  </div>
</div>

<section class="section">
  <div class="wrap">
    {shead("02", "Selected work",
           ["Three projects.", "One industry."],
           "Two ecommerce stores and one coaching practice. I would rather show depth in a single sport than breadth across ten unrelated ones.")}
    {worklist()}
    <div style="margin-top:clamp(2rem,4vw,3rem)" data-reveal>
      <a class="btn btn--ghost" href="work.html" data-magnet="0.22"><span>All work</span>{ARROW}</a>
    </div>
  </div>
</section>

<section class="section" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="court" aria-hidden="true"></div>
  <div class="wrap" style="position:relative;z-index:2">
    {shead("03", "Capabilities",
           ["What I build."],
           "Four services. Most projects are one of them; some are two running together.")}
    <div class="deck" data-stagger>{cards}</div>
    <div style="margin-top:clamp(2rem,4vw,3rem)" data-reveal>
      <a class="btn btn--ghost" href="services.html" data-magnet="0.22"><span>Services in detail</span>{ARROW}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("04", "Clients",
           ["Who I work with."],
           "Everyone here sells something different, and the site has to reflect that. A distributor and a coach do not need the same website.")}
    <div class="segs" data-stagger>{segs}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("05", "Process",
           ["How a project", "actually runs."],
           "Four stages, in order. Nothing is designed before the catalogue and the buying path are understood.")}
    <div class="steps" data-stagger>{steplist}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("06", "The person",
           ["Built by a real person."],
           "No account managers, no handoffs, and nobody the work quietly gets passed to after the pitch.")}
    <div class="person">
      <div class="person__media">
        {portrait("akintayo.jpg",
                  "Akingbehin Akintayo, the designer and developer behind AKINTAYO, in a studio portrait",
                  tag="Available for projects")}
      </div>
      <div class="person__body">
        <div class="prose" data-reveal data-delay="120">
          <p>I am Akingbehin Akintayo. I read your email, go through your store, design the pages and write the
          code that ships them. <strong>Nobody else is on the thread.</strong></p>
          <p>On Table Tennis Store, the person who mapped the buying path was the same person who rebuilt it.</p>
        </div>
        <div class="creds" data-reveal data-delay="180">
          <span class="pill">Osun State, Nigeria &mdash; working worldwide</span>
          <span class="pill">Shopify &amp; Liquid</span>
          <span class="pill">Ecommerce UX &amp; CRO</span>
        </div>
        <div style="margin-top:clamp(1.6rem,3vw,2.2rem)" data-reveal data-delay="220">
          <a class="btn btn--ghost" href="about.html" data-magnet="0.22"><span>More about me</span>{ARROW}</a>
        </div>
      </div>
    </div>
  </div>
</section>

{cta_block("Tell me about the site and the problem.",
           "Send an email with your store or site, what is going wrong, and what you want it to do. I will tell you honestly whether I am the right person for it.",
           "Email only &mdash; no forms, no calls to book, no chat widget.")}
"""
    return page("index.html", "AKINTAYO — Website Design for Table Tennis",
                "Website design, ecommerce and conversion work for the table tennis industry — "
                "brands, stores, distributors, clubs and coaches. Case study: Table Tennis USA, "
                "conversion rate 0.68% to 2.24%, with the analytics screenshots attached.", "index.html", body)


# ===================================================================== WORK ==
def build_work():
    body = f"""
<section class="hero" style="padding-bottom:clamp(1.6rem,3vw,2.6rem)">
  <div class="aura" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <p class="mono eyebrow" data-reveal="fade" data-onload>Work &mdash; 2 stores, 1 coaching practice</p>
    <div style="margin-top:clamp(1.4rem,3vw,2.4rem)">
      {lines('Three projects.', 'One industry.', onload=True)}
    </div>
    <div class="hero__body">
      <div class="hero__lead">
        <p class="lead lead--wide" data-reveal data-onload>Every project below is a table tennis business. That is deliberate.
        A portfolio of ten unrelated logos proves you can make things look good; a portfolio in one sport
        proves you understand a market.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    {worklist(show_live=True)}
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">A note on proof</p>
        <h2 class="bigquote" style="margin-top:1.2rem">Only one of these projects has published numbers. I say so on the other two.</h2>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>Table Tennis Store has four consecutive periods of analytics, screenshots attached, including the two
        months it was falling. GEWO USA has speed data but no conversion data. Paul David has neither, and says so.</p>
        <p><strong>A portfolio is worth more when you can trust the parts that are not flattering.</strong></p>
      </div>
    </div>
  </div>
</section>

{cta_block("Your project could be the fourth.",
           "Brands, stores, distributors, clubs, coaches — if it is table tennis and it needs a website, describe it in an email.")}
"""
    return page("work.html", "Work — AKINTAYO",
                "Table tennis website projects by AKINTAYO: Table Tennis USA, GEWO USA and coach Paul David.",
                "work.html", body)


# ====================================================== CASE: TABLE TENNIS USA
def livebtn(url, label):
    return f"""<div class="live" data-reveal>
  <a class="btn btn--ghost" href="{url}" target="_blank" rel="noopener" data-magnet="0.22">
    <span>{label}</span>{ARROW}</a>
  <p class="mono">The work is live &mdash; judge it there</p>
</div>"""


def flow(steps):
    out = ""
    for i, (t, d) in enumerate(steps):
        out += f"""<div class="fstep" data-reveal>
  <p class="fstep__n">{i+1:02d}</p>
  <h3 class="fstep__t">{t}</h3>
  <p class="fstep__d">{d}</p>
</div>"""
    return f'<div class="flow" data-stagger>{out}</div>'


def build_ttusa():
    problems = [
        "No conversion-focused homepage layout",
        "Weak product discovery for brand-loyal players",
        "Thin trust signals on the pages that needed them",
        "Unclear variant selection on equipment",
        "Shipping cost arriving as a surprise at checkout",
        "Broken breadcrumbs and SEO heading structure",
    ]
    probs = "".join(
        f'<div class="prob" data-reveal="fade"><i>{i+1:02d}</i><span>{t}</span></div>'
        for i, t in enumerate(problems))

    role = ["UX design improvements", "Shopify theme customisation", "Homepage restructuring",
            "Product page optimisation", "Conversion rate optimisation", "SEO structural fixes",
            "Custom feature implementation"]
    rolelist = "".join(f"<li>{r}</li>" for r in role)

    sol = [
        ("Homepage structure",
         "Rebuilt to move a visitor through the store instead of leaving them to work it out.",
         ["Hero section", "Trust bar", "Brand discovery", "Featured products", "New arrivals"]),
        ("Trust signals",
         "Placed early, where hesitation happens, rather than buried in a policy page.",
         ["Authentic global table tennis brands", "Professional quality equipment",
          "Secure checkout", "Trusted by players"]),
        ("Product page improvements",
         "Reworked around the moment of decision: compare the specification, then commit.",
         ["Clearer layout and spacing", "Improved product image presentation",
          "Trust messaging under the product price", "Improved quantity selector and purchase area"]),
    ]
    solcards = ""
    for i, (t, d, items) in enumerate(sol):
        li = "".join(f"<li>{x}</li>" for x in items)
        solcards += f"""<article class="card card--third" data-reveal>
  <p class="card__no mono">{i+1:02d}</p>
  <h3 class="h4">{t}</h3>
  <p style="color:var(--fg-2)">{d}</p>
  <ul class="slist">{li}</ul>
</article>"""

    homeflow = flow([
        ("Hero", "What the store is, in one screen."),
        ("Trust bar", "Four reasons to believe it, before any product."),
        ("Brand discovery", "Butterfly, GEWO, Stiga, Victas &mdash; players shop by brand."),
        ("Featured products", "Proof the catalogue is deep and current."),
        ("New arrivals", "A reason for returning customers to look again."),
    ])

    # Conversion rate, four consecutive periods as recorded in Shopify.
    # Scale 0 - 2.50%, gridline at 1.25%. Heights are proportional to that scale.
    data = [("Jul", "1.43%", 57, "before"), ("Aug", "0.68%", 27, "before"),
            ("Sep", "1.95%", 78, "after"),  ("Oct", "2.24%", 90, "after")]
    bars = ""
    for i, (m, v, h, phase) in enumerate(data):
        bars += f"""<div class="bar bar--{phase}">
  <p class="bar__val">{v}</p>
  <div class="bar__col" style="--h:{h}%;--d:{i*150}ms"></div>
  <span class="bar__x">{m}</span>
</div>"""

    # July's funnel — the diagnosis. Each bar is that step's conversion from the
    # step immediately before it, which is how a funnel is read. Absolute counts
    # are the figures Shopify recorded.
    julyfunnel = funnel([
        ("Sessions",           "16,349", "all traffic",        100,  False),
        ("Added to cart",      "899",    "5.5% of sessions",   5.5,  False),
        ("Reached checkout",   "466",    "52% of those carts", 52,   False),
        ("Completed checkout", "234",    "50% of checkouts",   50,   True),
    ])

    rows = [
        ("Jul 1&ndash;31, 2026",    "Before", "1.43%", "&minus;31%", False),
        ("Aug 1&ndash;31, 2026",    "Before", "0.68%", "&minus;52%", True),
        ("Sep 1&ndash;30, 2026",    "After",  "1.95%", "+191%",      False),
        ("Sep 5&ndash;Oct 5, 2026", "After",  "2.24%", "+190%",      False),
    ]
    trows = ""
    for period, phase, cvr, delta, split in rows:
        cls = ' class="is-split"' if split else ""
        hl = ' class="num hl"' if phase == "After" else ' class="num"'
        trows += (f'<tr{cls}><td>{period}</td><td class="phase">{phase}</td>'
                  f'<td{hl}>{cvr}</td><td class="num">{delta}</td></tr>')

    stats = [
        ("2.24%", "Conversion rate, 5 September to 5 October 2026", True),
        ("+190%", "Against the previous thirty days, as Shopify reports it", False),
        ("5.5%", "Share of July sessions that ever reached a cart &mdash; the leak the work targeted", False),
        ("$75", "Free shipping threshold the new cart progress bar counts toward", False),
    ]
    statrow = "".join(
        f"""<div class="stat{' stat--hl' if hl else ''}" data-reveal>
  <p class="stat__v">{v}</p><p class="stat__l mono">{l}</p>
</div>""" for v, l, hl in stats)

    body = f"""
<section class="case-hero">
  <div class="aura" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <p class="mono eyebrow" data-reveal="fade" data-onload>Case study 01 &mdash; Shopify ecommerce</p>
    <div style="margin-top:clamp(1.4rem,3vw,2.4rem)">
      {lines('Table Tennis', '<span class="accent">USA</span>', cls="display case-hero__title", onload=True)}
    </div>
    <div class="hero__body">
      <div class="hero__lead">
        <p class="lead lead--wide" data-reveal data-onload>A Shopify store selling table tennis equipment across
        the United States. It was sliding when I came in, bottomed at <strong>0.68%</strong> in August 2026, and the
        latest thirty days sit at <strong>2.24%</strong>. Every figure here has its screenshot attached.</p>
      </div>
    </div>
    {livebtn("https://tabletennisstore.us/", "Open the live store")}
    {meta_rail([
        ("Client", "Table Tennis USA"),
        ("Sector", "Table tennis ecommerce"),
        ("Platform", "Shopify"),
        ("Role", "UX design, theme customisation, CRO, SEO"),
        ("Live site", '<a href="https://tabletennisstore.us/" target="_blank" rel="noopener">tabletennisstore.us &#8599;</a>'),
        ("Measured", "Jul&ndash;Oct 2026, Shopify Analytics"),
    ])}
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">Project overview</p>
        <h2 class="bigquote" style="margin-top:1.2rem">A big catalogue that was hard to shop.</h2>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>In July 2026 the store pulled <strong>16,349 sessions</strong> and converted 234 of them. Only 5.5% of
        those visitors ever reached a cart.</p>
        <p>That is not a traffic problem and it is not a pricing problem. It was a business losing orders inside its
        own catalogue, and then losing a second batch between the cart and the card.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("01", "The problem",
           ["Nine things standing", "between a visitor", "and an order."],
           "Everything below was documented before any design work started. The list is what the project was scoped against.")}
    <div class="probs" data-stagger>{probs}</div>
    <p class="note" style="margin-top:clamp(1.6rem,3vw,2.4rem)" data-reveal>The goal was to turn the store into a
    structured, high-trust shopping experience while keeping the Shopify setup scalable and maintainable &mdash; so the
    client could keep running it without me.</p>
  </div>
</section>

<section class="section" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="court" aria-hidden="true"></div>
  <div class="wrap" style="position:relative;z-index:2">
    {shead("02", "The solution",
           ["What actually", "changed."],
           "Three areas of work. Each addresses specific items on the problem list rather than a general sense that things could look better.")}
    <div class="deck" data-stagger>{solcards}</div>

    <div style="margin-top:clamp(2.8rem,5.5vw,4.4rem)">
      <p class="mono eyebrow" data-reveal style="margin-bottom:1.4rem">The homepage, in sequence</p>
      <h3 class="display h3" data-reveal style="max-width:24ch;margin-bottom:clamp(1.6rem,3vw,2.4rem)">Five sections, in the
      order a visitor needs them.</h3>
      {homeflow}
      <p class="note" style="margin-top:1.6rem" data-reveal>Each section answers the question the previous one
      raises. A visitor who lands cold learns what the store is, why to trust it, which brands it carries, what it
      sells, and what is new &mdash; without having to search for any of it.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">My role</p>
        <h2 class="display h3" style="margin-top:1.2rem;max-width:16ch">Design and implementation, both.</h2>
        <p style="color:var(--fg-2);margin-top:1.2rem;max-width:34ch">I was not handing files to a developer.
        The design decisions and the code that shipped them were the same job.</p>
      </div>
      <div class="split__r" data-reveal data-delay="120">
        <ul class="slist" style="margin-top:0">{rolelist}</ul>
      </div>
    </div>
  </div>
</section>

<section class="results section">
  <div class="wrap">
    {shead("03", "Diagnosis",
           ["Where the orders", "were leaking."],
           "July 2026, before the work. Of every hundred arrivals, five reached a cart, and half of the ones who reached checkout never finished.")}

    {julyfunnel}
    <p class="note" style="margin-top:1rem">Each bar is that step&rsquo;s conversion from the step immediately
    before it. Counts are exactly as Shopify recorded them for 1&ndash;31 July 2026.</p>

    {shot("tts-jul.jpg", "July 2026 in the store&rsquo;s own Shopify Analytics. <b>16,349 sessions, 899 carts, 466 checkouts, 234 orders, 1.43% conversion</b> — and July itself already down 31% on June.", 934, 492)}

    <div class="split" style="margin-top:clamp(2.4rem,5vw,3.6rem)">
      <div class="split__l" data-reveal>
        <h3 class="display h3" style="max-width:20ch">Two separate leaks, two different fixes.</h3>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p><strong>Before the cart.</strong> Only 5.5% got that far. People could not find the right product fast
        enough, and nothing told them why to trust the store with a card.</p>
        <p><strong>After the cart.</strong> Half of everyone at checkout left. In equipment retail that is usually
        shipping cost arriving as a surprise at the final step.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="wrap">
    {shead("04", "The shipping fix",
           ["Shipping stopped being", "a surprise at the end."],
           "Two changes aimed squarely at the second leak.")}

    <div class="split" style="margin-top:clamp(1.6rem,3vw,2.4rem)">
      <div class="split__l prose" data-reveal>
        <p>Shipping options were rebuilt around what customers actually buy. A rubber sheet and a full-size table
        are not the same parcel and should never have been offered the same way.</p>
        <p>Then the threshold was made visible. A <strong>free shipping progress bar</strong> sits in the side cart
        and at checkout, counting in real money toward the $75 mark.</p>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>It does two jobs. Removes the late surprise that was killing checkouts, and gives a shopper a reason to
        add one more item rather than leave. Both states below, from the live store.</p>
      </div>
    </div>

    {shotgrid(
      shot("tts-cart-partial.jpg", "Not there yet. <b>&ldquo;You&rsquo;re $20.03 away from free shipping&rdquo;</b> — a part-filled bar and a specific number, shown while there is still time to act on it.", 1347, 633),
      shot("tts-cart-unlocked.jpg", "Threshold cleared. <b>&ldquo;You&rsquo;ve unlocked FREE SHIPPING&rdquo;</b> — confirmed in the cart, long before checkout can take it back.", 1354, 675, url="tabletennisstore.us"),
      cls="shotgrid--2")}
  </div>
</section>

<section class="results section">
  <div class="wrap">
    {shead("05", "Proof",
           ["What happened", "to the number."],
           "Four consecutive periods from the store&rsquo;s analytics, including the two that are not flattering.")}
    <div class="chartwrap">
      <div class="chart" data-reveal="fade">
        <figure class="chartfig chartfig--marked">
          <figcaption>Site-wide conversion rate &mdash; Table Tennis Store, 2026</figcaption>
          <div class="plot">
            <div class="yaxis" aria-hidden="true"><span>2.50%</span><span>1.25%</span><span>0</span></div>
            <div class="bars bars--four">
              <div class="bars__mark" aria-hidden="true"><span>Work went in</span></div>
              {bars}
            </div>
          </div>
        </figure>
      </div>
      <div class="chart__note" data-reveal>
        <p class="note">The store was already falling before the work started. July was down 31% on June, then
        August dropped another 52% to 0.68%. September came back to 1.95%, and the most recent thirty days sit at
        2.24% &mdash; above where the store was in July, before the slide bottomed out.</p>
      </div>
    </div>

    <div class="statrow" style="margin-top:clamp(2.4rem,5vw,4rem)" data-stagger>{statrow}</div>

    <div style="margin-top:clamp(2.8rem,5.5vw,4.4rem)" data-reveal>
      <p class="mono eyebrow" style="margin-bottom:1.2rem">The receipts</p>
      {receipts(
        shot("tts-aug.jpg", "<b>Aug 2026 &mdash; 0.68%</b>, down 52% on July. The low point.", 934, 470),
        shot("tts-sep.jpg", "<b>Sep 2026 &mdash; 1.95%</b>, up 191% on August.", 934, 467),
        shot("tts-oct.jpg", "<b>5 Sep&ndash;5 Oct &mdash; 2.24%</b>, up 190% on the previous thirty days.", 934, 468))}
      <p class="note" style="margin-top:1rem">Shopify Analytics, USD, human sessions only. Date ranges are visible
      in each capture so every figure on this page can be checked against its source.</p>
    </div>

    <div style="margin-top:clamp(2.6rem,5vw,4rem)" data-reveal>
      <p class="mono eyebrow" style="margin-bottom:1.2rem">All four periods</p>
      <div class="dtable-wrap">
        <table class="dtable">
          <thead><tr><th>Period</th><th>Phase</th><th class="num">Conversion rate</th><th class="num">Change on prior period</th></tr></thead>
          <tbody>{trows}</tbody>
        </table>
      </div>
    </div>

    <div class="split" style="margin-top:clamp(2.4rem,5vw,3.6rem)">
      <div class="split__l" data-reveal>
        <h3 class="display h3" style="max-width:18ch">What I will and will not claim.</h3>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>The store was sliding before I touched it, and that is on this page because leaving it off would make the
        recovery look like something it is not.</p>
        <p><strong>What I claim:</strong> the direction and the timing, both visible in the screenshots above.</p>
        <p><strong>What I do not:</strong> that every point of the recovery is mine. Traffic mix and seasonality move
        month to month, and conversion rate on its own does not isolate a cause. No revenue figure is claimed
        anywhere on this site.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">What this means</p>
        <h2 class="bigquote" style="margin-top:1.2rem">The redesign did not just change how the site looks.</h2>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>It changed how quickly people find a product, how much they trust the store, and whether shipping
        ambushes them at the last step. That is what a conversion rate is actually measuring.</p>
        <p><strong>And it stayed a Shopify store the client can run and extend themselves.</strong></p>
      </div>
    </div>
  </div>
</section>

<a class="next" href="gewo-usa.html" data-cursor="Next case">
  <div class="wrap">
    <p class="mono mono--accent" data-reveal="fade">Next project &mdash; 02</p>
    <h2 class="next__t" data-reveal style="margin-top:1rem">GEWO USA</h2>
  </div>
</a>

{cta_block("Want this run on your store?",
           "Send the URL and your current conversion rate. I will tell you where I think the orders are leaking before you pay me anything.")}
"""
    return page("table-tennis-usa.html", "Table Tennis USA — Case Study — AKINTAYO",
                "Shopify UX and conversion work for Table Tennis Store. Conversion rate from a 0.68% low in "
                "August 2026 to 2.24% across the latest thirty days, with the analytics screenshots attached.",
                "work.html", body, og_img="og-ttusa.jpg")


# =============================================================== CASE: GEWO ==
def build_gewo():
    tree = [
        ("Rackets", "3", ["Paddles <em>Shakehand</em>", "Blades <em>Shakehand, Chinese penhold</em>", "Combo specials"]),
        ("Rubber", "4", ["Inverted", "Short pips", "Long pips", "Anti-spin"]),
        ("Tables", "5", ["Indoor", "Outdoor", "Nets &amp; net sets", "Cleaner", "Accessories"]),
        ("Ball", "5", ["Tournament", "Training", "Cases", "Collectors", "Collector nets"]),
        ("Accessories", "6", ["Clothing", "Bags", "Shoes", "Racket care", "Rubber accessories", "Novelty"]),
        ("Deals", "4", ["Bundles", "New arrivals", "On sale", "Clearance"]),
    ]
    branches = ""
    for name, n, kids in tree:
        li = "".join(f"<li>{k}</li>" for k in kids)
        branches += f"""<div class="branch" data-reveal>
  <h3 class="branch__h">{name}<span>{n} sub</span></h3>
  <ul>{li}</ul>
</div>"""

    # Product counts as shown on the homepage collection tiles. Single series.
    counts = [("Blades", 50), ("Rubber", 50), ("Shirts", 35), ("Paddles", 19),
              ("Balls", 18), ("Combo specials", 17), ("Shoes", 7)]
    hbars = ""
    for i, (k, v) in enumerate(counts):
        hbars += f"""<div class="hbar">
  <span class="hbar__k">{k}</span>
  <div class="hbar__track"><div class="hbar__fill" style="--w:{v/50*100:.0f}%;--d:{i*90}ms"></div></div>
  <span class="hbar__v">{v}</span>
</div>"""

    beats = "".join([
        beat("01", "A manufacturer&rsquo;s store has two jobs at once", [
            "GEWO USA was established by Ben Nisbet with professional player Mishel Levinski, on the principle of "
            "building equipment &ldquo;with the eyes of a player&rdquo;.",
            "That changes the brief. A multi-brand retailer helps you choose <em>between</em> brands. A "
            "manufacturer&rsquo;s store has to carry the brand itself and still work as a shop. Every layout "
            "decision is a negotiation between those two jobs."]),
        beat("02", "Navigation built on how equipment is classified", [
            "Twenty-seven subcategories under six headings, following the sport&rsquo;s own taxonomy rather than a "
            "generic shop template. A player who knows they want long pips reaches them in two moves.",
            "The menu is doing the work a shop assistant would do, and it can only do that if whoever built it "
            "understands the categories."]),
        beat("03", "Four claims a reseller cannot make", [
            "Pro tested, match-ready consistency, premium materials, precision engineered. Those are manufacturing "
            "claims, and a reseller has no standing to make them.",
            "Sitting them under the hero, before the catalogue, frames everything below as the manufacturer&rsquo;s "
            "own equipment rather than another storefront selling the same boxes."]),
        beat("04", "Combo specials, for the customer who does not know what to ask", [
            "The hardest customer in table tennis retail is the one who cannot pair a blade with a rubber. "
            "Pre-matched setups get their own navigation category, homepage section and tile, with the saving shown "
            "as a percentage.",
            "An intimidating configuration problem becomes one product decision, without hiding the components from "
            "players who do want to choose."]),
    ])

    body = f"""
<section class="case-hero">
  <div class="aura" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <p class="mono eyebrow" data-reveal="fade" data-onload>Case study 02 &mdash; Shopify ecommerce</p>
    <div style="margin-top:clamp(1.4rem,3vw,2.4rem)">
      {lines('GEWO', '<span class="accent">USA</span>', cls="display case-hero__title", onload=True)}
    </div>
    <div class="hero__body">
      <div class="hero__lead">
        <p class="lead lead--wide" data-reveal data-onload>The US store of a table tennis equipment manufacturer,
        carrying two jobs at once: be the brand, and be the shop. It loads its largest element in
        <strong>1.2 seconds</strong> and moves nothing while it does. The store is live, so judge it there.</p>
      </div>
    </div>
    {livebtn("https://www.gewousa.com/", "Open the live store")}
    {meta_rail([
        ("Client", "GEWO USA"),
        ("Sector", "Manufacturer-owned ecommerce"),
        ("Platform", "Shopify"),
        ("Role", "Website design"),
        ("Live site", '<a href="https://www.gewousa.com/" target="_blank" rel="noopener">gewousa.com &#8599;</a>'),
        ("Measured", "Core Web Vitals, 30 days"),
    ])}
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">The brief in one line</p>
        <h2 class="bigquote" style="margin-top:1.2rem">Make the brand and the catalogue stop fighting each other.</h2>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>The catalogue runs from shakehand and penhold blades through four categories of rubber, indoor and
        outdoor tables, balls, apparel, footwear, and maintenance items down to edge tape and glue.</p>
        <p>Those are not one kind of purchase. <strong>Apparel is browsed. Rubber is specified. A table is
        researched. Edge tape is re-ordered.</strong> The store has to let all four happen without the brand story
        blocking someone who came to buy glue.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    {shotgrid(
      shot("gewo-home.jpg", "The homepage. Brand first, then the trust strip, then eight collection tiles — so a player who came to shop is two clicks from the right category.", 1365, 1180, url="gewousa.com", cls="shot--crop"),
      shot("gewo-pdp.jpg", "A product page. Price, variant, stock count and both buy paths above the fold, with the full specification underneath for the players who read it.", 1366, 1180, url="gewousa.com/products", cls="shot--crop"),
      cls="shotgrid--2")}
    {shot("gewo-pdp-bands.jpg", "Below every product: <b>who it is for</b>, a four-point performance read, and endorsements from GEWO&rsquo;s own sponsored players. A reseller cannot publish any of this. The manufacturer can.", 1366, 1250, cls="shot--crop")}
  </div>
</section>

<section class="section" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="wrap" style="position:relative;z-index:2">
    {shead("01", "Information architecture",
           ["The menu is the", "shop assistant."],
           "Six headings, twenty-seven subcategories, organised by how table tennis equipment is actually classified rather than how a generic store template wants to group it.")}
    <div class="tree" data-stagger>{branches}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("02", "Catalogue depth",
           ["What is actually", "behind each tile."],
           "Product counts as shown on the homepage collection tiles. Publishing them tells a customer whether a category is worth opening.")}
    <div class="hbars" data-reveal="fade" style="margin-top:clamp(1rem,2vw,1.6rem)">{hbars}</div>
    <p class="note" style="margin-top:1.8rem" data-reveal>Blades and rubber carry the range; shoes and novelty
    items do not. A store that hides those numbers sends a customer into an empty room and loses them there.</p>
  </div>
</section>

<section class="results section">
  <div class="wrap">
    {shead("03", "Performance",
           ["It is fast, and", "nothing jumps."],
           "Core Web Vitals as Shopify recorded them over thirty days. These are the three measurements Google uses to judge whether a page is usable.")}

    {shot("gewo-vitals.jpg", "Thirty days of real visitor data. <b>LCP 1201ms. INP 56ms. CLS 0.</b> All three rated Good.", 688, 76)}

    <div class="statrow" style="margin-top:clamp(2.2rem,4.5vw,3.4rem)" data-stagger>
      <div class="stat stat--hl" data-reveal>
        <p class="stat__v">1.2s</p>
        <p class="stat__l mono">Largest Contentful Paint. Google calls anything under 2.5s good, so this is less than half the limit</p>
      </div>
      <div class="stat" data-reveal>
        <p class="stat__v">56ms</p>
        <p class="stat__l mono">Interaction to Next Paint. The threshold is 200ms. This is roughly a quarter of it</p>
      </div>
      <div class="stat" data-reveal>
        <p class="stat__v">0</p>
        <p class="stat__l mono">Cumulative Layout Shift. Nothing on the page moves while it loads. Not low, zero</p>
      </div>
    </div>

    <div class="split" style="margin-top:clamp(2.2rem,4.5vw,3.4rem)">
      <div class="split__l" data-reveal>
        <h3 class="display h3" style="max-width:20ch">Why a store owner should care about the third one.</h3>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>Layout shift is what happens when a page loads in pieces and the thing you were about to tap slides out
        from under your thumb. On a phone it is the reason people tap the wrong button and leave.</p>
        <p>A score of zero means it never happens here. That is not a design flourish, it is a checkout that does
        not lose people for a stupid reason.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="rail">
      <div class="rail__side" data-reveal="fade">
        <p class="mono mono--accent">Design decisions</p>
        <p class="mono" style="margin-top:.6rem">Four choices and the reasoning behind them</p>
        <div class="facts" style="margin-top:2rem">
          <div class="fact"><span class="mono">Store type</span><span class="fact__v">Manufacturer-owned</span></div>
          <div class="fact"><span class="mono">Nav headings</span><span class="fact__v">6, nested</span></div>
          <div class="fact"><span class="mono">Subcategories</span><span class="fact__v">27</span></div>
          <div class="fact"><span class="mono">Products on tiles</span><span class="fact__v">196</span></div>
          <div class="fact"><span class="mono">Sponsored players</span><span class="fact__v">6 featured</span></div>
          <div class="fact"><span class="mono">Free shipping</span><span class="fact__v">Orders over $60</span></div>
        </div>
      </div>
      <div class="rail__main">
        {beats}
        <div class="caveat" data-reveal>
          <p class="mono mono--accent">What I am not claiming</p>
          <p>The speed numbers above are real and measured. <strong>There is no conversion or revenue data I can
          publish for this store</strong>, so none appears here. The conversion figures on this site belong to the
          Table Tennis Store project and only to it.</p>
          <p>What GEWO USA shows is a different problem solved: a brand-owned catalogue rather than a multi-brand
          retailer, built fast. The store is live. Judge the execution there.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<a class="next" href="paul-david.html" data-cursor="Next case">
  <div class="wrap">
    <p class="mono mono--accent" data-reveal="fade">Next project &mdash; 03</p>
    <h2 class="next__t" data-reveal style="margin-top:1rem">Paul David</h2>
  </div>
</a>

{cta_block("Selling your own brand direct?",
           "A manufacturer store has a different problem from a retailer. Tell me about your range and where customers get lost in it.")}
"""
    return page("gewo-usa.html", "GEWO USA — Case Study — AKINTAYO",
                "Website design for GEWO USA, the US store of a table tennis equipment manufacturer — navigation "
                "built on equipment taxonomy across 27 subcategories, trust claims only a manufacturer can make, "
                "and combo specials for customers who don't yet know what to ask for.",
                "work.html", body, og_img="og-gewo.jpg")


# ========================================================= CASE: PAUL DAVID ==
def build_paul():
    services = [
        ("In-Home Coaching", "60 min", "$150",
         "One-on-one coaching at your location focused on technique, footwork, consistency, strategy and personalised skill development."),
        ("Private Lessons", "60 min", "$150",
         "Personalised private coaching focused on individual goals, for beginner, intermediate or competitive players."),
        ("Group Lessons", "60 min", "$120",
         "Structured group coaching for players who want to train together while improving technique and movement."),
        ("Camp Clinic", "Full day", "$250",
         "Intensive day-based training with drills, coaching, match play and skill-building activities."),
    ]
    srows = "".join(
        f'<tr><td>{n}</td><td class="phase">{d}</td><td class="num hl">{p}</td><td>{desc}</td></tr>'
        for n, d, p, desc in services)

    bookflow = flow([
        ("Lands on the site", "From a search, a flyer or another player&rsquo;s recommendation."),
        ("Opens Services", "Four offers, each with duration and price stated."),
        ("Picks one", "The choice is made before any contact happens."),
        ("Book now", "Opens an email already addressed, with that service as the subject."),
        ("Paul&rsquo;s inbox", "A coach who checks his email checks his bookings."),
    ])

    kitflow = flow([
        ("&ldquo;What racket should I buy?&rdquo;", "Every coach is asked this, constantly."),
        ("Recommended Equipment", "One page, three setups, tiered by level."),
        ("Starter / Intermediate / Advanced", "GEWO CS Energy Control, CS Energy Carbon Pro, Xolo Offensive with Neoflexx."),
        ("Code PDCGEWO", "12% off, so the recommendation is worth acting on."),
        ("GEWO USA", "A properly stocked store &mdash; and another client of mine."),
    ])

    beats = "".join([
        beat("01", "A coaching business is not a shop", [
            "Paul David sells time: in-home coaching, private lessons, group lessons and camp clinics.",
            "None of that belongs in a cart. He is paid at the table, so a checkout adds a step his business does "
            "not have. Which makes the question a different one: <strong>how do you get someone from &lsquo;I want "
            "lessons&rsquo; to a message in his inbox, in as few steps as possible?</strong>"]),
        beat("02", "Four services, priced in the open", [
            "Name, duration, price and who it is for, with travel fees noted. Coaches routinely hide pricing and "
            "lose the enquiry to the uncertainty, because the visitor assumes it is expensive.",
            "Publishing it filters out the people who were never going to book and gives everyone else a reason to "
            "act now."]),
        beat("03", "One booking action per service", [
            "Each service has its own <em>Book now</em> button opening a pre-addressed email, with the service "
            "already in the subject line.",
            "No form to build or maintain, no submissions lost in a plugin, and no ambiguity at Paul&rsquo;s end "
            "about which service the enquiry is for."]),
        beat("04", "The equipment page, which is really a partner path", [
            "Rather than run a shop himself, Paul has a <em>Recommended Equipment</em> page "
            "naming three GEWO setups by level, blade and rubber specified.",
            "Each links to GEWO USA, a properly stocked store I had already worked on, and carries his own code, "
            "PDCGEWO, for 12% off. <strong>The student gets a straight answer and a discount; the coach gets a "
            "credible recommendation and zero inventory.</strong>"]),
        beat("05", "Built to be handed over", [
            "The unglamorous half: services Paul can edit himself, payment matched to how he actually gets paid, "
            "domain connected, ownership transferred.",
            "A site the client cannot change goes stale within a year."]),
    ])

    body = f"""
<section class="case-hero">
  <div class="aura" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <p class="mono eyebrow" data-reveal="fade" data-onload>Case study 03 &mdash; Coaching practice</p>
    <div style="margin-top:clamp(1.4rem,3vw,2.4rem)">
      {lines('Paul', '<span class="accent">David</span>', cls="display case-hero__title", onload=True)}
    </div>
    <div class="hero__body">
      <div class="hero__lead">
        <p class="lead lead--wide" data-reveal data-onload>A coach with four services to sell and no cart to sell
        them in. Turn coaching hours into enquiries, connect students to equipment without making him a retailer,
        and leave the whole thing in his hands.</p>
      </div>
    </div>
    {livebtn("https://pauldavidcoach.com/", "Open the live site")}
    {meta_rail([
        ("Client", "Paul David"),
        ("Sector", "Table tennis coaching"),
        ("Model", "Booked online, paid in person"),
        ("Role", "Full site build, launch &amp; handover"),
        ("Live site", '<a href="https://pauldavidcoach.com/" target="_blank" rel="noopener">pauldavidcoach.com &#8599;</a>'),
        ("Published data", "None &mdash; see note"),
    ])}
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <p class="mono eyebrow" data-reveal="fade">What is being sold</p>
    <h2 class="display h3" data-reveal style="margin-top:1.2rem;max-width:20ch">Four services, each with its own booking path.</h2>
    <div class="dtable-wrap" style="margin-top:clamp(1.8rem,3.4vw,2.6rem)" data-reveal>
      <table class="dtable">
        <thead><tr><th>Service</th><th>Duration</th><th class="num">Price</th><th>Who it is for</th></tr></thead>
        <tbody>{srows}</tbody>
      </table>
    </div>
    <p class="note" style="margin-top:1.4rem" data-reveal>Travel fees are stated on the page rather than raised
    after someone has committed.</p>
  </div>
</section>

<section class="section" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="court" aria-hidden="true"></div>
  <div class="wrap" style="position:relative;z-index:2">
    {shead("01", "The booking path",
           ["Five steps, no form,", "no checkout."],
           "The whole problem is the distance between wanting a lesson and the coach knowing about it.")}
    {bookflow}
    <p class="note" style="margin-top:1.8rem" data-reveal>A contact form would add two steps, a plugin to maintain,
    and a place for enquiries to go missing. The email opens already knowing which service was chosen.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("02", "The equipment path",
           ["Answering the", "question every coach", "gets asked."],
           "A coach who says &lsquo;buy whatever&rsquo; loses authority. A coach who runs a shop loses time. This is the third option.")}
    {kitflow}
    <p class="note" style="margin-top:1.8rem" data-reveal>The student gets a specific answer and a reason to act.
    The coach carries no stock, no shipping, no returns. Two of my clients worth more to each other than alone.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="rail">
      <div class="rail__side" data-reveal="fade">
        <p class="mono mono--accent">Design decisions</p>
        <p class="mono" style="margin-top:.6rem">Five choices, and why</p>
        <div class="facts" style="margin-top:2rem">
          <div class="fact"><span class="mono">Services</span><span class="fact__v">4, individually priced</span></div>
          <div class="fact"><span class="mono">Payments</span><span class="fact__v">In person, by design</span></div>
          <div class="fact"><span class="mono">Booking</span><span class="fact__v">Pre-addressed email, per service</span></div>
          <div class="fact"><span class="mono">Equipment</span><span class="fact__v">3 setups, tiered by level</span></div>
          <div class="fact"><span class="mono">Partner code</span><span class="fact__v">12% off at GEWO USA</span></div>
          <div class="fact"><span class="mono">Handover</span><span class="fact__v">Domain &amp; ownership transferred</span></div>
        </div>
      </div>
      <div class="rail__main">
        {beats}
        <div class="caveat" data-reveal>
          <p class="mono mono--accent">What I am not claiming</p>
          <p>No booking or revenue figures are published for this project, so none appear here. What it shows is
          that the same thinking works away from ecommerce: understand how the business actually takes money,
          then build the shortest honest path to it &mdash; and notice where two clients can be worth more to each
          other than either is alone. The site is live; judge the execution there.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<a class="next" href="table-tennis-usa.html" data-cursor="Back to 01">
  <div class="wrap">
    <p class="mono mono--accent" data-reveal="fade">Back to the flagship &mdash; 01</p>
    <h2 class="next__t" data-reveal style="margin-top:1rem">Table Tennis USA</h2>
  </div>
</a>

{cta_block("Coach, club or academy?",
           "You do not need a shop. You need the shortest possible path between someone deciding to train and you hearing about it.")}
"""
    return page("paul-david.html", "Paul David — Case Study — AKINTAYO",
                "Website build for table tennis coach Paul David: four services priced in the open, a five-step "
                "booking path with no form or checkout, and an equipment page that partners students to GEWO USA.",
                "work.html", body, og_img="og-paul.jpg")


# ================================================================= SERVICES ==
def build_services():
    svcs = [
        ("01", "Website design from scratch",
         "For a business with no website, or one whose site was never really designed. A placeholder, an unfinished "
         "template, a page that exists only because something had to.",
         "Brands launching direct, new clubs and academies, coaches, event organisers, distributors.",
         ["Structure and page architecture", "Visual design and design system",
          "Full build and launch", "Mobile and performance work",
          "Domain and DNS setup", "Handover so you can run it"]),
        ("02", "Ecommerce website design",
         "The catalogue is the site: how it is organised, how a customer narrows it down, and what a product page "
         "has to prove before someone buys a blade they cannot hold.",
         "Equipment brands, retailers, manufacturer-owned stores, distributors, clubs running a pro shop.",
         ["Catalogue and collection architecture", "Product page design for specifications",
          "Filtering and search behaviour", "Cart and checkout flow",
          "Shopify theme customisation and Liquid", "Shipping, currency and region handling"]),
        ("03", "Website redesign",
         "For a site that works but holds the business back. A redesign has to move things forward without throwing "
         "away what already earns: rankings, product data, URLs, and customer habits.",
         "Stores that outgrew their design, brands after a rebrand, sites built by someone no longer available.",
         ["Audit of the existing site", "Redesign against the current buying path",
          "URL and content preservation", "Migration without losing product data",
          "Before-and-after measurement", "Staged launch"]),
        ("04", "Conversion-focused optimisation",
         "For a site with traffic that does not turn into orders. Not a redesign. Work on the specific points where "
         "people leave, then measurement.",
         "Any table tennis business with real traffic and a conversion rate that has stopped moving.",
         ["Buying-path mapping, end to end", "Product and collection page work",
          "Cart and checkout friction removal", "Trust, shipping and returns clarity",
          "Analytics and conversion tracking", "Month-over-month reporting"]),
    ]
    blocks = ""
    for n, t, what, who, items in svcs:
        li = "".join(f"<li>{i}</li>" for i in items)
        blocks += f"""<div class="svc" data-reveal>
  <p class="svc__no mono">{n}</p>
  <div class="svc__head">
    <h2 class="svc__t">{t}</h2>
    <p class="svc__for mono">Who it is for</p>
    <p style="color:var(--fg-2);max-width:34ch;margin-top:.5rem">{who}</p>
  </div>
  <div class="svc__body"><p style="color:var(--fg-2)">{what}</p></div>
  <ul class="svc__list">{li}</ul>
</div>"""

    body = f"""
<section class="hero" style="padding-bottom:clamp(1.6rem,3vw,2.6rem)">
  <div class="aura" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <p class="mono eyebrow" data-reveal="fade" data-onload>Services &mdash; four, and only four</p>
    <div style="margin-top:clamp(1.4rem,3vw,2.4rem)">
      {lines('What I build,', 'and who it is for.', onload=True)}
    </div>
    <div class="hero__body">
      <div class="hero__lead">
        <p class="lead lead--wide" data-reveal data-onload>Four services. Most projects are one of them. Some run
        two together.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div style="border-top:1px solid var(--line)" data-stagger>{blocks}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("&mdash;", "Process",
           ["The same four stages,", "every time."],
           "Nothing is designed before the catalogue and the buying path are understood. Getting that order wrong is what produces a beautiful site that does not sell.")}
    <div class="steps" data-stagger>
      <div class="step" data-reveal><p class="step__no mono mono--accent">01</p><h3 class="step__t">Learn the catalogue</h3><p class="step__d">What you sell, how it is organised, and where the money actually comes from.</p></div>
      <div class="step" data-reveal><p class="step__no mono mono--accent">02</p><h3 class="step__t">Map the buying path</h3><p class="step__d">Arrival to completed order, written out, with the stalling points marked.</p></div>
      <div class="step" data-reveal><p class="step__no mono mono--accent">03</p><h3 class="step__t">Design and build</h3><p class="step__d">Design that follows the map, then a working site, tested on real devices.</p></div>
      <div class="step" data-reveal><p class="step__no mono mono--accent">04</p><h3 class="step__t">Measure and refine</h3><p class="step__d">Changes made on the evidence rather than on preference.</p></div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">Not sure which one</p>
        <h2 class="bigquote" style="margin-top:1.2rem">Describe the problem. I will tell you which of these it is.</h2>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>Plenty of businesses ask for a redesign when the real problem is three product pages and a checkout
        step. Others ask for conversion work when the site underneath cannot support it. Worth knowing which one
        you have before anyone quotes you.</p>
        <p>Send the URL and a sentence about what is not working. <strong>If the answer is that you do not need me
        yet, I will say that.</strong></p>
      </div>
    </div>
  </div>
</section>

{cta_block("Start with the problem, not the brief.",
           "Send your site and what is going wrong with it. The right service usually becomes obvious in one email.")}
"""
    return page("services.html", "Services — AKINTAYO",
                "Website design from scratch, ecommerce design, website redesign and conversion-focused "
                "optimisation for table tennis brands, stores, clubs and coaches.",
                "services.html", body)


# ==================================================================== ABOUT ==
def build_about():
    principles = [
        ("Proof over adjectives",
         "Numbers where numbers exist. That rule is why the Table Tennis Store decline sits on this site beside the recovery."),
        ("The catalogue comes first",
         "Decisions made before anyone understands the products are guesses, and in this sport the guesses are usually wrong."),
        ("Build it, do not just draw it",
         "I hand over working websites, not concept files for someone else to interpret and dilute."),
        ("Leave the client in control",
         "Ownership transferred, domain connected, structure editable. A site the owner cannot change goes stale."),
    ]
    cards = "".join(f"""<article class="card" style="grid-column:span 6" data-reveal>
  <p class="card__no mono">{i+1:02d}</p>
  <h3 class="h4">{t}</h3>
  <p class="card__body">{d}</p>
</article>""" for i, (t, d) in enumerate(principles))

    human = [
        ("Home", "Osun State, Nigeria",
         "Born and based here. My clients are not, so everything runs on email and shipped work, which is why this site leads with evidence instead of a promise."),
        ("Study", "Doctor of Pharmacy",
         "A PharmD candidate at Obafemi Awolowo University. Pharmacy is a degree in reading technical specifications carefully and getting the details exactly right."),
        ("Chess", "A serious habit",
         "Not a titled player, a serious one. Chess is pattern recognition and thinking several moves past the obvious, under time pressure."),
        ("Gadgets", "Phones, laptops, cameras",
         "The real obsession. Caring how an object feels in the hand is not unrelated to caring how an interface feels under a thumb."),
        ("Off the desk", "Books, restaurants, a map",
         "I read constantly, I will try any restaurant once, and the long plan is to see as much of the world as I can manage."),
    ]
    hcards = "".join(f"""<article class="hcard" data-reveal>
  <p class="mono mono--accent">{k}</p>
  <h3 class="h4">{t}</h3>
  <p>{d}</p>
</article>""" for k, t, d in human)

    stack = ["Shopify", "Liquid templating", "Theme customisation", "Custom CSS",
             "HTML &amp; JavaScript", "Responsive &amp; mobile", "Conversion rate optimisation",
             "Ecommerce UX", "SEO structure", "Domain &amp; DNS setup",
             "Meta Business integration", "Analytics &amp; conversion tracking"]
    pills = "".join(f'<span class="pill">{s}</span>' for s in stack)

    body = f"""
<section class="hero" style="padding-bottom:clamp(1.6rem,3vw,2.6rem)">
  <div class="aura" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <p class="mono eyebrow" data-reveal="fade" data-onload>About &mdash; Akingbehin Akintayo</p>
    <div class="intro-grid" style="margin-top:clamp(1.6rem,3.4vw,2.6rem)">
      {portrait("akintayo.jpg", "Akingbehin Akintayo", tag="Akingbehin Akintayo", eager=True)}
      <div>
        {lines('A designer who', 'picked <span class="ital accent">one</span> sport', 'on purpose.', cls="display h2", onload=True)}
        <div class="prose" style="margin-top:clamp(1.2rem,2.4vw,1.8rem)">
          <p class="lead" data-reveal data-onload>I am an ecommerce web designer in Osun State, Nigeria, and I work
          with table tennis businesses internationally. Stores, academies, coaches.</p>
          <p data-reveal data-onload data-delay="90">Three of them are documented on this site, with the analytics
          screenshots attached rather than described.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">Why this niche</p>
        <h2 class="bigquote" style="margin-top:1.2rem">Specialists get to skip the first month of every project.</h2>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>Most web designers take whatever comes in. A dentist, a law firm, a gym. Reasonable living, one
        structural cost: every project starts with the designer learning a market from zero, on your money.</p>
        <p>Going narrow removes that cost. Table tennis has real money in it, manufacturers through to coaches, and very
        little of it is served by anyone who understands both the equipment and how a store actually converts.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="court" aria-hidden="true"></div>
  <div class="wrap" style="position:relative;z-index:2">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">Beyond table tennis</p>
        <h2 class="bigquote" style="margin-top:1.2rem">Table tennis is the specialism, not the extent of the experience.</h2>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>The most recent work outside the sport is <strong>ORIMI</strong>, a fine jewellery house selling
        made-to-order pieces in solid 18K gold, built on Shopify and shipping to more than twenty-five countries.</p>
        <p>A five-figure ring and a $40 rubber sheet are not the same sale, but they are the same discipline. Make the
        thing legible, make it trustworthy, get out of the way at the moment someone decides to buy.</p>
        <p><a class="tlink" href="https://orimijewelry.com/" target="_blank" rel="noopener">orimijewelry.com &#8599;</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("&mdash;", "How I work", ["Four things I do not", "compromise on."])}
    <div class="deck" data-stagger>{cards}</div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">Working in</p>
        <h2 class="display h3" style="margin-top:1.2rem;max-width:14ch">What I build with.</h2>
      </div>
      <div class="split__r" data-reveal data-delay="120">
        <div class="stack">{pills}</div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("&mdash;", "Off the clock", ["The rest of it."],
           "You are hiring a person, not a studio. Reasonable to want to know who that is before sending money across an ocean.")}
    <div class="human" data-stagger>{hcards}</div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">Working with me</p>
        <h2 class="bigquote" style="margin-top:1.2rem">One person, start to finish.</h2>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>No account manager between you and the person doing the work, and nothing handed to a junior after the
        pitch. You email me, I answer, I build it.</p>
        <p><strong>I am hungry, and I would rather say so than pretend otherwise.</strong> Your result becomes my
        portfolio, so I will go a long way to make it work. That is also the limit: I take few projects, and if the
        timing is wrong I will say so.</p>
      </div>
    </div>
  </div>
</section>

{cta_block("Working in table tennis? Let&rsquo;s talk.",
           "One email with your site and the problem is enough to start.")}
"""
    return page("about.html", "About — AKINTAYO",
                "Akingbehin Akintayo (AKINTAYO) — ecommerce web designer in Osun State, Nigeria, specialising in "
                "the table tennis industry, with wider ecommerce work including the ORIMI fine jewellery store.",
                "about.html", body)


# ================================================================== CONTACT ==
def build_contact():
    include = [
        "Your website address, if you have one.",
        "What kind of table tennis business you run &mdash; brand, store, distributor, club, academy, coach, event.",
        "What is not working, in your own words. &ldquo;Traffic but no orders&rdquo; is a perfectly good brief.",
        "Roughly when you want it live, and whether there is a budget range in mind.",
    ]
    li = "".join(f"<li>{i}</li>" for i in include)

    body = f"""
<section class="hero" style="padding-bottom:clamp(1.6rem,3vw,2.6rem)">
  <div class="aura" aria-hidden="true"></div>
  {ARC}
  <div class="wrap hero__inner">
    <p class="mono eyebrow" data-reveal="fade" data-onload>Contact &mdash; email only</p>
    <div style="margin-top:clamp(1.4rem,3vw,2.4rem)">
      {lines('Tell me about', 'the site and', 'the problem.', onload=True)}
    </div>
    <div class="hero__body">
      <div class="hero__lead">
        <p class="lead lead--wide" data-reveal data-onload>No forms, no calls to book, no chat widget. Email keeps
        the first conversation in writing, and gets you a considered answer rather than a scheduling link.</p>
      </div>
    </div>
    <div style="margin-top:clamp(2.4rem,5vw,4rem)" data-reveal data-onload>
      <a class="cta__mail" href="{mail()}">{EMAIL}</a>
    </div>
  </div>
</section>

<section class="section" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="wrap">
    <div class="contact-person">
      <div class="contact-person__body">
        <p class="mono eyebrow" data-reveal="fade">Who answers</p>
        <h2 class="display h2" data-reveal style="margin-top:1.2rem;max-width:14ch">Let&rsquo;s build something that works.</h2>
        <div class="prose" data-reveal data-delay="120" style="margin-top:1.4rem">
          <p>Every email reaches me and I answer it myself. No assistant screening
          enquiries, no discovery call before anyone has looked at your site, and no proposal written by
          someone who has never opened it.</p>
          <p>Tell me what you sell and what is going wrong with it. <strong>If I am not the right person for
          the job, I will say so rather than quote you.</strong></p>
        </div>
        <div style="margin-top:clamp(1.6rem,3vw,2.2rem)" data-reveal data-delay="180">
          <a class="btn btn--primary" href="{mail()}" data-magnet="0.22"><span>Email me directly</span>{ARROW}</a>
        </div>
      </div>
      <div class="contact-person__media">
        {portrait("akintayo-seated.jpg",
                  "Akingbehin Akintayo, the designer who will work on your project directly",
                  tag="Replies come from me")}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">Make the first email a good one</p>
        <h2 class="display h3" style="margin-top:1.2rem;max-width:16ch">What to include.</h2>
        <p style="color:var(--fg-2);margin-top:1.2rem;max-width:32ch">None of this is required. It just means the first
        reply can be useful instead of a list of questions.</p>
      </div>
      <div class="split__r" data-reveal data-delay="120">
        <ul class="checklist">{li}</ul>
        <div style="margin-top:2rem">
          <a class="btn btn--primary" data-magnet="0.22" href="{mail('Website project enquiry', 'My website: %0D%0AMy business: %0D%0AWhat is not working: %0D%0ATimeline: %0D%0A')}">
            <span>Open a pre-filled email</span>{ARROW}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="wrap">
    {shead("&mdash;", "What happens next",
           ["Three replies, then", "a decision."],
           "No discovery calls, no proposal decks that take a fortnight.")}
    <div class="steps" data-stagger>
      <div class="step" data-reveal><p class="step__no mono mono--accent">01</p><h3 class="step__t">You email</h3><p class="step__d">Your site, your business and what is going wrong with it. A few sentences is enough.</p></div>
      <div class="step" data-reveal><p class="step__no mono mono--accent">02</p><h3 class="step__t">I look properly</h3><p class="step__d">I go through the site before replying and tell you what the actual problem is, including when it is not one I should be paid to fix.</p></div>
      <div class="step" data-reveal><p class="step__no mono mono--accent">03</p><h3 class="step__t">Scope and price</h3><p class="step__d">If it is a fit, you get the scope, what it costs and what you will have at the end, in writing.</p></div>
    </div>
  </div>
</section>

{cta_block("One email is enough to start.",
           "Brands, stores, distributors, clubs, academies, coaches and event organisers in table tennis.",
           "I read and reply to every email myself.")}
"""
    return page("contact.html", "Contact — AKINTAYO",
                "Email AKINTAYO about a table tennis website project: " + EMAIL,
                "contact.html", body)


# ====================================================================== 404 ==
def build_404():
    body = f"""
<section class="hero" style="min-height:62vh">
  <div class="aura" aria-hidden="true"></div>
  {ARC}
  <div class="wrap hero__inner">
    <p class="mono eyebrow" data-onload>Error 404</p>
    <div style="margin-top:clamp(1.4rem,3vw,2.4rem)">
      {lines('That ball went', 'off the table.', onload=True)}
    </div>
    <p class="lead lead--wide" data-onload style="margin-top:2rem">The page you were looking for is not here.</p>
    <div class="hero__actions" style="margin-top:2.4rem;justify-content:flex-start" data-onload>
      <a class="btn btn--ghost" href="./" data-magnet="0.22"><span>Home</span>{ARROW}</a>
      <a class="btn btn--primary" href="work.html" data-magnet="0.22"><span>See the work</span>{ARROW}</a>
    </div>
  </div>
</section>
"""
    return page("404.html", "Page not found — AKINTAYO",
                "That page does not exist.", "index.html", body)


# ==================================================================== EXTRAS ==
def build_extras():
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN)

    pages = ["index.html", "work.html", "table-tennis-usa.html", "gewo-usa.html",
             "paul-david.html", "services.html", "about.html", "contact.html"]
    urls = "".join(
        '  <url><loc>%s/%s</loc><priority>%s</priority></url>\n' % (
            DOMAIN, p, "1.0" if p == "index.html" else ("0.9" if "usa" in p or p == "work.html" else "0.8"))
        for p in pages)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + urls + '</urlset>\n')

    open(os.path.join(OUT, ".nojekyll"), "w").write("")

    favicon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
               '<rect width="32" height="32" fill="#070B0D"/>'
               '<circle cx="16" cy="16" r="7" fill="#155EEF"/></svg>')
    with open(os.path.join(OUT, "favicon.svg"), "w") as f:
        f.write(favicon)


if __name__ == "__main__":
    built = [build_home(), build_work(), build_ttusa(), build_gewo(),
             build_paul(), build_services(), build_about(), build_contact(), build_404()]
    build_extras()
    print("Built:", ", ".join(built))
