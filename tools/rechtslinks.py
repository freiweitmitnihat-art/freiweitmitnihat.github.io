#!/usr/bin/env python3
# ============================================================
# RECHTSLINKS in jede Fusszeile
# ------------------------------------------------------------
# Impressum und Datenschutzerklaerung muessen von jeder Seite aus
# erreichbar sein, nicht nur von der Startseite. Seit die Website
# verkauft (Beratung, Digistore, Stripe), zaehlt das doppelt.
#
# Diese Datei haengt die beiden Links an die Copyright-Zeile der
# Fusszeile an, aber nur dort, wo sie fehlen. Seiten auf noindex
# und 404.html bleiben aussen vor.
#
# Vorschau (aendert nichts):  python3 tools/rechtslinks.py
# Wirklich aendern:           python3 tools/rechtslinks.py --schreiben
# ============================================================
import pathlib, re, sys

BASIS = pathlib.Path(__file__).resolve().parent.parent
SCHREIBEN = '--schreiben' in sys.argv
TRENNER = '&nbsp;&middot;&nbsp;'

NOINDEX = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)


def hat_link(text, ziel):
    for treffer in re.findall(r'href=["\']([^"\']*%s[^"\']*)["\']' % ziel, text, re.I):
        if 'vgwort' in treffer or treffer.startswith('#'):
            continue
        if '#' in treffer:          # Anker auf die Startseite zaehlt nicht,
            continue                # die Sprungmarken gibt es dort nicht
        return True
    return False


def main():
    seiten = sorted(list(BASIS.glob('*.html')) + list((BASIS / 'blog').glob('*.html')))
    ergaenzt, schon_gut, unklar = [], 0, []

    for f in seiten:
        t = f.read_text(encoding='utf-8')
        if NOINDEX.search(t) or f.name == '404.html':
            continue
        if hat_link(t, 'impressum') and hat_link(t, 'datenschutz'):
            schon_gut += 1
            continue

        vor = '../' if f.parent.name == 'blog' else ''
        zusatz = (' %s <a href="%simpressum.html">Impressum</a>'
                  ' %s <a href="%sdatenschutz.html">Datenschutz</a>'
                  % (TRENNER, vor, TRENNER, vor))

        # An die letzte Absatz-Zeile der Fusszeile anhaengen, das ist
        # ueberall die Copyright-Zeile.
        fuss = list(re.finditer(r'<footer[^>]*>.*?</footer>', t, re.S | re.I))
        if not fuss:
            unklar.append((f.name, 'keine Fusszeile gefunden'))
            continue
        block = fuss[-1]
        absaetze = list(re.finditer(r'</p>', block.group(0), re.I))
        if not absaetze:
            unklar.append((f.name, 'kein Absatz in der Fusszeile'))
            continue
        letzter = absaetze[-1]
        stelle = block.start() + letzter.start()
        t = t[:stelle] + zusatz + t[stelle:]

        # Anker-Links auf die Startseite waren immer schon tot
        t = t.replace('href="index.html#impressum"', 'href="impressum.html"')
        t = t.replace('href="index.html#datenschutz"', 'href="datenschutz.html"')

        if SCHREIBEN:
            f.write_text(t, encoding='utf-8')
        ergaenzt.append(str(f.relative_to(BASIS)))

    wort = 'ergaenzt' if SCHREIBEN else 'zu ergaenzen (Vorschau)'
    print('Rechtslinks: %d %s, %d hatten sie schon, %d unklar'
          % (len(ergaenzt), wort, schon_gut, len(unklar)))
    for n in ergaenzt:
        print('  ', n)
    for n, grund in unklar:
        print('   UNKLAR:', n, '(%s)' % grund)
    if ergaenzt and not SCHREIBEN:
        print('\nZum Anwenden: python3 tools/rechtslinks.py --schreiben')


if __name__ == '__main__':
    main()
