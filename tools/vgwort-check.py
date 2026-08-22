#!/usr/bin/env python3
# ============================================================
# VG WORT · Zeichen zaehlen
# ------------------------------------------------------------
# Die VG WORT verguetet nur Texte ab 1.800 Zeichen, die im Jahr
# mindestens 1.500 Zugriffe erreichen. Dieses Skript sagt dir,
# welche Artikel die Zeichengrenze ueberhaupt schaffen.
#
#   python3 tools/vgwort-check.py
# ============================================================
import re, pathlib, html

BASIS = pathlib.Path(__file__).resolve().parent.parent
GRENZE = 1800


def fliesstext(t):
    t = re.sub(r'<head.*?</head>', ' ', t, flags=re.S | re.I)
    for tag in ('script', 'style', 'nav', 'footer', 'header', 'svg', 'form'):
        t = re.sub(r'<%s.*?</%s>' % (tag, tag), ' ', t, flags=re.S | re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()


def main():
    reihen = []
    for f in sorted((BASIS / 'blog').glob('*.html')):
        if f.name in ('index.html', 'blog-template.html'):
            continue
        n = len(fliesstext(f.read_text(encoding='utf-8')))
        marke = 'ja' if 'met.vgwort.de' in f.read_text(encoding='utf-8') else 'nein'
        reihen.append((n, f.name, marke))
    reihen.sort(reverse=True)

    schafft = [r for r in reihen if r[0] >= GRENZE]
    print('%d von %d Artikeln erreichen die 1.800 Zeichen\n' % (len(schafft), len(reihen)))
    print('%-8s %-52s %s' % ('Zeichen', 'Datei', 'Zaehlmarke drin'))
    print('-' * 78)
    for n, name, marke in reihen:
        flagge = ' ' if n >= GRENZE else '  zu kurz'
        print('%-8d %-52s %-4s%s' % (n, name, marke, flagge))


if __name__ == '__main__':
    main()
