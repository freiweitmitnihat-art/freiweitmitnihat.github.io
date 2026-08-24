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
python3 homepage/tools/vorschaubilder.py --schreiben
python3 homepage/tools/kopfbilder.py --schreiben
python3 homepage/tools/titel-marke.py --schreiben
python3 homepage/tools/kurz-gesagt.py --schreiben
python3 homepage/tools/gedankenstriche.py
python3 homepage/tools/rechtslinks.py --schreiben
python3 homepage/tools/brotkrumen.py --schreiben
python3 homepage/tools/seo-pruefen.py
```

| Werkzeug | Was es macht | Ändert Dateien |
|---|---|---|
| `sitemap-bauen.py` | baut `sitemap.xml` aus dem echten Dateibestand | ja |
| `seo-strukturdaten.py` | schreibt die Schema-Blöcke in jede Seite, inklusive `VideoObject` | ja |
| `blog-index-pflegen.py` | trägt neue Artikel in die Blog-Übersicht ein, neueste zuerst | ja |
| `og-bilder.py` | setzt das echte Artikelbild als Teilen-Bild, zieht die Maße nach | nur mit `--schreiben` |
| `vorschaubilder.py` | füllt die Kacheln der Blog-Übersicht und der „Weitere Artikel"-Kästen | nur mit `--schreiben` |
| `kopfbilder.py` | legt das Artikelbild in das Banner unter der Überschrift | nur mit `--schreiben` |
| `gedankenstriche.py` | ersetzt lange Striche durch normale Satzzeichen | nur mit `--schreiben` |
| `kurz-gesagt.py` | setzt den Antwort-Kasten oben in die Ratgeber-Artikel | nur mit `--schreiben` |
| `titel-marke.py` | nimmt den Marken-Zusatz aus Artikel-Titeln, Funktionsseiten behalten ihn | nur mit `--schreiben` |
| `rechtslinks.py` | hängt Impressum und Datenschutz an jede Fußzeile, wo sie fehlen | nur mit `--schreiben` |
| `brotkrumen.py` | setzt den sichtbaren Pfad „Startseite › Blog › Artikel" in jeden Artikel | nur mit `--schreiben` |
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
| `huahin-maps-zugang-5893a3.html` | Zugangsseite für Käufer | nie |
| `danke.html` | Dankeseite nach dem Kauf | nie |
| `hilfe.html` | Kaufhilfe für die Ratgeber, Digistore und PDF | nie |
| `maps-hilfe.html` | Kaufhilfe für die Maps Guides, Stripe und Google Maps | nie |
| `ratgeber.html` | alte Seite, leitet auf `/rechnung` | nie |
| `r b h i g w o hh .html` | Kurz-URLs für QR-Codes, reine Weiterleitungen | nie |
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

## „Kurz gesagt": die Antwort steht oben

Seit dem 23.08.2026 beginnt jeder Ratgeber-Artikel mit einem Kasten, der die Frage
des Artikels in drei bis vier Zeilen beantwortet, mit den Zahlen fett.

**Warum das der wichtigste Hebel ist:** Google beantwortet inzwischen etwa jede fünfte
Suche direkt in der KI-Übersicht, und ChatGPT, Perplexity und Gemini lesen dabei den
**sichtbaren** Text einer Seite. Die Strukturdaten werden in dieser Phase ignoriert.
Zitiert wird, wer die Antwort oben hinschreibt, statt sie in einen langen Fließtext zu
vergraben. Und Zitiertwerden zahlt sich aus: Marken, die in einer KI-Übersicht genannt
werden, bekommen deutlich mehr Klicks als Marken auf derselben Trefferliste, die nicht
genannt werden.

Der zweite Grund ist die Zielgruppe: 55+, ein Drittel schaut auf dem Fernseher. Die
wollen die Antwort nicht erst suchen.

**Regel:** Jede Zahl im Kasten muss so auch im Artikel stehen. Die Kästen liegen im
Klartext in `tools/kurz-gesagt.py`. Wer eine Zahl ändert, ändert sie an beiden Stellen.
Aktuell haben ihn die elf Ratgeber, bei denen Google eine KI-Übersicht zeigt: Kosten
Thailand, Kosten Vietnam, Kosten Pattaya, Visum Thailand, Visum Vietnam, TDAC,
SIM Thailand, SIM Vietnam, Grab, Vietnam-Behörden und die 7 Fehler.

**Was wir bewusst NICHT gemacht haben:** eine `llms.txt`. Google hat bestätigt, dass
kein Suchsystem die Datei liest, und OpenAI, Anthropic, Google und Meta haben sich
bis heute nicht darauf festgelegt, sie zu benutzen. Der Aufwand bringt nichts.

---

## Impressum und Datenschutz

Beide müssen von **jeder** Seite aus erreichbar sein, nicht nur von der Startseite.
Seit die Website verkauft (Beratung, Digistore, Stripe), zählt das doppelt.

Am 23.08.2026 fehlten die Links auf 25 von 60 öffentlichen Seiten, darunter
`beratung.html`, `kontakt.html`, `mediakit.html` und die ganze Blog-Übersicht.
`immobilien.html` zeigte auf `index.html#impressum` und `index.html#datenschutz`,
diese Sprungmarken gibt es auf der Startseite gar nicht. `mediakit.html` hatte
überhaupt keine Fußzeile. Alles behoben, `rechtslinks.py` hält es künftig sauber
und `seo-pruefen.py` schlägt Alarm, wenn wieder eine Seite ohne die beiden Links
dazukommt.

Der Standard in der Fußzeile lautet:
`© 2026 Nihat Bucakli · Freiweit mit Nihat · Impressum · Datenschutz`

---

## Teilen-Bilder (og:image)

Beim Teilen auf Facebook, WhatsApp und Co. zeigt jede Seite das Bild aus
`og:image`. Steht dort das allgemeine `og-image.jpg`, sehen alle Artikel gleich
aus. `og-bilder.py` setzt stattdessen das echte Artikelbild und zieht
`og:image:width` und `:height` auf die tatsächlichen Maße.

**Seit dem 23.08.2026 hat jeder der 45 Artikel sein eigenes Bild.** Vorher fehlte
zehn Ratgeber-Artikeln eines. Sie haben jetzt das Vorschaubild des thematisch
passenden Kanal-Videos bekommen:

| Artikel | Bildquelle (Video auf dem Kanal) |
|---|---|
| stefan-bramburi-pattaya-naklua | „Ich lebte von 150 Euro die Woche" (eigenes Thumbnail von der Extreme Pro) |
| da-nang-vietnam-entdeckt | Da Nang: Vor- & Nachteile, nach 7 Jahren Weltreise |
| lebenshaltungskosten-thailand | Thailand Kosten 2026, warum viele falsch rechnen |
| sim-karte-thailand | Thailand 2026: 1 € SIM-Karte |
| thailand-tdac | Einreise Thailand 2026, alle Änderungen |
| thailand-e-visum | Muss ich raus? Thai-Visum verlängern |
| 7-fehler-auswandern | Niemand sagt dir das, an alles gedacht? |
| grab-app-einrichten | Die erste Stunde in Thailand: SIM, BTS, Taxi |
| vietnam-e-visum | Ich muss Vietnam verlassen |
| vietnam-behoerden | Geld abheben in Vietnam |

Die Bilder liegen als 1280x720 in `blog/images/` und heißen genau wie der Artikel.
Das ist die Regel: **`blog/images/<artikelname>.jpg`**, daran erkennt `og-bilder.py`
das richtige Bild. Wer ein besseres Foto hat, überschreibt einfach die Datei.

**Ein Bild kommt nicht vom Kanal:** `vietnam-behoerden` behandelt das Online-Portal
Dich Vu Cong, dazu gibt es kein Video und auch kein eigenes Foto. Dort liegt jetzt eine
Aufnahme eines vietnamesischen Behördenhauses aus Wikimedia Commons:
„Thạch Bàn government office (2017)" von Donald Trung, CC BY-SA 4.0, zugeschnitten.
**Die Lizenz verlangt die Nennung**, deshalb steht der Nachweis sichtbar unter dem
Artikeltext. Wer das Bild austauscht, muss den Nachweis mit entfernen.

Das ist das einzige Fremdbild auf der Website. Alles andere stammt von Nihat selbst.

---

## Titel

**Regel seit dem 23.08.2026, zwei Fälle:**

| Seitenart | Muster | Beispiel |
|---|---|---|
| Blogartikel | **ohne** Marken-Zusatz, Schlüsselwort vorne | `Haus in Thailand kaufen: 164 m² für 124.000 €` |
| Funktionsseiten | **mit** ` · Freiweit mit Nihat` | `Impressum · Freiweit mit Nihat` |

Warum der Unterschied: Google zeigt rund 60 Zeichen. Bei einem Artikel sind
21 Zeichen für „ · Freiweit mit Nihat" genau die Stelle, an der das Schlüsselwort
stehen sollte. Den Kanalnamen setzt Google bei bekannten Seiten ohnehin selbst dazu.
Bei „Impressum" oder „Kontakt" dagegen ist die Marke der Inhalt: ohne sie wäre der
Treffer nicht zuzuordnen.

Vorher galt bis zum Vormittag des 23.08.2026 die umgekehrte Regel, mit Zusatz überall.
`titel-marke.py` hat die Umstellung gemacht, `seo-pruefen.py` meldet jede Abweichung.
Wo ein Trenner nötig ist, ist es das Mittelpunkt-Zeichen, nie Doppelpunkt oder
senkrechter Strich.

`seo-pruefen.py` misst außerdem die Länge und meldet ab 65 Zeichen.

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


---

## VideoObject: damit die Videos selbst gefunden werden (seit 23.08.2026)

36 Blogartikel binden ein YouTube-Video ein. Bis zum 23.08.2026 stand in keinem
einzigen ein `VideoObject`, Google konnte die Videos also nicht als Videos erkennen.
Seitdem schreibt `seo-strukturdaten.py` den Block automatisch mit.

Upload-Datum und Laufzeit sind bei Google **Pflichtangaben**. Beides steht echt in
`homepage/tools/videodaten.json`, geholt direkt von der jeweiligen YouTube-Seite.
Geschätzte Daten wären wertlos, Google prüft sie gegen YouTube.

```bash
python3 homepage/tools/seo-strukturdaten.py --videos-aktualisieren
```

Das ergänzt fehlende Videos in der Datei und lässt vorhandene stehen. Nötig ist es
nur, wenn ein Artikel mit einem neuen Video dazugekommen ist.

Kontrolle nach dem Push: Google Rich Results Test auf eine Artikel-URL, dort muss
„Video" als erkannter Typ auftauchen. In der Search Console kommt danach der Bericht
„Videos" dazu, dort sieht man, wie viele Videos indexiert sind.

---

## Sichtbarer Pfad (Brotkrumen, seit 23.08.2026)

Die Strukturdaten behaupteten in jedem Artikel einen Pfad „Startseite › Blog › Artikel",
auf der Seite war davon nichts zu sehen. Dazu bekam `blog/index.html` nur 5 interne
Verweise, obwohl 45 Artikel darunter hängen.

`tools/brotkrumen.py` setzt den Pfad oben in den Textbereich. Damit stimmen Anzeige und
Strukturdaten überein, und die Blog-Übersicht bekommt 45 interne Verweise.

**Merker für spätere Änderungen:** Der Pfad ist bewusst ein `<div role="navigation">`
und **kein** `<nav>`. Zwei der drei Artikel-Vorlagen haben eine nackte CSS-Regel
`nav{position:fixed;height:60px}`, die jedes `nav` in die Kopfleiste zieht. Beim ersten
Versuch am 23.08.2026 hat genau das die Seite zerlegt.


---

## Übersichtsseiten (Pillar Pages, seit 24.08.2026)

Einzelne Artikel ranken für lange, spezifische Suchen („162 Euro Miete Si Racha").
Für die kurzen, umkämpften Suchen („auswandern thailand") braucht es eine starke
Übersichtsseite, auf die viele Artikel zeigen. Genau das sind:

| Seite | Cluster | Verweise aus Artikeln |
|---|---|---|
| `auswandern-thailand.html` | Kosten, Visum, Wohnen, Versicherung, Alltag, Interviews | 39 |
| `auswandern-vietnam.html` | Kosten, E-Visum, Wohnen, Alltag | 6 |

Die Verweise setzt `tools/ressourcen-block.py` automatisch. Es erkennt am Text, ob ein
Artikel eher Thailand oder Vietnam ist, und setzt den passenden Übersichts-Link an die
erste Stelle des Blocks. Bei neuen Artikeln passiert das von allein. Wenn sich die
Angebotsliste ändert, alle Blöcke erneuern mit:

```bash
python3 homepage/tools/ressourcen-block.py --erneuern
```

**Titel-Regel:** Übersichtsseiten tragen **keinen** Marken-Zusatz im Titel, wie
Blogartikel auch. Sonst schneidet Google den Titel mitten im Keyword ab. Der Prüfer
kennt sie über die Liste `UEBERSICHT` in `tools/seo-pruefen.py`. Neue Übersichtsseiten
dort eintragen.

---

## FAQ-Blöcke

Eine Seite bekommt automatisch `FAQPage`-Auszeichnung, sobald sie einen sichtbaren
Block dieser Form enthält:

```html
<div class="fw-faq" data-faq>
  <details><summary>Frage?</summary>
    <div class="antwort"><p>Antwort.</p></div>
  </details>
</div>
```

`seo-strukturdaten.py` liest ihn aus. Aufklappbar ist erlaubt, die Fragen müssen aber
im Seitentext stehen, nicht per JavaScript nachgeladen werden.

Aktuell auf fünf Seiten: `auswandern-thailand`, `auswandern-vietnam`, `beratung`,
`immobilien`, `rechnung`.

**Ehrliche Einordnung:** Google zeigt FAQ-Ausklapper in der Trefferliste seit August
2023 fast nur noch für Behörden- und Gesundheitsseiten. Der Block bringt trotzdem
etwas, nur an anderer Stelle: KI-Antworten und die Rubrik „Ähnliche Fragen" greifen
darauf zu, und für Leser beantwortet er die Fragen, die sonst per Mail kommen.
