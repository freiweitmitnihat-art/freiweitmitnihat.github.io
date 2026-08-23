# CLAUDE.md · Freiweit mit Nihat · Homepage
## Master-Instruction für alle Homepage-Arbeiten

Lies diese Datei vollständig bevor du irgendetwas änderst.
Zuerst die Root-CLAUDE.md, dann diese hier.

**Stand: 22.08.2026. Startseite neu gebaut (20.08.). Die alten Fassungen `index-alt.html`
und `index-vorher-b.html` wurden am 22.08.2026 geloescht. Sicherungen liegen unter
`/Volumes/Extreme Pro/Claude/homepage-backup-20260820-1754/` und als Einzelkopien in
`/Volumes/Extreme Pro/Claude/Video-Pakete-Archiv/`.**

---

## PROJEKT-ÜBERSICHT

**Website:** freiweitmitnihat.com, Homepage zum YouTube-Kanal @FreiweitmitNihat
**Zweck (in dieser Reihenfolge):** E-Mail-Adressen einsammeln, Ratgeber verkaufen,
Interview-Gäste gewinnen, Beratung und Immobilien vermitteln
**Zielgruppe:** DACH, Kern 55 bis 65+, 84 % männlich, 35 % sehen über den Fernseher
**Hosting:** GitHub Pages (`freiweitmitnihat-art/freiweitmitnihat.github.io`)
**Domain:** Cloudflare

---

## DIE WICHTIGSTE REGEL: DIE ZIELGRUPPE IST ÄLTER

Alles andere folgt daraus:

- **Fließtext 20 px**, niemals kleiner. Sekundärtext nie unter 16 px.
- **Kontrast mindestens 7:1** für Fließtext (WCAG AAA), nicht 4,5:1.
  `--sand` ist eine Linien- und Flächenfarbe und darf **nie** Text tragen.
- **Klickflächen mindestens 48 px hoch.**
- **Keine Bewegung ohne Grund.** Kein Scroll-Reveal, kein Parallax, keine Zähler,
  die hochlaufen. `prefers-reduced-motion` wird respektiert.
- **Kurze, tippbare URLs.** Auf YouTube-TV sind Links in Videobeschreibungen
  systemisch abgeschaltet, ein Drittel der Zuschauer kann nicht klicken.
  Deshalb `/r` und `/b` als Kurzweiterleitungen, deshalb die QR-Einblendungen.

---

## DESIGN-SYSTEM (Stand 20.08.2026)

### Farben
```css
--ink:    #1A1410   /* Fließtext, 17,2:1 auf Creme */
--ink-2:  #4A4238   /* Sekundärtext, 9,3:1 */
--terra:  #B4551F   /* Akzent, nur Buttons, Links, Zahlen. Dunkler als das alte C4622D */
--sand:   #C8A97E   /* NUR Linien und Flächen, nie Text auf Hell */
--paper:  #FAF8F5   /* Hintergrund */
--paper-2:#F1ECE4   /* Hintergrund getönt */
--line:   rgba(26,20,16,0.14)
```

### Typografie
- Überschriften: Playfair Display
- Fließtext und Bedienelemente: Inter, 20 px, Zeilenhöhe 1.7

### Warum es nicht nach KI aussehen darf
Creme plus Terrakotta plus Playfair ist genau das, was KI-Baukästen 2026 ausspucken.
Die Palette bleibt, aber sie darf nie allein tragen. Was den Unterschied macht:

- **Echte Fotos mit echter Bildunterschrift.** Jedes Bild sagt, wo es aufgenommen
  wurde und was darauf passiert. Keine Symbolbilder, keine Fotos ohne Text darunter.
- **Echte Zahlen statt Versprechen.** „1.254 € im Monat" statt „günstig leben".
- **Asymmetrische Raster** (7fr/5fr, 8fr/4fr), nie drei gleich große Kacheln nebeneinander.
- **Linien statt Karten.** Abschnitte werden mit `border-top` getrennt, nicht in
  Kästen mit Schlagschatten gelegt.
- **Keine Icon-Reihen**, keine Verlaufsflächen, keine Glasoptik.

### Harte Verbote
- **Keine Gedankenstriche.** Nirgends, in keiner Datei. Stattdessen Komma,
  Doppelpunkt oder Punkt. Am 20.08.2026 wurden 891 Stück projektweit entfernt.
- **Keine Emojis** in Website-Texten.
- Kein „Hey Leute", kein „Ihr". Du-Ansprache.
- Kein „Bullshit" oder Ähnliches.
- **Wohnort-Framing:** Nihat ist nicht ausgewandert. Nie „ich lebe in X".
  Immer „seit 2018 unterwegs, 70 Länder". Sein Aufenthaltsort wird nie Thema.

---

## SEITEN

| Datei | Zweck | Status |
|---|---|---|
| `index.html` | Startseite, 9 Abschnitte | neu, 20.08.2026 |
| `rechnung.html` | Landingpage Lead Magnet, ein Feld, ein Button | live |
| `r.html` / `b.html` | Kurzweiterleitungen für die QR-Codes | **Ziel nie ändern** |
| `ratgeber.html` | leitet auf `/rechnung` weiter | Weiterleitung |
| `bibliothek.html` | Ratgeber kaufen, 6 Hefte plus Paket | Digistore-IDs fehlen |
| `hilfe.html` | Kaufhilfe, „wo ist mein Download-Ordner" | 4 Screenshots fehlen |
| `freiweit-woche.html` | Programmwoche vor Ort | `noindex` bis Rechtsprüfung |
| `beratung.html` | 97 € Beratungsgespräch, Cal.eu | live |
| `immobilien.html` `interview.html` `kontakt.html` | | live |
| `reality-check.html` | Selbsttest, 10 Fragen | live |
| `city-guides.html` | Maps Guide Pattaya, 29 EUR, Kauf ueber Stripe | live seit 22.08.2026 |
| `pattaya-maps-zugang-57651b.html` | Zugangsseite nach der Zahlung, **nicht verlinken**, noindex | live |
| `agb.html` | AGB und Widerrufsbelehrung fuer die digitalen Produkte | live seit 22.08.2026 |
| `blog/` | 44 Artikel plus `blog/index.html` | live |
| `blog/blog-template.html` | Vorlage fuer `auto-blog.py`, **nicht loeschen, nicht verschieben** | noindex |
| `impressum.html` `datenschutz.html` | | live |

### Aufbau index.html
1 Hero (Foto plus drei Zahlen) · 2 Neu auf dem Kanal · 3 Drei Wege ·
4 Lead Magnet (dunkel) · 5 Ratgeber · 6 Immobilien · 7 Mit mir arbeiten ·
8 Deine Geschichte (dunkel) · 9 Wer ich bin · Footer

---

## FORMULARE UND NEWSLETTER

**`js/brevo.js` ist die einzige Stelle**, an der die Brevo-Adresse steht
(`BREVO_ENDPOINT`). Erkennt automatisch eine sibforms-URL oder einen eigenen
Cloudflare-Worker und fällt ohne Eintrag auf Web3Forms zurück.
Angebunden: `rechnung.html`, `reality-check.html`.
Felder an Brevo: EMAIL, VORNAME, QUELLE, MAGNET, OPT_IN.
Anleitung: `README-brevo.md`. Mailtexte: `outputs/_bausteine/brevo-mails.md`.

**`?via=` Konvention:** `qr` · `yt` · `pinned` · `web`. Wird als QUELLE
mitgeschickt, damit sichtbar wird, welcher Kanal Anmeldungen bringt.

**Erledigt am 20.08.2026:** Liste `Newsletter` (ID 3), Formular `Website Anmeldung`,
Double-Opt-in, Weiterleitung auf `/danke`. Live geprueft: EMAIL, VORNAME, QUELLE und
MAGNET werden angenommen, nur EMAIL ist Pflicht.

**Merker:** Brevo speichert den Design-Schritt eines Formulars erst, wenn man sich bis
**Fertig** durchklickt. Wer nach dem Ziehen die Seite verlaesst, verliert alles.

---

## BILDER

Liegen als Datei in `homepage/img/`, **nicht mehr base64 eingebettet**.
Neue Bilder: max. 1600 px Breite, JPEG 82 bis 88 %, immer `alt` und
immer eine `<figcaption>` mit Ort und Situation.

**Fotos immer als JPEG, nie als PNG.** Am 20.08.2026 wurden 22 Blog-PNGs (48 MB) in JPEG
umgerechnet (Qualitaet 70, max. 1400 px): jetzt 7 MB. PNG nur bei Transparenz oder harten
Kanten wie Logos.

Fehlende Beitragsbilder gibt es keine mehr. Drei Artikel bekamen am 20.08.2026 das
YouTube-Vorschaubild des zugehoerigen Videos plus einen Video-Kasten (`.vid-karte`),
der auf das konkrete Video zeigt statt nur auf den Kanal.

---

## VOR JEDEM ABSCHLUSS PRÜFEN

```bash
grep -c '—' *.html blog/*.html          # muss überall 0 sein
```
Dazu: alle internen Links auflösen, jedes `<img>` hat `alt`, jedes Foto hat
`<figcaption>`, Kontrast im Fließtext mindestens 7:1, Klickflächen mindestens 48 px.

---

## SICHERHEIT UND SAUBERKEIT (am 20.08.2026 geprueft)

Kein Schluessel im Code, kein XSS, keine unverschluesselten Links, alle `target="_blank"`
mit `rel="noopener"`. Vor jedem Abschluss zusaetzlich pruefen: keine sichtbaren Platzhalter
(`SCREENSHOT`, `TODO`, `Nach Upload`) ausserhalb von HTML-Kommentaren, und ob `og:image`
auf eine Datei zeigt, die es wirklich gibt.

Neue Entwurfsseiten: `404.html` (live), `danke.html` (live).
`kachelstart.html`, `hero-varianten.html`, `hero-b-plus.html` und `startseite-b.html`
sind nicht mehr vorhanden.

---

## RESSOURCEN-BLOCK IN DEN BLOG-ARTIKELN (seit 22.08.2026)

**Befund:** Von 46 Artikeln verlinkten 31 auf die Beratung, aber nur 2 auf die kostenlose
Monatsrechnung und kein einziger auf Bibliothek, City Guides, Freiweit-Woche,
Interview-Bewerbung oder Hotels. Die groesste Flaeche der Website leitete alles in das
teuerste Angebot mit der hoechsten Huerde.

**Loesung:** `tools/ressourcen-block.py` setzt ueber der Autorenbox (bzw. vor der Fusszeile
auf den acht Seiten ohne Autorenbox) einen Block mit fuenf themenpassenden Verweisen.

| Ziel | vorher | nachher |
|---|---|---|
| `/rechnung` | 2 | 44 |
| `/interview` | 0 | 44 |
| `/bibliothek` | 0 | 38 |
| `/city-guides` | 0 | 30 |
| `/immobilien` | 2 | 19 |
| `/reality-check` | 0 | 18 |
| `/freiweit-woche` | 0 | 15 |
| `/hotel-reise` | 0 | 6 |
| `/beratung` | 31 | 33 |

Das Skript ist idempotent, ein zweiter Lauf aendert nichts. Neue Artikel bekommen den Block
mit `python3 tools/ressourcen-block.py`. Mit `--pruefen` sieht man die Verteilung, ohne zu
schreiben. Klassen-Praefix ist `fw-res`, das CSS liegt in jeder Artikeldatei.

**Achtung Sitemap:** `bibliothek`, `city-guides`, `freiweit-woche` und `hilfe` stehen auf
`noindex` und gehoeren deshalb **nicht** in die Sitemap. Der Ressourcen-Block verlinkt sie
trotzdem, das ist richtig: Der Block ist fuer Leser da, nicht fuer Suchmaschinen. Sobald
die Produkte freigegeben und die Rechtspruefung durch ist, beides zusammen umstellen:
`noindex` raus **und** in die Sitemap rein.

---

## SEO-STAND 23.08.2026

Die Prüfkette meldete vorher 41 Punkte, jetzt 16, und die 16 sind nur ungenutzte
Bilddateien (Favicons und die Kaufhilfe-Screenshots auf der noindex-Seite), keine Fehler.

Was an dem Tag dazukam:

- **`VideoObject` in 36 Artikeln.** Vorher hatte kein einziger Artikel Video-Markup,
  obwohl 36 ein Video einbinden. Upload-Datum und Laufzeit stehen echt in
  `tools/videodaten.json`. Details in `README-seo.md`.
- **Sichtbarer Pfad in 45 Artikeln** über `tools/brotkrumen.py`. Wichtig für später:
  **kein `<nav>` benutzen**, zwei Vorlagen haben `nav{position:fixed}`.
- **17 Seitentitel gekürzt** auf unter 60 Zeichen und keyword-zuerst gestellt. Die H1
  im Artikel blieb jeweils unverändert, nur der `<title>` wurde umgeschrieben.
- **20 Meta-Beschreibungen** von über 165 auf 135 bis 156 Zeichen gekürzt.
- **8 Bilder** von 2.170 KB auf 1.910 KB gebracht, alle jetzt unter 250 KB.

Die sechs Gedankenstriche, die `gedankenstriche.py` meldet, stehen alle in echten
YouTube-Videotiteln und bleiben absichtlich stehen.

---

## ÜBERSICHTSSEITEN UND FAQ (24.08.2026)

Neu: `auswandern-thailand.html` und `auswandern-vietnam.html`. Das sind Übersichtsseiten
für die kurzen, umkämpften Suchbegriffe, auf die die Einzelartikel zeigen (39 bzw. 6
Verweise, gesetzt von `tools/ressourcen-block.py`). Sie folgen der Artikel-Regel und
tragen **keinen** Marken-Zusatz im Titel.

Beide Seiten und `beratung`, `immobilien`, `rechnung` haben einen FAQ-Block
(`<div class="fw-faq" data-faq>` mit `<details>`), aus dem `seo-strukturdaten.py`
automatisch `FAQPage` baut. Details und die ehrliche Einordnung dazu in `README-seo.md`.

Beim Immobilien-FAQ gelten die Leitplanken: **keine Provision bei Abschluss**, Objekte
immer als Fremdangebot ausweisen, kein Auftreten als Makler.

---

*Letzte Aktualisierung: 24.08.2026*

---

## MAPS GUIDE PATTAYA (Stand 22.08.2026)

Verkauf laeuft ueber **Stripe Payment Link**, nicht ueber Digistore24.
Kette: `city-guides.html` (Kaufknopf) → Stripe Checkout → Weiterleitung auf
`pattaya-maps-zugang-57651b.html` → sieben geteilte Google-Maps-Listen.

- Zahlungslink: `https://buy.stripe.com/9B67sLe6a6edaYIeQj3Ru00`
- Kurz-URL `/g` zeigt auf `/city-guides?via=qr`
- 50 Orte in sieben Listen. Die Zahl steht an fuenf Stellen in `city-guides.html`
  und in den Untertiteln der Zugangsseite. Bei Aenderung **ueberall** nachziehen,
  ausserdem im Stripe-Produkt (Beschreibung) und im Produktbild.
- Produktbild: `daten/maps-orte/produktion/produktbild/cover-A-dunkel.png`
- Die Maps-Listen liegen im Google-Konto `nyhattalk@gmail.com`, Anzeigename
  „Freiweit mit Nihat". Listen lassen sich zwischen Konten **nicht** umziehen.
- Die Teilen-Links bleiben gueltig, auch wenn Orte in den Listen geaendert werden.
  Nur beim Loeschen und Neuanlegen einer Liste bricht der Link.
