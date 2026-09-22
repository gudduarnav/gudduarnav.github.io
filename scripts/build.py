#!/usr/bin/env python3
"""Build both GitHub Pages entrypoints from one bilingual content source.

No build dependencies. Run from any directory with: python3 scripts/build.py
"""
import json
from html import escape
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONTENT = json.loads((ROOT / 'data/content.json').read_text())
PUBLICATIONS = json.loads((ROOT / 'data/publications.json').read_text())
METRICS = json.loads((ROOT / 'data/journal-metrics.json').read_text())
SECTION_IDS = ['home', 'research', 'publications', 'education', 'experience', 'service', 'profiles', 'contact']
PROFILE_URLS = [
    'https://orcid.org/0000-0002-8167-7501',
    'https://scholar.google.com/citations?user=HdMekI8AAAAJ',
    'https://ieeexplore.ieee.org/author/37087052296',
    'https://dblp.org/pid/417/8805',
    'https://www.researchgate.net/profile/Arnav-Mukhopadhyay',
    'https://github.com/gudduarnav',
]
PROFILE_INITIALS = ['iD', 'Gs', 'Ie', 'Db', 'Rg', 'Gh']
TOOLS = ['Python', 'C', 'C++', 'CVXPY', 'PyTorch', 'Stable-Baselines', 'GNU Radio', 'OptiSystem', 'LaTeX']
REVIEW_COUNTS = [13, 7, 6, 2, 2, 1]
BASE = 'https://gudduarnav.github.io'


def e(value):
    return escape(str(value), quote=True)


def arrow():
    return '<span aria-hidden="true">↗</span>'


def external(url, label, css='', aria=None):
    accessibility = f' aria-label="{e(aria)}"' if aria else ''
    return f'<a class="{css}" href="{e(url)}" target="_blank" rel="noopener noreferrer"{accessibility}>{e(label)} {arrow()}</a>'


def section_head(c, key, intro=False):
    return f'''<div class="section-heading"><p class="eyebrow">{e(c[key+'Eyebrow'])}</p>
    <h2 id="{key}-title">{e(c[key+'Title'])}</h2>
    {f'<p class="section-intro">{e(c[key+"Intro"])}</p>' if intro and c[key+'Intro'] else ''}</div>'''


def timeline(c, key):
    rows = []
    for row in c[key]:
        rows.append(f'''<li class="timeline-entry"><p class="timeline-date">{e(row['date'])}</p>
        <div><h3>{e(row['title'])}</h3><p class="place">{e(row['place'])}</p><p>{e(row['text'])}</p></div></li>''')
    return f'<ol class="timeline">{"".join(rows)}</ol>'


def metrics_guide(c):
    legend = ''.join(f'<li class="quartile q{i}">{e(label)}</li>' for i, label in enumerate(c['quartileNames'], 1))
    return f'''<div class="metrics-guide"><div class="quartile-key"><span>{e(c['quartileLegend'])}</span>
    <ul aria-label="{e(c['quartileLegend'])}">{legend}</ul></div>
    <details><summary>{e(c['metricsGuide'])}</summary><p>{e(c['metricsGuideText'])}</p><p>{e(c['metricsConferenceText'])}</p></details></div>'''


def journal_metrics(p, c, lang):
    if 'venue_id' not in p:
        return f'<p class="metrics-na">{e(c["metricsNA"])}</p>'
    m = METRICS['venues'][p['venue_id']]
    year = m['metric_year']
    category = c['metricsCategories'][m['category']]
    sources = f'<li>{external(m["jcr_url"], c["metricsJcrLink"]+" · "+str(year))}</li>'
    sources += ''.join(f'<li>{external(METRICS["sources"][key]["url"], METRICS["sources"][key]["label"][lang])}</li>' for key in m['source_ids'])
    rank_label = f'{c["metricsJcrLink"]}: {m["name"]} · {category} · {m["rank"]}/{m["total"]} · {year}'
    other = ''.join(f'<li><span class="quartile q{r["quartile"]}">Q{r["quartile"]}</span> {e(c["metricsCategories"][r["category"]])} · {r["rank"]}/{r["total"]} · {year}</li>' for r in m.get('other_categories', []))
    history = f'<span class="metric-history">{e(c["metricsHistorical"])}</span>' if m['historical'] else ''
    note = f'<p class="metric-status"><strong>{e(c["metricsOnHold"])}</strong> · {e(c["metricsHistoricalNote"])}</p>' if m['on_hold'] else ''
    return f'''<div class="journal-metrics" aria-label="{e(c['metricsLabel'])}">
    <ul class="metric-badges"><li class="quartile q{m['quartile']}" aria-label="{e(c['metricsQuartileLabel'])}: Q{m['quartile']} · {e(category)} · {year}">Q{m['quartile']} · {e(category)} · {year}</li>
    <li class="metric-jif">{e(c['metricsJif'])} {year} <strong>{e(m['jif'])}</strong></li>
    <li class="metric-rank"><a href="{e(m['jcr_url'])}" target="_blank" rel="noopener noreferrer" aria-label="{e(rank_label)}">{e(c['metricsCategory'])} <strong>{m['rank']}/{m['total']}</strong> · {year} {arrow()}</a></li></ul>
    {history}{note}
    <details class="metric-details"><summary>{e(c['metricsSources'])}</summary>
    <p>{e(c['metricsJci'])} {year}: <strong>{e(m['jci'])}</strong></p>
    {f'<ul class="other-categories">{other}</ul>' if other else ''}
    <p>{e(c['metricsRankSources'])}</p>
    <ul class="metric-sources">{sources}</ul><p>{e(c['metricsSourceNote'])}</p></details></div>'''


def publications(c, lang):
    groups = []
    for year, label in [(2026, '2026'), (2025, '2025'), (0, c['earlier'])]:
        rows = []
        for p in PUBLICATIONS:
            if not (p['year'] == year or (year == 0 and p['year'] < 2025)):
                continue
            author_names = ' · '.join(f'<strong>{e(a)}</strong>' if a == 'Arnav Mukhopadhyay' else e(a) for a in p['authors'])
            title = p['title'][lang]
            rows.append(f'''<article class="publication" id="pub-{e(p['doi'].split('/')[-1].lower().replace('.', '-'))}">
            <div class="publication-meta"><span class="pub-type">{e(c['types'][p['type']])}</span><span>{e(c['firstAuthor'] if p['first'] else c['coAuthor'])}</span>{f'<span>{p["year"]}</span>' if year == 0 else ''}</div>
            <h4><a href="https://doi.org/{e(p['doi'])}" target="_blank" rel="noopener noreferrer">{e(title)}</a></h4>
            <p class="authors" lang="en">{author_names}</p><p class="venue">{e(p['venue'][lang])}</p>
            {journal_metrics(p, c, lang)}
            {external('https://doi.org/'+p['doi'], c['readPaper'], 'paper-link', c['doiLabel']+' '+title)}</article>''')
        groups.append(f'<div class="publication-group"><h3 class="year-label">{e(label)}</h3><div class="publication-list">{"".join(rows)}</div></div>')
    return ''.join(groups)


def render(lang):
    c = CONTENT[lang]
    zh = lang == 'zh-TW'
    prefix = '../' if zh else './'
    path = '/zh-tw/' if zh else '/'
    other_path = '/' if zh else '/zh-tw/'
    monogram = '安' if zh else 'AM'
    navigation = []
    for i, (id_, label) in enumerate(zip(SECTION_IDS, c['nav'])):
        current = ' class="active" aria-current="location"' if i == 0 else ''
        navigation.append(f'<a href="#{id_}"{current}><span class="nav-index" aria-hidden="true">{i:02d}</span>{e(label)}</a>')
    nav = ''.join(navigation)
    research = ''.join(f'''<article class="research-card card-{i}"><span class="card-number" aria-hidden="true">0{i+1}</span>
    <p class="card-tag">{e(r['tag'])}</p><h3>{e(r['title'])}</h3><p>{e(r['text'])}</p>
    <ul class="chips">{''.join(f'<li>{e(t)}</li>' for t in r['chips'])}</ul></article>''' for i, r in enumerate(c['research']))
    stats = ''.join(f'<div class="stat"><strong>{v}</strong><span>{e(label)}</span></div>' for v, label in zip([len(PUBLICATIONS), sum(p['first'] for p in PUBLICATIONS), sum(REVIEW_COUNTS), '4.07'], c['stats']))
    review_rows = ''.join(f'<li><span>{e(name)}</span><strong>{count}</strong></li>' for name, count in zip(c['reviewVenues'], REVIEW_COUNTS))
    awards = ''.join(f'<li><h4>{e(a["title"])}</h4><p>{e(a["text"])}</p>{external(a["link"], c["announcement"], "text-link") if "link" in a else ""}</li>' for a in c['awards'])
    profiles = ''.join(f'''<a class="profile-card" href="{e(url)}" target="_blank" rel="noopener noreferrer"><span class="profile-icon" aria-hidden="true">{PROFILE_INITIALS[i]}</span><span><h3>{e(c['profileNames'][i])}</h3><span class="profile-description">{e(c['profileDescriptions'][i])}</span></span>{arrow()}</a>''' for i, url in enumerate(PROFILE_URLS))
    person = {
        '@context': 'https://schema.org', '@type': 'Person',
        'name': 'Arnav Mukhopadhyay', 'alternateName': '安納夫', 'url': BASE + path,
        'jobTitle': c['role'], 'email': 'mailto:gudduarnav@gmail.com',
        'affiliation': {'@type': 'CollegeOrUniversity', 'name': c['university']},
        'sameAs': PROFILE_URLS, 'knowsAbout': [r['title'] for r in c['research']],
    }
    return f'''<!doctype html>
<!-- Generated by scripts/build.py. Edit the JSON files in data/. -->
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(c['title'])}</title>
  <meta name="description" content="{e(c['description'])}">
  <meta name="author" content="Arnav Mukhopadhyay">
  <meta name="theme-color" content="#f6f7fb">
  <meta name="color-scheme" content="light dark">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{BASE}{path}">
  <link rel="alternate" hreflang="en" href="{BASE}/">
  <link rel="alternate" hreflang="zh-TW" href="{BASE}/zh-tw/">
  <link rel="alternate" hreflang="x-default" href="{BASE}/">
  <link rel="icon" href="{prefix}favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="{e(c['title'])}">
  <meta property="og:description" content="{e(c['description'])}">
  <meta property="og:url" content="{BASE}{path}">
  <meta property="og:locale" content="{'zh_TW' if zh else 'en_US'}">
  <meta property="og:locale:alternate" content="{'en_US' if zh else 'zh_TW'}">
  <meta property="og:image" content="{BASE}/fav_icon.png">
  <meta property="og:image:alt" content="{e(c['portrait'])}">
  <meta name="twitter:card" content="summary">
  <script type="application/ld+json">{json.dumps(person, ensure_ascii=False).replace('<', chr(92)+'u003c')}</script>
  <script src="{prefix}assets/theme.js"></script>
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script src="{prefix}assets/site.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">{e(c['skip'])}</a>
<aside class="sidebar">
  <a class="brand" href="#home" aria-label="{e(c['name'])}"><span class="monogram" aria-hidden="true">{monogram}</span><span>{e(c['name'])}<small>{e(c['portfolio'])}</small></span></a>
  <nav id="section-navigation" aria-label="{e(c['navLabel'])}">{nav}</nav>
  <div class="sidebar-footer"><span class="color-bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span><p>{e(c['location'])}</p><small>{e(c['footer'])}</small></div>
</aside>
<div class="page-shell">
  <header class="topbar">
    <a class="mobile-brand" href="#home" aria-label="{e(c['name'])}"><span class="monogram" aria-hidden="true">{monogram}</span><span>{e(c['shortName'])}</span></a>
    <span class="topbar-title">{e(c['portfolio'])}<span class="topbar-separator" aria-hidden="true">/</span><span>{e(c['location'])}</span></span>
    <div class="preferences">
      <button type="button" class="theme-toggle" aria-label="{e(c['theme'])}" aria-pressed="false" data-label="{e(c['theme'])}" data-light="{e(c['light'])}" data-dark="{e(c['dark'])}"><span class="theme-icon" aria-hidden="true">☼</span><span class="theme-text">{e(c['light'])}</span></button>
      <a class="language-switch" href="{other_path}" hreflang="{'en' if zh else 'zh-TW'}" lang="{'en' if zh else 'zh-TW'}" aria-label="{e(c['otherLanguageLabel'])}"><span class="language-icon" aria-hidden="true">文/A</span>{e(c['otherLanguage'])}</a>
      <button class="menu-toggle" type="button" aria-controls="section-navigation" aria-expanded="false" data-open="{e(c['menu'])}" data-close="{e(c['closeMenu'])}"><span class="menu-icon" aria-hidden="true"><i></i><i></i></span><span class="menu-text">{e(c['menu'])}</span></button>
    </div>
  </header>
  <main id="main" tabindex="-1">
    <section class="hero" id="home" aria-labelledby="hero-title">
      <div class="hero-copy"><p class="eyebrow"><span class="tiny-line" aria-hidden="true"></span>{e(c['role'])}</p>
        <h1 id="hero-title">{'安納夫' if zh else 'Arnav<br>Mukhopadhyay'}<span class="name-dot" aria-hidden="true">.</span></h1>
        <p class="hero-line">{e(c['heroLine'])}</p><p class="hero-description">{e(c['intro'])}</p>
        <div class="hero-actions"><a class="button primary" href="#publications">{e(c['viewPubs'])}<span aria-hidden="true">↗</span></a><a class="text-link" href="mailto:gudduarnav@gmail.com">{e(c['getInTouch'])} {arrow()}</a></div>
      </div>
      <div class="portrait-panel"><div class="portrait-frame"><img src="{prefix}fav_icon.png" alt="{e(c['portrait'])}" width="720" height="960" fetchpriority="high"></div><div class="portrait-label"><span>{e(c['current'])}</span><strong>{e(c['university'])}</strong><span>{e(c['institute'])}</span></div></div>
      <div class="appointment"><span class="appointment-mark" aria-hidden="true">◈</span><p>{e(c['expected'])}</p><a href="{PROFILE_URLS[0]}" target="_blank" rel="noopener noreferrer">{'研究者識別碼' if zh else 'ORCID'} {arrow()}</a></div>
    </section>
    <div class="stats-strip">{stats}</div>
    <section class="section" id="research" aria-labelledby="research-title">
      {section_head(c, 'research', True)}<div class="research-grid">{research}</div>
      <div class="methods"><h3>{e(c['methodsTitle'])}</h3><div><ul class="method-list">{''.join(f'<li>{e(m)}</li>' for m in c['methods'])}</ul><ul class="tool-list" lang="en">{''.join(f'<li>{e(t)}</li>' for t in TOOLS)}</ul></div></div>
    </section>
    <section class="section" id="publications" aria-labelledby="pub-title">
      {section_head(c, 'pub', True)}<p class="verified-note"><span aria-hidden="true">✓</span> {e(c['pubVerified'])}</p>
      {metrics_guide(c)}
      {publications(c, lang)}{f'<p class="record-note">{e(c["translationNote"])}</p>' if zh else ''}
    </section>
    <section class="section" id="education" aria-labelledby="education-title">{section_head(c, 'education')}{timeline(c, 'education')}</section>
    <section class="section" id="experience" aria-labelledby="experience-title">{section_head(c, 'experience')}{timeline(c, 'experience')}</section>
    <section class="section" id="service" aria-labelledby="service-title">{section_head(c, 'service')}
      <div class="service-grid"><div class="review-panel"><h3>{e(c['reviewsTitle'])}</h3><p class="review-subtitle">{e(c['reviewsSubtitle'])}</p><ul class="review-list">{review_rows}</ul><p class="record-note">{e(c['reviewsNote'])}</p>{external(PROFILE_URLS[0]+'/peer-reviews',c['verify'],'text-link')}</div>
      <div class="awards-panel"><h3>{e(c['awardsTitle'])}</h3><ul class="award-list">{awards}</ul></div></div>
    </section>
    <section class="section" id="profiles" aria-labelledby="profiles-title">{section_head(c, 'profiles', True)}<div class="profiles-grid">{profiles}</div></section>
    <section class="contact-section" id="contact" aria-labelledby="contact-title"><div><p class="eyebrow">{e(c['contactEyebrow'])}</p><h2 id="contact-title">{e(c['contactTitle'])}</h2><p>{e(c['contactText'])}</p><a class="contact-email" href="mailto:gudduarnav@gmail.com" aria-label="{e(c['emailLabel'])}">gudduarnav@gmail.com {arrow()}</a></div><span class="contact-symbol" aria-hidden="true">✳</span></section>
  </main>
  <footer class="footer"><p>© 2026 {e(c['name'])}<span>{e(c['updated'])}</span></p><a href="#home">{e(c['backTop'])} <span aria-hidden="true">↑</span></a></footer>
</div>
</body>
</html>
'''


def main():
    assert CONTENT['en'].keys() == CONTENT['zh-TW'].keys(), 'Translation keys must match'
    assert len({p['doi'].lower() for p in PUBLICATIONS}) == len(PUBLICATIONS), 'Duplicate DOI'
    for p in PUBLICATIONS:
        journal = p['type'] in {'Journal', 'Survey', 'Magazine'}
        assert ('venue_id' in p) == journal, 'Only journal publications receive journal metrics'
        if journal:
            m = METRICS['venues'][p['venue_id']]
            assert m['quartile'] in range(1, 5) and 0 < m['rank'] <= m['total']
            assert m['metric_year'] < m['release_year']
            assert all(key in METRICS['sources'] for key in m['source_ids'])
            profile = urlsplit(m['jcr_url'])
            assert profile.scheme == 'https' and profile.netloc == 'jcr.clarivate.com'
            assert profile.path == '/jcr-jp/journal-profile'
            assert parse_qs(profile.query) == {'journal': [m['jcr_abbreviation']], 'year': [str(m['metric_year'])]}, 'JCR links must identify the exact journal and displayed metric year'
    for lang, output in [('en', ROOT / 'index.html'), ('zh-TW', ROOT / 'zh-tw/index.html')]:
        output.parent.mkdir(exist_ok=True)
        output.write_text('\n'.join(line.rstrip() for line in render(lang).splitlines()) + '\n')
        print(f'Built {output.relative_to(ROOT)}')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    for path in ['/', '/zh-tw/']:
        sitemap += f'  <url><loc>{BASE}{path}</loc><lastmod>2026-09-22</lastmod><xhtml:link rel="alternate" hreflang="en" href="{BASE}/"/><xhtml:link rel="alternate" hreflang="zh-TW" href="{BASE}/zh-tw/"/><xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/"/></url>\n'
    (ROOT / 'sitemap.xml').write_text(sitemap + '</urlset>\n')


if __name__ == '__main__':
    main()
