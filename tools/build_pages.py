"""Generate the hub's secondary pages: certificate viewers, project case studies and the HTML CV.

The site itself has no build step. This script only writes plain HTML files into the site folder,
so rerun it after changing any content below, then commit the output.
"""
import re
from datetime import date
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]  # the site root, one level up from tools/
# "Last updated" note in every footer: the date this script last ran. It also restamps the home page's footer,
# so rerun the script after editing index.html too.
TODAY = date.today()
UPDATED = f'Last updated <time datetime="{TODAY.isoformat()}">{TODAY:%B %Y}</time>'
CSS_V = 33
ORIGIN = 'https://darrenrosbon.github.io/DarrenRobsonHub/'

CERTS = [
    dict(slug='comptia-a-plus', title='CompTIA A+', issuer='IT Academy', meta='IT Academy course · March 2022',
         file='Darren-Robson-CompTIA-A-Plus.pdf', h=1978, redacted=True),
    dict(slug='comptia-network-plus', title='CompTIA Network+', issuer='IT Academy', meta='IT Academy course · N10-008 · July 2022',
         file='Darren-Robson-CompTIA-Network-Plus.pdf', h=1978, redacted=True),
    dict(slug='mcsa-windows-server-2016', title='MCSA Windows Server 2016', issuer='IT Academy', meta='IT Academy course · July 2022',
         file='Darren-Robson-MCSA-Windows-Server-2016.pdf', h=1978, redacted=True),
    dict(slug='ef-set-english-c2', title='EF SET English', issuer='EF SET', meta='Proficient (C2) · 85/100 · August 2026',
         file='Darren-Robson-EF-SET-English-C2.pdf', h=1981, redacted=False, verify='https://cert.efset.org/tcme9p'),
]

# Portfolio pieces are Darren's own products and concept sites, never client work.
PROJECTS = [
    dict(slug='chroma-gg', name='Chroma.GG', url='https://darrenrosbon.github.io/chroma-gg/', alt='Chroma.GG homepage',
         kind='Own product', what='Windows app + website', role='Solo design + build', status='In development',
         lede='A Windows tray app for PC gamers that switches display profiles per game, with a crosshair, performance HUD and instant replay in one process.',
         idea=['Gamers often run four or five separate tools for colour profiles, crosshairs, FPS counters and clip capture. Chroma.GG puts them behind one tray icon.',
               'It watches which window has focus, applies that game’s display profile the moment you alt-tab in, and puts the desktop back when you leave.'],
         points=['Event-driven focus tracking with SetWinEventHook. Nothing polls, so CPU use at idle stays near zero.',
                 'A 300 ms debounce stops Discord, Steam and RTSS overlays from making the screen flicker.',
                 'Six colour axes per game, written to the GPU’s output ramp so they show up in recordings too.',
                 'An instant-replay buffer encoded on the GPU (DXGI to NVENC), with a library, player and trimmer.',
                 'A product site with a working in-browser demo: drag the sliders, move the HUD and switch crosshairs.']),
    dict(slug='occlude', name='occlude.', url='https://darrenrosbon.github.io/occlude/', alt='occlude. homepage',
         kind='Concept product', what='Protocol launch site', role='Design + frontend', status='Live concept',
         lede='A launch site for a concept zero-knowledge settlement protocol that lets traders settle on-chain without revealing the amount, counterparty or wallet.',
         idea=['Privacy protocols are hard to explain. The site’s job is to make one feel trustworthy and clear to someone who has never read a whitepaper.',
               'A near-black palette, monospace details and a glowing orb signal privacy and security, while the copy stays in plain English.'],
         points=['A boot-style “establishing connection” intro that sets the tone before the page appears.',
                 'The whole protocol explained in three steps: Shield, Prove, Settle.',
                 'A “what’s shielded, what isn’t” table that shows exactly which trade details stay hidden and which stay public.',
                 'A stats row for shielded volume, proofs settled and average settlement time.']),
    dict(slug='talos', name='TALOS', url='https://darrenrosbon.github.io/talos/', alt='TALOS homepage',
         kind='Concept product', what='Security product site', role='Design + build', status='Live concept',
         lede='A concept site for an autonomous threat-detection product that scans network, cloud and API surfaces continuously.',
         idea=['Most security tools check on a schedule. TALOS is pitched as the one that never stops, so the whole site is built around that single promise.',
               'The brand story borrows the Greek myth of Talos, the bronze guardian who patrolled Crete, and ties the name back to the product.'],
         points=['A classical statue of the bronze guardian beside a paper-toned panel of bold, condensed type.',
                 'A five-part “how it works” section: the patrol, the scan, the intervention, the coastline and human escalation.',
                 'A short origin story that explains the name and turns the myth’s one weakness into the product’s selling point.',
                 'One clear call to action, repeated: request access.']),
    dict(slug='van-wyk-dlamini', name='Van Wyk Dlamini', url='https://darrenrosbon.github.io/van-wyk-dlamini/', alt='Van Wyk Dlamini homepage',
         kind='Concept site', what='Law firm website', role='Design + build', status='Live concept',
         lede='A website concept for a commercial and property law firm in Sandton, designed to feel established, calm and trustworthy.',
         idea=['People looking for an attorney want reassurance fast. The page leads with experience and results, then makes booking a consultation the obvious next step.',
               'A serif headline with an italic accent, a restrained palette and a Sandton skyline keep it serious without feeling dated.'],
         points=['A stats band up front: years in practice, value of transactions, team size and courts appeared before.',
                 'Six practice areas, each explained in one plain sentence.',
                 'Profiles of the senior attorneys, and a client testimonial.',
                 '“Book a consultation” placed in the hero and repeated down the page.']),
    dict(slug='rooted-landscaping', name='Rooted & Co.', url='https://darrenrosbon.github.io/rooted-landscaping/', alt='Rooted & Co. homepage',
         kind='Concept site', what='Landscaping business site', role='Design + build', status='Live concept',
         lede='A lead-generation site concept for a landscaping company in the Portland metro area.',
         idea=['A local trade business lives on quote requests and phone calls, so every section points back to one of those two actions.',
               'Deep greens, full-bleed garden photography and a warm orange call to action make it feel like a crew you could call today.'],
         points=['“Get a free quote” and the phone number are always one tap away in the nav.',
                 'A before-and-after slider: drag the divider to see a lawn brought back.',
                 'Six services with short, practical descriptions, and a four-step process that starts with a walk around the property.',
                 'Trust signals up front: years in business, properties maintained, licensing and service area.']),
    dict(slug='kruger-body-paint', name='Kruger Body & Paint', url='https://darrenrosbon.github.io/kruger-body-paint/', alt='Kruger Body &amp; Paint homepage',
         kind='Concept site', what='Auto body shop site', role='Design + build', status='Live concept',
         lede='A website concept for a family-owned panel beater in Booysens, Johannesburg, styled like a workshop spec sheet.',
         idea=['Panel beaters are hard to trust from the outside. This concept wins trust with precision: real measurements, tolerances and processes instead of vague promises.',
               'The industrial type and condensed caps borrow from workshop signage and job cards.'],
         points=['A “bay status” board in the hero showing bench availability, booth cure cycle, cycle time and courtesy cars.',
                 'Every repair type listed with its technical spec, such as frame tolerance and clear-coat thickness.',
                 'Estimate requests, a paint-code check and 24-hour towing placed up front.',
                 'Heritage and accreditation shown as facts: family owned since 1984, accredited shop, qualified artisans.']),
]

SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-down" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v12M6.5 10.5 12 16l5.5-5.5M5 20h14"/></symbol>
  <symbol id="i-left" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></symbol>
  <symbol id="i-out" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 16 16 8M9 8h7v7"/></symbol>
  <symbol id="i-print" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 9V4h10v5M7 17H5a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2"/><rect x="7" y="14" width="10" height="6" rx="1"/></symbol>
  <symbol id="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></symbol>
  <symbol id="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6l1.4 1.4M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/></symbol>
  <symbol id="i-mail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/></symbol>
</svg>'''

SPECULATION = ('<script type="speculationrules">{"prerender":[{"where":{"href_matches":["../index.html","../certificates/*","../work/*","../cv/*"],'
               '"relative_to":"document"},"eagerness":"moderate"}]}</script>')


# When the visitor came from the page the back link points to, go back through history instead.
# The browser then restores their exact scroll position rather than jumping to the anchor again.
BACK_SCRIPT = '''
<script>
  document.querySelector('.back').addEventListener('click', (e) => {
    const page = (u) => new URL(u, location.href).pathname.replace(/index\\.html$/, '');
    if (document.referrer && page(document.referrer) === page(e.currentTarget.href) && history.length > 1) {
      e.preventDefault();
      history.back();
    }
  });
</script>'''


def page(*, title, description, path, back_href, back_label, main, og, og_alt, head_extra='', body_extra=''):
    return f'''<!DOCTYPE html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="Darren Robson">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{ORIGIN}{path}">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="icon" href="../assets/icons/icon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../assets/icons/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Darren Robson">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{ORIGIN}{path}">
<meta property="og:image" content="{ORIGIN}assets/og/{og}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<script>(() => {{ try {{ if (localStorage.getItem('theme') === 'dark') {{ document.documentElement.dataset.theme = 'dark'; document.querySelector('meta[name="theme-color"]').content = '#141518'; }} }} catch {{}} }})();</script>
<link rel="stylesheet" href="../styles.css?v={CSS_V}">{head_extra}
{SPECULATION}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{SPRITE}

<nav class="nav is-scrolled" aria-label="Main">
  <div class="wrap nav__in">
    <a class="nav__mark" href="../index.html"><img src="../assets/headshot-160.webp" alt="" width="30" height="30"><span class="nav__name">Darren Robson</span></a>
    <div class="nav__tools">
      <button class="icon-btn" id="theme-toggle" type="button" aria-label="Appearance: Light. Switch to Dark"><svg aria-hidden="true"><use href="#i-sun"/></svg></button>
      <a class="back" href="{back_href}"><svg aria-hidden="true"><use href="#i-left"/></svg>{back_label}</a>
    </div>
  </div>
</nav>

{main}

<footer class="fine">
  <div class="wrap"><span>© 2026 Darren Robson · Hand-coded HTML, CSS and JavaScript. No frameworks, no trackers.</span><span>Sandton, Johannesburg · English &amp; Afrikaans · {UPDATED}</span></div>
</footer>
<button class="to-top" type="button" aria-label="Back to top" title="Back to top"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 19V5M5.5 11.5 12 5l6.5 6.5"/></svg></button>
<p class="sr" role="status" aria-live="polite" id="status"></p>
<script src="../common.js?v=2" defer></script>{BACK_SCRIPT}{body_extra}
</body>
</html>
'''


def cert_page(c):
    s = c['slug']
    verify = f'\n      <a class="more" href="{c["verify"]}">Verify on efset.org</a>' if c.get('verify') else ''
    note = '\n    <figcaption class="note">Personal ID and student numbers have been removed from this certificate.</figcaption>' if c['redacted'] else ''
    h700 = round(700 * c['h'] / 1400)
    main = f'''<main id="main" class="viewer wrap">
  <header class="viewer__head">
    <p class="viewer__eyebrow">Certificate · {c['issuer']}</p>
    <h1 style="view-transition-name: cert-title-{s}">{c['title']}</h1>
    <p class="viewer__meta">{c['meta']}</p>
    <div class="viewer__cta">
      <a class="pill" href="../assets/certs/{s}.pdf" download="{c['file']}"><svg aria-hidden="true"><use href="#i-down"/></svg>Download PDF</a>
      <a class="more" href="../assets/certs/{s}.pdf">Open full-size PDF</a>{verify}
    </div>
  </header>
  <figure class="viewer__doc">
    <a href="../assets/certs/{s}.pdf" aria-label="Open the {c['title']} certificate as a PDF" style="view-transition-name: cert-{s}">
      <img src="../assets/certs/previews/{s}-700.webp" srcset="../assets/certs/previews/{s}-700.webp 700w, ../assets/certs/previews/{s}.webp 1400w" sizes="(max-width: 760px) calc(100vw - 2.5rem), 700px" width="700" height="{h700}" alt="{c['title']} certificate issued to Darren Robson by {c['issuer']}" fetchpriority="high">
    </a>{note}
  </figure>
</main>'''
    return page(title=f'{c["title"]} certificate · Darren Robson',
                description=f'Darren Robson’s {c["title"]} certificate. {c["meta"].replace(" · ", ", ")}.',
                path=f'certificates/{s}.html', back_href='../index.html#certifications', back_label='All certifications', main=main,
                og=f'cert-{s}', og_alt=f'{c["title"]} certificate, Darren Robson')


def work_page(i, p):
    s = p['slug']
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    idea = '\n'.join(f'      <p>{t}</p>' for t in p['idea'])
    points = '\n'.join(f'        <li>{t}</li>' for t in p['points'])
    img = f'../assets/projects/{s}'
    main = f'''<main id="main" class="case">
  <header class="case__head wrap">
    <p class="viewer__eyebrow">{p['kind']} · {p['what']}</p>
    <h1 style="view-transition-name: shot-title-{s}">{p['name'].replace('&', '&amp;')}</h1>
    <p class="case__lede">{p['lede']}</p>
    <dl class="case__facts">
      <div><dt>Role</dt><dd>{p['role']}</dd></div>
      <div><dt>Type</dt><dd>{p['kind']}</dd></div>
      <div><dt>Status</dt><dd>{p['status']}</dd></div>
    </dl>
    <div class="viewer__cta">
      <a class="pill" href="{p['url']}">Visit the live site<svg aria-hidden="true"><use href="#i-out"/></svg></a>
    </div>
  </header>
  <figure class="case__shot wrap">
    <a href="{p['url']}" aria-label="Visit the {p['name'].replace('&', '&amp;')} live site" style="view-transition-name: shot-{s}">
      <img src="{img}-960.webp" srcset="{img}-480.webp 480w, {img}-640.webp 640w, {img}-960.webp 960w" sizes="(max-width: 1080px) calc(100vw - 2.5rem), 1000px" width="960" height="600" alt="{p['alt']}" fetchpriority="high">
    </a>
  </figure>
  <div class="case__body wrap">
    <section aria-labelledby="idea-h">
      <h2 id="idea-h">The idea</h2>
{idea}
    </section>
    <section aria-labelledby="points-h">
      <h2 id="points-h">What stands out</h2>
      <ul class="case__points">
{points}
      </ul>
    </section>
  </div>
  <nav class="case__next wrap" aria-label="More projects">
    <a href="{nxt['slug']}.html"><span>Next project</span><strong>{nxt['name'].replace('&', '&amp;')}</strong></a>
  </nav>
</main>'''
    return page(title=f'{p["name"].replace("&", "&amp;")} · Darren Robson',
                description=f'{p["lede"]} {p["role"]} by Darren Robson.',
                path=f'work/{s}.html', back_href='../index.html#work', back_label='All work', main=main,
                og=f'work-{s}', og_alt=f'{p["name"].replace("&", "&amp;")}, a project by Darren Robson')


def cv_page():
    # A web copy of the A4 PDF (A2 layout, Charcoal Coral palette): charcoal sidebar, coral section bands.
    def tags(items):
        return ''.join(f'<li>{t}</li>' for t in items)

    projects = '\n'.join(
        f'''        <li><a class="sq" href="{p['url']}"><strong>{p['name'].replace('&', '&amp;')} <span aria-hidden="true">↗</span></strong>'''
        f'''<span>{p['what'].replace('Windows app + website', 'App + website').replace('Protocol launch site', 'ZK settlement site').replace('Security product site', 'Security monitoring site')}</span>'''
        f'''<em>{p['role']}</em></a></li>''' for p in PROJECTS)
    main = f'''<main id="main" class="cvpage">
  <div class="cvbar wrap">
    <a class="pill" href="../assets/cv/Darren_Robson_CV.pdf" download><svg aria-hidden="true"><use href="#i-down"/></svg>Download PDF</a>
  </div>

  <article class="sheet" aria-label="Curriculum vitae">
    <aside class="sheet__side">
      <img class="sheet__photo" src="../assets/headshot-320.webp" width="150" height="150" alt="Portrait of Darren Robson">

      <h2>Contact</h2>
      <ul class="sheet__contact">
        <li><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 21s-7-6.1-7-11.5a7 7 0 0 1 14 0C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>Sandton, Gauteng, South Africa</li>
        <li><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg><a data-phone href="../index.html#contact">Phone number in the PDF</a></li>
        <li><svg aria-hidden="true" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg><a data-email href="../index.html#contact"><span data-email-text>darrenrobson2001 [at] gmail [dot] com</span></a></li>
        <li><svg aria-hidden="true" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M6 16c.6-1.5 1.7-2 3-2s2.4.5 3 2M14 10h4M14 13h3"/></svg>Valid SA Driver’s License</li>
        <li><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M5 16V11l2-5h10l2 5v5M3 16h18M7 16v2M17 16v2"/><circle cx="7.5" cy="13" r="1"/><circle cx="16.5" cy="13" r="1"/></svg>Own Vehicle</li>
      </ul>

      <h2>LinkedIn</h2>
      <p><a href="https://www.linkedin.com/in/darren-robson-215b77373/">linkedin.com/in/<br>darren‑robson‑215b77373</a></p>

      <h2>Web design portfolio</h2>
      <p><a href="https://robsonwebstudio.com">robsonwebstudio.com</a></p>

      <h2>Key skills</h2>
      <h3>Data &amp; Reporting</h3>
      <ul class="sheet__tags">{tags(['Excel', 'VBA/Macros', 'Google Sheets', 'PayPal &amp; Stripe data', 'Bookkeeping support', 'Data &amp; file organisation'])}</ul>
      <h3>Web</h3>
      <ul class="sheet__tags">{tags(['HTML', 'CSS', 'JavaScript', 'Responsive UI', 'Git/GitHub', 'GitHub Pages', 'Vercel', 'Website admin'])}</ul>
      <h3>IT &amp; Systems</h3>
      <ul class="sheet__tags">{tags(['Hardware build &amp; repair', 'Windows Server 2016', 'Windows &amp; macOS'])}</ul>

      <h2>Certifications</h2>
      <ul class="sheet__certs">
        <li><a href="../certificates/comptia-network-plus.html">CompTIA Network+</a><span>2022</span></li>
        <li><a href="../certificates/comptia-a-plus.html">CompTIA A+</a><span>2022</span></li>
        <li><a href="../certificates/mcsa-windows-server-2016.html">MCSA: Windows Server 2016</a><span>2022</span></li>
      </ul>
      <p class="sheet__aside">Issuing body: IT Academy (CompTIA)</p>

      <h2>Languages</h2>
      <p>English — fluent (home language)<br>Afrikaans — fluent (home language)</p>
    </aside>

    <div class="sheet__main">
      <header class="sheet__head">
        <h1>Darren Robson</h1>
        <p>Data Reporting Specialist &amp; Web Developer</p>
      </header>

      <section aria-labelledby="s-profile">
        <h2 class="band" id="s-profile">Profile</h2>
        <p class="sheet__profile">Data reporting specialist and web developer. Reconciles PayPal and Stripe sales data for accounting teams and builds bespoke tools, like Excel VBA automations, that speed up recurring work tasks. Also designs and develops responsive websites and web apps end to end, from visual design to deployment. CompTIA A+, Network+ and MCSA certified, quick to learn new systems, and always looking for a more efficient way to work.</p>
      </section>

      <section aria-labelledby="s-work">
        <h2 class="band" id="s-work">Work experience</h2>
        <div class="sheet__role">
          <h3>Data Entry &amp; Reporting Specialist</h3>
          <span class="sheet__chip">18+ hrs/month saved</span>
          <p class="sheet__org"><em>MacPherson Crafts (Canada) — Remote</em><em>Mar 2023 – Present</em></p>
        </div>
        <p class="sheet__scope">Scope has grown over the course of this role to include reporting automation and website administration alongside core data-entry duties, while title and level have remained the same.</p>
        <ul class="sheet__bullets">
          <li>Read in and reconcile sales and payment reports from platforms such as PayPal and Stripe for the accounting and bookkeeping department.</li>
          <li>Format, clean, and maintain Excel and Google Sheets containing large volumes of sales data for accounting purposes.</li>
          <li>Automated the daily formatting of PayPal and Stripe transaction reports (~50 transactions per sheet) using VBA and Macros, cutting per-sheet processing time from ~30 minutes to near-instant — <strong>saving an estimated 18+ hours per month</strong> across daily, weekly, and monthly reporting cycles, while significantly reducing manual entry errors.</li>
          <li>Manage website content and product listings, keeping information accurate and up to date.</li>
        </ul>
      </section>

      <section aria-labelledby="s-projects">
        <h2 class="band" id="s-projects">Selected web design projects</h2>
        <p class="sheet__scope">Own products and concept sites — designed and built end to end. <a href="https://robsonwebstudio.com">robsonwebstudio.com</a></p>
        <ul class="sheet__cards">
{projects}
        </ul>
      </section>

      <section aria-labelledby="s-edu">
        <h2 class="band" id="s-edu">Education</h2>
        <h3 class="sheet__h">Grade 12 (National Senior Certificate) — Think Digital College</h3>
        <p>Subjects included Mathematical Literacy and Computer Applications Technology.</p>
        <p class="sheet__scope">Previous institution: Hoërskool Waterkloof (Grade 8–10)</p>
      </section>

      <section aria-labelledby="s-refs">
        <h2 class="band" id="s-refs">References</h2>
        <h3 class="sheet__h">Antoinette De Villiers</h3>
        <p>South African Representative, MacPherson Crafts</p>
        <p><a data-ref-phone href="../index.html#contact">Phone number in the PDF</a></p>
      </section>
    </div>
  </article>
</main>'''
    script = '''
<script>
  // Email and phone numbers are assembled at runtime so scrapers never see them in the HTML.
  const email = ['darrenrobson2001.dr', 'gmail.com'].join('@');
  const phone = ['084', '411', '4748'];
  const refPhone = ['+27', '84', '710', '0006'];
  document.querySelectorAll('[data-email]').forEach((a) => { a.href = 'mailto:' + email; });
  document.querySelectorAll('[data-email-text]').forEach((el) => { el.textContent = email; });
  document.querySelectorAll('[data-phone]').forEach((a) => { a.href = 'tel:+27' + phone.join('').slice(1); a.textContent = phone.join(' '); });
  document.querySelectorAll('[data-ref-phone]').forEach((a) => { a.href = 'tel:' + refPhone.join(''); a.textContent = refPhone.join(' '); });
</script>'''
    return page(title='CV · Darren Robson',
                description='The CV of Darren Robson, Data Reporting Specialist and Web Developer in Sandton, Johannesburg: experience, web projects, skills, certifications and education.',
                path='cv/', back_href='../index.html', back_label='Home', main=main, og='cv', og_alt='CV of Darren Robson, Data Reporting Specialist and Web Developer',
                head_extra=f'\n<link rel="stylesheet" href="cv.css?v={CSS_V}">', body_extra=script)


# ---------- share images (1200 x 630), styled like the home page's assets/og.png ----------
OG_BG, OG_ACCENT, OG_TEXT, OG_MUTED = (36, 39, 44), (184, 86, 10), (240, 240, 240), (190, 192, 196)
FONTS = 'C:/Windows/Fonts/'


def og_image(name, eyebrow, title, sub, art, art_box):
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), OG_BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 14, W, H], fill=OG_ACCENT)

    # artwork on the right: a rounded card with a soft shadow
    x, y, w, h = art_box
    card = ImageOps.fit(Image.open(art).convert('RGB'), (w, h), centering=(0.5, 0.0))
    mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], 22, fill=255)
    shadow = Image.new('L', (W, H), 0); ImageDraw.Draw(shadow).rounded_rectangle([x, y + 18, x + w, y + h + 18], 22, fill=150)
    im.paste((10, 11, 13), (0, 0), shadow.filter(ImageFilter.GaussianBlur(28)))
    im.paste(card, (x, y), mask)

    # text on the left, wrapped to the space beside the artwork
    left, maxw = 80, x - 80 - 60
    f_eye = ImageFont.truetype(FONTS + 'seguisb.ttf', 26)
    f_sub = ImageFont.truetype(FONTS + 'segoeui.ttf', 28)
    f_by = ImageFont.truetype(FONTS + 'seguisb.ttf', 26)
    size = 72
    while True:
        f_title = ImageFont.truetype(FONTS + 'seguisb.ttf', size)
        lines, line = [], ''
        for word in title.split():
            trial = (line + ' ' + word).strip()
            if d.textlength(trial, font=f_title) <= maxw: line = trial
            else: lines.append(line); line = word
        lines.append(line)
        if len(lines) <= 3 or size <= 48: break
        size -= 6
    sub_lines, line = [], ''
    for word in sub.split():
        trial = (line + ' ' + word).strip()
        if d.textlength(trial, font=f_sub) <= maxw: line = trial
        else: sub_lines.append(line); line = word
    sub_lines.append(line)

    block = 40 + len(lines) * size * 1.12 + 24 + len(sub_lines) * 38
    ty = (H - 14 - 120 - block) / 2 + 20
    d.text((left, ty), eyebrow.upper(), font=f_eye, fill=OG_ACCENT)
    ty += 44
    for ln in lines:
        d.text((left, ty), ln, font=f_title, fill=OG_TEXT); ty += size * 1.12
    ty += 22
    for ln in sub_lines:
        d.text((left, ty), ln, font=f_sub, fill=OG_MUTED); ty += 38

    # byline with the round headshot, pinned to the bottom
    by_y = H - 14 - 96
    photo = ImageOps.fit(Image.open(SITE / 'assets/headshot-160.webp').convert('RGB'), (56, 56))
    ring = Image.new('L', (64, 64), 0); ImageDraw.Draw(ring).ellipse([0, 0, 63, 63], fill=255)
    im.paste(OG_ACCENT, (left, by_y), ring)
    pm = Image.new('L', (56, 56), 0); ImageDraw.Draw(pm).ellipse([0, 0, 55, 55], fill=255)
    im.paste(photo, (left + 4, by_y + 4), pm)
    d.text((left + 80, by_y + 16), 'Darren Robson · Data Reporting Specialist & Web Developer', font=f_by, fill=OG_TEXT)

    out = SITE / 'assets/og' / f'{name}.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)
    print('wrote', out.relative_to(SITE).as_posix())


def build_og_images():
    import pymupdf
    for c in CERTS:
        og_image(f'cert-{c["slug"]}', f'Certificate · {c["issuer"]}', c['title'], c['meta'],
                 SITE / f'assets/certs/previews/{c["slug"]}-700.webp', (830, 44, 290, 410))
    for p in PROJECTS:
        og_image(f'work-{p["slug"]}', f'{p["kind"]} · {p["what"]}', p['name'], p['role'],
                 SITE / f'assets/projects/{p["slug"]}-960.webp', (640, 105, 480, 300))
    # the CV card shows the top of the real PDF
    tmp = SITE / 'assets/og/_cv-page.png'
    tmp.parent.mkdir(parents=True, exist_ok=True)
    pdf = pymupdf.open(SITE / 'assets/cv/Darren_Robson_CV.pdf')[0]
    pdf.get_pixmap(matrix=pymupdf.Matrix(1.2, 1.2)).save(tmp)
    og_image('cv', 'Curriculum vitae', 'Darren Robson’s CV', 'Experience, projects, skills, certifications and education',
             tmp, (830, 44, 290, 410))
    tmp.unlink()


def lost_page(base='/DarrenRobsonHub/'):
    """The 404 page. GitHub Pages serves it at whatever missing URL was asked for, at any depth,
    so every link is made absolute to the site root (`base`) instead of relative."""
    main = f'''<main id="main" class="lost wrap">
  <p class="lost__code" aria-hidden="true">404</p>
  <h1>This page doesn’t exist.</h1>
  <p class="lost__text">The link may be old or mistyped. Here’s where everything lives:</p>
  <ul class="lost__links">
    <li><a class="pill" href="../index.html">Go to the home page</a></li>
    <li><a class="more" href="../cv/">View the CV</a></li>
    <li><a class="more" href="../index.html#work">Selected work</a></li>
    <li><a class="more" href="../index.html#certifications">Certifications</a></li>
  </ul>
</main>'''
    html = page(title='Page not found · Darren Robson', description='This page doesn’t exist. Find the CV, projects and certifications of Darren Robson on the home page.',
                path='404.html', back_href='../index.html', back_label='Home', main=main, og='cv', og_alt='')
    # not a real page: keep it out of search results and link previews
    html = re.sub(r'<link rel="canonical".*?<meta name="twitter:card" content="summary_large_image">\n', '<meta name="robots" content="noindex">\n', html, flags=re.S)
    html = re.sub(r'<script type="speculationrules">.*?</script>\n', '', html)
    return html.replace('"../', f'"{base}')


def write(rel, html):
    out = SITE / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8', newline='\n')
    print('wrote', rel)


if __name__ == '__main__':
    for c in CERTS:
        write(f'certificates/{c["slug"]}.html', cert_page(c))
    for i, p in enumerate(PROJECTS):
        write(f'work/{p["slug"]}.html', work_page(i, p))
    write('cv/index.html', cv_page())
    write('404.html', lost_page())
    build_og_images()
    home = SITE / 'index.html'
    html, n = re.subn(r'Last updated <time datetime="[^"]*">[^<]*</time>', UPDATED, home.read_text(encoding='utf-8'))
    if not n:
        html, n = re.subn(re.escape('<span>Sandton, Johannesburg · English &amp; Afrikaans</span></div>'),
                          f'<span>Sandton, Johannesburg · English &amp; Afrikaans · {UPDATED}</span></div>', html)
    assert n == 1, 'home page footer not found'
    home.write_text(html, encoding='utf-8', newline='\n')
    print('stamped index.html:', f'{TODAY:%B %Y}')
