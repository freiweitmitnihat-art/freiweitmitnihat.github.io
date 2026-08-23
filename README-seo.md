# SEO der Website: wie es läuft und was gilt

Stand: 23.08.2026. Diese Datei erklärt, welche Werkzeuge es gibt, was sie tun
und welche Seiten absichtlich nicht bei Google auftauchen sollen. Wer hier
nachliest, muss nichts raten.

---

## Der Ablauf nach jedem neuen Artikel

Der Slash-Befehl `/seo` arbeitet die Kette ab. Von Hand geht es auch:

```bash
python3 homepage/tools/sitemap-bauen.py
python3 homepage/tools/seo-strukturdaten.py
python3 homepage/tools/blog-index-pflegen.py
python3 homepage/tools/og-bilder.py --schreiben
python3 homepage/tools/gedankenstriche.py
python3 homepage/tools/seo-pruefen.py
```

| Werkzeug | Was es macht | Ändert Dateien |
|---|---|---|
| `sitemap-bauen.py` | baut `sitemap.xml` aus dem echten Dateibestand | ja |
| `seo-strukturdaten.py` | schreibt die Schema-Blöcke in jede Seite | ja |
| `blog-index-pflegen.py` | trägt neue Artikel in die Blog-Übersicht ein, neueste zuerst | ja |
| `og-bilder.py` | setzt das echte Artikelbild als Teilen-Bild, zieht die Maße nach | nur mit `--schreiben` |
| `gedankenstriche.py` | ersetzt lange Striche durch normale Satzzeichen | nur mit `--schreiben` |
| `seo-pruefen.py` | reiner Bericht, findet die Fehler, die man nicht sieht | nein |

Nach dem Push gehören zwei Handgriffe in der Search Console dazu:
Sitemap neu einreichen und neue Seiten per URL-Prüfung zur Indexierung anmelden.

---

## Welche Seiten absichtlich nicht in die Suche gehören

`noindex` ist kein Fehler, solange es hier steht. Das Sitemap-Werkzeug lässt
diese Seiten automatisch draußen.

| Seite | Warum | Wann fällt es weg |
|---|---|---|
| `bibliothek.html` | Ratgeber warten auf die Digistore-Freigabe | nach der Freigabe |
| `freiweit-woche.html` | Programmwoche noch nicht verkauft | beim Liveschalten |
| `pattaya-maps-zugang-57651b.html` | Zugangsseite für Käufer | nie |
| `danke.html` | Dankeseite nach dem Kauf | nie |
| `hilfe.html` | Kaufhilfe mit Screenshots | nie |
| `ratgeber.html` | alte Seite, leitet auf `/rechnung` | nie |
| `r b h i g w o .html` | Kurz-URLs für QR-Codes, reine Weiterleitungen | nie |
| `blog/bang-saen-villa-1.html` | Artikel zurückgezogen | nie |
| `blog/bang-saray-villa-pool.html` | Artikel zurückgezogen | nie |
| `blog/blog-template.html` | Vorlage, kein Artikel | nie |
| `404.html` | Fehlerseite | nie |
| `_entwuerfe/*` | Entwürfe der Startseite | nie |

**Wichtig für `sitemap-bauen.py`:** geprüft wird nur ein echtes robots-Meta.
Bis zum 23.08.2026 reichte das bloße Wort „noindex" irgendwo in der Datei, auch
in einem Kommentar. Dadurch ist `city-guides.html` bei jedem Lauf still aus der
Sitemap geflogen, obwohl die Seite verkauft. Der Fehler ist behoben.

---

## Teilen-Bilder (og:image)

Beim Teilen auf Facebook, WhatsApp und Co. zeigt jede Seite das Bild aus
`og:image`. Steht dort das allgemeine `og-image.jpg`, sehen alle Artikel gleich
aus. `og-bilder.py` setzt stattdessen das echte Artikelbild und zieht
`og:image:width` und `:height` auf die tatsächlichen Maße.

Zehn Ratgeber-Artikel haben kein eigenes Bild und behalten das allgemeine:
7-fehler-auswandern, da-nang-vietnam-entdeckt, grab-app-einrichten,
lebenshaltungskosten-thailand, sim-karte-thailand, stefan-bramburi-pattaya-naklua,
thailand-e-visum, thailand-tdac, vietnam-behoerden, vietnam-e-visum.
Wer dort ein Bild nachlegt, führt das Werkzeug einfach noch einmal aus.

---

## Titel

Muster: **Inhalt · Freiweit mit Nihat**. Der Trenner ist immer das Mittelpunkt-Zeichen,
nie Doppelpunkt und nie senkrechter Strich. Dass der Marken-Zusatz bei Google
hinten abgeschnitten wird, ist normal und stört nicht. `seo-pruefen.py` misst
deshalb nur den Teil davor und meldet ab 65 Zeichen.

---

## Gedankenstriche

Lange Striche wirken nach Maschine und sind auf der Website unerwünscht.
`gedankenstriche.py` räumt sie auf. **Eine Ausnahme bleibt bewusst stehen:**
sechs Striche in `bonus-suki-si-racha.html`, `ladda-condoview.html` und
`si-racha-barber-boxer.html` stecken in echten YouTube-Videotiteln. Würde man
sie ändern, stünde auf der Website ein anderer Titel als auf dem Kanal.
Deshalb wird dieses Werkzeug nie blind mit `--schreiben` gestartet, sondern
erst nach einem Blick auf die Fundstellen.

---

## Bilder

Die Fotos liegen bei 250 bis 300 KB und sind damit schon sauber komprimiert.
Nachgemessen am 23.08.2026: erneutes Komprimieren macht sie größer, WebP spart
nur rund 16 Prozent und wäre den Aufwand mit `<picture>` nicht wert.
Der Bericht meldet sie trotzdem, damit niemand versehentlich ein 2-MB-Foto
hochlädt. Erst ab dieser Größenordnung lohnt sich Handarbeit.

---

## Was der Bericht am 23.08.2026 noch offen lässt

1. **`blog/stefan-bramburi-pattaya-naklua.html` sucht ein Bild, das es nicht gibt**
   (`images/stefan-bramburi-pattaya-naklua.jpg`). Der Artikel fängt das ab und
   zeigt eine Farbfläche, aber das Bild fehlt, weil das Video noch nicht
   veröffentlicht ist. Sobald es online ist: Vorschaubild ablegen, Videolink
   nachtragen, `og-bilder.py` laufen lassen.
2. **`https://freiweitmitnihat.com/index.html` ist dieselbe Seite wie `/`.**
   Google kennt beide, indexiert `/`. Das Canonical auf der Startseite zeigt
   bereits auf `/`, damit ist es sauber gelöst.
3. **16 Bilddateien bindet keine öffentliche Seite ein**, zusammen rund 2 MB.
   Die Kaufhilfe-Bilder gehören zu `hilfe.html` und sind nur deshalb dabei,
   weil die Seite auf noindex steht. Der Rest sind Reste alter Entwürfe.
   Nichts davon schadet, aufräumen ist eine Aufgabe für einen ruhigen Tag.
