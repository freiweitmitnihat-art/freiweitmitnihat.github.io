#!/usr/bin/env python3
# ============================================================
# VORSCHAUBILDER in alle Kacheln
# ------------------------------------------------------------
# Die Kacheln auf der Blog-Uebersicht und die "Weitere Artikel"-
# Kaesten am Ende jedes Artikels zeigten teils nur einen
# Farbverlauf. Das sieht nach Baustelle aus.
#
# Diese Datei legt das echte Artikelbild darueber und laesst den
# Farbverlauf als Notfall dahinter stehen, falls eine Bilddatei
# einmal fehlt. Gibt es kein Bild, bleibt die Kachel wie sie ist.
#
# Betroffen sind drei Kachel-Arten:
#   blog-thumb-grad   Blog-Uebersicht
#   more-thumb        "Weitere Artikel" am Artikelende
#   prev-thumb        Vorschau-Kaesten auf anderen Seiten
#
# Vorschau (aendert nichts):  python3 tools/vorschaubilder.py
# Wirklich aendern:           python3 tools/vorschaubilder.py --schreiben
# ============================================================
import pathlib, re, sys

BASIS = pathlib.Path(__file__).resolve().parent.parent
BILDER = BASIS / 'blog' / 'images'
SCHREIBEN = '--schreiben' in sys.argv

# <a href="artikel.html" ... class="...card"> ... <div class="...thumb..."
#   style="background:linear-gradient(...)">
# Die Kacheln heissen in aelteren Artikeln kuerzer: mc statt more-card,
# mt bzw. mt2 statt more-thumb. Beide Schreibweisen muessen rein, sonst
# bleiben 34 Kacheln als Farbverlauf stehen.
KACHEL = re.compile(
    r'(<a\s+href="(?:\.\./blog/|blog/)?([a-z0-9._-]+)\.html"[^>]*'
    r'class="(?:[^"]*card[^"]*|mc)"[^>]*>'
    r'(?:(?!</a>).){0,400}?'
    r'class="(?:blog-thumb-grad|more-thumb|prev-thumb|mt|mt2)"\s+style="background:)'
    r'(linear-gradient)',
    re.S)


def bild_fuer(stamm):
    p = BILDER / (stamm + '.jpg')
    return p if p.exists() else None


def main():
    seiten = sorted(list(BASIS.glob('*.html')) + list((BASIS / 'blog').glob('*.html')))
    gefuellt, ohne_bild = 0, {}

    for f in seiten:
        t = f.read_text(encoding='utf-8')
        original = t
        vor = 'blog/images/' if f.parent == BASIS else 'images/'

        # von hinten nach vorne ersetzen, damit die Positionen stimmen
        for m in reversed(list(KACHEL.finditer(t))):
            stamm = m.group(2)
            if not bild_fuer(stamm):
                ohne_bild.setdefault(stamm, 0)
                ohne_bild[stamm] += 1
                continue
            ersatz = "url('%s%s.jpg') center/cover no-repeat, linear-gradient" % (vor, stamm)
            t = t[:m.start(3)] + ersatz + t[m.end(3):]
            gefuellt += 1

        if SCHREIBEN and t != original:
            f.write_text(t, encoding='utf-8')

    wort = 'gefuellt' if SCHREIBEN else 'zu fuellen (Vorschau)'
    print('Kacheln: %d %s' % (gefuellt, wort))
    if ohne_bild:
        print('\nKein Artikelbild vorhanden, Kachel bleibt Farbverlauf:')
        for stamm, n in sorted(ohne_bild.items()):
            print('   %-45s %dx' % (stamm, n))
    if gefuellt and not SCHREIBEN:
        print('\nZum Anwenden: python3 tools/vorschaubilder.py --schreiben')


if __name__ == '__main__':
    main()
