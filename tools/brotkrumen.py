#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sichtbaren Pfad (Brotkrumen) in die Blog-Artikel setzen.

Warum es das gibt (Befund vom 23.08.2026):
In den Strukturdaten behauptet jeder Artikel einen Pfad
"Startseite > Blog > Artikel", auf der Seite selbst war davon nichts zu sehen.
Google mag es, wenn beides zusammenpasst, und zeigt den Pfad dann auch in der
Trefferliste statt der nackten Adresse an.

Dazu kam ein zweites Problem: die Blog-Uebersicht bekam nur 5 interne Verweise,
obwohl 45 Artikel darunter haengen. Damit war die wichtigste Uebersichtsseite
der Website intern fast unsichtbar. Der Pfad verlinkt sie aus jedem Artikel.

Was das Skript macht:
Setzt oben im Textbereich eine Zeile "Startseite > Blog > Artikeltitel".
Der Artikeltitel kommt aus dem <title> der Seite, ist also derselbe Text,
der auch in den Strukturdaten steht.

Eigenschaften:
  - idempotent, ein zweiter Lauf aendert nichts
  - funktioniert auf allen drei Artikel-Vorlagen der Website
  - eigener Klassen-Praefix fw-krumen, kollidiert mit nichts
  - ohne --schreiben nur Vorschau

Aufruf:  python3 tools/brotkrumen.py [--schreiben]
"""
import glob
import html
import os
import re
import sys

BASIS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SCHREIBEN = "--schreiben" in sys.argv
MARKER = 'data-quelle="brotkrumen"'

ANKER = [
    '<main class="article-wrap">',
    '<div class="article-wrap">',
    '<div class="wrap">',
    '<main class="wrap">',
]

# Wichtig: KEIN <nav>-Element benutzen. Zwei der drei Artikel-Vorlagen haben eine
# nackte Regel nav{position:fixed;height:60px}, die jedes nav zur Kopfleiste macht.
# Deshalb ein div mit role="navigation", plus defensive Ruecksetzer im Stil.
STIL = """  <style %s>
.fw-krumen{position:static;height:auto;width:auto;background:none;border:0;box-shadow:none;padding:0;z-index:auto;font-size:15px;line-height:1.6;color:#6b5e52;margin:0 0 26px;display:flex;flex-wrap:wrap;gap:8px;align-items:baseline}
.fw-krumen a{color:#6b5e52;text-decoration:none;border-bottom:1px solid rgba(0,0,0,.18)}
.fw-krumen a:hover,.fw-krumen a:focus-visible{color:#A44A18;border-bottom-color:#A44A18}
.fw-krumen span[aria-hidden]{color:#a09488}
.fw-krumen .fw-krumen-hier{color:#1a1410;font-weight:600}
@media(max-width:600px){.fw-krumen{font-size:14px;margin-bottom:20px}}
  </style>
""" % MARKER


def seitentitel(t):
    m = re.search(r"<title>(.*?)</title>", t, re.S)
    if not m:
        return ""
    s = html.unescape(m.group(1)).strip()
    for suf in (" · Freiweit mit Nihat", " | Freiweit mit Nihat",
                " – Freiweit mit Nihat", " - Freiweit mit Nihat"):
        if s.endswith(suf):
            s = s[: -len(suf)].strip()
    return s


def krumen_html(titel):
    return (
        '\n  <div class="fw-krumen" %s role="navigation" aria-label="Sie sind hier">'
        '<a href="../index.html">Startseite</a>'
        '<span aria-hidden="true">›</span>'
        '<a href="index.html">Blog</a>'
        '<span aria-hidden="true">›</span>'
        '<span class="fw-krumen-hier">%s</span>'
        "</div>\n" % (MARKER, html.escape(titel))
    )


def main():
    gesetzt = schon = uebersprungen = 0
    for pfad in sorted(glob.glob(os.path.join(BASIS, "blog", "*.html"))):
        name = os.path.basename(pfad)
        if name in ("index.html", "blog-template.html"):
            continue
        t = open(pfad, encoding="utf-8").read()
        if "noindex" in t:
            uebersprungen += 1
            continue
        if MARKER in t:
            schon += 1
            continue
        anker = next((a for a in ANKER if a in t), None)
        if not anker:
            print("  kein Anker gefunden: %s" % name)
            uebersprungen += 1
            continue
        titel = seitentitel(t)
        if not titel:
            print("  kein Titel gefunden: %s" % name)
            uebersprungen += 1
            continue
        neu = t.replace(anker, anker + krumen_html(titel), 1)
        if "</head>" in neu:
            neu = neu.replace("</head>", STIL + "</head>", 1)
        gesetzt += 1
        if SCHREIBEN:
            open(pfad, "w", encoding="utf-8").write(neu)

    wort = "gesetzt" if SCHREIBEN else "zu setzen (Vorschau)"
    print("Brotkrumen: %d %s, %d hatten sie schon, %d uebersprungen"
          % (gesetzt, wort, schon, uebersprungen))
    if gesetzt and not SCHREIBEN:
        print("Zum Anwenden: python3 tools/brotkrumen.py --schreiben")


if __name__ == "__main__":
    main()
