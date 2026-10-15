#!/usr/bin/env python3
"""Build a lightweight three-journal site from Markdown. Requires mistune 3.x."""
from __future__ import annotations
import html
import os
import json
import re
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import mistune

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
SETTINGS = json.loads((ROOT / 'settings.json').read_text(encoding='utf-8'))
TITLE = SETTINGS['site_title']
# Cloudflare Pages supplies CF_PAGES_URL during every Git-based build.
# PUBLIC_SITE_URL can later override it when a permanent custom domain is connected.
SITE = (os.getenv('PUBLIC_SITE_URL') or os.getenv('CF_PAGES_URL') or SETTINGS['site_url']).rstrip('/') + '/'
PREVIEW = SETTINGS.get('preview_mode', True)
ES = lambda s: html.escape(str(s), quote=True)
SECTIONS = {
    'game': {'title': 'Game development', 'short': 'Crust & Crime', 'subtitle': 'Building a stylized 3D world, one experiment at a time.', 'description': 'Development notes on mechanics, player controls, prototypes, code, and lessons from Crust & Crime.', 'glyph': '⌘', 'kicker': '01 / Build'},
    'water': {'title': 'Water engineering & research', 'short': 'Water Engineering', 'subtitle': 'Rivers, maps, models, and reproducible experiments.', 'description': 'Field notes on GIS, hydrology, HEC-RAS, flood studies, and computational hydraulics.', 'glyph': '≈', 'kicker': '02 / Research'},
    'career': {'title': 'Career journal', 'short': 'AI-Assisted Job Hunt', 'subtitle': 'An evidence-driven experiment in finding meaningful technical work.', 'description': 'An open account of searching, assessing, and applying for engineering and technical roles with AI assistance.', 'glyph': '◉', 'kicker': '03 / Explore'},
}


def read_post(path: Path):
    raw = path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', raw, flags=re.S)
    if not match:
        raise ValueError(f'Missing front matter in {path}')
    meta = {}
    for line in match.group(1).splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        meta[key.strip()] = value.strip()
    section = path.parent.name
    if section not in SECTIONS:
        raise ValueError(f'Unknown section {section}')
    if not all(meta.get(x) for x in ('title', 'date', 'description')):
        raise ValueError(f'Title, date, description required in {path}')
    date = datetime.strptime(meta['date'], '%Y-%m-%d').date()
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', path.stem)
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise ValueError(f'Invalid post slug {slug}')
    return {
        **meta, 'date_obj': date, 'section': section, 'slug': slug,
        'tags': [x.strip() for x in meta.get('tags', '').split(',') if x.strip()],
        'url': f'/{section}/{slug}/', 'body': match.group(2),
    }


def discover_posts():
    content_root = ROOT / 'content'
    unexpected = sorted(d.name for d in content_root.iterdir() if d.is_dir() and d.name not in SECTIONS)
    if unexpected:
        raise ValueError(f'Unexpected content sections; public build aborted: {unexpected}')
    return sorted([read_post(p) for p in content_root.glob('*/*.md')], key=lambda p: (-p['date_obj'].toordinal(), {'game': 0, 'water': 1, 'career': 2}[p['section']], p['slug']))

POSTS = discover_posts()
render_md = mistune.create_markdown(escape=True, plugins=['table', 'strikethrough'])


def nice_date(d):
    return f'{d.strftime("%B")} {d.day}, {d.year}'


def nav(active):
    navitems = [('home', '/', 'Home'), ('game', '/game/', 'Game'), ('water', '/water/', 'Water'), ('career', '/career/', 'Career'), ('about', '/about/', 'About')]
    links = ''.join(f'<a href="{href}" class="{"active" if active == key else ""} {"hide-mobile" if key == "about" else ""}">{label}</a>' for key,href,label in navitems)
    ribbon = '<div class="preview-ribbon">SITE PREVIEW — introductory articles ready for review; not published</div>' if PREVIEW else ''
    return f'{ribbon}<header class="site-header"><div class="wrap navrow"><a class="brand" href="/"><span class="brand-mark">FR.</span>Fikri Radiyan</a><nav aria-label="Primary navigation" class="topnav">{links}</nav></div></header>'


def layout(content, *, title, desc, active, page_url):
    canonical = ES(urljoin(SITE, page_url.lstrip('/')))
    fulltitle = ES(title + ' — Fikri Radiyan' if title != 'Home' else TITLE)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{fulltitle}</title><meta name="description" content="{ES(desc)}"><meta name="theme-color" content="#0d1419">
<meta property="og:type" content="website"><meta property="og:title" content="{fulltitle}"><meta property="og:description" content="{ES(desc)}">
<link rel="canonical" href="{canonical}"><link rel="stylesheet" href="/assets/site.css">
<link rel="alternate" type="application/rss+xml" title="Fikri Radiyan journal RSS" href="/rss.xml">
</head><body>{nav(active)}<main>{content}</main><footer class="footer"><div class="wrap footer-content"><span>© {datetime.now().year} Fikri Radiyan · Work in progress, documented in public.</span><span><a href="/rss.xml">RSS feed ↗</a> &nbsp; · &nbsp; <a href="/about/">About</a></span></div></footer></body></html>'''


def post_row(post):
    sect = post['section']
    return f'''<a class="post-row" href="{post['url']}"><time datetime="{post['date']}">{nice_date(post['date_obj'])}</time><div><span class="chip {sect}">{ES(SECTIONS[sect]['short'])}</span><h3>{ES(post['title'])}</h3><p>{ES(post['description'])}</p></div><span class="arrow" aria-hidden="true">↗</span></a>'''


def write(url, content):
    relative = url.strip('/')
    path = OUT / relative / 'index.html' if relative else OUT / 'index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def homepage():
    cards = []
    for key, s in SECTIONS.items():
        cards.append(f'''<a href="/{key}/" class="journal-card {key}"><div class="journal-visual"><span class="journal-symbol">{s['glyph']}</span></div><div class="journal-body"><span class="smallcaps">{ES(s['kicker'])}</span><h3>{ES(s['short'])}</h3><p>{ES(s['description'])}</p><span class="more">Read the journal &nbsp; ↗</span></div></a>''')
    entries = ''.join(post_row(p) for p in POSTS[:6])
    content = f'''<div class="wrap"><section class="hero"><div><div class="eyebrow">An independent public notebook / 2026</div><h1>Ideas in progress.<br><em>Evidence in public.</em></h1><p>I'm Fikri. I build things, test ideas, and document what I learn — across a game, water engineering experiments, and the search for meaningful technical work.</p><a class="primary-link" href="#journals">Explore the journals <span aria-hidden="true">↘</span></a></div><div class="hero-art" role="img" aria-label="Three floating labels representing the game, research, and career journals"><span class="floatcard c1"><i></i>CREATE / game</span><span class="floatcard c2"><i></i>MODEL / water</span><span class="floatcard c3"><i></i>LEARN / career</span></div></section><section class="journals" id="journals"><div class="section-head"><div><div class="eyebrow">01 — The projects</div><h2>Three ongoing journals</h2></div><p>Different topics. Same curiosity.</p></div><div class="journal-grid">{''.join(cards)}</div></section></div><section class="posts-section"><div class="wrap"><div class="section-head"><div><div class="eyebrow">02 — The notebook</div><h2>Recent writing</h2></div><p>A record of what I'm learning along the way.</p></div><div class="posts-list">{entries}</div></div></section>'''
    write('/', layout(content, title='Home', desc=SETTINGS['description'], active='home', page_url='/'))


def section_page(section):
    info = SECTIONS[section]
    items = [p for p in POSTS if p['section'] == section]
    title = ES(info['title'])
    heading = f'''<div class="wrap"><section class="interior-hero"><div class="eyebrow">{ES(info['kicker'])} / field notes</div><h1>{title}</h1><p>{ES(info['subtitle'])}</p></section><section class="page-grid"><div class="section-head"><div><div class="smallcaps">Article archive</div><h2>Entries &amp; experiments</h2></div><p>{len(items)} {"entry" if len(items) == 1 else "entries"}</p></div><div class="posts-list">{''.join(post_row(p) for p in items) if items else '<div class="empty">No entries yet.</div>'}</div></section></div>'''
    write(f'/{section}/', layout(heading, title=info['title'], desc=info['description'], active=section, page_url=f'/{section}/'))


def comments_html():
    g = SETTINGS.get('giscus', {})
    if all(g.get(key) for key in ['repo','repo_id','category','category_id']):
        props = {'src': 'https://giscus.app/client.js','data-repo':g['repo'],'data-repo-id':g['repo_id'],'data-category':g['category'],'data-category-id':g['category_id'],'data-mapping':'pathname','data-strict':'1','data-reactions-enabled':'1','data-emit-metadata':'0','data-input-position':'top','data-theme':'dark','data-lang':'en','crossorigin':'anonymous'}
        scriptattrs = ' '.join(f'{key}="{ES(value)}"' for key,value in props.items())
        return f'<section class="comments"><h2>Discussion</h2><p>Join the conversation through GitHub Discussions.</p><script {scriptattrs} async></script></section>'
    return '<section class="comments"><h2>Comments coming soon</h2><p>Reader discussions can be enabled with GitHub Discussions (Giscus) when the site repository is ready.</p></section>'


def article(post):
    meta = f'<span class="chip {post["section"]}">{ES(SECTIONS[post["section"]]["short"])}</span><time datetime="{post["date"]}">{nice_date(post["date_obj"])}</time>'
    if post.get('status'):
        meta += f'<span class="chip">{ES(post["status"])}</span>'
    for tag in post['tags']:
        meta += f'<span class="chip">#{ES(tag)}</span>'
    body = render_md(post['body'])
    content = f'''<div class="wrap"><article class="article"><header><div class="eyebrow"><a href="/{post['section']}/">← {ES(SECTIONS[post['section']]['title'])}</a></div><h1>{ES(post['title'])}</h1><p class="deck">{ES(post['description'])}</p><div class="postmeta">{meta}</div></header><div class="prose">{body}</div><div class="article-footer"><a class="primary-link" href="/{post['section']}/">← Back to journal</a></div>{comments_html()}</article></div>'''
    write(post['url'], layout(content, title=post['title'], desc=post['description'], active=post['section'], page_url=post['url']))


def about():
    content = '''<div class="wrap"><div class="interior-hero"><div class="eyebrow">About the author</div><h1>Hi, I'm Fikri.</h1><p>An engineer and researcher documenting work in progress.</p></div><div class="about"><p>This website is a home for three projects: developing Crust &amp; Crime, exploring water engineering with GIS, hydrology, and hydraulic models, and conducting an AI-assisted search for meaningful technical roles.</p><p>My background spans civil and environmental engineering, numerical modeling, hydrology, and computational research. I like systematic tests, reproducible work, and learning in public — including the experiments that don't succeed.</p><p>Posts are personal project notes, not professional engineering certifications or claims that a prototype is already a released product. I publish selected code and results when it's safe and useful to share them.</p><a class="primary-link" href="/">← Back to homepage</a></div></div>'''
    write('/about/', layout(content, title='About', desc='Meet Fikri Radiyan and the projects documented on this website.', active='about', page_url='/about/'))


def rss(section=None):
    subset = [p for p in POSTS if section is None or p['section']==section]
    ET.register_namespace('', 'http://www.w3.org/2005/Atom')
    root = ET.Element('rss', {'version':'2.0'})
    chan = ET.SubElement(root, 'channel')
    def el(parent, tag, txt): ET.SubElement(parent, tag).text=str(txt)
    el(chan, 'title', TITLE + (f' — {SECTIONS[section]["title"]}' if section else ''))
    el(chan, 'link', urljoin(SITE, (section + '/') if section else ''))
    el(chan, 'description', SETTINGS['description'])
    el(chan, 'language', 'en')
    for post in subset:
        node=ET.SubElement(chan, 'item')
        el(node, 'title', post['title']); el(node, 'link', urljoin(SITE, post['url'].lstrip('/')))
        el(node, 'guid', urljoin(SITE, post['url'].lstrip('/')))
        el(node, 'description', post['description'])
        el(node, 'pubDate', datetime.combine(post['date_obj'], datetime.min.time(), tzinfo=timezone.utc).strftime('%a, %d %b %Y %H:%M:%S +0000'))
    (OUT / (f'rss-{section}.xml' if section else 'rss.xml')).write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True))


def sitemap():
    urls=['/', '/about/'] + [f'/{section}/' for section in SECTIONS] + [p['url'] for p in POSTS]
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    root=ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    for path in urls:
        url=ET.SubElement(root, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        ET.SubElement(url, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text=urljoin(SITE,path.lstrip('/'))
    (OUT / 'sitemap.xml').write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True))
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {urljoin(SITE,"sitemap.xml")}\n', encoding='utf-8')


def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT / 'assets', OUT / 'assets')
    homepage()
    for section in SECTIONS: section_page(section)
    for post in POSTS: article(post)
    about()
    rss()
    for section in SECTIONS: rss(section)
    sitemap()
    print(f'Build complete: {len(POSTS)} entries, 3 journals, homepage, about, RSS & sitemap.')
    print(f'Output: {OUT}')


if __name__ == '__main__':
    main()
