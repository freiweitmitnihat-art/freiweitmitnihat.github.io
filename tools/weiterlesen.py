#!/usr/bin/env python3
# ============================================================
# WEITERLESEN: vier verwandte Artikel unter jedem Blogartikel
# ------------------------------------------------------------
# Setzt direkt ueber den Ressourcen-Block (fw-res) einen Block mit
# vier Artikeln aus demselben Thema oder Ort. Die Auswahl kommt aus
# tools/themen.py. Wer schon oft verlinkt ist, wird leicht nach
# hinten geschoben, damit auch stille Artikel Verweise bekommen.
#
# Jeder Lauf baut alle Bloecke neu, damit neue Artikel sofort
# auftauchen. Nach jedem neuen Artikel ausfuehren:
#   python3 tools/weiterlesen.py            # schreiben
#   python3 tools/weiterlesen.py --pruefen  # nur anzeigen
# ============================================================
import re, sys, html, collections
sys.path.insert(0, __import__('os').path.dirname(__file__))
import themen

ANZAHL = 4
MARKE = 'data-quelle="weiterlesen"'
# Frueher <nav>: die Artikelvorlage macht jedes nav zur festen Kopfleiste.
BLOCK = re.compile(r'\n?\s*<(nav|aside) class="fw-wl" %s.*?</\1>\n' % re.escape(MARKE), re.S)
STIL_MARKE = '<style data-quelle="weiterlesen">'
STIL = (STIL_MARKE +
        '\n.fw-wl{margin:40px 0;max-width:740px}'
        '\n.fw-wl .fw-wl-t{font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#A44A18;margin-bottom:14px}'
        '\n.fw-wl ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:12px}'
        '\n.fw-wl li{margin:0}'
        '\n.fw-wl a{display:block;height:100%;background:#fff;border:1px solid rgba(0,0,0,.09);border-radius:10px;padding:14px 16px;text-decoration:none;color:#1a1410;font-size:16px;font-weight:600;line-height:1.45;transition:border-color .2s,color .2s}'
        '\n.fw-wl a:hover,.fw-wl a:focus-visible{border-color:#A44A18;color:#A44A18}'
        '\n.fw-wl small{display:block;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#6b5e52;margin-bottom:4px}'
        '\n.fw-wl a.fw-wl-alle{display:inline-block;height:auto;background:none;border:0;padding:14px 0 0;color:#A44A18;font-size:16px}'
        '\n.fw-wl a.fw-wl-alle:hover{text-decoration:underline}'
        '\n@media(max-width:600px){.fw-wl ul{grid-template-columns:1fr}}'
        '\n</style>\n')

ORTNAME = {'bangkok': 'Bangkok', 'pattaya': 'Pattaya', 'hua-hin': 'Hua Hin', 'si-racha': 'Si Racha',
           'bang-saray': 'Bang Saray', 'bang-saen': 'Bang Saen', 'koh-samui': 'Koh Samui',
           'phuket': 'Phuket', 'vietnam': 'Vietnam'}
THEMANAME = {'wohnen': 'Wohnen', 'kaufen': 'Immobilien', 'interview': 'Interview', 'rente': 'Rente',
             'kosten': 'Kosten', 'einreise': 'Visum', 'praktisch': 'Praktisch', 'essen': 'Essen',
             'entdecken': 'Unterwegs', 'grundlagen': 'Auswandern'}
RANG = ['rente', 'einreise', 'kaufen', 'wohnen', 'interview', 'kosten', 'praktisch', 'grundlagen',
        'essen', 'entdecken']


def passt_land(a, b):
    return a['land'] == 'beide' or b['land'] == 'beide' or a['land'] == b['land']


def punkte(a, b):
    p = sum(themen.GEWICHT[t] for t in a['themen'] & b['themen'])
    p += 2 * len(a['orte'] & b['orte'])
    return p


def etikett(a, b):
    """Kleine Zeile ueber dem Titel: das gemeinsame Thema, sonst der Ort."""
    gemeinsam = [t for t in RANG if t in a['themen'] & b['themen']]
    if gemeinsam:
        return THEMANAME[gemeinsam[0]]
    for o in sorted(a['orte'] & b['orte']):
        return ORTNAME[o]
    eigen = [t for t in RANG if t in b['themen']]
    return THEMANAME[eigen[0]] if eigen else 'Artikel'


def auswahl(alle):
    eingehend = collections.Counter()
    ergebnis = {}
    for a in alle:
        kandidaten = []
        for b in alle:
            if b is a or not passt_land(a, b):
                continue
            kandidaten.append((punkte(a, b) - 0.4 * eingehend[b['datei']], b['datei'], b))
        kandidaten.sort(key=lambda k: (-k[0], k[1]))
        gewaehlt = [k[2] for k in kandidaten[:ANZAHL]]
        for b in gewaehlt:
            eingehend[b['datei']] += 1
        ergebnis[a['datei']] = gewaehlt
    return ergebnis, eingehend


# Sammelseiten aus tools/themenseiten.py. Jeder passende Artikel zeigt auf sie,
# damit Google sie als Mittelpunkt des Themas erkennt.
SAMMEL = [
    ('rente', '/rente-thailand.html', 'Alle Gespräche über Rente in Thailand'),
    ('wohnen', '/wohnen-thailand.html', 'Alle Wohnungen in Thailand mit Miete und Größe'),
    ('kaufen', '/wohnen-thailand.html', 'Alle Wohnungen und Häuser in Thailand mit Preisen'),
]


def sammel(a):
    if a['land'] == 'vietnam':
        return ''
    for thema, url, text in SAMMEL:
        if thema in a['themen']:
            return '\n      <a class="fw-wl-alle" href="%s">%s &rarr;</a>' % (url, text)
    return ''


def block(a, liste):
    zeilen = ''.join(
        '\n      <li><a href="%s"><small>%s</small>%s</a></li>'
        % (b['url'], etikett(a, b), html.escape(b['titel'])) for b in liste)
    return ('\n    <aside class="fw-wl" %s aria-label="Weiterlesen">'
            '\n      <div class="fw-wl-t">Weiterlesen</div>'
            '\n      <ul>%s\n      </ul>%s'
            '\n    </aside>\n' % (MARKE, zeilen, sammel(a)))


def main():
    pruefen = '--pruefen' in sys.argv
    alle = themen.artikel()
    ergebnis, eingehend = auswahl(alle)
    geschrieben = ohne_platz = 0
    for a in alle:
        pfad = themen.BLOG / a['datei']
        t = pfad.read_text(encoding='utf-8')
        neu = BLOCK.sub('\n', t)
        b = block(a, ergebnis[a['datei']])
        stelle = neu.find('<div class="fw-res"')
        if stelle < 0:
            stelle = neu.find('<div class="author-box"')
        if stelle < 0:
            print('  kein Platz gefunden: %s' % a['datei'])
            ohne_platz += 1
            continue
        zeilenanfang = neu.rfind('\n', 0, stelle)
        neu = neu[:zeilenanfang] + b.rstrip('\n') + neu[zeilenanfang:]
        # Stil bei jedem Lauf erneuern, damit Aenderungen hier ueberall ankommen.
        # An Ort und Stelle ersetzen, sonst wandert der Block bei jedem Lauf.
        alt = re.compile(re.escape(STIL_MARKE) + r'.*?</style>\n', re.S)
        if alt.search(neu):
            neu = alt.sub(lambda m: STIL, neu, count=1)
        else:
            neu = neu.replace('</head>', STIL + '</head>', 1)
        if pruefen:
            print('%s\n   %s' % (a['datei'], '\n   '.join(x['datei'] for x in ergebnis[a['datei']])))
        elif neu != t:
            pfad.write_text(neu, encoding='utf-8')
            geschrieben += 1
    nie = [a['datei'] for a in alle if eingehend[a['datei']] == 0]
    print('Weiterlesen: %d Artikel geschrieben, %d ohne Platz' % (geschrieben, ohne_platz))
    print('Artikel ohne eingehenden Verweis: %d %s' % (len(nie), ' '.join(nie)))


if __name__ == '__main__':
    main()
