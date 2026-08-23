#!/usr/bin/env python3
# ============================================================
# STRUKTURDATEN (JSON-LD) fuer freiweitmitnihat.com
# ------------------------------------------------------------
# Schreibt in jede Seite einen JSON-LD-Block, damit Google
# versteht, was die Seite ist und wer sie geschrieben hat.
#
#   Startseite      : WebSite + Person (Nihat) + Organization
#   Blogartikel     : Article + BreadcrumbList (+ VideoObject, wenn ein
#                     YouTube-Video eingebunden ist)
#   uebrige Seiten  : WebPage + BreadcrumbList
#
# VideoObject ist der Hebel, damit die Videos selbst in der Google-Suche
# und in der Google-Videosuche auftauchen. Upload-Datum und Laufzeit sind
# Pflichtangaben und stehen echt in tools/videodaten.json. Diese Datei neu
# holen mit:  python3 tools/seo-strukturdaten.py --videos-aktualisieren
#
# Laeuft beliebig oft: ein vorhandener Block wird ersetzt,
# nie doppelt angelegt. Nach jedem neuen Blogartikel ausfuehren:
#   python3 tools/seo-strukturdaten.py
# ============================================================
import re, pathlib, json, html, subprocess, datetime, sys, time, urllib.request

ROOT   = 'https://freiweitmitnihat.com/'
MARKER = 'data-quelle="seo-strukturdaten"'
BASIS  = pathlib.Path(__file__).resolve().parent.parent

PERSON = {
    "@type": "Person",
    "@id": ROOT + "#nihat",
    "name": "Nihat Bucakli",
    "url": ROOT,
    "jobTitle": "Journalist und Videoproduzent",
    "description": "Seit 2018 unterwegs, 70 Laender. Berichtet ueber das Leben im Ausland mit echten Zahlen.",
    "sameAs": [
        "https://www.youtube.com/@FreiweitmitNihat",
        "https://www.instagram.com/nihatbucakli/",
        "https://www.instagram.com/freiweit.mit.nihat/"
    ]
}

VERLAG = {
    "@type": "Organization",
    "@id": ROOT + "#organisation",
    "name": "Freiweit mit Nihat",
    "url": ROOT,
    "logo": {"@type": "ImageObject", "url": ROOT + "favicon-512.png"},
    "founder": {"@id": ROOT + "#nihat"},
    "sameAs": PERSON["sameAs"]
}


VIDEODATEN = pathlib.Path(__file__).resolve().parent / 'videodaten.json'
BROWSER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
           'Accept-Language': 'de-DE,de;q=0.9'}


def video_id(t):
    """Holt die YouTube-ID aus der Videokarte eines Artikels."""
    m = re.search(r'class="vid-karte"\s+href="https://youtu\.be/([\w-]+)"', t)
    if m:
        return m.group(1)
    m = re.search(r'youtu\.be/([\w-]+)|youtube\.com/(?:watch\?v=|embed/)([\w-]+)', t)
    if m:
        return m.group(1) or m.group(2)
    return None


def videos_laden():
    if VIDEODATEN.exists():
        return json.loads(VIDEODATEN.read_text(encoding='utf-8'))
    return {}


def videos_aktualisieren():
    """Holt Upload-Datum, Laufzeit und Titel frisch von YouTube."""
    daten = videos_laden()
    ids = set()
    for f in sorted((BASIS / 'blog').glob('*.html')):
        vid = video_id(f.read_text(encoding='utf-8'))
        if vid:
            ids.add(vid)
    neu = 0
    for vid in sorted(ids):
        try:
            h = urllib.request.urlopen(
                urllib.request.Request('https://www.youtube.com/watch?v=' + vid,
                                       headers=BROWSER), timeout=30).read().decode('utf-8', 'ignore')
            up = re.search(r'"uploadDate":"([^"]+)"', h)
            ln = re.search(r'"lengthSeconds":"(\d+)"', h)
            ti = re.search(r'<meta name="title" content="([^"]*)"', h)
            if up:
                daten[vid] = {'uploadDate': up.group(1),
                              'seconds': int(ln.group(1)) if ln else None,
                              'title': html.unescape(ti.group(1)) if ti else None}
                neu += 1
                print('  %s  %s' % (vid, up.group(1)[:10]))
        except Exception as e:
            print('  FEHLER bei %s: %s' % (vid, e))
        time.sleep(0.7)
    VIDEODATEN.write_text(json.dumps(daten, ensure_ascii=False, indent=1, sort_keys=True), encoding='utf-8')
    print('videodaten.json: %d Videos aktualisiert' % neu)


def laufzeit(sek):
    """825 -> PT13M45S, wie Schema.org es verlangt."""
    if not sek:
        return None
    return 'PT%dM%dS' % (sek // 60, sek % 60)


def videoblock(t, url, besch, videos):
    vid = video_id(t)
    if not vid or vid not in videos:
        return None
    v = videos[vid]
    block = {
        "@type": "VideoObject",
        "@id": url + "#video",
        "name": v.get('title') or seitentitel(t),
        "description": besch,
        "thumbnailUrl": "https://i.ytimg.com/vi/%s/maxresdefault.jpg" % vid,
        "uploadDate": v['uploadDate'],
        "contentUrl": "https://www.youtube.com/watch?v=" + vid,
        "embedUrl": "https://www.youtube.com/embed/" + vid,
        "inLanguage": "de-DE",
        "publisher": {"@id": ROOT + "#organisation"},
        "creator": {"@id": ROOT + "#nihat"},
        "mainEntityOfPage": {"@id": url}
    }
    d = laufzeit(v.get('seconds'))
    if d:
        block["duration"] = d
    return block


def entziffere(t, key, attr='name'):
    m = re.search(r'<meta\s+%s=["\']%s["\']\s+content=["\'](.*?)["\']' % (attr, key), t, re.S)
    if not m:
        m = re.search(r'<meta\s+content=["\'](.*?)["\']\s+%s=["\']%s["\']' % (attr, key), t, re.S)
    return html.unescape(m.group(1)).strip() if m else ''


def seitentitel(t):
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    if not m:
        return ''
    s = html.unescape(m.group(1)).strip()
    for suf in (' · Freiweit mit Nihat', ' | Freiweit mit Nihat', ' – Freiweit mit Nihat', ' - Freiweit mit Nihat'):
        if s.endswith(suf):
            s = s[:-len(suf)].strip()
    return s


def datum_der_datei(pfad, lastmod):
    if str(pfad) in lastmod:
        return lastmod[str(pfad)]
    try:
        aus = subprocess.run(['git', 'log', '-1', '--format=%as', '--', str(pfad)],
                             cwd=BASIS, capture_output=True, text=True, timeout=10)
        if aus.stdout.strip():
            return aus.stdout.strip()
    except Exception:
        pass
    return datetime.date.fromtimestamp(pfad.stat().st_mtime).isoformat()


def lastmod_aus_sitemap():
    p = BASIS / 'sitemap.xml'
    if not p.exists():
        return {}
    sm = p.read_text(encoding='utf-8')
    d = {}
    for m in re.finditer(r'<loc>https://freiweitmitnihat\.com/([^<]*)</loc><lastmod>([^<]+)</lastmod>', sm):
        d[m.group(1) or 'index.html'] = m.group(2)
    return d


def krumen(pfad, name):
    stufen = [{"@type": "ListItem", "position": 1, "name": "Startseite", "item": ROOT}]
    if str(pfad).startswith('blog/'):
        stufen.append({"@type": "ListItem", "position": 2, "name": "Blog", "item": ROOT + "blog/"})
        stufen.append({"@type": "ListItem", "position": 3, "name": name})
    else:
        stufen.append({"@type": "ListItem", "position": 2, "name": name})
    return {"@type": "BreadcrumbList", "itemListElement": stufen}


def bloecke_fuer(pfad, t, lastmod, videos):
    name  = seitentitel(t)
    besch = entziffere(t, 'description') or entziffere(t, 'og:description', 'property')
    bild  = entziffere(t, 'og:image', 'property') or ROOT + 'og-image.jpg'
    url   = ROOT if str(pfad) == 'index.html' else ROOT + str(pfad)
    tag   = datum_der_datei(pfad, lastmod)

    if str(pfad) == 'index.html':
        return [
            PERSON,
            VERLAG,
            {"@type": "WebSite", "@id": ROOT + "#website", "url": ROOT,
             "name": "Freiweit mit Nihat", "inLanguage": "de-DE",
             "description": besch, "publisher": {"@id": ROOT + "#organisation"}}
        ]

    if str(pfad).startswith('blog/') and pfad.name not in ('index.html', 'blog-template.html'):
        bloecke = [
            {"@type": "Article", "headline": name[:110], "description": besch,
             "image": bild, "datePublished": tag, "dateModified": tag,
             "inLanguage": "de-DE",
             "author": {"@id": ROOT + "#nihat"},
             "publisher": {"@id": ROOT + "#organisation"},
             "mainEntityOfPage": {"@type": "WebPage", "@id": url}},
            krumen(pfad, name)
        ]
        vb = videoblock(t, url, besch, videos)
        if vb:
            bloecke.append(vb)
        return bloecke

    return [
        {"@type": "WebPage", "@id": url, "url": url, "name": name,
         "description": besch, "inLanguage": "de-DE",
         "isPartOf": {"@id": ROOT + "#website"},
         "publisher": {"@id": ROOT + "#organisation"}},
        krumen(pfad, name)
    ]


def main():
    if '--videos-aktualisieren' in sys.argv:
        videos_aktualisieren()
    videos = videos_laden()
    lastmod = lastmod_aus_sitemap()
    seiten = sorted(list(BASIS.glob('*.html')) + list((BASIS / 'blog').glob('*.html')))
    ohne = {'404.html', 'index-alt.html', 'index-vorher-b.html', 'blog-template.html'}
    n = 0
    mit_video = 0
    for f in seiten:
        rel = f.relative_to(BASIS)
        t = f.read_text(encoding='utf-8')
        if f.name in ohne or 'noindex' in t or '</head>' not in t:
            continue
        graph = bloecke_fuer(rel, t, lastmod, videos)
        # Person und Organisation muessen auf JEDER Seite vollstaendig stehen,
        # sonst kann Google die @id-Verweise nicht aufloesen.
        if str(rel) != 'index.html':
            graph = graph + [PERSON, VERLAG]
        daten = {"@context": "https://schema.org", "@graph": graph}
        block = ('  <script type="application/ld+json" %s>\n%s\n  </script>\n'
                 % (MARKER, json.dumps(daten, ensure_ascii=False, indent=2)))
        t = re.sub(r'[ \t]*<script type="application/ld\+json" %s>.*?</script>\s*\n?'
                   % re.escape(MARKER), '', t, flags=re.S)
        t = t.replace('</head>', block + '</head>', 1)
        f.write_text(t, encoding='utf-8')
        n += 1
        if any(b.get('@type') == 'VideoObject' for b in graph):
            mit_video += 1
    print('Strukturdaten geschrieben in %d Seiten, davon %d mit VideoObject' % (n, mit_video))


if __name__ == '__main__':
    main()
