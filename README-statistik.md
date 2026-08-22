# Besucher messen, Suche verstehen, VG WORT

Kurzanleitung für alles, was jetzt auf der Seite vorbereitet ist.
Alles darin ist cookiefrei, deshalb braucht die Website kein Einwilligungsfenster.

---

## 1 · Umami einrichten (10 Minuten, einmalig)

1. Auf **cloud.umami.is** ein Konto anlegen. Bei der Frage nach der Region **EU (Deutschland)** wählen. Das ist wichtig, damit die Daten Europa nicht verlassen.
2. Unter *Settings · Websites · Add website* eintragen:
   Name `Freiweit mit Nihat`, Domain `freiweitmitnihat.com`
3. Umami zeigt dir danach eine **Website-ID**, sie sieht aus wie `1a2b3c4d-5e6f-...`
4. Diese ID in `js/stats.js` in die Zeile `var UMAMI_ID = 'TODO-UMAMI-ID';` eintragen.
5. Änderung hochladen. Ab dann läuft die Messung auf allen Seiten.

Solange dort `TODO-UMAMI-ID` steht, wird nichts gemessen und nichts geladen.
Der Free-Tarif reicht für 100.000 Ereignisse im Monat, das ist für den Anfang reichlich.

**Wichtig:** Die Datenschutzerklärung beschreibt Umami bereits als aktiv. Wenn du dich
doch für ein anderes Werkzeug entscheidest, sag Bescheid, dann wird der Abschnitt getauscht.

---

## 2 · Google Search Console und Bing (kostenlos, keine Datenschutzfolgen)

Umami zeigt dir, **wer da war**. Die Search Console zeigt, **wonach gesucht wurde**.
Das ist die eigentlich interessante Hälfte.

**Google Search Console**
1. `search.google.com/search-console` öffnen, Property vom Typ *Domain* anlegen: `freiweitmitnihat.com`
2. Google zeigt einen TXT-Eintrag. Den bei **Cloudflare** unter *DNS · Records* als TXT-Eintrag hinzufügen.
3. Nach der Bestätigung unter *Sitemaps* eintragen: `sitemap.xml`

**Bing Webmaster Tools**
`bing.com/webmasters` öffnen und die Search-Console-Property importieren. Zwei Klicks.
Lohnt sich, weil die Suche von ChatGPT auf Bing aufsetzt.

---

## 3 · Woher kommen die Leute? Kennzeichnung für Videos

Damit sichtbar wird, welches Video Besucher bringt, hänge an den Link in der
Videobeschreibung eine Kennzeichnung an:

```
https://freiweitmitnihat.com/r?utm_source=youtube&utm_campaign=si-racha-condo
```

- `utm_source` : woher, also `youtube`, `pinned`, `newsletter`, `instagram`
- `utm_campaign` : welches Video, am besten der Kurzname des Videos

Zusätzlich versteht die Seite weiterhin das kurze `?via=` aus den QR-Codes
(`qr`, `yt`, `pinned`, `web`). Beides landet in Umami, `via` als Ereignis `herkunft`.

**Diese Klicks werden automatisch gezählt**, ohne dass du etwas einbauen musst:
Beratung buchen, Kauf über Digistore, Hotel-Empfehlung, Versicherungs-Empfehlung,
BuyMeACoffee, YouTube, Instagram, Interview-Bewerbung, Mail-Klick.
Eigene Ereignisse gehen über `data-zaehl="name"` am Link.

---

## 4 · Was du wo abliest

| Frage | Wo |
|---|---|
| Wie viele Leute waren gestern auf der Seite? | Umami |
| Welches Video bringt Besucher? | Umami, Bereich *Campaigns* und Ereignis `herkunft` |
| Wonach wird bei Google gesucht? | Search Console, *Leistung* |
| Warum steigt oder fällt eine Seite? | Search Console, Position und Klickrate |
| Wie viele haben die Beratung angeklickt? | Umami, Ereignis `beratung-buchen` |

Sinnvoller Rhythmus: einmal die Woche zehn Minuten. Nicht täglich.

---

## 5 · VG WORT

Die VG WORT zahlt für Texte im Internet, wenn sie **mindestens 1.800 Zeichen** lang sind
und im Jahr **mindestens 1.500 Zugriffe** erreichen. Gezählt wird ab dem Tag, an dem die
Zählmarke im Artikel steht, rückwirkend geht nichts.

So gehst du vor:

1. Auf `vgwort.de` einen **Wahrnehmungsvertrag** abschließen, das ist kostenlos.
2. Im Portal **T.O.M.** unter METIS Zählmarken bestellen, eine pro Artikel.
3. Die Adressen in `tools/vgwort-marken.txt` hinter den jeweiligen Dateinamen schreiben.
4. Dann `python3 tools/vgwort-einbau.py` ausführen. Das Skript baut die Pixel ein
   und schaltet den passenden Abschnitt in der Datenschutzerklärung frei.
5. Meldefrist ist der **31. Januar** für das jeweils vorherige Jahr.

**Wichtige Einschränkung:** Gemeldet werden dürfen nur eigene Texte. Ein Text, der
nur aus einem Sprachmodell kommt, ist kein Werk im Sinne des Urheberrechts. Deine
Artikel beruhen auf deinen eigenen Drehs, Gesprächen und Zahlen. Geh sie trotzdem
vor der Veröffentlichung selbst durch und schreib sie in deiner Sprache um, dann ist
die Meldung sauber.

Die vollständige Anleitung mit allen Schritten steht in `README-vgwort.md`.

Welche Artikel die Zeichengrenze schaffen, zeigt:
```
python3 tools/vgwort-check.py
```
Stand heute: alle 44 Artikel liegen darüber, der kürzeste knapp.

---

## 6 · Werkzeuge im Ordner tools/

| Befehl | Was er macht |
|---|---|
| `python3 tools/sitemap-bauen.py` | Baut sitemap.xml aus dem Dateibestand neu |
| `python3 tools/seo-strukturdaten.py` | Schreibt die Google-Strukturdaten in alle Seiten |
| `python3 tools/blog-index-pflegen.py` | Trägt neue Artikel in die Blog-Übersicht ein |
| `python3 tools/vgwort-check.py` | Zeigt Zeichenzahl je Artikel |
| `python3 tools/vgwort-einbau.py` | Setzt die Zählmarken |
| `python3 tools/statistik-bericht.py` | Holt die Besucherzahlen aus Umami |
| `python3 tools/gedankenstriche.py` | Findet und ersetzt lange Striche im Text |

**Nach jedem neuen Blogartikel** die ersten drei laufen lassen, in dieser Reihenfolge.
Alle Skripte kann man beliebig oft ausführen, sie doppeln nichts.

---

## 7 · Die Zahlen abfragen

Drei Wege, je nach Situation:

**A) Du fragst mich.** Sag „zeig mir die Zahlen" oder „wie lief die Woche". Ich führe
`python3 tools/statistik-bericht.py` aus und erkläre dir, was auffällt. Dafür brauche
ich einmalig einen Schlüssel:

1. In Umami auf *Settings* → *API Keys* → *Create key*
2. Den Schlüssel in den Schlüsselbund legen (er landet so nicht in einer Datei
   und nicht in der Terminal-Historie):
   `security add-generic-password -U -a "$USER" -s UMAMI_API_KEY -w`
3. Fertig. Ab dann kann ich die Zahlen jederzeit abrufen.

**B) Selbst nachsehen.** cloud.umami.is öffnen. Das Dashboard zeigt Besucher, Seiten,
Herkunft und unter *Events* die Klicks und Anmeldungen.

**C) Automatisch jede Woche.** Wenn du willst, richte ich einen wöchentlichen Lauf ein,
der montags den Bericht erzeugt und dir die drei wichtigsten Änderungen schreibt.

**Was du wirklich beobachten solltest**, alles andere ist Beiwerk:

| Kennzahl | wo | warum |
|---|---|---|
| Newsletter-Anmeldungen | Umami, Ereignis `newsletter-anmeldung` | dein Fundament laut Monetarisierungsplan |
| Klicks auf Beratung | Ereignis `beratung-buchen` | direktes Geld |
| Herkunft YouTube | Umami, *Referrers* und Ereignis `herkunft` | zeigt, welche Videos ziehen |
| Suchbegriffe und Position | Search Console, *Leistung* | zeigt, wofür Google dich überhaupt zeigt |
| Meistgelesene Artikel | Umami, *Pages* | sagt dir, welche Themen du ausbauen solltest |

Ein Blick pro Woche reicht. Tägliches Draufschauen führt bei kleinen Zahlen nur zu
Fehlschlüssen, weil einzelne Besucher die Quote stark schwanken lassen.
