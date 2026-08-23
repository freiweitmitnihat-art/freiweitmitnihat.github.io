#!/usr/bin/env python3
# ============================================================
# OG-BILDER pruefen und setzen
# ------------------------------------------------------------
# Beim Teilen auf Facebook, WhatsApp und Co. zeigt jede Seite
# das Bild aus <meta property="og:image">. Steht dort das
# allgemeine og-image.jpg, sehen alle geteilten Artikel gleich
# aus und niemand klickt. Diese Datei setzt stattdessen das
# echte Artikelbild, sofern eines vorhanden ist.
#
# Regeln:
#   - nur Blog-Artikel, nicht die Uebersicht und nicht die Vorlage
#   - Seiten auf noindex bleiben unangetastet
#   - genommen wird das erste Bild aus blog/images/, das im
#     Artikel selbst vorkommt und wirklich auf der Platte liegt
#   - hat eine Seite schon ein eigenes Bild, bleibt es stehen
#   - og:image:width und :height werden auf die echten Masse
#     des gesetzten Bildes gezogen, sonst schneidet Facebook falsch
#
# Vorschau (aendert nichts):  python3 tools/og-bilder.py
# Wirklich aendern:           python3 tools/og-bilder.py --schreiben
# ============================================================
import pathlib, re, struct, sys

BASIS = pathlib.Path(__file__).resolve().parent.parent
ROOT = 'https://freiweitmitnihat.com/'
ALLGEMEIN = ROOT + 'og-image.jpg'
SCHREIBEN = '--schreiben' in sys.argv
AUS = {'index.html', 'blog-template.html'}

NOINDEX = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)
OGBILD = re.compile(
    r'(<meta[^>]+property=["\']og:image["\'][^>]*content=["\'])([^"\']+)(["\'])', re.I)


def jpg_masse(pfad):
    """Breite und Hoehe eines JPEG, ohne fremde Bibliothek."""
    try:
        d = pfad.read_bytes()
    except OSError:
        return None
    i = 2
    while i < len(d) - 9:
        if d[i] != 0xFF:
            i += 1
            continue
        marker = d[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            hoehe, breite = struct.unpack('>HH', d[i + 5:i + 9])
            return breite, hoehe
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        i += 2 + struct.unpack('>H', d[i + 2:i + 4])[0]
    return None


def masse_setzen(text, breite, hoehe):
    text = re.sub(r'(og:image:width["\'][^>]*content=["\'])\d+',
                  lambda m: m.group(1) + str(breite), text, flags=re.I)
    return re.sub(r'(og:image:height["\'][^>]*content=["\'])\d+',
                  lambda m: m.group(1) + str(hoehe), text, flags=re.I)


def artikelbild(text):
    """Erstes Bild aus blog/images/, das im Text steht und existiert."""
    for name in dict.fromkeys(re.findall(
            r'images/([A-Za-z0-9._-]+\.(?:jpg|jpeg|png|webp))', text)):
        if (BASIS / 'blog' / 'images' / name).exists():
            return name
    return None


def main():
    gesetzt, korrigiert, schon_gut, ohne_bild = [], [], 0, []
    for f in sorted((BASIS / 'blog').glob('*.html')):
        if f.name in AUS:
            continue
        t = f.read_text(encoding='utf-8')
        original = t
        if NOINDEX.search(t):
            continue
        m = OGBILD.search(t)
        if not m:
            ohne_bild.append((f.name, 'kein og:image-Tag'))
            continue

        if m.group(2) == ALLGEMEIN:
            bild = artikelbild(t)
            if not bild:
                ohne_bild.append((f.name, 'kein eigenes Bild vorhanden'))
                continue
            t = (t[:m.start()] + m.group(1) + ROOT + 'blog/images/' + bild
                 + m.group(3) + t[m.end():])
            gesetzt.append((f.name, bild))
        else:
            schon_gut += 1

        # Masse immer gegen die echte Datei ziehen, auch bei alten Seiten
        aktuell = OGBILD.search(t).group(2).replace(ROOT, '')
        datei = BASIS / aktuell
        masse = jpg_masse(datei) if datei.exists() else None
        if masse:
            vorher = t
            t = masse_setzen(t, masse[0], masse[1])
            if t != vorher and f.name not in [n for n, _ in gesetzt]:
                korrigiert.append((f.name, '%dx%d' % masse))

        if SCHREIBEN and t != original:
            f.write_text(t, encoding='utf-8')

    wort = 'gesetzt' if SCHREIBEN else 'zu setzen (Vorschau)'
    print('OG-Bilder: %d %s, %d Masse korrigiert, %d schon in Ordnung, '
          '%d bleiben allgemein'
          % (len(gesetzt), wort, len(korrigiert), schon_gut, len(ohne_bild)))
    for n, b in gesetzt:
        print('  neu:', n, '->', b)
    for n, masse in korrigiert:
        print('  Masse:', n, '->', masse)
    for n, grund in ohne_bild:
        print('  allgemein:', n, '(%s)' % grund)
    if (gesetzt or korrigiert) and not SCHREIBEN:
        print('\nZum Anwenden: python3 tools/og-bilder.py --schreiben')


if __name__ == '__main__':
    main()
