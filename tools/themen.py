#!/usr/bin/env python3
# ============================================================
# THEMEN der Blogartikel, gemeinsame Grundlage fuer
#   tools/weiterlesen.py     (verwandte Artikel unter jedem Text)
#   tools/themenseiten.py    (Sammelseiten Wohnen, Rente)
#
# Warum (05.11.2026): Die Artikel verwiesen fast nur auf Angebote,
# kaum aufeinander. Google erkennt Themen ueber Verweise. Ohne
# Cluster steht jeder Artikel allein, und Begriffe wie "Wohnung
# mieten Thailand" hat keine Seite, die sie buendelt.
#
# Die Zuordnung laeuft ueber Dateiname und Titel. Neue Artikel
# fallen automatisch hinein. Passt etwas nicht, in KORREKTUR
# eintragen statt die Regeln zu verbiegen.
# ============================================================
import re, html, pathlib

BASIS = pathlib.Path(__file__).resolve().parent.parent
BLOG = BASIS / 'blog'
NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)

ORTE = {
    'bangkok':   ['bangkok', 'sukhumvit', 'siam', 'lumphini', 'krachao', 'rama-9', 'phayathai',
                  'huai-khwang', 'wattana', 'samusorn', 'pier-21', 'noble-be33', 'mats-tunnel', 'matz'],
    'pattaya':   ['pattaya', 'jomtien', 'naklua', 'riviera', 'casey', 'oliver-lalana'],
    'hua-hin':   ['hua-hin', 'huahin', 'cha-am', 'khao-takiab', 'hua hin'],
    'si-racha':  ['si-racha', 'sriracha', 'sri-racha', 'koh-loi', 'bonus-suki', 'sharmonyx',
                  'trio-town', 'the-complete', 'ladda'],
    'bang-saray': ['bang-saray'],
    'bang-saen': ['bang-saen'],
    'koh-samui': ['koh-samui', 'samui'],
    'phuket':    ['phuket'],
    'vietnam':   ['vietnam', 'da-nang', 'danang', 'hanoi'],
}

THEMEN = {
    'wohnen':    ['miete', 'mieten', 'condo', 'wohnung', 'wohnungen', 'wohnen', 'ihouse', 'hideaway',
                  'the-strand', 'near-residence', 'riviera', 'oliver-lalana', 'skyrise', 'ideo',
                  'noble-be33', 'la-habana', 'dusit-d2', 'trio-town', 'sharmonyx', 'ladda', 'loft'],
    'kaufen':    ['kaufen', 'resort', 'immobilie', 'sri-racha-the-complete', 'loft', 'makler', 'pacht'],
    'interview': ['interview', 'matz', 'dietrich', 'florenz', 'marc', 'ralph', 'nico', 'thomas',
                  'stefan', 'casey', 'khwan', 'guido', 'elli', 'oliver', 'chris'],
    'rente':     ['rente', 'rentner', 'mit-72', 'dietrich', 'florenz', 'matz-interview-3',
                  'thomas-eltern', 'mit 58', 'mit 75', '(72)', '(75)'],
    'kosten':    ['kosten', 'lebenshaltung', 'preise', '€ im monat', 'finanzielle', 'krankenversicherung'],
    'einreise':  ['visum', 'visa', 'tdac', 'dtv', 'e-visum', 'visumfrei', 'behoerden'],
    'praktisch': ['sim-karte', 'grab', 'behoerden'],
    'essen':     ['suki', 'cafe', 'streetfood', 'pier-21', 'wattana', 'samusorn', 'german-corner',
                  'night-market', 'bluport', 'suessigkeiten'],
    'entdecken': ['strand', 'beach', 'tunnel', 'krachao', 'lumphini', 'koh-loi', 'khao-takiab',
                  'bahnhof', 'j-park', 'pet-expo', 'entdeckt', 'barber'],
    'grundlagen': ['fehler', 'deutschland-verlassen', 'finanzielle-freiheit', 'auswandern'],
}

# Handkorrekturen: Dateiname -> Themen, die ergaenzt (+) oder entfernt (-) werden.
KORREKTUR = {
    'bangkok-matz-interview-2.html': {'+': ['kosten']},
    'huahin-german-corner-khwan.html': {'-': ['essen']},
    'casey-papagei-maklerin.html': {'+': ['kaufen']},
    'bangkok-s-box-sukhumvit-hotel.html': {'-': ['wohnen']},
    'huahin-th-beach-hotel.html': {'-': ['wohnen', 'entdecken']},
    'sim-karte-vietnam.html': {'-': ['kaufen']},
    'si-racha-the-strand.html': {'-': ['entdecken']},
    '2026-06-16-thomas-loft-pattaya.html': {'-': ['interview']},
    'grab-app-einrichten.html': {'+': ['praktisch']},
}

# Gewicht beim Suchen verwandter Artikel
GEWICHT = {'wohnen': 3, 'kaufen': 3, 'rente': 4, 'interview': 2, 'kosten': 2, 'einreise': 4,
           'praktisch': 3, 'essen': 1, 'entdecken': 1, 'grundlagen': 2}


def titel(t):
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    s = html.unescape(m.group(1)).strip() if m else ''
    for suf in (' · Freiweit mit Nihat', ' | Freiweit mit Nihat', ' – Freiweit mit Nihat'):
        if s.endswith(suf):
            s = s[:-len(suf)].strip()
    return s


def beschreibung(t):
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', t, re.S)
    return html.unescape(m.group(1)).strip() if m else ''


def treffer(woerter, text):
    return any(w in text for w in woerter)


def artikel():
    """Alle veroeffentlichten Artikel mit Ort und Themen."""
    liste = []
    for f in sorted(BLOG.glob('*.html')):
        if f.name in ('index.html', 'blog-template.html'):
            continue
        t = f.read_text(encoding='utf-8')
        if NOINDEX.search(t):
            continue
        ti = titel(t)
        such = (f.name + ' ' + ti).lower()
        orte = {o for o, w in ORTE.items() if treffer(w, such)}
        themen = {th for th, w in THEMEN.items() if treffer(w, such)}
        k = KORREKTUR.get(f.name, {})
        themen |= set(k.get('+', []))
        themen -= set(k.get('-', []))
        # Land fuer die Auswahl verwandter Artikel. "beide" passt zu allem.
        if 'thailand' in such and 'vietnam' in such:
            land = 'beide'
        elif 'vietnam' in orte:
            land = 'vietnam'
        elif orte or 'thailand' in such:
            land = 'thailand'
        else:
            land = 'beide'
        liste.append({
            'datei': f.name, 'url': '/blog/' + f.name, 'titel': ti,
            'beschreibung': beschreibung(t), 'orte': orte, 'themen': themen,
            'land': land,
        })
    return liste


if __name__ == '__main__':
    for a in artikel():
        print('%-48s %-22s %s' % (a['datei'][:48], ','.join(sorted(a['orte'])) or '-',
                                   ','.join(sorted(a['themen'])) or '-'))
