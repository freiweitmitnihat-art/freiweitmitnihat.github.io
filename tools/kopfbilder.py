#!/usr/bin/env python3
# ============================================================
# KOPFBILDER in die Banner unter der Artikel-Ueberschrift
# ------------------------------------------------------------
# Unter der Ueberschrift liegt in jedem Artikel ein breites
# Banner. Bei einigen Artikeln war das ein reiner Farbverlauf,
# der Leser sah oben also nur eine braune Flaeche.
#
# Diese Datei legt das Artikelbild in dieses Banner. Der
# Farbverlauf bleibt dahinter stehen, falls die Datei fehlt.
#
# Nicht angefasst werden:
#   - Artikel, die schon ein echtes <img class="hero-img"> haben
#   - das dunkle Titelband selbst (article-hero), dort steht
#     weisse Schrift drauf
#
# Vorschau (aendert nichts):  python3 tools/kopfbilder.py
# Wirklich aendern:           python3 tools/kopfbilder.py --schreiben
# ============================================================
import pathlib, re, sys

BASIS = pathlib.Path(__file__).resolve().parent.parent
BILDER = BASIS / 'blog' / 'images'
SCHREIBEN = '--schreiben' in sys.argv
AUS = {'index.html', 'blog-template.html'}

NOINDEX = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)
# Banner-Div, mit oder ohne eigenen style
BANNER = re.compile(
    r'<div class="(hero-color-block|hero-block|hb)"'
    r'(\s+style="background:)?', re.I)
VERLAUF = 'linear-gradient(135deg,#2d1505 0%,#7a3a12 50%,#A44A18 100%)'


def main():
    gesetzt, schon_bild, ohne = [], 0, []
    for f in sorted((BASIS / 'blog').glob('*.html')):
        if f.name in AUS:
            continue
        t = f.read_text(encoding='utf-8')
        if NOINDEX.search(t):
            continue
        if 'class="hero-img"' in t:
            schon_bild += 1
            continue

        bild = BILDER / (f.stem + '.jpg')
        if not bild.exists():
            ohne.append((f.name, 'kein Artikelbild'))
            continue

        m = BANNER.search(t)
        if not m:
            ohne.append((f.name, 'kein Banner gefunden'))
            continue
        if "url('images/" in t[m.start():m.start() + 200]:
            schon_bild += 1
            continue

        neu_bg = "url('images/%s.jpg') center/cover no-repeat, " % f.stem
        if m.group(2):                       # hat schon style="background:"
            t = t[:m.end(2)] + neu_bg + t[m.end(2):]
        else:                                # ganz ohne style
            t = (t[:m.end(1)] + '" style="background:' + neu_bg + VERLAUF + '"'
                 + t[m.end(1) + 1:])
        if SCHREIBEN:
            f.write_text(t, encoding='utf-8')
        gesetzt.append(f.name)

    wort = 'gesetzt' if SCHREIBEN else 'zu setzen (Vorschau)'
    print('Kopfbilder: %d %s, %d hatten schon eines' % (len(gesetzt), wort, schon_bild))
    for n in gesetzt:
        print('  ', n)
    for n, grund in ohne:
        print('   offen:', n, '(%s)' % grund)
    if gesetzt and not SCHREIBEN:
        print('\nZum Anwenden: python3 tools/kopfbilder.py --schreiben')


if __name__ == '__main__':
    main()
