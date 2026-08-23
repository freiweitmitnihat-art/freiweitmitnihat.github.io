#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ressourcen-Block in die Blog-Artikel einsetzen.

Warum es das gibt (Befund vom 22.08.2026):
Von 46 Artikeln verlinkten 31 auf die Beratung, aber nur 2 auf die kostenlose
Monatsrechnung und KEIN EINZIGER auf Bibliothek, City Guides, Freiweit-Woche,
Interview-Bewerbung oder Hotels. Die groesste Flaeche der Website leitete alles
in das teuerste Angebot mit der hoechsten Huerde.

Was das Skript macht:
Setzt ueber der Autorenbox (bzw. vor der Fusszeile, wenn es keine gibt) einen
ruhigen Block mit fuenf Verweisen. Die Auswahl richtet sich nach dem Thema des
Artikels, damit bei einem Pattaya-Text der Stadt-Guide oben steht und bei einem
Kostentext die Monatsrechnung.

Eigenschaften:
  · idempotent, ein zweiter Lauf aendert nichts
  · funktioniert auf beiden Artikel-Vorlagen (mit und ohne .article-body)
  · eigener Klassen-Praefix fw-res, kollidiert mit nichts
  · --pruefen zeigt nur die Verteilung, ohne zu schreiben

Aufruf:  python3 tools/ressourcen-block.py [--pruefen] [--erneuern]

--erneuern ersetzt einen bereits vorhandenen Block, noetig wenn sich die
Angebotsliste geaendert hat.
"""
import glob, os, re, sys, collections

BLOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "blog")
NUR_PRUEFEN = "--pruefen" in sys.argv
ERNEUERN = "--erneuern" in sys.argv   # bestehenden Block ersetzen statt ueberspringen
# 6 statt 5 seit 23.08.2026: der Verweis auf die Uebersichtsseite kommt dazu,
# er soll den anderen Zielen keine Plaetze wegnehmen.
MAX_EINTRAEGE = 6

ANGEBOTE = {
    "rechnung":   ("/rechnung",       "Die echte Monatsrechnung",      "Was das Leben wirklich kostet, gratis als PDF"),
    "bibliothek": ("/bibliothek",     "Meine Ratgeber",                "Visum, Wohnung, Krankenversicherung, R&uuml;ckkehr"),
    "guides":     ("/city-guides",    "Meine City Guides",             "Die Orte, die ich selbst getestet habe"),
    "woche":      ("/freiweit-woche", "Die Freiweit-Woche",            "Eine Woche vor Ort, kleine Gruppe"),
    "interview":  ("/interview",      "Deine Geschichte auf dem Kanal", "Auf Wunsch auch anonym"),
    "immobilien": ("/immobilien",     "Immobilien in Asien",           "Mieten, kaufen, verkaufen, mit echten Preisen"),
    "reise":      ("/hotel-reise",    "Hotels und Versicherung",       "Was ich selbst buche, wenn ich unterwegs bin"),
    "quiz":       ("/reality-check",  "Der Reality-Check",             "Zehn Fragen, ehrliche Auswertung"),
    "beratung":   ("/beratung",       "Beratungsgespr&auml;ch",        "60 Minuten, nur deine Situation"),
    "ueberblick-th": ("/auswandern-thailand", "Auswandern nach Thailand",
                      "Kosten, Visum, Wohnen, alles auf einer Seite"),
    "ueberblick-vn": ("/auswandern-vietnam",  "Auswandern nach Vietnam",
                      "Kosten, E-Visum, Da Nang, alles auf einer Seite"),
}

# Land des Artikels, damit jeder Text auf die passende Uebersichtsseite zeigt.
# Das ist der Verweis, der SEO-technisch zaehlt: viele Einzelartikel, die auf
# eine starke Uebersichtsseite deuten.
VIETNAM_WOERTER = ["vietnam", "da nang", "danang", "hanoi", "ho chi minh",
                   "ho-chi-minh", "hoi an", "viettel", "dich vu cong"]
THAILAND_WOERTER = ["thailand", "pattaya", "bangkok", "jomtien", "si racha",
                    "sri racha", "sriracha", "hua hin", "bang saray", "bang saen",
                    "isaan", "chiang mai", "baht"]


def land(text):
    klein = text.lower()
    vn = sum(klein.count(w) for w in VIETNAM_WOERTER)
    th = sum(klein.count(w) for w in THAILAND_WOERTER)
    if vn > th and vn > 2:
        return "ueberblick-vn"
    if th > 2:
        return "ueberblick-th"
    return None

# Reihenfolge = Prioritaet bei der Auswahl
THEMEN = [
    ("immobilien", ["makler", "quadratmeter", "foreign quota", "kaufpreis", "eigentumswohnung",
                    "condo kaufen", "haus kaufen", "villa kaufen", "objekt", "zum verkauf"]),
    ("bibliothek", ["visum", "visa", "e-visum", "tdac", "beh&ouml;rde", "behoerde",
                    "krankenversicherung", "versicherung", "rente", "abwickeln",
                    "r&uuml;ckkehr", "zur&uuml;ckgekehrt", "anwartschaft"]),
    ("guides",     ["pattaya", "bangkok", "jomtien", "si racha", "sriracha", "bang saray",
                    "hua hin", "samui", "da nang", "hoi an", "naklua", "bang saen",
                    "markt", "restaurant", "tempel", "strand", "caf&eacute;"]),
    ("interview",  ["interview", "erz&auml;hlt", "ausgewandert", "auswanderer",
                    "seine geschichte", "im gespr&auml;ch"]),
    ("reise",      ["hotel", "flug", "sim-karte", "sim karte", "grab", "einreise", "ankunft"]),
    ("quiz",       ["fehler", "entscheidung", "&uuml;berlegen", "planen", "passt zu dir"]),
    ("woche",      ["community", "stammtisch", "anschluss", "einsam", "leute kennenlernen"]),
]

# Auffuellen, damit jedes Angebot Verlinkungen bekommt, auch wenn das Thema nicht passt
ROTATION = ["woche", "quiz", "reise", "guides", "woche", "immobilien", "bibliothek", "quiz", "beratung"]

CSS = """
/* Ressourcen-Block, eingesetzt 22.08.2026 (tools/ressourcen-block.py) */
.fw-res{background:#fff;border:1px solid rgba(0,0,0,.09);border-radius:12px;padding:24px 26px;margin:40px 0;max-width:740px}
.fw-res .fw-res-t{font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#A44A18;margin-bottom:14px}
.fw-res a{display:flex;align-items:baseline;gap:10px;padding:11px 0;border-bottom:1px solid rgba(0,0,0,.07);text-decoration:none;transition:color .2s}
.fw-res a:last-child{border-bottom:none;padding-bottom:0}
.fw-res a:hover{color:#A44A18}
.fw-res b{font-size:16.5px;font-weight:600;color:#1a1410;white-space:nowrap}
.fw-res span{font-size:15px;color:#6b5e52;line-height:1.5}
.fw-res .fw-res-p{margin-left:auto;color:#A44A18;font-weight:700;flex-shrink:0}
@media(max-width:600px){.fw-res a{flex-wrap:wrap;gap:2px}.fw-res b{white-space:normal;flex:1 1 100%;min-width:0}.fw-res span{flex:1 1 100%;min-width:0;overflow-wrap:anywhere}.fw-res .fw-res-p{display:none}}
"""


def waehle(dateiname, text, lauf):
    """Fuenf Verweise: immer die Monatsrechnung, dann Thema, dann Rotation."""
    klein = text.lower()
    gewaehlt = []
    ueberblick = land(text)
    if ueberblick:
        gewaehlt.append(ueberblick)
    gewaehlt.append("rechnung")
    MAX_THEMEN = 2
    for schluessel, woerter in THEMEN:
        if len(gewaehlt) >= len(gewaehlt[:2]) + MAX_THEMEN:
            break
        if schluessel in gewaehlt:
            continue
        if any(w in klein for w in woerter):
            gewaehlt.append(schluessel)
    # Der Casting-Aufruf gehoert unter jeden Artikel, er muss sich selbst fuellen
    if "interview" not in gewaehlt:
        gewaehlt.append("interview")
    # Rest reihum auffuellen, damit die Verlinkung sich gleichmaessig verteilt
    i = lauf
    while len(gewaehlt) < MAX_EINTRAEGE:
        kandidat = ROTATION[i % len(ROTATION)]
        i += 1
        if kandidat not in gewaehlt:
            gewaehlt.append(kandidat)
    return gewaehlt[:MAX_EINTRAEGE]


def block(schluessel_liste):
    zeilen = []
    for s in schluessel_liste:
        ziel, titel, text = ANGEBOTE[s]
        zeilen.append(f'  <a href="{ziel}"><b>{titel}</b><span>{text}</span>'
                      f'<span class="fw-res-p">&#8594;</span></a>')
    return ('<div class="fw-res">\n'
            '  <div class="fw-res-t">Das k&ouml;nnte dir weiterhelfen</div>\n'
            + "\n".join(zeilen) + "\n</div>\n\n")


def main():
    dateien = [p for p in sorted(glob.glob(os.path.join(BLOG, "*.html")))
               if os.path.basename(p) not in ("index.html", "blog-template.html")]
    zaehler = collections.Counter()
    gesetzt = uebersprungen = 0

    for lauf, pfad in enumerate(dateien):
        name = os.path.basename(pfad)
        t = open(pfad, encoding="utf-8").read()

        if len(t) < 3000:
            print(f"  uebersprungen (Weiterleitung): {name}"); uebersprungen += 1; continue
        if 'class="fw-res"' in t:
            if not ERNEUERN:
                print(f"  schon vorhanden: {name}"); uebersprungen += 1; continue
            t = re.sub(r'<div class="fw-res">.*?</div>\s*\n\n', '', t, count=1, flags=re.S)

        auswahl = waehle(name, t, lauf)
        for s in auswahl:
            zaehler[s] += 1
        if NUR_PRUEFEN:
            print(f"  {name:44s} {', '.join(auswahl)}")
            continue

        # CSS einsetzen
        if ".fw-res{" not in t:
            if "</style>" in t:
                t = t.replace("</style>", CSS + "</style>", 1)
            else:
                t = re.sub(r"(</head>)", "<style>" + CSS + "</style>\n\\1", t, count=1)

        # Anker: bevorzugt ueber der Autorenbox, sonst vor der Fusszeile
        if '<div class="author-box">' in t:
            i = t.find('<div class="author-box">')
            einzug = ""
            zeilenanfang = t.rfind("\n", 0, i) + 1
            einzug = t[zeilenanfang:i]
            t = t[:zeilenanfang] + einzug + block(auswahl).replace("\n", "\n" + einzug).rstrip() + "\n\n" + t[zeilenanfang:]
        elif "<footer" in t:
            i = t.rfind("<footer")
            t = t[:i] + '<div style="max-width:740px;margin:0 auto;padding:0 20px 40px">\n' + block(auswahl) + "</div>\n" + t[i:]
        else:
            print(f"  KEIN ANKER: {name}"); uebersprungen += 1; continue

        open(pfad, "w", encoding="utf-8").write(t)
        gesetzt += 1

    print()
    print(f"{'Geprueft' if NUR_PRUEFEN else 'Gesetzt'}: {gesetzt if not NUR_PRUEFEN else len(dateien)-uebersprungen}"
          f" · uebersprungen: {uebersprungen}")
    print("Verteilung der Verweise:")
    for s, n in zaehler.most_common():
        print(f"   {n:3d}x  {ANGEBOTE[s][1]}")


if __name__ == "__main__":
    main()
