#!/usr/bin/env python3
"""Generate one SEO-optimised tow-truck landing page per Townsville suburb.

Each page targets the keywords "tow truck <suburb>" and "towing <suburb>",
includes unique local context (landmarks/streets), a LocalBusiness JSON-LD
block scoped to the suburb, and shared header/footer/nav.

Run:  python3 generate-suburb-pages.py
Then: open the generated tow-truck-*.html files (one per suburb).
"""

import re
from pathlib import Path

SUBURBS = [
    # group, name, postcode, response, blurb (local context — keep unique)
    ("CBD & Inner", "Townsville City", "4810", "~15 mins",
     "the CBD core — Flinders Street, the Strand, Reef HQ, Maritime Museum and the Townsville ferry terminal. We run jobs through the city centre constantly, day and night."),
    ("CBD & Inner", "North Ward", "4810", "~15 mins",
     "the Strand, Jezzine Barracks, Rowes Bay foreshore and the base of Castle Hill. North Ward is our most-frequented suburb after the CBD."),
    ("CBD & Inner", "South Townsville", "4810", "~15 mins",
     "the Ross Creek waterfront, port precinct and Sealink ferry terminal. We're across the Dean Street and Victoria Bridge approaches every day."),
    ("CBD & Inner", "West End", "4810", "~15 mins",
     "the inner-west pocket between Flinders Street West and Castle Hill — Ingham Road, Eyre Street, the Townsville cemetery."),
    ("CBD & Inner", "Belgian Gardens", "4810", "~18 mins",
     "the Townsville University Hospital approach, Pallarenda Road and the Cape Pallarenda end of the city."),
    ("CBD & Inner", "Castle Hill", "4810", "~18 mins",
     "the famous 286 m granite monolith and the streets clinging to its slopes — Stanton Terrace, Mount Stuart Road, Hillside Crescent."),
    ("CBD & Inner", "Hyde Park", "4812", "~18 mins",
     "Charters Towers Road, the Stockland Hyde Park precinct and the southern fringe of the city centre."),
    ("CBD & Inner", "Pimlico", "4812", "~18 mins",
     "the Mater Private Hospital strip, Fulham Road and the Pimlico shopping precinct."),
    ("CBD & Inner", "Hermit Park", "4812", "~20 mins",
     "Charters Towers Road shops, Hugh Street and the inner-south side of the river."),
    ("CBD & Inner", "Mysterton", "4812", "~18 mins",
     "the small inner-south pocket bounded by Charters Towers Road and Hugh Street."),

    ("Western Suburbs", "Aitkenvale", "4814", "~22 mins",
     "Stockland Townsville, Domain Central, Ross River Road and the Aitkenvale strip — the busiest carparks in town and one of our top breakdown call-out areas."),
    ("Western Suburbs", "Currajong", "4812", "~22 mins",
     "the Currajong shops, Ross River Road frontage and the schools precinct."),
    ("Western Suburbs", "Mundingburra", "4812", "~22 mins",
     "Charters Towers Road, the Mundingburra State School area and Wills Street."),
    ("Western Suburbs", "Cranbrook", "4814", "~22 mins",
     "the Cranbrook shopping centre, Ross River Road south and the residential streets either side of Nathan Street."),
    ("Western Suburbs", "Vincent", "4814", "~25 mins",
     "Vincent Plaza, Fulham Road and the streets running to the Ring Road."),
    ("Western Suburbs", "Heatley", "4814", "~25 mins",
     "Heatley shops, Bayswater Road and the rugby league fields."),
    ("Western Suburbs", "Garbutt", "4814", "~22 mins",
     "the Townsville Airport approach, Ingham Road industrial precinct, Stockland car yards and the airport carparks."),
    ("Western Suburbs", "Rosslea", "4812", "~22 mins",
     "the inner-south enclave between the river and Charters Towers Road."),
    ("Western Suburbs", "Gulliver", "4812", "~22 mins",
     "the small residential pocket bounded by Charters Towers Road, Anne Street and Bayswater Road."),
    ("Western Suburbs", "Oonoonba", "4811", "~22 mins",
     "the southern bank of the Ross River — Bowen Road bridge, the racecourse approach and Vickers Road."),

    ("Riverside & Idalia", "Idalia", "4811", "~25 mins",
     "the planned riverside community south of the Ross River — Idalia Boulevard, Riverside Boulevard and the Cunningham Street precinct."),
    ("Riverside & Idalia", "Stuart", "4811", "~25 mins",
     "the Stuart Highway corridor, Stuart Drive industrial yards and the southern Townsville approaches."),
    ("Riverside & Idalia", "Wulguru", "4811", "~25 mins",
     "the south-Townsville suburb either side of the Bruce Highway, Stuart Drive and the Lavarack Barracks gates."),
    ("Riverside & Idalia", "Cluden", "4811", "~25 mins",
     "the Cluden Park racetrack precinct and the southern Bruce Highway frontage."),
    ("Riverside & Idalia", "Annandale", "4814", "~22 mins",
     "the Annandale Central shops, the Lakes precinct and the streets along Ross River Parkway."),
    ("Riverside & Idalia", "Douglas", "4814", "~25 mins",
     "James Cook University, the Townsville University Hospital, IIB and the Douglas student housing precinct."),
    ("Riverside & Idalia", "Murray", "4812", "~22 mins",
     "the Murray Sports Complex, Sports Reserve and the residential streets near JCU."),
    ("Riverside & Idalia", "Mount Stuart", "4811", "~28 mins",
     "the radio-tower hilltop suburb overlooking Townsville from the south."),

    ("Thuringowa", "Mount Louisa", "4814", "~28 mins",
     "the suburb's hill estates, Mount Louisa Drive and the streets ringing the Bohle and Hervey Range Road approaches."),
    ("Thuringowa", "Kirwan", "4817", "~28 mins",
     "Riverway, the Kirwan shopping centres, Thuringowa Drive and Townsville's biggest residential population pocket."),
    ("Thuringowa", "Thuringowa Central", "4817", "~28 mins",
     "the Willows Shopping Centre, Thuringowa Drive and the heart of Townsville's western city."),
    ("Thuringowa", "Condon", "4815", "~30 mins",
     "the Condon shopping precinct, Hervey Range Road and the streets around the Stuart Drive overpass."),
    ("Thuringowa", "Rasmussen", "4815", "~30 mins",
     "the southern Thuringowa pocket bounded by the Ross River and Riverway Drive."),
    ("Thuringowa", "Kelso", "4815", "~32 mins",
     "the suburban edge of Thuringowa — Kelso Drive, Loam Island Drive and the streets running to Hervey Range."),
    ("Thuringowa", "Pinnacles", "4815", "~32 mins",
     "the Hervey Range fringe pocket on the western edge of Townsville."),
    ("Thuringowa", "Bohle Plains", "4817", "~30 mins",
     "the industrial-residential mix off Hervey Range Road and the western side of the Bohle River."),
    ("Thuringowa", "Shaw", "4818", "~30 mins",
     "the Shaw residential estates west of Bohle Plains."),
    ("Thuringowa", "Alice River", "4817", "~32 mins",
     "the outer-west residential pocket along the Alice River."),

    ("Northern Beaches", "Burdell", "4818", "~30 mins",
     "the Burdell residential estates, North Shore precinct and Bruce Highway frontage."),
    ("Northern Beaches", "Mount Low", "4818", "~32 mins",
     "the Mount Low estates and the approach to Bushland Beach."),
    ("Northern Beaches", "Bushland Beach", "4818", "~32 mins",
     "the Bushland Beach Tavern, beach foreshore and the residential streets running from the Bruce Highway to the sand."),
    ("Northern Beaches", "Deeragun", "4818", "~32 mins",
     "the Deeragun shopping precinct, Mount Low Parkway and the Bruce Highway service centres."),
    ("Northern Beaches", "Saunders Beach", "4818", "~35 mins",
     "the Saunders Beach foreshore — a regular 4WD recovery spot for first-time beach drivers caught by the tide."),
    ("Northern Beaches", "Yabulu", "4818", "~38 mins",
     "the Yabulu residential pocket and the Yabulu refinery road approach."),
    ("Northern Beaches", "Black River", "4818", "~38 mins",
     "the Black River crossing, Northern Beaches estates and the Bruce Highway approach to Bluewater."),
    ("Northern Beaches", "Bluewater", "4818", "~40 mins",
     "the northern fringe of our service area — Bluewater Park, the Bruce Highway and the rural-residential streets."),

    ("Magnetic Island", "Magnetic Island", "4819", "By ferry",
     "Picnic Bay, Nelly Bay, Arcadia and Horseshoe Bay. Vehicle moves to and from the island are coordinated via the Sealink barge."),
]

NAV = """<div class="topbar">
  <div class="container">
    <span><span class="pulse"></span> Operating 24 hours · 7 days · Townsville</span>
    <span><a href="tel:+61409739332">📞 0409 739 332</a> · <a href="mailto:accounts@kwiktow.com.au">accounts@kwiktow.com.au</a></span>
  </div>
</div>

<header class="site-header">
  <nav class="nav" aria-label="Main">
    <a href="index.html" class="logo"><img class="logo-img" src="kwik-tow-logo.webp" alt="Kwiktow NQ logo"><span>Kwiktow NQ <small>Townsville Towing</small></span></a>
    <button class="menu-toggle" aria-label="Toggle menu">☰</button>
    <ul class="nav-links">
      <li><a href="index.html">Home</a></li>
      <li><a href="services.html">Services</a></li>
      <li><a href="service-areas.html">Service Areas</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="blog.html">Blog</a></li>
      <li><a href="faq.html">FAQ</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li><a href="tel:+61409739332" class="nav-cta">Call 0409 739 332</a></li>
    </ul>
  </nav>
</header>"""

FOOTER = """<footer>
  <div class="container">
    <div class="grid">
      <div>
        <div class="logo" style="margin-bottom:1rem"><img class="logo-img" src="kwik-tow-logo.webp" alt="Kwiktow NQ logo"><span>Kwiktow NQ <small>Townsville Towing</small></span></div>
        <p>Townsville's family-run 24/7 towing &amp; recovery specialists.</p>
        <p><strong style="color:var(--white)">📞 0409 739 332</strong><br><a href="mailto:accounts@kwiktow.com.au">accounts@kwiktow.com.au</a></p>
      </div>
      <div><h4>Services</h4><ul>
        <li><a href="services.html#tilt-tray">Tilt Tray</a></li>
        <li><a href="services.html#accident">Accident Recovery</a></li>
        <li><a href="services.html#breakdown">Breakdown</a></li>
        <li><a href="services.html#heavy">Heavy Vehicle</a></li>
        <li><a href="services.html#offroad">4WD Recovery</a></li>
        <li><a href="services.html#boat">Boat Transport</a></li>
      </ul></div>
      <div><h4>Townsville Suburbs</h4><ul>
        <li><a href="service-areas.html#cbd">CBD &amp; Inner</a></li>
        <li><a href="service-areas.html#western">Western Suburbs</a></li>
        <li><a href="service-areas.html#riverside">Riverside &amp; Idalia</a></li>
        <li><a href="service-areas.html#northern-beaches">Northern Beaches</a></li>
        <li><a href="service-areas.html#thuringowa">Thuringowa</a></li>
        <li><a href="service-areas.html#magnetic-island">Magnetic Island</a></li>
      </ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="about.html">About</a></li>
        <li><a href="blog.html">Blog</a></li>
        <li><a href="faq.html">FAQ</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul></div>
    </div>
    <p class="copyright">© <span id="yr"></span> Kwiktow NQ — Towing &amp; Recovery in Townsville, QLD.</p>
  </div>
</footer>

<a href="tel:+61409739332" class="float-call" aria-label="Call Kwiktow NQ">📞</a>

<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>
<script src="assets/js/main.js"></script>"""


def slug(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def render(group, name, postcode, response, blurb):
    s = slug(name)
    file = f"tow-truck-{s}.html"
    url = f"https://kwiktownq.com.au/{file}"
    nearby_links = ""
    same_group = [x for x in SUBURBS if x[0] == group and x[1] != name]
    nearby_chips = "\n        ".join(
        f'<a class="chip" href="tow-truck-{slug(x[1])}.html">{x[1]}</a>' for x in same_group[:6]
    )

    schema = (
        '{'
        '"@context":"https://schema.org",'
        '"@type":"AutomotiveBusiness",'
        f'"name":"Kwiktow NQ — Tow Truck {name}",'
        f'"url":"{url}",'
        '"image":"https://kwiktownq.com.au/KwikTow-hero-img.webp",'
        '"telephone":"+61-409-739-332",'
        '"email":"accounts@kwiktow.com.au",'
        '"priceRange":"$$",'
        f'"description":"24/7 tow truck and towing service for {name}, Townsville QLD {postcode}. Tilt tray, accident recovery, breakdown, heavy vehicle and 4WD recovery — local, fast, fully insured.",'
        '"address":{"@type":"PostalAddress",'
        f'"addressLocality":"{name}","addressRegion":"QLD","postalCode":"{postcode}","addressCountry":"AU"' + '},'
        f'"areaServed":' + '{"@type":"Place",' + f'"name":"{name}, Townsville QLD"' + '},'
        '"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}'
        '}'
    )

    html = f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Tow Truck {name} | 24/7 Towing {name} Townsville | Kwiktow NQ</title>
<meta name="description" content="Need a tow truck in {name}? Kwiktow NQ provides 24/7 towing in {name}, Townsville {postcode} — tilt tray, accident, breakdown, heavy vehicle &amp; 4WD recovery. Average response {response}. Call 0409 739 332." />
<meta name="keywords" content="tow truck {name}, towing {name}, tow truck {name} Townsville, towing {name} Townsville, tilt tray {name}, breakdown towing {name}, accident towing {name}, Kwiktow NQ" />
<meta name="robots" content="index, follow" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Tow Truck {name} — 24/7 Towing in {name}, Townsville" />
<meta property="og:description" content="Local tow truck service for {name} drivers. Tilt tray, accident, breakdown &amp; recovery — average response {response}." />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="https://kwiktownq.com.au/KwikTow-hero-img.webp" />
<meta name="theme-color" content="#ffb400" />
<link rel="icon" type="image/svg+xml" href="assets/images/favicon.svg" />
<link rel="stylesheet" href="assets/css/style.css" />

<script type="application/ld+json">{schema}</script>
</head>
<body>

{NAV}

<section class="page-header">
  <div class="container">
    <p class="breadcrumb"><a href="index.html">Home</a> / <a href="service-areas.html">Service Areas</a> / {name}</p>
    <h1>Tow Truck {name} — 24/7 Towing in {name}, Townsville</h1>
    <p style="max-width:720px;margin:1rem auto 0">Need a tow truck in {name}? Kwiktow NQ is the local 24/7 towing and recovery operator for {name} ({postcode}) and every surrounding street. Average response: <strong style="color:var(--primary)">{response}</strong>.</p>
    <div style="margin-top:1.5rem;display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap">
      <a href="tel:+61409739332" class="btn btn-primary">📞 Call 0409 739 332</a>
      <a href="contact.html#quote" class="btn btn-outline">Request a Quote</a>
    </div>
  </div>
</section>

<section>
  <div class="container split">
    <div>
      <span class="eyebrow" style="color:var(--primary);font-weight:800;text-transform:uppercase;font-size:.8rem;letter-spacing:.15em;">Local towing — {name}</span>
      <h2>Why {name} drivers call Kwiktow NQ</h2>
      <p>{name} is part of {blurb} If you've broken down, been in a prang, locked your keys in the car or bogged the 4WD nearby, we've almost certainly got a tow truck a few minutes away.</p>
      <ul class="checks">
        <li>24/7 dispatch — real Townsville locals on the phone, not a call centre</li>
        <li>Tilt tray fleet — safe for sedans, utes, 4WDs, EVs, prestige &amp; lowered cars</li>
        <li>Insurance-approved accident recovery, billed direct to your insurer</li>
        <li>Average response in {name}: <strong>{response}</strong></li>
        <li>Up-front quote on the phone — no surprise call-out fees</li>
      </ul>
      <a href="tel:+61409739332" class="btn btn-primary" style="margin-top:1rem">📞 0409 739 332</a>
    </div>
    <img src="KwikTow-hero-img.webp" alt="Kwiktow NQ tow truck servicing {name}, Townsville" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--radius)" loading="lazy">
  </div>
</section>

<section style="background:var(--darker)">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Services in {name}</span>
      <h2>Every type of tow truck job — covered</h2>
      <p>Whatever's gone wrong in {name}, we have the right truck and the right crew. All services available 24/7, every day of the year.</p>
    </div>
    <div class="grid cols-3">
      <article class="card">
        <div class="icon">🚗</div>
        <h3>Tilt Tray Towing in {name}</h3>
        <p>Damage-free flatbed transport for any passenger vehicle, including EVs, hybrids, AWDs and prestige cars.</p>
        <a class="more" href="services.html#tilt-tray">More on tilt tray →</a>
      </article>
      <article class="card">
        <div class="icon">🚨</div>
        <h3>Accident Recovery — {name}</h3>
        <p>Authorised accident tow operator. We work directly with RACQ, AAMI, Suncorp, NRMA, Allianz and others.</p>
        <a class="more" href="services.html#accident">Crash recovery →</a>
      </article>
      <article class="card">
        <div class="icon">🔧</div>
        <h3>Breakdown Towing in {name}</h3>
        <p>Won't start? Cooked it? We'll come to you in {name} and get the vehicle to your mechanic of choice.</p>
        <a class="more" href="services.html#breakdown">Breakdown service →</a>
      </article>
      <article class="card">
        <div class="icon">🚛</div>
        <h3>Heavy Vehicle Tows</h3>
        <p>Trucks, buses, large caravans, horse floats and trailers — heavy wreckers ready when {name} needs them.</p>
        <a class="more" href="services.html#heavy">Heavy towing →</a>
      </article>
      <article class="card">
        <div class="icon">🛻</div>
        <h3>4WD &amp; Off-Road Recovery</h3>
        <p>Bogged near {name}? Winches, snatch gear and recovery vehicles ready to go.</p>
        <a class="more" href="services.html#offroad">4WD recovery →</a>
      </article>
      <article class="card">
        <div class="icon">⛽</div>
        <h3>Roadside Assistance — {name}</h3>
        <p>Out of fuel, flat battery, flat tyre or locked out? Quick roadside fixes, on the spot.</p>
        <a class="more" href="services.html#roadside">Roadside help →</a>
      </article>
    </div>
  </div>
</section>

<section>
  <div class="container" style="max-width:880px">
    <div class="section-head">
      <span class="eyebrow">FAQ</span>
      <h2>Tow truck in {name} — what to know</h2>
    </div>

    <details class="faq-item" open>
      <summary>How fast can you get to {name}?</summary>
      <div class="answer">Average response in {name} is <strong>{response}</strong> from when we dispatch a truck. CBD and inner Townsville suburbs are usually quicker; outer-area times include drive time from the closest available truck.</div>
    </details>
    <details class="faq-item">
      <summary>How much does a tow truck cost in {name}?</summary>
      <div class="answer">Pricing depends on vehicle size, distance and time of day. We'll give you a clear, obligation-free quote on the phone before dispatching. Insurance jobs are billed direct to your insurer at no cost to you above any policy excess.</div>
    </details>
    <details class="faq-item">
      <summary>Can you tow my car after an accident in {name}?</summary>
      <div class="answer">Yes — we're an authorised accident tow operator. Call us once the scene is safe and police are dealt with. We'll deliver your vehicle to your nominated repairer or our secure compound.</div>
    </details>
    <details class="faq-item">
      <summary>Do you tow EVs and hybrids in {name}?</summary>
      <div class="answer">Yes. EVs and most hybrids must be transported on a tilt tray (flatbed) — never on two wheels. All Kwiktow NQ tilt trays are EV-safe.</div>
    </details>
  </div>
</section>

<section style="background:var(--darker)">
  <div class="container" style="max-width:880px;text-align:center">
    <h2>Nearby suburbs we also cover</h2>
    <p>Kwiktow NQ is Townsville's local tow truck operator across every suburb — including these neighbours of {name}:</p>
    <div class="chips" style="justify-content:center;margin-top:1rem">
        {nearby_chips}
    </div>
    <p style="margin-top:2rem"><a href="service-areas.html" class="btn btn-ghost">See full Townsville coverage →</a></p>
  </div>
</section>

<section class="cta-banner">
  <div class="container">
    <div>
      <h2 style="margin-bottom:.5rem">Need a tow in {name} right now?</h2>
      <p style="margin:0">Skip the waiting — pick up the phone.</p>
    </div>
    <div style="display:flex;gap:.75rem;flex-wrap:wrap">
      <a href="tel:+61409739332" class="btn btn-primary">📞 0409 739 332</a>
      <a href="contact.html" class="btn btn-outline">Send a Message</a>
    </div>
  </div>
</section>

{FOOTER}
</body>
</html>
"""
    Path(file).write_text(html)
    return file


def main():
    files = []
    for s in SUBURBS:
        files.append(render(*s))
    print(f"Generated {len(files)} suburb pages.")
    return files


if __name__ == "__main__":
    main()
