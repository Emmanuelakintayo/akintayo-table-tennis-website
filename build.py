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
    home_cur = ' aria-current="page"' if current == "./" else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="grain" aria-hidden="true"></div>
<div class="curtain" aria-hidden="true"></div>
<div class="progress" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"><span class="cursor__label"></span></div>
<div class="cursor-dot" aria-hidden="true"></div>
<div class="peek" aria-hidden="true"></div>

<header class="nav">
  <div class="nav__inner">
    <a class="logo" href="./" aria-label="AKINTAYO — home"{home_cur}><span class="logo__ball"></span>AKINTAYO</a>
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
        <a class="logo" href="./"><span class="logo__ball"></span>AKINTAYO</a>
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


def page(fname, title, desc, current, body, og_img="assets/img/og-default.jpg"):
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}/{'' if fname == 'index.html' else fname}">
<meta name="theme-color" content="#08090b">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AKINTAYO">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}/{'' if fname == 'index.html' else fname}">
<meta property="og:image" content="{DOMAIN}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/css/site.css">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/site.js" defer></script>
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

PROJECTS = [
    dict(no="01", name="Table Tennis USA", href="table-tennis-usa.html",
         tags=["Ecommerce", "Shopify", "Redesign &amp; CRO"],
         res="0.72% &rarr; 1.56% conversion rate",
         stat="1.56%", sub="Conversion rate in February — from 0.72% before the redesign", live="tabletennisstore.us"),
    dict(no="02", name="GEWO USA", href="gewo-usa.html",
         tags=["Ecommerce", "Shopify", "Manufacturer store"],
         res="Multi-category equipment store",
         stat="196", sub="Products across 7 collections, 27 nested subcategories", live="gewousa.com"),
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
        ("01", "Learn the catalogue", "Before anything is designed, I go through what you sell and how it is organised — brands, categories, specifications, price bands, the things customers ask about before they buy."),
        ("02", "Map the buying path", "The route from landing page to completed order, written out step by step, with the points where people stall marked on it."),
        ("03", "Design and build", "Design that follows that map, then a working site. Not a concept file handed over for someone else to interpret."),
        ("04", "Measure and refine", "Conversion rate and behaviour after launch, and changes made on the basis of what the numbers show rather than what looks better."),
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
        <a class="btn btn--ball" href="{mail()}" data-magnet="0.22"><span>Start a project</span>{ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="proof">
  <div class="wrap">
    <a class="proof__link" href="table-tennis-usa.html" data-cursor="Case study">
      <div class="proof__k">
        <p class="mono mono--accent">Flagship project</p>
        <p class="mono">Table Tennis USA &mdash; conversion rate, before and after the redesign</p>
      </div>
      <div class="proof__figs">
        <span class="fig">0.72%</span><span class="fig fig__sep">&rarr;</span>
        <span class="fig">1.26%</span><span class="fig fig__sep">&rarr;</span>
        <span class="fig fig--now">1.56%</span>
      </div>
      <p class="proof__go mono mono--fg">+75% in the first<br>month &mdash; read it &rarr;</p>
    </a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("01", "Positioning",
           ["A generalist spends your first", "month learning this market.", "I already know it."],
           "Table tennis is a specialist catalogue sold to specialist buyers. The websites that work in it are built by someone who understands what is being sold.")}
    <div class="split">
      <div class="split__l prose" data-reveal>
        <p>A customer buying a blade is comparing ply counts, speed and control ratings, handle shapes and weight.
        A customer buying rubber is choosing between inverted, short pips, long pips and anti-spin, then a sponge
        thickness, then checking whether it is ITTF approved. A club is ordering tables and nets in volume.
        A coach is not selling a product at all &mdash; they are selling a time slot.</p>
        <p><strong>That detail is the whole job.</strong> It decides how a catalogue is structured, what a product page
        has to show before a customer scrolls, which filters matter, and where a buyer hesitates. I have worked
        inside three table tennis businesses &mdash; two ecommerce stores and one coaching practice.</p>
      </div>
      <div class="split__r" data-reveal data-delay="120">
        <p class="mono" style="margin-bottom:1.2rem">What that changes in practice</p>
        <ul class="checklist">
          <li>Category structure that follows how players shop &mdash; by equipment type and play style, not by brand alone.</li>
          <li>Product pages built around the specifications buyers actually compare, not around a paragraph of description.</li>
          <li>Filtering that survives pips, sponge thickness, speed and control ratings without turning into a dead end.</li>
          <li>Service and booking paths for coaches, clubs and events, where there is no cart and never should be.</li>
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

{cta_block("Tell me about the site and the problem.",
           "Send an email with your store or site, what is going wrong, and what you want it to do. I will tell you honestly whether I am the right person for it.",
           "Email only &mdash; no forms, no calls to book, no chat widget.")}
"""
    return page("index.html", "AKINTAYO — Website Design for Table Tennis",
                "Website design, ecommerce and conversion work for the table tennis industry — "
                "brands, stores, distributors, clubs and coaches. Case study: Table Tennis USA, "
                "conversion rate 0.72% to 1.56%.", "./", body)


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
        <p>Table Tennis USA has four consecutive months of recorded analytics &mdash; two before the redesign and two
        after it &mdash; and all four are on the case study page, including the month traffic fell. The GEWO USA and
        Paul David projects have no performance data I can publish, so none is claimed for them.</p>
        <p>What those two show instead is design reasoning across different problems: a manufacturer-owned store
        that has to be brand and shop at once, and a coaching practice with no cart at all. <strong>A portfolio is
        worth more when you can trust the parts that are not flattering.</strong></p>
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
        "Homepage lacked a clear conversion-focused layout",
        "Product discovery was limited for brand-loyal players",
        "Trust signals were weak on key pages",
        "Product pages had layout inconsistencies",
        "Variant selection for equipment was unclear",
        "Navigation breadcrumbs were incorrect",
        "Video content redirected users away from the store",
        "Email exposure created spam risk",
        "SEO heading structure needed correction",
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
         "The homepage was rebuilt to move a visitor through the store instead of leaving them to work it out.",
         ["Hero section", "Trust bar", "Brand discovery", "Featured products", "New arrivals"]),
        ("Trust signals",
         "A trust section was placed early on the homepage, where hesitation actually happens, rather than buried in a policy page.",
         ["Authentic global table tennis brands", "Professional quality equipment",
          "Secure checkout", "Trusted by players"]),
        ("Product page improvements",
         "Equipment pages were reworked around the moment of decision &mdash; comparing specifications, then committing.",
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

    # Conversion rate, four consecutive months. Scale 0 - 2.00%, gridline at 1.00%.
    data = [("Nov", "0.66%", 33, "before"), ("Dec", "0.72%", 36, "before"),
            ("Jan", "1.26%", 63, "after"),  ("Feb", "1.56%", 78, "after")]
    bars = ""
    for i, (m, v, h, phase) in enumerate(data):
        bars += f"""<div class="bar bar--{phase}">
  <p class="bar__val">{v}</p>
  <div class="bar__col" style="--h:{h}%;--d:{i*150}ms"></div>
  <span class="bar__x">{m}</span>
</div>"""

    # Two single-series small multiples. Separate charts, separate scales — never
    # two measures on one axis.
    def mini(cap, rows):
        b = ""
        for i, (m, v, h, phase) in enumerate(rows):
            b += f"""<div class="bar bar--{phase}">
  <p class="bar__val">{v}</p>
  <div class="bar__col" style="--h:{h}%;--d:{i*160}ms"></div>
  <span class="bar__x">{m}</span>
</div>"""
        return f"""<div class="mini" data-reveal="fade">
  <p class="mini__cap">{cap}</p>
  <div class="bars bars--two">{b}</div>
</div>"""

    minis = (mini("Visitors &mdash; December vs January",
                  [("Dec", "36.8k", 100, "before"), ("Jan", "20.5k", 56, "after")]) +
             mini("Orders &mdash; December vs January",
                  [("Dec", "686", 100, "before"), ("Jan", "669", 98, "after")]))

    rows = [
        ("Nov 1&ndash;30", "Before", "39.4k", "0.66%", "&mdash;", False),
        ("Dec 1&ndash;30", "Before", "36.8k", "0.72%", "686", True),
        ("Jan 1&ndash;30", "After", "20.5k", "1.26%", "669", False),
        ("Feb 1&ndash;28", "After", "16.8k", "1.56%", "&mdash;", False),
    ]
    trows = ""
    for period, phase, vis, cvr, orders, split in rows:
        cls = ' class="is-split"' if split else ""
        hl = ' class="num hl"' if phase == "After" else ' class="num"'
        trows += (f'<tr{cls}><td>{period}</td><td class="phase">{phase}</td>'
                  f'<td class="num">{vis}</td><td{hl}>{cvr}</td>'
                  f'<td class="num">{orders}</td></tr>')

    stats = [
        ("+75%", "Conversion rate, December to January &mdash; the first full month after launch", True),
        ("+117%", "Conversion rate, December to February", False),
        ("&minus;44%", "Visitors over the same period, December to January", False),
        ("&minus;2.5%", "Orders over that period &mdash; 686 to 669", False),
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
        <p class="lead lead--wide" data-reveal data-onload>A Shopify store selling professional table tennis equipment &mdash;
        blades, rubbers and accessories from global brands. I handled the UX restructuring, theme customisation
        and conversion work. Conversion rate went from 0.72% to 1.26% in the first full month after launch,
        and to 1.56% the month after that.</p>
      </div>
    </div>
    {livebtn("https://tabletennisstore.us/", "Open the live store")}
    {meta_rail([
        ("Client", "Table Tennis USA"),
        ("Sector", "Table tennis ecommerce"),
        ("Platform", "Shopify"),
        ("Role", "UX design, theme customisation, CRO, SEO"),
        ("Live site", '<a href="https://tabletennisstore.us/" target="_blank" rel="noopener">tabletennisstore.us &#8599;</a>'),
        ("Measured", "4 consecutive months, before and after"),
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
        <p>TableTennisStore.us sells professional table tennis equipment &mdash; blades, rubbers and accessories
        from global brands &mdash; to players across the United States and beyond.</p>
        <p>The store needed structural improvements to make navigation clearer, improve trust signals and increase
        product discovery, <strong>while keeping the Shopify architecture scalable</strong>. It was not a business
        that needed a prettier website. It was a business losing orders inside its own catalogue.</p>
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
    {shead("03", "Proof",
           ["The numbers,", "all four months."],
           "Two months before the redesign and two months after it, as recorded in the store&rsquo;s analytics. The full picture, including the part that is less flattering.")}
    <div class="chartwrap">
      <div class="chart" data-reveal="fade">
        <figure class="chartfig chartfig--marked">
          <figcaption>Site-wide conversion rate &mdash; Table Tennis USA</figcaption>
          <div class="plot">
            <div class="yaxis" aria-hidden="true"><span>2.00%</span><span>1.00%</span><span>0</span></div>
            <div class="bars bars--four">
              <div class="bars__mark" aria-hidden="true"><span>Redesign launched</span></div>
              {bars}
            </div>
          </div>
        </figure>
      </div>
      <div class="chart__note" data-reveal>
        <p class="note">Conversion rate roughly doubled across the launch: 0.72% in December to 1.26% in January,
        the first full month on the new store, then 1.56% in February. Before the redesign the same metric had moved
        only from 0.66% to 0.72%.</p>
      </div>
    </div>

    <div class="statrow" style="margin-top:clamp(2.4rem,5vw,4rem)" data-stagger>{statrow}</div>

    <div style="margin-top:clamp(2.8rem,5.5vw,4.4rem)" data-reveal>
      <p class="mono eyebrow" style="margin-bottom:1.6rem">Traffic fell. Orders did not.</p>
      <div class="minis">{minis}</div>
      <p class="note" style="margin-top:.6rem">Two separate measures, each on its own scale. Bars are proportional
      within each chart; the figures above them are the recorded values.</p>
    </div>

    <div style="margin-top:clamp(2.6rem,5vw,4rem)" data-reveal>
      <p class="mono eyebrow" style="margin-bottom:1.2rem">All four months, in full</p>
      <div class="dtable-wrap">
        <table class="dtable">
          <thead><tr><th>Period</th><th>Phase</th><th class="num">Visitors</th><th class="num">Conversion rate</th><th class="num">Orders</th></tr></thead>
          <tbody>{trows}</tbody>
        </table>
      </div>
    </div>

    <div class="split" style="margin-top:clamp(2.4rem,5vw,3.6rem)">
      <div class="split__l" data-reveal>
        <h3 class="display h3" style="max-width:18ch">Nearly the same orders, from 44% fewer visitors.</h3>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>Two things are true in these figures and both belong here. Conversion rate roughly doubled after the
        redesign. Traffic also fell over the same period &mdash; 36.8k visitors in December to 20.5k in January.</p>
        <p><strong>Which is why orders are the number worth looking at: 686 in December, 669 in January.</strong>
        Almost the same number of orders from 44% fewer visitors. The store was converting the traffic it had far
        more efficiently than before.</p>
        <p>Conversion rate on its own does not isolate every contributing factor &mdash; traffic mix and seasonality
        move month to month, and a smaller, higher-intent audience converts better by definition. Visitors,
        conversion rate and orders are each reported here as the store&rsquo;s analytics recorded them. What four
        consecutive months show consistently is direction: 0.66% to 0.72% before the redesign, 1.26% to 1.56%
        after it. No revenue figure is claimed.</p>
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
        <p>It changed how people understand the store, how much they trust the brand, how quickly they find a
        product, and how easily they finish buying it. Those four things are what a conversion rate is measuring.</p>
        <p>By improving structure, trust and the purchase flow, the store became measurably better at turning
        visitors into customers &mdash; <strong>and it stayed a Shopify store the client can run and extend
        themselves.</strong></p>
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
                "Shopify UX optimisation and conversion-focused redesign for Table Tennis USA. Conversion rate "
                "0.72% to 1.26% in the first full month after launch, 1.56% the month after — with orders holding "
                "steady on 44% fewer visitors.",
                "work.html", body, og_img="assets/img/og-ttusa.jpg")


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
            "GEWO USA is the American arm of GEWO, a table tennis equipment manufacturer. It was established by "
            "Ben Nisbet, a long-time table tennis equipment specialist, in partnership with professional player "
            "Mishel Levinski &mdash; on the principle that, in their words, building a better foundation "
            "&ldquo;with the eyes of a player&rdquo; is what the youth and professional levels of the sport need.",
            "That changes the design brief. A multi-brand retailer helps a customer choose <em>between</em> brands. "
            "A manufacturer&rsquo;s store has to carry the brand itself &mdash; its range logic, its sponsored players, "
            "its reason for existing &mdash; while still functioning as a shop. Every layout decision on the site is "
            "a negotiation between those two jobs."]),
        beat("02", "Navigation built on how equipment is classified, not how it is stocked", [
            "The menu follows the sport&rsquo;s own taxonomy rather than a generic shop structure &mdash; twenty-seven "
            "subcategories under six headings, mapped above. A player who already knows they want long pips reaches "
            "them in two moves.",
            "That is the entire point: the menu is doing the work a shop assistant would do, and it can only do it "
            "if whoever built it understands the categories."]),
        beat("03", "Collection tiles that set expectations before the click", [
            "The homepage carries collection tiles showing how many products sit behind each one. Fifty blades and "
            "fifty rubbers is a serious range; seven pairs of shoes is not, and there is no reason to pretend "
            "otherwise.",
            "Showing the count costs nothing and stops a customer bouncing off a category that was never going to "
            "have what they wanted."]),
        beat("04", "Four claims a manufacturer can make that a reseller cannot", [
            "A rotating trust strip sits directly under the hero: pro tested, match-ready consistency, premium "
            "materials, precision engineered. Those are manufacturing claims, not retail ones &mdash; a reseller has "
            "no standing to make them.",
            "Placing them immediately after the hero, before the catalogue, frames everything below as the "
            "manufacturer&rsquo;s own equipment rather than another storefront selling the same boxes."]),
        beat("05", "Proof placed after the catalogue, not before it", [
            "The site features its sponsored players &mdash; Alex Averin, Kokou Fanny, Felix Lartey, Romain Lorentz, "
            "Amoolya Menon and Kazeem Makanjuola &mdash; but positions them below the product sections rather than "
            "above them.",
            "A visitor who arrived to buy rubber does not want to meet the roster first. A visitor who has been "
            "scrolling for two minutes is exactly the person for whom &lsquo;these players use this equipment&rsquo; "
            "is the closing argument."]),
        beat("06", "Combo specials, for the customer who does not yet know what to ask", [
            "The hardest customer in table tennis retail is the one who does not know which blade goes with which "
            "rubber. The store answers that with combo specials &mdash; pre-matched setups carried as their own "
            "navigation category, their own homepage section and their own collection tile, with the saving "
            "shown as a percentage.",
            "It converts an intimidating configuration problem into a single product decision, and it does it "
            "without hiding the components from the players who do want to choose them."]),
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
        <p class="lead lead--wide" data-reveal data-onload>The US store of a table tennis equipment manufacturer.
        Blades, rubbers, tables, balls, apparel and maintenance items sold to players from beginner to elite &mdash;
        by a brand that also has to look like a brand. Design work on a store carrying two jobs at once.</p>
      </div>
    </div>
    {livebtn("https://www.gewousa.com/", "Open the live store")}
    {meta_rail([
        ("Client", "GEWO USA"),
        ("Sector", "Manufacturer-owned ecommerce"),
        ("Platform", "Shopify"),
        ("Role", "Website design"),
        ("Live site", '<a href="https://www.gewousa.com/" target="_blank" rel="noopener">gewousa.com &#8599;</a>'),
        ("Published data", "None &mdash; see note"),
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
        <p>&ldquo;Your Game. Powered by GEWO&rdquo; sits at the top of the homepage; &ldquo;GEWO: the better way to
        play&rdquo; sits further down. Between them is a catalogue spanning shakehand and Chinese penhold blades,
        four categories of rubber, indoor and outdoor tables, tournament and training balls, apparel, footwear, and
        maintenance items down to blade sealer, edge tape, glue and cutting knives.</p>
        <p>Those are not one kind of purchase. <strong>Apparel is browsed. Rubber is specified. A table is
        researched. Edge tape is re-ordered.</strong> The structure of the store has to let each of those happen
        without forcing everyone down the same route &mdash; and without the brand story getting in the way of
        someone who came to buy glue.</p>
      </div>
    </div>
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

<section class="section">
  <div class="wrap">
    <div class="rail">
      <div class="rail__side" data-reveal="fade">
        <p class="mono mono--accent">Design decisions</p>
        <p class="mono" style="margin-top:.6rem">Six choices and the reasoning behind them</p>
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
          <p>There is no performance data I can publish for this project, so none is presented. The conversion
          figures on this site belong to the Table Tennis USA project and only to it. What GEWO USA demonstrates
          is a different problem solved &mdash; a brand-owned catalogue rather than a multi-brand retailer &mdash;
          and the design reasoning behind it. The store is live; judge the execution there.</p>
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
                "work.html", body, og_img="assets/img/og-gewo.jpg")


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
            "Paul David coaches table tennis. What he sells is time: in-home coaching, private lessons, group "
            "lessons and camp clinics &mdash; an hour or a day, at a stated price, with travel affecting some bookings.",
            "None of that belongs in a cart. Paul is paid in person, so a checkout would have added a step that "
            "does not exist in his business and would have to be maintained forever. The site was built with no "
            "online payments, which made the design question a different one entirely: <strong>how do you get "
            "someone from &lsquo;I want lessons&rsquo; to a message in his inbox, in as few steps as possible?</strong>"]),
        beat("02", "Four services, priced in the open", [
            "Each service carries its name, its duration, its price and a plain description of who it is for, with "
            "travel fees noted where they apply. Coaches routinely hide pricing and lose the enquiry to the "
            "uncertainty &mdash; the visitor assumes it is expensive, or assumes asking commits them to something.",
            "Publishing it does two jobs: it filters out the people who were never going to book, and it gives "
            "everyone else a reason to act now rather than &lsquo;think about it&rsquo;."]),
        beat("03", "One booking action per service", [
            "Every service has its own <em>Book now</em> button, and each one opens a pre-addressed email rather "
            "than dropping the visitor into a generic contact page. The service they picked is already the subject "
            "of the message.",
            "No form to build, no form to maintain, no submissions disappearing into a plugin &mdash; and no "
            "ambiguity on Paul&rsquo;s end about which service the enquiry is for."]),
        beat("04", "The equipment page, which is really a partner path", [
            "Rather than build a shop Paul would have to run, the site carries a <em>Recommended Equipment</em> page "
            "with three setups tiered by level: the GEWO CS Energy Control for youth starting out, the CS Energy "
            "Carbon Pro for adults and kids wanting more speed, and the Xolo Offensive combo with Neoflexx rubber "
            "for players serious about developing their game.",
            "Each links through to GEWO USA &mdash; a properly stocked store I had already worked on &mdash; "
            "and carries a coach-specific code, PDCGEWO, for 12% off. <strong>The student gets a straight answer "
            "and a discount; the coach gets a credible recommendation and zero inventory.</strong>"]),
        beat("05", "Built to be handed over", [
            "The unglamorous half of the project: services structured so Paul can edit them himself, payment "
            "configured to match how he actually gets paid, the domain connected, and ownership transferred to him "
            "at the end.",
            "A site the client cannot change is a site that goes stale within a year and quietly stops "
            "representing the business."]),
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
        <p class="lead lead--wide" data-reveal data-onload>A table tennis coach with four services to sell and no cart
        to sell them in. The job was to turn coaching hours into a site that produces enquiries, connect his students
        to equipment without making him a retailer, and leave the whole thing in his hands.</p>
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
    <p class="note" style="margin-top:1.4rem" data-reveal>Travel fees may apply depending on location &mdash; stated on
    the page rather than raised after someone has already committed.</p>
  </div>
</section>

<section class="section" style="background:var(--ink-2);border-block:1px solid var(--line)">
  <div class="court" aria-hidden="true"></div>
  <div class="wrap" style="position:relative;z-index:2">
    {shead("01", "The booking path",
           ["Five steps, no form,", "no checkout."],
           "The entire design problem for a coaching site is the distance between wanting a lesson and the coach knowing about it. Every step that can be removed, is.")}
    {bookflow}
    <p class="note" style="margin-top:1.8rem" data-reveal>A conventional contact form would add two steps &mdash;
    fill in fields, wait for a confirmation &mdash; plus a plugin to maintain and a place for enquiries to go missing.
    The email opens already knowing which service was chosen.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("02", "The equipment path",
           ["Answering the", "question every coach", "gets asked."],
           "A coach who says &lsquo;buy whatever&rsquo; loses authority. A coach who runs a shop loses time. This is the third option.")}
    {kitflow}
    <p class="note" style="margin-top:1.8rem" data-reveal>The student gets a specific answer matched to their level
    and a reason to act on it. The coach carries no stock, no shipping and no returns. Two of my clients end up
    worth more to each other than either was alone.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="rail">
      <div class="rail__side" data-reveal="fade">
        <p class="mono mono--accent">Design decisions</p>
        <p class="mono" style="margin-top:.6rem">Five choices and the reasoning behind them</p>
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
          that the same thinking applies away from ecommerce: understand how the business actually takes money,
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
                "work.html", body, og_img="assets/img/og-paul.jpg")


# ================================================================= SERVICES ==
def build_services():
    svcs = [
        ("01", "Website design from scratch",
         "For a table tennis business with no website, or one whose site was never really designed &mdash; a placeholder, "
         "a template that was never finished, a page that exists only because something had to.",
         "Brands launching direct-to-consumer, new clubs and academies, coaches, event organisers, distributors "
         "putting a proper face on an established business.",
         ["Structure and page architecture", "Visual design and design system",
          "Full build and launch", "Mobile and performance work",
          "Domain and DNS setup", "Handover so you can run it"]),
        ("02", "Ecommerce website design",
         "For businesses selling equipment. The catalogue is the site: how it is organised, how a customer narrows "
         "it down, and what a product page has to prove before someone spends money on a blade they cannot hold.",
         "Equipment brands, multi-brand retailers, manufacturer-owned stores, distributors selling direct and "
         "clubs running a pro shop.",
         ["Catalogue and collection architecture", "Product page design for specifications",
          "Filtering and search behaviour", "Cart and checkout flow",
          "Shopify theme customisation and Liquid", "Shipping, currency and region handling"]),
        ("03", "Website redesign",
         "For a site that works but is holding the business back. A redesign has to move the business forward without "
         "throwing away what is already earning &mdash; search rankings, product data, URL structure and the habits of "
         "customers who already know their way around.",
         "Established stores that have outgrown their design, brands after a rebrand, and businesses whose site "
         "was built years ago by someone no longer available.",
         ["Audit of the existing site", "Redesign against the current buying path",
          "URL and content preservation", "Migration without losing product data",
          "Before-and-after measurement", "Staged launch"]),
        ("04", "Conversion-focused optimisation",
         "For a site that gets traffic and does not turn enough of it into orders. This is not a redesign &mdash; it is "
         "work on the specific points where people decide to leave, followed by measurement.",
         "Any table tennis business with real traffic and a conversion rate that has stopped moving, whether or not "
         "I built the site.",
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
        <p class="lead lead--wide" data-reveal data-onload>Four services. Most projects are one of them. Some run two together &mdash;
        a redesign that is really a redesign plus conversion work, or a new build for a brand that is also
        launching a store.</p>
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
           "Nothing is designed before the catalogue and the buying path are understood. That order is not negotiable, because getting it wrong is what produces a beautiful site that does not sell.")}
    <div class="steps" data-stagger>
      <div class="step" data-reveal><p class="step__no mono mono--accent">01</p><h3 class="step__t">Learn the catalogue</h3><p class="step__d">What you sell, how it is organised, what customers ask before buying, and where the money actually comes from.</p></div>
      <div class="step" data-reveal><p class="step__no mono mono--accent">02</p><h3 class="step__t">Map the buying path</h3><p class="step__d">The route from arrival to completed order or enquiry, written out step by step, with the stalling points marked.</p></div>
      <div class="step" data-reveal><p class="step__no mono mono--accent">03</p><h3 class="step__t">Design and build</h3><p class="step__d">Design that follows the map, then a working site &mdash; built, tested on real devices, and launched.</p></div>
      <div class="step" data-reveal><p class="step__no mono mono--accent">04</p><h3 class="step__t">Measure and refine</h3><p class="step__d">Conversion and behaviour after launch, and changes made on the evidence rather than on preference.</p></div>
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
        <p>Plenty of businesses arrive asking for a redesign when the real problem is three product pages and a
        checkout step. Others ask for conversion work when the site underneath cannot support it. Those are
        different jobs with different costs, and it is worth knowing which one you have before anyone quotes you.</p>
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
        ("Proof over adjectives", "A portfolio should carry numbers where numbers exist and say so plainly where they do not. Everything on this site follows that rule, including the parts that would look better if it did not &mdash; the Table Tennis USA traffic figures among them."),
        ("The catalogue comes first", "Design decisions made before anyone understands the products are guesses. In this sport the products are technical and the guesses are usually wrong."),
        ("Build it, do not just draw it", "On Table Tennis USA I did the UX design and the Shopify implementation. I hand over working websites, not concept files for someone else to interpret and dilute."),
        ("Leave the client in control", "Ownership transferred, domain connected, structure editable. A site the owner cannot change is a site that goes stale within a year."),
    ]
    cards = "".join(f"""<article class="card" style="grid-column:span 6" data-reveal>
  <p class="card__no mono">{i+1:02d}</p>
  <h3 class="h4">{t}</h3>
  <p class="card__body">{d}</p>
</article>""" for i, (t, d) in enumerate(principles))

    human = [
        ("Study", "Doctor of Pharmacy",
         "I am a PharmD candidate at Obafemi Awolowo University. Pharmacy is a degree in reading technical specifications carefully and getting the details exactly right &mdash; which turns out to be most of this job too."),
        ("Chess", "Grandmaster",
         "The thing most people do not know about me. Chess is pattern recognition and thinking several moves past the obvious one, under time pressure. It is closer to conversion work than it sounds."),
        ("Gadgets", "Phones, laptops, cameras",
         "My genuine obsession. I want to see them, hold them, unbox them. Caring how a physical object feels in the hand is not unrelated to caring how an interface feels under a thumb."),
        ("Base", "Nigeria, working worldwide",
         "I am in Nigeria and my clients are not. Everything runs over email and shipped work, which is why this site leads with evidence rather than a headshot and a promise."),
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
    <div style="margin-top:clamp(1.4rem,3vw,2.4rem)">
      {lines('A designer who', 'picked <span class="ital accent">one</span> sport', 'on purpose.', onload=True)}
    </div>
    <div class="hero__body">
      <div class="hero__lead">
        <p class="lead lead--wide" data-reveal data-onload>AKINTAYO is the working name of Akingbehin Akintayo &mdash; an
        ecommerce web designer in Nigeria, working with table tennis businesses internationally.</p>
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
        <p>Most web designers work across whatever comes in &mdash; a dentist, a law firm, a clothing brand, a gym.
        It is a reasonable way to make a living and it has one structural cost: every project begins with the
        designer learning the client&rsquo;s market from zero, on the client&rsquo;s time and the client&rsquo;s money.</p>
        <p>I removed that cost by going narrow. Table tennis is a real market with real money in it &mdash;
        manufacturers, multi-brand retailers, distributors, clubs, academies, coaches, tournaments &mdash; and very
        little of it is served by people who understand both the sport&rsquo;s equipment and how an ecommerce store
        actually converts.</p>
        <p><strong>So that is the business.</strong> Two table tennis ecommerce stores and one coaching practice so
        far, with the work and the numbers documented on this site.</p>
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
        <h2 class="bigquote" style="margin-top:1.2rem">Table tennis is the specialism. It is not the extent of the experience.</h2>
      </div>
      <div class="split__r prose" data-reveal data-delay="120">
        <p>I have worked in ecommerce for a long time, and not only in this sport. The most recent example outside
        it is <strong>ORIMI</strong> &mdash; a fine jewellery house selling made-to-order pieces in solid 18K gold with
        natural diamonds and precious gemstones, built on Shopify and shipping to more than twenty-five countries.</p>
        <p>Its positioning is &ldquo;sculptural fine jewellery, rooted in Yoruba philosophy&rdquo;, with collections
        named AJ&Eacute;, IN&Aacute; and &Agrave;WO. A five-figure ring and a $40 rubber sheet are not the same sale,
        but they are the same discipline: make the thing legible, make it trustworthy, and get out of the way at the
        moment someone decides to buy.</p>
        <p><a class="tlink" href="https://orimijewelry.com/" target="_blank" rel="noopener">orimijewelry.com &#8599;</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("&mdash;", "How I work",
           ["Four things I do not", "compromise on."])}
    <div class="deck" data-stagger>{cards}</div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="split__l" data-reveal>
        <p class="mono eyebrow">Working in</p>
        <h2 class="display h3" style="margin-top:1.2rem;max-width:14ch">What I build with.</h2>
        <p style="color:var(--fg-2);margin-top:1.2rem;max-width:34ch">Most table tennis stores run on Shopify, so most
        of my ecommerce work does too &mdash; theme customisation and Liquid rather than fighting the platform.</p>
      </div>
      <div class="split__r" data-reveal data-delay="120">
        <div class="stack">{pills}</div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("&mdash;", "Off the clock",
           ["The rest of it."],
           "You are hiring a person, not a studio. It is reasonable to want to know who that is before you send money across an ocean.")}
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
        <p>There is no account manager between you and the person doing the work, and nothing is handed to a junior
        after the pitch. You email me, I answer, I build it.</p>
        <p>That is a limit as much as a feature: I take a small number of projects, and if the timing does not work
        I will tell you rather than stretch a schedule you are paying for.</p>
      </div>
    </div>
  </div>
</section>

{cta_block("Working in table tennis? Let&rsquo;s talk.",
           "One email with your site and the problem is enough to start. I read and reply to every one myself.")}
"""
    return page("about.html", "About — AKINTAYO",
                "Akingbehin Akintayo (AKINTAYO) — ecommerce web designer in Nigeria specialising in the table "
                "tennis industry, with wider ecommerce work including the ORIMI fine jewellery store.",
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
        <p class="lead lead--wide" data-reveal data-onload>No forms, no calls to book, no chat widget. Email keeps the first
        conversation in writing, which is where project details belong &mdash; and it means you get a considered
        answer rather than a scheduling link.</p>
      </div>
    </div>
    <div style="margin-top:clamp(2.4rem,5vw,4rem)" data-reveal data-onload>
      <a class="cta__mail" href="{mail()}">{EMAIL}</a>
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
          <a class="btn btn--ball" data-magnet="0.22" href="{mail('Website project enquiry', 'My website: %0D%0AMy business: %0D%0AWhat is not working: %0D%0ATimeline: %0D%0A')}">
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
      <div class="step" data-reveal><p class="step__no mono mono--accent">02</p><h3 class="step__t">I look properly</h3><p class="step__d">I go through the site before replying, and tell you what I think the actual problem is &mdash; including if it is not one I should be paid to fix.</p></div>
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
      <a class="btn btn--ball" href="work.html" data-magnet="0.22"><span>See the work</span>{ARROW}</a>
    </div>
  </div>
</section>
"""
    return page("404.html", "Page not found — AKINTAYO",
                "That page does not exist.", "./", body)


# ==================================================================== EXTRAS ==
def build_extras():
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN)

    pages = ["", "work.html", "table-tennis-usa.html", "gewo-usa.html",
             "paul-david.html", "services.html", "about.html", "contact.html"]
    urls = "".join(
        '  <url><loc>%s/%s</loc><priority>%s</priority></url>\n' % (
            DOMAIN, p, "1.0" if p == "" else ("0.9" if "usa" in p or p == "work.html" else "0.8"))
        for p in pages)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + urls + '</urlset>\n')

    favicon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
               '<rect width="32" height="32" fill="#08090b"/>'
               '<circle cx="16" cy="16" r="7" fill="#ff5a1f"/></svg>')
    with open(os.path.join(OUT, "assets/img/favicon.svg"), "w") as f:
        f.write(favicon)


if __name__ == "__main__":
    built = [build_home(), build_work(), build_ttusa(), build_gewo(),
             build_paul(), build_services(), build_about(), build_contact(), build_404()]
    build_extras()
    print("Built:", ", ".join(built))
