#!/usr/bin/env python3
# ============================================================
# MARKEN-ZUSATZ aus den Artikel-Titeln nehmen
# ------------------------------------------------------------
# Entscheidung vom 23.08.2026: Blogartikel tragen den Zusatz
# " · Freiweit mit Nihat" nicht mehr. Google zeigt nur rund 60
# Zeichen, und 21 davon an den Markennamen zu verlieren kostet
# genau die Stelle, an der das Schluesselwort stehen sollte.
# Den Kanalnamen setzt Google bei bekannten Seiten ohnehin
# selbst dazu.
#
# Die Funktionsseiten behalten den Zusatz: "Impressum" oder
# "Kontakt" allein waere in einer Trefferliste nicht zuzuordnen.
# Dort ist die Marke der Inhalt, nicht Beiwerk.
#
# Angefasst werden <title>, og:title und twitter:title.
#
# Vorschau (aendert nichts):  python3 tools/titel-marke.py
# Wirklich aendern:           python3 tools/titel-marke.py --schreiben
# ============================================================
import pathlib, re, sys

BASIS = pathlib.Path(__file__).resolve().parent.parent
SCHREIBEN = '--schreiben' in sys.argv
AUS = {'blog-template.html', 'index.html'}   # Uebersicht ist Funktionsseite

NOINDEX = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)
MARKE = re.compile(r'\s*[·|:]\s*Freiweit mit Nihat\s*$')


def ohne_marke(text):
    neu = MARKE.sub('', text).strip()
    return neu if neu else text          # nie einen leeren Titel erzeugen


def main():
    geaendert, schon_gut = [], 0
    for f in sorted((BASIS / 'blog').glob('*.html')):
        if f.name in AUS:
            continue
        t = f.read_text(encoding='utf-8')
        if NOINDEX.search(t):
            continue
        original = t

        m = re.search(r'<title>(.*?)</title>', t, re.S)
        if m:
            t = t[:m.start(1)] + ohne_marke(m.group(1)) + t[m.end(1):]
        for eigenschaft in ('og:title', 'twitter:title'):
            muster = re.compile(
                r'(<meta[^>]+(?:property|name)=["\']%s["\'][^>]*content=["\'])([^"\']*)'
                % re.escape(eigenschaft))
            mm = muster.search(t)
            if mm:
                t = t[:mm.start(2)] + ohne_marke(mm.group(2)) + t[mm.end(2):]

        if t == original:
            schon_gut += 1
            continue
        if SCHREIBEN:
            f.write_text(t, encoding='utf-8')
        geaendert.append(f.name)

    wort = 'bereinigt' if SCHREIBEN else 'zu bereinigen (Vorschau)'
    print('Titel: %d %s, %d waren schon ohne Zusatz' % (len(geaendert), wort, schon_gut))
    for n in geaendert:
        print('  ', n)
    if geaendert and not SCHREIBEN:
        print('\nZum Anwenden: python3 tools/titel-marke.py --schreiben')


if __name__ == '__main__':
    main()
