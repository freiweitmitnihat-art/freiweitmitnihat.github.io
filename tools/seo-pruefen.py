#!/usr/bin/env python3
# ============================================================
# SEO-PRUEFUNG fuer freiweitmitnihat.com
# ------------------------------------------------------------
# Reiner Bericht. Diese Datei aendert nie etwas.
# Sie sucht die Fehler, die man auf einer Seite nicht sieht,
# die aber Google und die sozialen Netze stoeren.
#
# Geprueft wird:
#   1. tote interne Links und fehlende Bilddateien
#   2. Seiten, die von nirgendwo verlinkt sind
#   3. fehlende Pflicht-Angaben (title, description, canonical,
#      og:image, h1)
#   4. Platzhalter, die im Text stehen geblieben sind
#   5. og:image: Datei vorhanden, Masse stimmen
#   6. doppelte Titel und Beschreibungen
#   7. zu lange Titel. Gemessen wird nur der Inhalt vor dem
#      Marken-Zusatz, denn dass » · Freiweit mit Nihat« hinten
#      abgeschnitten wird, ist normal und stoert nicht
#   8. Sitemap gegen den Dateibestand
#   8b. Impressum und Datenschutz von jeder Seite erreichbar
#   9. Bilder: welche sind zu gross, welche liegen ungenutzt
#      herum. Ungenutzt heisst: keine oeffentliche Seite bindet
#      sie ein. Das ist kein Fehler, aber es sammelt sich an.
#
# Seiten mit noindex und 404.html bleiben aussen vor, die
# sollen nicht in die Suche.
#
#   python3 tools/seo-pruefen.py
# ============================================================
import pathlib, re, struct, urllib.parse, collections

BASIS = pathlib.Path(__file__).resolve().parent.parent
ROOT = 'https://freiweitmitnihat.com/'
BILD_GRENZE = 250 * 1024
TITEL_GRENZE = 65   # gilt fuer den Inhalt ohne Marken-Zusatz
MARKE = re.compile(r'\s*[·|:]\s*Freiweit mit Nihat\s*$')

NOINDEX = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)
PLATZHALTER = ('[VIDEO-ID]', 'DIGISTORE-ID-', 'LOREM IPSUM', 'TODO:')

befunde = []


def melde(bereich, zeilen):
    befunde.append((bereich, zeilen))


def alle_seiten():
    return sorted(list(BASIS.glob('*.html')) + list((BASIS / 'blog').glob('*.html')))


def oeffentlich(f, t):
    return not NOINDEX.search(t) and f.name != '404.html'


def jpg_masse(pfad):
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


def ziel(f, u):
    """Verweis in einen Dateipfad uebersetzen."""
    p = (BASIS / u.lstrip('/')) if u.startswith('/') else (f.parent / u)
    return pathlib.Path(urllib.parse.unquote(str(p)))


def main():
    seiten = alle_seiten()
    texte = {f: f.read_text(encoding='utf-8') for f in seiten}

    # 1. tote Verweise
    tot = []
    for f, t in texte.items():
        for m in re.finditer(r'(?:href|src)=["\']([^"\'#?]+)["\']', t):
            u = m.group(1).strip()
            if not u or u.startswith(('http', '//', 'mailto:', 'tel:',
                                      'data:', 'javascript:')):
                continue
            p = ziel(f, u)
            if p.exists() or p.with_suffix('.html').exists() or (p / 'index.html').exists():
                continue
            tot.append('%s  ->  %s' % (f.relative_to(BASIS), u))
    melde('Tote interne Verweise', tot)

    # 2. verwaiste Seiten
    verlinkt = set()
    for f, t in texte.items():
        for m in re.finditer(r'href=["\']([^"\'#?]+)["\']', t):
            u = m.group(1).strip()
            if not u or u.startswith(('http', '//', 'mailto:', 'tel:',
                                      'data:', 'javascript:')):
                continue
            p = ziel(f, u)
            for kand in (p, p.with_suffix('.html'), p / 'index.html'):
                if kand.suffix == '.html' and kand.exists():
                    verlinkt.add(str(kand.resolve()))
    waisen = [str(f.relative_to(BASIS)) for f, t in texte.items()
              if oeffentlich(f, t) and f.name != 'index.html'
              and str(f.resolve()) not in verlinkt]
    melde('Seiten, die von nirgendwo verlinkt sind', waisen)

    # 3. + 4. Pflicht-Angaben und Platzhalter
    fehlt, reste = [], []
    for f, t in texte.items():
        if not oeffentlich(f, t):
            continue
        rel = str(f.relative_to(BASIS))
        for name, muster in (
                ('title', r'<title>'),
                ('description', r'<meta[^>]+name=["\']description'),
                ('canonical', r'<link[^>]+rel=["\']canonical'),
                ('og:image', r'<meta[^>]+property=["\']og:image["\']'),
                ('h1', r'<h1')):
            if not re.search(muster, t, re.I):
                fehlt.append('%s: kein %s' % (rel, name))
        for ph in PLATZHALTER:
            if ph in t:
                reste.append('%s: %s' % (rel, ph))
    melde('Fehlende Pflicht-Angaben', fehlt)
    melde('Platzhalter im Text', reste)

    # 5. og:image gegenpruefen
    ogfehler = []
    for f, t in texte.items():
        if not oeffentlich(f, t):
            continue
        mi = re.search(r'og:image["\'][^>]*content=["\']([^"\']+)', t, re.I)
        if not mi:
            continue
        pfad = BASIS / mi.group(1).replace(ROOT, '')
        rel = str(f.relative_to(BASIS))
        if not pfad.exists():
            ogfehler.append('%s: Bilddatei fehlt (%s)' % (rel, mi.group(1)))
            continue
        mw = re.search(r'og:image:width["\'][^>]*content=["\'](\d+)', t, re.I)
        mh = re.search(r'og:image:height["\'][^>]*content=["\'](\d+)', t, re.I)
        masse = jpg_masse(pfad) if pfad.suffix.lower() in ('.jpg', '.jpeg') else None
        if masse and mw and mh and (str(masse[0]) != mw.group(1)
                                    or str(masse[1]) != mh.group(1)):
            ogfehler.append('%s: Masse stimmen nicht, angegeben %sx%s, echt %dx%d'
                            % (rel, mw.group(1), mh.group(1), masse[0], masse[1]))
    melde('og:image', ogfehler)

    # 6. + 7. Titel und Beschreibungen
    titel = collections.defaultdict(list)
    besch = collections.defaultdict(list)
    for f, t in texte.items():
        if not oeffentlich(f, t):
            continue
        rel = str(f.relative_to(BASIS))
        mt = re.search(r'<title>(.*?)</title>', t, re.S)
        md = re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"\']*)',
                       t, re.I)
        if mt:
            titel[mt.group(1).strip()].append(rel)
        if md:
            besch[md.group(1).strip()].append(rel)
    melde('Doppelte Titel',
          ['»%s«: %s' % (k[:55], ', '.join(v)) for k, v in titel.items() if len(v) > 1])
    melde('Doppelte Beschreibungen',
          ['»%s…«: %s' % (k[:55], ', '.join(v)) for k, v in besch.items() if len(v) > 1])
    lang = []
    for k, v in titel.items():
        kern = MARKE.sub('', k)
        if len(kern) > TITEL_GRENZE:
            lang.append('%3d  %s  (%s)' % (len(kern), kern[:70], v[0]))
    melde('Titel-Kern ueber %d Zeichen, wird mitten im Satz abgeschnitten'
          % TITEL_GRENZE, sorted(lang, reverse=True))

    # Seit 23.08.2026: Blogartikel ohne Marken-Zusatz, Funktionsseiten mit.
    marke = []
    for f, t in texte.items():
        if not oeffentlich(f, t):
            continue
        rel = str(f.relative_to(BASIS))
        mt = re.search(r'<title>(.*?)</title>', t, re.S)
        if not mt:
            continue
        ti = mt.group(1).strip()
        artikel = f.parent.name == 'blog' and f.name != 'index.html'
        if artikel and MARKE.search(ti):
            marke.append('%s: Artikel traegt den Marken-Zusatz noch' % rel)
        if not artikel and 'Freiweit mit Nihat' not in ti:
            marke.append('%s: Funktionsseite ohne Marke im Titel' % rel)
    melde('Marken-Zusatz im Titel falsch gesetzt', marke)

    # title und og:title duerfen verschieden formuliert sein, das ist eine
    # Entscheidung. Sie sollten es aber absichtlich sein und nicht, weil bei
    # einer Umbenennung nur eins von beiden angefasst wurde.
    drift = []
    for f, t in texte.items():
        if not oeffentlich(f, t):
            continue
        mt = re.search(r'<title>(.*?)</title>', t, re.S)
        mo = re.search(r'og:title["\'][^>]*content=["\']([^"\']*)', t, re.I)
        if mt and mo and mt.group(1).strip() != mo.group(1).strip():
            drift.append('%s\n        title: %s\n        og   : %s'
                         % (str(f.relative_to(BASIS)), mt.group(1).strip()[:60],
                            mo.group(1).strip()[:60]))
    melde('title und og:title verschieden formuliert (pruefen, ob gewollt)', drift)

    # 8. Sitemap
    sm = BASIS / 'sitemap.xml'
    smfehler = []
    if sm.exists():
        drin = set(re.findall(r'<loc>([^<]+)</loc>', sm.read_text(encoding='utf-8')))
        for f, t in texte.items():
            if not oeffentlich(f, t) or f.name == 'blog-template.html':
                continue
            rel = str(f.relative_to(BASIS))
            url = ROOT if rel == 'index.html' else ROOT + rel
            if url not in drin:
                smfehler.append('fehlt in der Sitemap: ' + rel)
        for url in drin:
            p = BASIS / url.replace(ROOT, '')
            if url != ROOT and not p.exists():
                smfehler.append('steht in der Sitemap, Datei fehlt: ' + url)
    else:
        smfehler.append('sitemap.xml fehlt ganz')
    melde('Sitemap', smfehler)

    # 8b. Rechtslinks
    def rechtslink(text, wort):
        for treffer in re.findall(r'href=["\']([^"\']*%s[^"\']*)["\']' % wort,
                                  text, re.I):
            if 'vgwort' in treffer or '#' in treffer:
                continue
            return True
        return False

    recht = []
    for f, t in texte.items():
        if not oeffentlich(f, t):
            continue
        rel = str(f.relative_to(BASIS))
        for wort, name in (('impressum', 'Impressum'),
                           ('datenschutz', 'Datenschutz')):
            if not rechtslink(t, wort):
                recht.append('%s: kein Link auf %s' % (rel, name))
    melde('Pflichtangaben nicht von jeder Seite erreichbar', recht)

    # 9. Bilder
    bildverweis = re.compile(
        r'(?:src|href|content)\s*=\s*["\']([^"\']+\.(?:jpg|jpeg|png|webp|gif|ico|svg))["\']'
        r'|url\(\s*["\']?([^"\')]+\.(?:jpg|jpeg|png|webp|gif|svg))', re.I)
    benutzt = set()
    for f, t in texte.items():
        if NOINDEX.search(t):
            continue
        for m in bildverweis.finditer(t):
            u = urllib.parse.unquote(m.group(1) or m.group(2))
            if u.startswith(ROOT):
                p = BASIS / u[len(ROOT):]
            elif u.startswith(('http', '//', 'data:')):
                continue
            elif u.startswith('/'):
                p = BASIS / u.lstrip('/')
            else:
                p = f.parent / u
            try:
                benutzt.add(str(p.resolve()))
            except OSError:
                pass

    bilder = [p for p in BASIS.rglob('*')
              if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.gif')]
    gross, ungenutzt = [], []
    for p in sorted(bilder, key=lambda x: -x.stat().st_size):
        kb = p.stat().st_size // 1024
        drin = str(p.resolve()) in benutzt
        if p.stat().st_size > BILD_GRENZE and drin:
            gross.append('%4d KB  %s' % (kb, p.relative_to(BASIS)))
        if not drin:
            ungenutzt.append('%4d KB  %s' % (kb, p.relative_to(BASIS)))
    melde('Eingebundene Bilder ueber %d KB' % (BILD_GRENZE // 1024), gross)
    melde('Bilddateien, die keine oeffentliche Seite einbindet', ungenutzt)

    # Ausgabe
    print('SEO-Pruefung fuer freiweitmitnihat.com')
    print('=' * 60)
    summe = 0
    for bereich, zeilen in befunde:
        summe += len(zeilen)
        print('\n%s: %d' % (bereich, len(zeilen)))
        for z in zeilen:
            print('   ', z)
        if not zeilen:
            print('    nichts zu beanstanden')
    print('\n' + '=' * 60)
    print('Meldungen gesamt: %d' % summe)


if __name__ == '__main__':
    main()
