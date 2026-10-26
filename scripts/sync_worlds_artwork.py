"""Sync approved Seer Worlds cover designs and illustrations into the web project.

Run python scripts/sync_worlds_artwork.py --source C:/SEERWORLDS.
Use --pages-only after editing the local theme. Requires Pillow, fonttools,
and BeautifulSoup. Never builds or modifies the source books.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import sys

from PIL import Image, ImageOps
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://seerworlds.com'


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version(path):
    path = path.split('?')[0]
    return path + '?v=' + fingerprint(ROOT / path.lstrip('/'))[:12]


def export(source):
    designs = [ast.literal_eval(m) for m in re.findall(r'"cover_design": (\{[^\n]+\})', (source / 'config.py').read_text(encoding='utf-8'))]
    assert len(designs) == 54, 'Expected the 54 current book-specific palettes'
    later = json.loads((source / 'cover-concepts/books10-54-activation.json').read_text(encoding='utf-8'))
    previews = {int(b['book'][4:]): b for b in later['books']}
    covers = ROOT / 'assets/covers'
    scenes = ROOT / 'assets/scenes'
    fonts = ROOT / 'assets/fonts'
    for folder in (covers, scenes, fonts):
        folder.mkdir(exist_ok=True)
    titles = []
    for n in range(1,55):
        copy = (source / f'book{n:02}/images-print/cover-copy.txt').read_text(encoding='utf-8-sig')
        match = re.search(r'^## TITLE[ \t]*\n+([^\n]+)', copy, re.M)
        if not match:
            raise ValueError(f'Missing approved title for book{n:02}')
        titles.append(match[1].strip())
    assert len(set(titles)) == 54, 'Source titles must be unique before exporting'
    records = []
    for n in range(1, 55):
        book = source / f'book{n:02}'
        title = titles[n-1]
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        if n <= 9:
            front_path = book / 'images-print/cover-front.png'
            art_path = book / 'images-print/background-concept4-approved.png'
            kind = 'current production front cover'
        else:
            # Production files for many later books still show the older style.
            # Use the approved native previews explicitly activated in the source.
            front_path = book / 'cover-concepts' / Path(previews[n]['front_preview']).name
            art_path = book / 'images-print/background-concept4-manuscript.png'
            kind = 'approved activated cover preview'
        if not front_path.is_file() or not art_path.is_file():
            raise FileNotFoundError(f'Missing current artwork for {book.name}')
        front = Image.open(front_path).convert('RGB')
        front.thumbnail((1280, 2048), Image.Resampling.LANCZOS)
        cover = covers / f'{slug}.webp'
        front.save(cover, quality=88, method=6)
        if n <= 9:
            front.save(covers / f'{slug}.png', optimize=True)
            if n <= 7:
                shutil.copyfile(cover, ROOT / f'assets/placeholders/book-{n}.webp')
        scene = Image.open(art_path).convert('RGB')
        art = scenes / f'{slug}.webp'
        ImageOps.fit(scene, (1600, 900), Image.Resampling.LANCZOS, centering=(.65, .58)).save(art, quality=87, method=6)
        if n == 1:
            hero = ImageOps.fit(scene, (1920, 1080), Image.Resampling.LANCZOS, centering=(.65, .58))
            hero.save(ROOT / 'assets/seer-worlds-river-hero.webp', quality=90, method=6)
            hero.save(ROOT / 'assets/seer-collections/seer-worlds-20261022.webp', quality=90, method=6)
        records.append({'number': n, 'title': title.title(), 'slug': slug,
                        'cover': f'/assets/covers/{slug}.webp', 'size': list(front.size),
                        'source_cover': front_path.relative_to(source).as_posix(),
                        'source_cover_sha256': fingerprint(front_path), 'cover_kind': kind,
                        'artwork': f'/assets/scenes/{slug}.webp',
                        'source_art': art_path.relative_to(source).as_posix(),
                        'source_art_sha256': fingerprint(art_path),
                        'accent': '#' + ''.join(f'{v:02x}' for v in designs[n-1]['accent'])})
        print(f'Synced {n:02}: {title} ({kind})', flush=True)
    for name in ('AlegreyaSC-Black', 'Charter-Regular', 'Charter-Italic', 'Charter-Bold'):
        font = TTFont(source / 'fonts' / f'{name}.ttf')
        options = subset.Options()
        options.flavor = 'woff'
        worker = subset.Subsetter(options=options)
        worker.populate(unicodes=list(range(0x250)) + list(range(0x2010, 0x2028)) + list(range(0x2190, 0x219A)))
        worker.subset(font)
        font.flavor = 'woff'
        font.save(fonts / f'{name}.woff')
    for name in ('AlegreyaSC-OFL.txt', 'Charter-LICENSE.txt'):
        shutil.copyfile(source / 'fonts' / name, fonts / name)
    (ROOT / 'data/worlds-artwork.json').write_text(json.dumps({'source': 'SEERWORLDS', 'books': records}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    registry = ROOT / 'data/seer-collections.json'
    data = json.loads(registry.read_text(encoding='utf-8'))
    current = next(s for s in data['collections'] if s['slug'] == 'seer-worlds')
    current.update(width=1920, height=1080, alt='An engraved ivory cliff city with blue foliage, a small traveler and the black Dot, from the Distance cover artwork')
    registry.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def development_note():
    return '<aside class="development-note" id="in-development"><div class="development-mark" aria-hidden="true">···</div><div><p class="eyebrow">The journey continues</p><h2>More worlds in development.</h2><p>New worlds, new rules, and more questions are planned. Follow the news for the next books in the journey.</p><a class="text-link" href="/news">Follow the publication news →</a></div></aside>'


def update_pages():
    sys.path.insert(0, str(ROOT / '.runtime'))
    from bs4 import BeautifulSoup
    records = json.loads((ROOT / 'data/worlds-artwork.json').read_text(encoding='utf-8'))['books']
    by_slug = {b['slug']: b for b in records}
    status_path = ROOT / 'data/worlds-publication.json'
    states = json.loads(status_path.read_text(encoding='utf-8')) if status_path.is_file() else {'published': [b['slug'] for b in records[:6]], 'in_review': 'memory', 'in_writing': 'shadows'}
    status_path.write_text(json.dumps(states, indent=2) + '\n', encoding='utf-8')
    css_path = ROOT / 'assets/site.css'
    css = css_path.read_text(encoding='utf-8')
    css = re.sub(r'url\([\"\']?(/assets/[^\s\"\'()]+)[\"\']?\)', lambda m:'url("' + version(m[1]) + '")', css)
    css_path.write_text(css, encoding='utf-8')
    pages = [p for p in ROOT.rglob('*.html') if '.runtime' not in p.relative_to(ROOT).parts]
    for file in pages:
        doc = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
        route = '/' + file.parent.relative_to(ROOT).as_posix().strip('.')
        slug = file.parent.name if file.parent.parent.name == 'books' else None
        book = by_slug.get(slug)
        brand = doc.select_one('.site-header .brand')
        if brand:
            brand.clear()
            brand.append(BeautifulSoup('<span>SEER</span><strong>WORLDS</strong>', 'html.parser'))
        nav = doc.select_one('.main-nav')
        if nav:
            nav['id'] = 'main-nav'
            active = nav.select_one('a.active')
            if active:
                active['aria-current'] = 'page'
        button = doc.select_one('.menu-btn')
        if button:
            button['aria-controls'] = 'main-nav'
        color = doc.select_one('meta[name="theme-color"]')
        if color:
            color['content'] = '#091b29'
        if file == ROOT / '404.html':
            canonical = doc.select_one('link[rel="canonical"]')
            if canonical:
                canonical['href'] = SITE + '/404.html'
            social_url = doc.select_one('meta[property="og:url"]')
            if social_url:
                social_url['content'] = SITE + '/404.html'
        if file == ROOT / 'index.html':
            summary = doc.select_one('meta[property="og:description"]')
            if summary:
                summary['content'] = 'Different worlds. Same curious Dot. Explore the published Seer Worlds books by B. Carter.'
        if not doc.select_one('link[rel="preload"][as="font"]'):
            doc.head.append(BeautifulSoup('<link rel="preload" as="font" href="/assets/fonts/AlegreyaSC-Black.woff" type="font/woff" crossorigin>', 'html.parser'))
        # Use actual illustrated worlds in place of the previous glossy Dot cutout.
        for image in doc.select('.dot-panel img,.dot-stage img'):
            scene_slug = 'lies' if file.parent.name == 'journey' else 'doors'
            image['src'] = by_slug[scene_slug]['artwork']
            image['alt'] = 'The black Dot exploring the engraved world of ' + scene_slug.title()
            image['width'], image['height'] = '1600', '900'
        if book:
            doc.body['class'] = ['book-detail']
            doc.body['style'] = '--book-accent:' + book['accent'] + ';--book-art:url(\'' + version(book['artwork']) + '\')'
            title = doc.select_one('.book-info h1')
            if title:
                title.name = 'h2'
                title['class'] = ['book-display-title']
            if not doc.select_one('meta[property="og:image"]'):
                image_tag = doc.new_tag('meta', property='og:image', content=SITE + book['cover'])
                doc.head.append(image_tag)
            if slug in (states['in_review'], states['in_writing']):
                eyebrow = doc.select_one('.book-info>.eyebrow')
                if eyebrow:
                    eyebrow.string = f'Book {book["number"]} · ' + ('In review' if slug == states['in_review'] else 'In writing')
        for image in doc.select('img[src*="/assets/covers/"]'):
            name = Path(image['src'].split('?')[0]).stem
            if name in by_slug:
                image['width'], image['height'] = map(str, by_slug[name]['size'])
        if file == ROOT / 'index.html':
            hero = doc.select_one('.cinematic-art')
            hero['src'] = '/assets/seer-worlds-river-hero.webp'
            hero['width'], hero['height'] = '1920', '1080'
            hero['alt'] = 'An engraved white cliff city above a blue sea, with blue-leaved trees, a small traveler carrying fruit, and the black Dot, from Distance'
            for tile in doc.select('.approved-placeholder'):
                if tile.get('href', '').rstrip('/').split('/')[-1] not in states['published']:
                    tile.decompose()
            if not doc.select_one('#in-development'):
                shelf = doc.select_one('.approved-books')
                shelf.append(BeautifulSoup(development_note(), 'html.parser'))
        if file == ROOT / 'books/index.html':
            for card in doc.select('.book-card'):
                if card.get('href', '').rstrip('/').split('/')[-1] not in states['published']:
                    card.decompose()
            if not doc.select_one('#in-development'):
                grid = doc.select_one('.books-grid')
                grid.insert_after(BeautifulSoup(development_note(), 'html.parser'))
            for image in doc.select('.book-card img')[:2]:
                image['loading'] = 'eager'
        # Published pages must not funnel visitors into an unreleased book.
        for link in doc.select('.book-nav a'):
            target = link.get('href', '').rstrip('/').split('/')[-1]
            if target in by_slug and target not in states['published']:
                link['href'] = '/books'
                link.string = 'All published books →'
        if file == ROOT / 'news/index.html':
            old = doc.select_one('#progress-update')
            if old:
                old.decompose()
            news = doc.select_one('.news-list')
            review, writing = by_slug[states['in_review']], by_slug[states['in_writing']]
            entry = '<article class="news-item" id="progress-update"><div class="news-date"><time datetime="2026-10-26">October 26, 2026</time><br>Work in progress</div><div><h2>The next worlds are taking shape.</h2><div class="news-progress">'
            for item,label in ((review,'In review'),(writing,'In writing')):
                entry += f'<section><p class="eyebrow">Book {item["number"]:02}</p><h3>{html.escape(item["title"])}</h3><span class="progress-status">{label}</span></section>'
            entry += '</div></div></article>'
            news.insert(0, BeautifulSoup(entry, 'html.parser'))
        for image in doc.find_all('img'):
            if not image.has_attr('decoding'):
                image['decoding'] = 'async'
            if not image.has_attr('loading') and image.get('fetchpriority') != 'high':
                image['loading'] = 'eager' if 'book-cover' in image.get('class',[]) else 'lazy'
        file.write_text(str(doc), encoding='utf-8')
    # Refresh stylesheet, images, fonts, icons and social-image versions in order.
    pattern = re.compile(r'(?P<path>/assets/[^\s\"\'<>?()]+\.(?:css|js|webp|png|svg|woff)|/site\.webmanifest)(?:\?v=[a-zA-Z0-9]+)?')
    for file in pages:
        content = file.read_text(encoding='utf-8')
        content = pattern.sub(lambda m: version(m['path']) if (ROOT / m['path'].lstrip('/')).is_file() else m[0], content)
        file.write_text(content, encoding='utf-8')
    sitemap = ROOT / 'sitemap.xml'
    import xml.etree.ElementTree as ET
    tree = ET.parse(sitemap)
    namespace = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    for url in list(tree.getroot()):
        loc = url.find(namespace + 'loc')
        slug = loc.text.rstrip('/').split('/')[-1]
        if '/books/' in loc.text and slug in by_slug and slug not in states['published']:
            tree.getroot().remove(url)
    ET.register_namespace('', namespace[1:-1])
    tree.write(sitemap, encoding='utf-8', xml_declaration=True)
    print(f'Updated {len(pages)} pages; {len(states["published"])} published books; Memory in review and Shadows in writing.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT.parent / 'SEERWORLDS')
    parser.add_argument('--pages-only', action='store_true')
    parser.add_argument('--assets-only', action='store_true')
    args = parser.parse_args()
    if not args.pages_only:
        export(args.source)
    if not args.assets_only:
        update_pages()
