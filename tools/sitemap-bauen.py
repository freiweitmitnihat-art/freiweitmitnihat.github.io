#!/usr/bin/env python3
# ============================================================
# SITEMAP bauen fuer freiweitmitnihat.com
# ------------------------------------------------------------
# Erzeugt sitemap.xml aus dem tatsaechlichen Dateibestand.
# Seiten mit noindex und interne Testseiten bleiben draussen,
# tote Eintraege verschwinden von selbst.
#
# Das Datum einer Seite bleibt erhalten, solange die Seite schon
# in der alten Sitemap stand. Nur neue Seiten bekommen ein neues.
# Bei echter inhaltlicher Ueberarbeitung: --neu <pfad> mitgeben.
#
#   python3 tools/sitemap-bauen.py
#   python3 tools/sitemap-bauen.py --neu blog/mein-artikel.html
# ============================================================
import re, sys, pathlib, subprocess, datetime

ROOT  = 'https://freiweitmitnihat.com/'
BASIS = pathlib.Path(__file__).resolve().parent.parent
AUS   = {'404.html', 'index-alt.html', 'index-vorher-b.html', 'blog-template.html'}

WICHTIG = {
    'index.html': '1.0', 'beratung.html': '0.9', 'immobilien.html': '0.9',
    'interview.html': '0.9', 'city-guides.html': '0.9', 'ratgeber.html': '0.8',
    'kontakt.html': '0.7', 'mediakit.html': '0.7', 'reality-check.html': '0.8',
    'rechnung.html': '0.8', 'blog/index.html': '0.8', 'agb.html': '0.3',
}


# Nur ein echtes robots-Meta zaehlt. Das blosse Wort "noindex" in einem
# HTML-Kommentar hat frueher fertige Seiten aus der Sitemap geworfen.
NOINDEX = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)


def hat_noindex(text):
    return bool(NOINDEX.search(text))


def alte_daten():
    p = BASIS / 'sitemap.xml'
    if not p.exists():
        return {}
    sm = p.read_text(encoding='utf-8')
    d = {}
    for m in re.finditer(r'<loc>https://freiweitmitnihat\.com/([^<]*)</loc><lastmod>([^<]+)</lastmod>', sm):
        d[m.group(1) or 'index.html'] = m.group(2)
    return d


def git_datum(rel):
    try:
        aus = subprocess.run(['git', 'log', '-1', '--format=%as', '--', str(rel)],
                             cwd=BASIS, capture_output=True, text=True, timeout=10)
        if aus.stdout.strip():
            return aus.stdout.strip()
    except Exception:
        pass
    return None


def main():
    frisch = set(a for a in sys.argv[1:] if a != '--neu')
    heute  = datetime.date.today().isoformat()
    alt    = alte_daten()

    seiten = sorted(list(BASIS.glob('*.html')) + list((BASIS / 'blog').glob('*.html')))
    zeilen, drin, raus = [], 0, []
    for f in seiten:
        rel = str(f.relative_to(BASIS))
        t = f.read_text(encoding='utf-8')
        if rel in AUS or f.name in AUS or hat_noindex(t):
            raus.append(rel)
            continue
        url = ROOT if rel == 'index.html' else ROOT + rel
        if rel in frisch or rel not in alt:
            datum = heute if rel in frisch else (git_datum(rel) or heute)
        else:
            datum = alt[rel]
        prio = WICHTIG.get(rel, '0.6' if rel.startswith('blog/') else '0.7')
        zeilen.append('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>'
                      % (url, datum, prio))
        drin += 1

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + '\n'.join(zeilen) + '\n</urlset>\n')
    (BASIS / 'sitemap.xml').write_text(xml, encoding='utf-8')
    print('Sitemap neu gebaut: %d Seiten drin, %d bewusst draussen' % (drin, len(raus)))
    for r in raus:
        print('  draussen:', r)


if __name__ == '__main__':
    main()
