#!/usr/bin/env python3
# ============================================================
# VG WORT · Zaehlmarken einbauen
# ------------------------------------------------------------
# Liest tools/vgwort-marken.txt und setzt pro Artikel den
# 1x1-Pixel direkt vor </body>. Statisch, also ohne JavaScript,
# damit die VG WORT jeden Aufruf zaehlt.
#
# Format der Liste (eine Zeile je Artikel):
#   dateiname.html  https://vg0X.met.vgwort.de/na/DEIN-CODE
# Zeilen mit # sind Kommentare, leere Felder werden uebersprungen.
#
#   python3 tools/vgwort-einbau.py
# ============================================================
import re, pathlib

BASIS = pathlib.Path(__file__).resolve().parent.parent
LISTE = BASIS / 'tools' / 'vgwort-marken.txt'
MARKER = 'data-quelle="vgwort"'


def main():
    if not LISTE.exists():
        print('Liste fehlt:', LISTE)
        return

    gesetzt, offen, fehler = 0, 0, []
    for zeile in LISTE.read_text(encoding='utf-8').splitlines():
        zeile = zeile.strip()
        if not zeile or zeile.startswith('#'):
            continue
        teile = zeile.split()
        name = teile[0]
        url = teile[1] if len(teile) > 1 else ''
        ziel = BASIS / 'blog' / name
        if not ziel.exists():
            fehler.append('Datei fehlt: ' + name)
            continue
        if not url:
            offen += 1
            continue
        if not re.match(r'^https://vg\d+\.met\.vgwort\.de/na/[A-Za-z0-9]+$', url):
            fehler.append('Adresse sieht falsch aus bei %s: %s' % (name, url))
            continue

        t = ziel.read_text(encoding='utf-8')
        t = re.sub(r'[ \t]*<img[^>]*%s[^>]*>\s*\n?' % re.escape(MARKER), '', t)
        pixel = ('  <img src="%s" width="1" height="1" alt="" %s '
                 'style="position:absolute;left:-9999px" aria-hidden="true">\n'
                 % (url, MARKER))
        if '</body>' not in t:
            fehler.append('kein </body> in ' + name)
            continue
        t = t.replace('</body>', pixel + '</body>', 1)
        ziel.write_text(t, encoding='utf-8')
        gesetzt += 1

    if gesetzt:
        ds = BASIS / 'datenschutz.html'
        d = ds.read_text(encoding='utf-8')
        if 'VGWORT-BLOCK-ANFANG' in d:
            d = d.replace('<!-- VGWORT-BLOCK-ANFANG (wird von tools/vgwort-einbau.py '
                          'aktiviert, sobald die erste Zaehlmarke gesetzt ist)', '')
            d = d.replace('VGWORT-BLOCK-ENDE -->', '')
            ds.write_text(d, encoding='utf-8')
            print('Datenschutzerklaerung: Abschnitt zur Zaehlmarke aktiviert')

    print('Zaehlmarken gesetzt: %d' % gesetzt)
    print('Noch ohne Marke:     %d' % offen)
    for f in fehler:
        print('  ACHTUNG:', f)


if __name__ == '__main__':
    main()
