# CLAUDE.md · Freiweit mit Nihat · Homepage
## Master-Instruction für alle Homepage-Arbeiten

Lies diese Datei vollständig bevor du irgendetwas änderst.
Zuerst die Root-CLAUDE.md, dann diese hier.

**Stand: 20.08.2026. Startseite komplett neu gebaut, alte Fassung liegt als
`index-alt.html` daneben und unter `/Volumes/Extreme Pro/Claude/homepage-backup-*`.**

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
| `index-alt.html` | alte Startseite, nur als Fundus | löschbar, sobald alles steht |
| `rechnung.html` | Landingpage Lead Magnet, ein Feld, ein Button | live |
| `r.html` / `b.html` | Kurzweiterleitungen für die QR-Codes | **Ziel nie ändern** |
| `ratgeber.html` | leitet auf `/rechnung` weiter | Weiterleitung |
| `bibliothek.html` | Ratgeber kaufen, 6 Hefte plus Paket | Digistore-IDs fehlen |
| `hilfe.html` | Kaufhilfe, „wo ist mein Download-Ordner" | 4 Screenshots fehlen |
| `freiweit-woche.html` | Programmwoche vor Ort | `noindex` bis Rechtsprüfung |
| `beratung.html` | 97 € Beratungsgespräch, Cal.eu | live |
| `immobilien.html` `interview.html` `kontakt.html` | | live |
| `reality-check.html` | Selbsttest, 10 Fragen | live |
| `city-guides.html` | Maps-Guides | wartet auf Guides |
| `blog/` | 50 Artikel plus `blog/index.html` | live |
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

**Offen, das kann nur Nihat:** Formular in Brevo anlegen, Serve-Adresse in
`js/brevo.js` eintragen.

---

## BILDER

Liegen als Datei in `homepage/img/`, **nicht mehr base64 eingebettet**.
Neue Bilder: max. 1600 px Breite, JPEG 82 bis 88 %, immer `alt` und
immer eine `<figcaption>` mit Ort und Situation.

Fehlen noch: drei Beitragsbilder im Blog
(`bang-saray-beach.png`, `jomtien-oliver-lalana.png`, `pattaya-ralph-interview.png`).

---

## VOR JEDEM ABSCHLUSS PRÜFEN

```bash
grep -c '—' *.html blog/*.html          # muss überall 0 sein
```
Dazu: alle internen Links auflösen, jedes `<img>` hat `alt`, jedes Foto hat
`<figcaption>`, Kontrast im Fließtext mindestens 7:1, Klickflächen mindestens 48 px.

---

*Letzte Aktualisierung: 20.08.2026*
