#!/usr/bin/env python3
# ============================================================
# BLOG-UEBERSICHT pflegen
# ------------------------------------------------------------
# Traegt jeden Artikel aus blog/ in blog/index.html ein, der
# dort noch fehlt, und sortiert alle Karten nach Datum, neueste
# zuerst. Bestehende Karten bleiben unveraendert, auch ihre
# Suchbegriffe.
#
# Nach jedem neuen Blogartikel ausfuehren:
#   python3 tools/blog-index-pflegen.py
# ============================================================
import re, pathlib, html, datetime

BASIS = pathlib.Path(__file__).resolve().parent.parent
BLOG  = BASIS / 'blog'
LAND  = {'thailand': ('bc-th', 'Thailand'), 'vietnam': ('bc-vn', 'Vietnam'),
         'auswandern': ('bc-aus', 'Auswandern'), 'all': ('bc-aus', 'Auswandern')}
VERLAUF = "linear-gradient(135deg,#2d1505 0%,#7a3a12 50%,#c4622d 100%)"
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
          'August', 'September', 'Oktober', 'November', 'Dezember']


def lastmod():
    sm = (BASIS / 'sitemap.xml').read_text(encoding='utf-8')
    d = {}
    for m in re.finditer(r'<loc>https://freiweitmitnihat\.com/blog/([^<]*)</loc><lastmod>([^<]+)</lastmod>', sm):
        d[m.group(1)] = m.group(2)
    return d


def meta(t, key, attr='name'):
    m = re.search(r'<meta\s+%s=["\']%s["\']\s+content=["\'](.*?)["\']' % (attr, key), t, re.S)
    return html.unescape(m.group(1)).strip() if m else ''


def titel(t):
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    if not m:
        return ''
    s = html.unescape(m.group(1)).strip()
    for suf in (' · Freiweit mit Nihat', ' | Freiweit mit Nihat', ' – Freiweit mit Nihat'):
        if s.endswith(suf):
            s = s[:-len(suf)].strip()
    return s


def land_erkennen(t):
    text = t.lower()
    if text.count('vietnam') > text.count('thailand'):
        return 'vietnam'
    if 'thailand' in text or 'pattaya' in text or 'racha' in text or 'bangkok' in text:
        return 'thailand'
    return 'auswandern'


def lesezeit(t):
    roh = re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style|nav|footer).*?</\1>', ' ', t, flags=re.S | re.I))
    woerter = len(re.sub(r'\s+', ' ', roh).split())
    return max(3, round(woerter / 200))


def bild_pfad(name, t):
    og = meta(t, 'og:image', 'property')
    if og and '/blog/images/' in og:
        return 'images/' + og.rsplit('/', 1)[-1]
    kandidat = BLOG / 'images' / (name.replace('.html', '.jpg'))
    return 'images/' + kandidat.name if kandidat.exists() else ''


def karte_bauen(name, t, datum):
    lnd = land_erkennen(t)
    klasse, beschriftung = LAND[lnd]
    ttl = titel(t)
    besch = meta(t, 'description') or meta(t, 'og:description', 'property')
    bild = bild_pfad(name, t)
    hintergrund = ("url('%s') center/cover no-repeat, %s" % (bild, VERLAUF)) if bild else VERLAUF
    j, m, _ = datum.split('-')
    datumstext = '%s %s' % (MONATE[int(m) - 1], j)
    suche = re.sub(r'[^a-zäöüß0-9 ]', ' ', (ttl + ' ' + besch).lower())
    suche = ' '.join(dict.fromkeys(suche.split()))[:240]
    return (
        '    <a href="%s" class="blog-card" data-land="%s" data-search="%s">\n'
        '      <div class="blog-thumb">\n'
        '        <div class="blog-thumb-grad" style="background:%s"></div>\n'
        '        <span class="blog-country %s">%s</span>\n'
        '      </div>\n'
        '      <div class="blog-body">\n'
        '        <div class="blog-meta">%s &middot; %d Min. Lesezeit</div>\n'
        '        <h3 class="blog-title">%s</h3>\n'
        '        <p class="blog-excerpt">%s</p>\n'
        '        <span class="blog-link">Artikel lesen &#8594;</span>\n'
        '      </div>\n'
        '    </a>\n'
        % (name, lnd, suche, hintergrund, klasse, beschriftung,
           datumstext, lesezeit(t), html.escape(ttl), html.escape(besch))
    )


def main():
    idx = BLOG / 'index.html'
    t = idx.read_text(encoding='utf-8')
    daten = lastmod()

    anfang = t.index('<div class="blog-grid" id="grid">') + len('<div class="blog-grid" id="grid">')
    rest = t[anfang:]
    # Das Grid endet mit der LETZTEN Karte, nicht mit dem letzten </a> der Seite.
    # Sonst verschluckt der Schnitt die schliessenden Tags und den Fusszeilen-Anfang.
    stuecke_m = list(re.finditer(r'    <a href="[^"]+" class="blog-card".*?</a>\n?', rest, re.S))
    if not stuecke_m:
        print('Keine Karten gefunden, nichts geaendert')
        return
    letzte = stuecke_m[-1].end()
    grid, schwanz = rest[:letzte], rest[letzte:]

    stuecke = [m.group(0) for m in stuecke_m]
    vorhanden = {re.search(r'href="([^"]+)"', s).group(1): s for s in stuecke}

    alle = sorted(p.name for p in BLOG.glob('*.html')
                  if p.name not in ('index.html', 'blog-template.html'))
    neu = 0
    for name in alle:
        if name in vorhanden:
            continue
        roh = (BLOG / name).read_text(encoding='utf-8')
        datum = daten.get(name, datetime.date.today().isoformat())
        vorhanden[name] = karte_bauen(name, roh, datum)
        neu += 1
        print('  ergaenzt:', name)

    def sortierschluessel(name):
        return daten.get(name, '0000-00-00')

    geordnet = sorted(vorhanden, key=sortierschluessel, reverse=True)
    neues_grid = '\n' + '\n'.join(vorhanden[n].rstrip('\n') for n in geordnet) + '\n  '
    idx.write_text(t[:anfang] + neues_grid + schwanz, encoding='utf-8')
    print('Blog-Uebersicht: %d Karten gesamt, %d neu' % (len(geordnet), neu))


if __name__ == '__main__':
    main()
