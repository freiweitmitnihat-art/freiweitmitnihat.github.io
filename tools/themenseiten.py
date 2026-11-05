#!/usr/bin/env python3
# ============================================================
# THEMENSEITEN bauen: Wohnen in Thailand, Rente in Thailand
# ------------------------------------------------------------
# Sammelseiten, die alle Artikel eines Themas buendeln. Sie sind
# das Ziel fuer Suchbegriffe wie "Wohnung mieten Thailand" oder
# "Rente in Thailand Erfahrungen", die kein einzelner Artikel
# allein tragen kann. Die Artikel kommen aus tools/themen.py,
# neue fallen beim naechsten Lauf automatisch hinein.
#
# Gestaltung, Kopf und Fuss kommen von auswandern-thailand.html,
# damit die Seiten aussehen wie die Uebersichtsseiten.
#
# Die Zahlen in der Wohnungstabelle stehen in PREISE, jeweils so,
# wie sie in Titel oder Beschreibung des Artikels stehen. Nichts
# erfinden: was der Artikel nicht nennt, bleibt leer. Fehlt ein
# neuer Wohnartikel in PREISE, meldet das Skript ihn.
#
#   python3 tools/themenseiten.py
# Danach: sitemap-bauen, seo-strukturdaten, seo-pruefen.
# ============================================================
import re, sys, html, os
sys.path.insert(0, os.path.dirname(__file__))
import themen

BASIS = themen.BASIS
VORLAGE = BASIS / 'auswandern-thailand.html'

ORTNAME = {'bangkok': 'Bangkok', 'pattaya': 'Pattaya und Jomtien', 'hua-hin': 'Hua Hin',
           'si-racha': 'Si Racha', 'bang-saray': 'Bang Saray', 'bang-saen': 'Bang Saen',
           'koh-samui': 'Koh Samui', 'phuket': 'Phuket'}
ORTKURZ = {'pattaya': 'Pattaya'}
ORTFOLGE = ['bangkok', 'pattaya', 'hua-hin', 'si-racha', 'bang-saray', 'bang-saen', 'koh-samui', 'phuket']

# datei: (Objekt, Miete pro Monat, Groesse, Miete in Euro als Zahl fuer die Spanne oder None)
PREISE = {
    'si-racha-the-near-residence.html':        ('The Near Residence', '162 €', '35 m²', 162),
    'sharmonyx-sriracha-wohnungen.html':       ('Sharmonyx', '186 €', 'Studio', 186),
    'bang-saray-condo-miete-nebenkosten.html': ('Condo in Bang Saray', '210 €', '', 210),
    'si-racha-the-strand.html':                ('The Strand', '216 €', 'Studio', 216),
    'excel-hideaway-sukhumvit-71.html':        ('Excel Hideaway Sukhumvit 71', '270 €', '28 m²', 270),
    'ladda-condoview.html':                    ('Ladda Condo View', 'ab 270 €', '', 270),
    'jomtien-oliver-lalana.html':              ('Baan Suan Lalana', 'ab 300 €', 'Studio', 300),
    'bangkok-cu-ihouse-guenstig-wohnen-siam.html': ('CU iHouse', 'ab 340 €', 'Studio', 340),
    'hua-hin-dusit-d2-wohnung-miete.html':     ('Dusit D2', '469 €', '30 m²', 469),
    'hua-hin-la-habana-wohnung-miete.html':    ('La Habana', 'ab 20.000 Baht', '34 m²', None),
    'bangkok-paar-condo-huai-khwang.html':     ('Condo in Huai Khwang', '520 €', '40 m²', 520),
    'bangkok-condo-skyrise-sukhumvit-64-miete.html': ('Skyrise Avenue Sukhumvit 64', '547 €', '35 m²', 547),
    'riviera-ocean-drive.html':                ('Riviera Ocean Drive', '550 €', '35 m²', 550),
    'bangkok-ideo-rama-9-wohnung-miete.html':  ('Ideo Rama 9', 'knapp 600 €', '', 600),
    'bangkok-xt-phayathai-wohnung-miete.html': ('XT Phayathai', '651 €', '43 m²', 651),
    'bangkok-noble-be33-wohnung-miete.html':   ('Noble BE33', '677 €', '35 m²', 677),
    'trio-town-si-racha.html':                 ('Trio Town, Haus mit 3 Zimmern', '675 €', '', None),
    'the-complete-sriracha-2.html':            ('The Complete, Haus', '917 €', '220 m²', None),
}
KAUF = {
    'si-racha-the-near-residence.html':   ('The Near Residence', 'ab 27.000 €', ''),
    'sharmonyx-sriracha-wohnungen.html':  ('Sharmonyx', 'ab 52.000 €', ''),
    '2026-06-16-thomas-loft-pattaya.html': ('Loft-Condo in Jomtien', '78.000 €', '82 m²'),
    'si-racha-immobilie.html':            ('Doppelhaushälfte bei Si Racha', '124.000 €', '164 m²'),
    'sri-racha-the-complete.html':        ('The Complete, Haus', '230.000 €', 'über 200 m²'),
    'haus-kaufen-thailand-pacht-hua-hin.html': ('Haus in Hua Hin, 2 Schlafzimmer', 'knapp 2,5 Mio. Baht', ''),
    'bang-saray-resort.html':             ('Resort in Bang Saray', '51 Mio. Baht Gutachten', '24 Zimmer'),
}
OHNE_PREIS = {'pattaya-poolvilla-guido-dojo-miete.html', 'jomtien-condo-kaufen-vermieten.html',
              '2026-06-16-thomas-loft-pattaya.html'}


def e(s):
    return html.escape(s, quote=True)


def schale():
    """Kopf (Stil, Header) und Fuss aus der Vorlage."""
    t = VORLAGE.read_text(encoding='utf-8')
    stil = re.search(r'<style>.*?</style>', t, re.S).group(0)
    header = re.search(r'<header class="top">.*?</header>', t, re.S).group(0)
    fuss = re.search(r'<footer>.*', t, re.S).group(0)
    return stil, header, fuss


def kopf(titel, beschreibung, datei, bild):
    url = 'https://freiweitmitnihat.com/' + datei
    return ('<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<meta name="description" content="%(b)s">\n<title>%(t)s</title>\n'
            '<link rel="canonical" href="%(u)s">\n'
            '<meta property="og:site_name" content="Freiweit mit Nihat">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:title" content="%(t)s">\n'
            '<meta property="og:description" content="%(b)s">\n'
            '<meta property="og:url" content="%(u)s">\n'
            '<meta property="og:image" content="%(i)s">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="twitter:title" content="%(t)s">\n'
            '<meta name="twitter:description" content="%(b)s">\n'
            '<meta name="twitter:image" content="%(i)s">\n'
            '<link rel="icon" href="/favicon-512.png">\n'
            '<link rel="stylesheet" href="/fonts/fonts.css">\n'
            % {'t': e(titel), 'b': e(beschreibung), 'u': url, 'i': bild})


def links(liste, art):
    return ''.join('\n    <a href="%s"><span>%s</span><em>%s</em></a>'
                   % (a['url'], e(a['titel']), art(a)) for a in liste)


def art_von(a):
    if 'interview' in a['themen']:
        return 'Interview'
    if 'kaufen' in a['themen'] and 'wohnen' not in a['themen']:
        return 'Kaufen'
    return 'Artikel'


def seite(datei, titel, beschreibung, bild, krume, kick, h1, lead, inhalt, schluss):
    stil, header, fuss = schale()
    zusatz = ('<style data-quelle="themenseiten">.buehne-in{grid-template-columns:1fr}'
              '.liste td a{color:var(--ink)}.liste td:first-child{min-width:9em}'
              '.liste td:not(:first-child){padding-left:14px}'
              '@media(max-width:600px){.liste td:nth-child(2),.liste th:nth-child(2){display:none}.liste td,.liste th{font-size:16px}.liste td:not(:first-child){white-space:normal}}</style>\n')
    return (kopf(titel, beschreibung, datei, bild) + stil + '\n' + zusatz + '</head>\n<body>\n\n'
            + header + '\n\n<div class="wrap"><div class="krumen"><a href="/">Startseite</a>'
            '<span aria-hidden="true">›</span><a href="/auswandern-thailand.html">Auswandern nach Thailand</a>'
            '<span aria-hidden="true">›</span><span class="hier">%s</span></div></div>\n\n' % e(krume)
            + '<section class="buehne">\n  <div class="wrap buehne-in">\n    <div>\n'
            '      <div class="kick">%s</div>\n      <h1>%s</h1>\n      <p class="lead">%s</p>\n'
            '    </div>\n  </div>\n</section>\n' % (kick, h1, lead)
            + inhalt + schluss + '\n' + fuss)


def wohnen(alle):
    w = [a for a in alle if a['land'] != 'vietnam' and 'wohnen' in a['themen']]
    k = [a for a in alle if a['land'] != 'vietnam' and 'kaufen' in a['themen']]
    nach_datei = {a['datei']: a for a in alle}
    fehlt = [a['datei'] for a in w if a['datei'] not in PREISE and a['datei'] not in OHNE_PREIS]

    zeilen = []
    for datei, (obj, miete, groesse, _) in PREISE.items():
        a = nach_datei.get(datei)
        if not a:
            continue
        ort = next((ORTKURZ.get(o, ORTNAME[o]) for o in ORTFOLGE if o in a['orte']), '')
        zeilen.append('    <tr><td><a href="%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td></tr>'
                      % (a['url'], e(obj), e(ort), e(miete), e(groesse)))
    kauf = []
    for datei, (obj, preis, groesse) in KAUF.items():
        a = nach_datei.get(datei)
        if a:
            ort = next((ORTKURZ.get(o, ORTNAME[o]) for o in ORTFOLGE if o in a['orte']), '')
            kauf.append('    <tr><td><a href="%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td></tr>'
                        % (a['url'], e(obj), e(ort), e(preis), e(groesse)))

    euro = [(v[3], v[0], d) for d, v in PREISE.items() if v[3] and d in nach_datei
            and 'Haus' not in v[0]]
    tief, hoch = min(euro), max(euro)
    ort_von = lambda d: next((ORTNAME[o] for o in ORTFOLGE if o in nach_datei[d]['orte']), '')

    kurz = ('\n<section><div class="wrap eng">\n  <div class="kurz">\n    <h2>Kurz gesagt</h2>\n    <ul>'
            '\n      <li>Die günstigste Wohnung auf dieser Seite kostet <strong>%d € im Monat</strong> (%s, %s).</li>'
            '\n      <li>Die teuerste kostet <strong>%d € im Monat</strong> (%s, %s).</li>'
            '\n      <li>Zu jeder Wohnung gibt es ein Video und einen Artikel mit allen Zahlen. Die Preise stammen vom Drehtag.</li>'
            '\n    </ul>\n  </div>\n</div></section>\n'
            % (tief[0], e(tief[1]), ort_von(tief[2]), hoch[0], e(hoch[1]), ort_von(hoch[2])))

    tabelle = ('\n<section style="background:var(--paper-2);padding-top:clamp(34px,4vw,58px)"><div class="wrap eng">'
               '\n  <div class="kick-d">Mieten</div>\n  <h2>Alle Wohnungen mit Miete und Größe</h2>'
               '\n  <p>Sortiert nach Miete. Ein Klick auf den Namen führt zum Artikel mit dem Video und allen Zahlen.</p>'
               '\n  <table class="liste">\n    <tr><th>Wohnung</th><th>Ort</th><th>Miete im Monat</th><th>Größe</th></tr>\n'
               + '\n'.join(zeilen) + '\n  </table>\n</div></section>\n')

    orte = ''
    for o in ORTFOLGE:
        liste = [a for a in w if o in a['orte']]
        if len(liste) < 2:
            continue
        orte += ('\n<section><div class="wrap eng">\n  <div class="kick-d">%s</div>'
                 '\n  <h2>Wohnen in %s</h2>\n  <div class="mehr">%s\n  </div>\n</div></section>\n'
                 % (ORTNAME[o], ORTNAME[o], links(liste, art_von)))

    kaufen = ('\n<section style="background:var(--paper-2)"><div class="wrap eng">'
              '\n  <div class="kick-d">Kaufen</div>\n  <h2>Kaufen statt mieten</h2>'
              '\n  <p>Diese Objekte standen zum Zeitpunkt des Drehs zum Verkauf. Was Ausländer kaufen dürfen und was nicht, steht in den Artikeln selbst.</p>'
              '\n  <table class="liste">\n    <tr><th>Objekt</th><th>Ort</th><th>Preis</th><th>Größe</th></tr>\n'
              + '\n'.join(kauf) + '\n  </table>'
              '\n  <div class="mehr">%s\n  </div>\n</div></section>\n'
              % links([a for a in k if a['datei'] not in KAUF], art_von))

    schluss = ('\n<section class="schluss"><div class="wrap eng">\n  <div class="kick">Nächster Schritt</div>'
               '\n  <h2>Du suchst etwas <i>Bestimmtes?</i></h2>'
               '\n  <p>Schreib mir, was du suchst: Ort, Budget, mieten oder kaufen. Ich stelle den Kontakt her.</p>'
               '\n  <div class="knoepfe">\n    <a class="btn" href="/immobilien">Immobilien anfragen</a>'
               '\n    <a class="btn hell" href="/rechnung">Die echte Monatsrechnung</a>'
               '\n    <a class="btn hell" href="/auswandern-thailand.html">Auswandern nach Thailand, der Überblick</a>'
               '\n  </div>\n</div></section>\n')

    inhalt = kurz + tabelle + orte + kaufen
    t = seite('wohnen-thailand.html',
              'Wohnung in Thailand mieten: %d Wohnungen mit echter Miete' % len(zeilen),
              'Wohnung in Thailand mieten oder kaufen: %d Wohnungen und Häuser in Bangkok, Pattaya, Hua Hin '
              'und Si Racha, mit Miete und Größe vom Drehtag. Ab %d € im Monat.' % (len(zeilen), tief[0]),
              'https://freiweitmitnihat.com/blog/images/si-racha-the-strand.jpg',
              'Wohnen in Thailand', 'Mieten und kaufen',
              'Wohnung in Thailand mieten, <i>mit echten Preisen.</i>',
              'Zu jeder Wohnung auf dieser Seite gibt es ein Video vom Kanal. Hier stehen alle an einem Ort, '
              'mit Miete und Größe, dazu die Häuser, die zum Verkauf standen.',
              inhalt, schluss)
    return t, fehlt


def rente(alle):
    r = [a for a in alle if 'rente' in a['themen']]
    dazu_dateien = ['bangkok-matz-interview-2.html', 'lebenshaltungskosten-thailand.html',
                    'thailand-visumfrei-30-tage-dtv-2026.html', 'thailand-e-visum.html',
                    'deutschland-verlassen-thailand-auswandern.html', '7-fehler-auswandern.html']
    nach_datei = {a['datei']: a for a in alle}
    dazu = [nach_datei[d] for d in dazu_dateien if d in nach_datei]

    karten = ''.join(
        '\n    <a href="%s"><span><b>%s</b><br>%s</span><em>Interview</em></a>'
        % (a['url'], e(a['titel']), e(a['beschreibung'])) for a in r)
    inhalt = ('\n<section><div class="wrap eng">\n  <div class="kick-d">Die Gespräche</div>'
              '\n  <h2>Rentner in Thailand, mit Namen und Zahlen</h2>'
              '\n  <p>Jedes Gespräch gibt es als Video und als Artikel mit den wichtigsten Zahlen.</p>'
              '\n  <div class="mehr rente">%s\n  </div>\n</div></section>\n' % karten
              + '\n<section style="background:var(--paper-2)"><div class="wrap eng">\n  <div class="kick-d">Was dazugehört</div>'
              '\n  <h2>Krankenversicherung, Kosten, Visum</h2>\n  <div class="mehr">%s\n  </div>\n</div></section>\n'
              % links(dazu, lambda a: 'Interview' if 'interview' in a['themen'] else 'Artikel'))
    schluss = ('\n<section class="schluss"><div class="wrap eng">\n  <div class="kick">Nächster Schritt</div>'
               '\n  <h2>Rechne es einmal <i>ehrlich durch.</i></h2>'
               '\n  <p>In der Monatsrechnung stehen alle Posten, auch die, die man gern vergisst. Kostenlos.</p>'
               '\n  <div class="knoepfe">\n    <a class="btn" href="/rechnung">Die echte Monatsrechnung holen</a>'
               '\n    <a class="btn hell" href="/beratung">Beratungsgespräch, 60 Minuten</a>'
               '\n    <a class="btn hell" href="/interview">Du bist selbst Rentner im Ausland? Erzähl es</a>'
               '\n  </div>\n</div></section>\n')
    stil_extra = '<style data-quelle="themenseiten-rente">.mehr.rente span b{font-weight:600}.mehr.rente span{line-height:1.5}</style>\n'
    t = seite('rente-thailand.html',
              'Rente in Thailand: Erfahrungen aus %d Interviews' % len(r),
              'Rente in Thailand aus erster Hand: Menschen zwischen 58 und über 80 erzählen im Interview, '
              'was Miete, Krankenversicherung und Alltag kosten und was sie stört.',
              'https://freiweitmitnihat.com/blog/images/koh-samui-rentner-florenz-kittel-interview.jpg',
              'Rente in Thailand', 'Erfahrungen',
              'Rente in Thailand, <i>erzählt von denen, die es leben.</i>',
              'Auf dem Kanal sitze ich Menschen gegenüber, die ihre Rente in Thailand verbringen, und frage nach Zahlen: '
              'Miete, Krankenversicherung, was im Monat übrig bleibt. Hier stehen alle diese Gespräche.',
              inhalt, schluss)
    return t.replace('</head>', stil_extra + '</head>', 1)


def main():
    alle = themen.artikel()
    t, fehlt = wohnen(alle)
    (BASIS / 'wohnen-thailand.html').write_text(t, encoding='utf-8')
    (BASIS / 'rente-thailand.html').write_text(rente(alle), encoding='utf-8')
    print('Themenseiten geschrieben: wohnen-thailand.html, rente-thailand.html')
    for d in fehlt:
        print('  Wohnartikel ohne Eintrag in PREISE: %s' % d)


if __name__ == '__main__':
    main()
