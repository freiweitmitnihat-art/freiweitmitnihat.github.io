# VG Wort METIS · Bestandsaufnahme und Plan

**Erstellt am 24.08.2026.** Grundlage: alle Artikel unter `Homepage/blog/`, maschinell
ausgewertet (Zeichenzahl im Fließtext, eigenes Video verlinkt, O-Töne im Text).

---

## Die Ausgangslage

| | |
|---|---|
| Artikel gesamt | **45** (zwei weitere Dateien sind nur Weiterleitungen) |
| davon über 1.800 Zeichen | **45, also alle** |
| Durchschnittliche Länge | rund 4.400 Zeichen |
| Artikel mit Zählmarke | **0** |

**Die Längenschwelle ist bei keinem einzigen Artikel ein Problem.** Das war meine
Sorge, sie hat sich erledigt.

---

## Was VG Wort tatsächlich zahlt

Die Beträge sinken seit Jahren deutlich:

| Jahr | pro gemeldetem Text |
|---|---|
| 2022 | 43,86 € |
| 2023 | 33,34 € |
| 2024 | 25,05 € |
| 2025 | **19,73 €** |

Quelle: xgadget.de zur METIS-Ausschüttung 2025.

**Rechnung für dich, ehrlich:** 45 Artikel × rund 20 € = **höchstens 900 € im Jahr**,
und das nur, wenn **jeder einzelne** Artikel die 1.500 Zugriffe schafft. Das wird
er nicht. Realistisch sind es die zehn bis fünfzehn stärksten Artikel, also
grob **200 bis 300 € im Jahr**.

Das ist kein Geschäftsmodell. Es ist Geld, das ohnehin da liegt und das man
mitnimmt, weil der Aufwand einmalig ist.

---

## Die eigentliche Hürde ist nicht die Länge, sondern zweierlei

### 1. Die Zugriffe

**1.500 Zugriffe im Jahr** braucht jeder Text bei 1.800 bis 9.999 Zeichen.
Wie viele deiner Artikel das schaffen, weiß ich nicht: Der Umami-Schlüssel liegt
nicht im Schlüsselbund, ich komme an deine Besucherzahlen nicht heran.

**Das ist die erste Zahl, die wir brauchen.**

### 2. Die Urheberschaft

VG Wort schüttet an den **Urheber** aus, und Urheber kann nur ein Mensch sein.
Ein Text, der vollständig von einer KI geschrieben wurde, hat nach deutschem
Urheberrecht keinen Urheber. Bei der Meldung in T.O.M. erklärst du, dass der Text
von dir ist. Diese Erklärung muss stimmen.

**Das heißt nicht, dass die Artikel wertlos sind.** Die Fakten darin sind deine:
deine Interviews, deine Wohnungsbesichtigungen, deine Zahlen vor Ort. Was fehlt,
ist deine Formulierung.

---

## Der Zeitfaktor, der alles umdreht

**Zählmarken zählen erst ab dem Moment, in dem sie eingebaut sind.** Rückwirkend
zählt nichts. Wer heute einbaut, sammelt ab heute für die Ausschüttung 2027.
Wer ein Jahr wartet, verliert ein Jahr.

**Deshalb ist die Reihenfolge umgekehrt, als man denkt:**
Erst die Marken einbauen, dann in Ruhe überarbeiten. Nicht andersherum.

---

## Der Plan, in dieser Reihenfolge

### Schritt 1 · Diese Woche, nur du (kostenlos)
1. **Wahrnehmungsvertrag** bei der VG Wort abschließen, auf vgwort.de. Kostet nichts.
2. **Zugang zu T.O.M.** einrichten.
3. **45 Zählmarken** bestellen. Geht in einem Rutsch.
4. Die Codes in `Homepage/tools/vgwort-marken.txt` eintragen, eine Zeile je Artikel.

### Schritt 2 · Dann ich, an einem Abend
```bash
python3 tools/vgwort-einbau.py
```
Setzt jede Marke automatisch an die richtige Stelle vor `</body>`. Statisch, ohne
JavaScript, damit wirklich jeder Aufruf gezählt wird. Danach committen und pushen.
**Ab dem Moment läuft die Zählung.**

### Schritt 3 · Besucherzahlen holen
Umami-Schlüssel in den Schlüsselbund legen:
```bash
security add-generic-password -U -a "$USER" -s UMAMI_API_KEY -w
```
Dann sehe ich mit `tools/statistik-bericht.py`, welche Artikel überhaupt in die Nähe
von 1.500 Zugriffen kommen. **Erst diese Zahl sagt, wo sich Überarbeiten lohnt.**

### Schritt 4 · Überarbeiten, nach Zugriffen sortiert
Nur die Artikel, die die Schwelle realistisch schaffen. Pro Artikel etwa eine halbe
Stunde: deine Einschätzungen rein, Formulierungen ändern, eine Meinung dort, wo du
eine hast. Dann ist es dein Text.

### Schritt 5 · Januar 2027 melden
In T.O.M. die Texte melden, die 1.500 Zugriffe erreicht haben.

---

## Wo sich das Überarbeiten am ehesten lohnt

Sortiert nach dem Anteil deines eigenen Materials. Das ist **nicht** die Reihenfolge
fürs Überarbeiten, dafür entscheiden die Zugriffe aus Schritt 3. Es zeigt nur,
wo am wenigsten Arbeit nötig ist, damit ein Text glaubwürdig deiner wird.

### Gruppe A · Eigenes Interview mit O-Tönen (4 Artikel)
Hier stehen wörtliche Zitate von Menschen, mit denen du selbst gesprochen hast.
Am schnellsten zu deinem Text gemacht.

| Artikel | Zeichen |
|---|---|
| `huahin-german-corner-khwan` | 7.553 |
| `stefan-bramburi-pattaya-naklua` | 7.519 |
| `bangkok-matz-interview-1` | 7.007 |
| `chris-interview-huahin` | 5.007 |

### Gruppe B · Eigenes Video, wenig Zitate (32 Artikel)
Orte, Wohnungen, Lokale, die du selbst gefilmt hast. Die Beobachtungen sind deine,
die Formulierung nicht.

| Artikel | Zeichen |
|---|---|
| `si-racha-j-park-2` | 6.910 |
| `pattaya-ralph-interview` | 6.606 |
| `bangkok-matz-interview-2` | 6.505 |
| `si-racha-koh-loi` | 6.454 |
| `bangkok-mats-tunnel` | 6.296 |
| `excel-hideaway-sukhumvit-71` | 6.100 |
| `bangkok-matz-interview-3` | 5.800 |
| `bonus-suki-si-racha` | 5.666 |
| `casey-papagei-maklerin` | 5.572 |
| `ladda-condoview` | 5.552 |
| `jomtien-oliver-lalana` | 5.530 |
| `si-racha-immobilie` | 5.260 |
| `bang-saray-resort` | 5.164 |
| `sharmonyx-sriracha-wohnungen` | 5.138 |
| `sri-racha-the-complete` | 4.888 |
| `2026-06-16-thomas-loft-pattaya` | 4.803 |
| `interview-bang-saen-nico` | 4.649 |
| `riviera-ocean-drive` | 4.559 |
| `interview-bang-saen-nico-2` | 4.504 |
| `si-racha-barber-boxer` | 4.458 |
| `trio-town-si-racha` | 4.109 |
| `si-racha-baan-talay-cafe` | 4.104 |
| `the-complete-sriracha-2` | 4.095 |
| `bang-saray-beach` | 4.012 |
| `si-racha-the-near-residence` | 3.901 |
| `si-racha-the-strand` | 3.818 |
| `lebenshaltungskosten-vietnam` | 3.690 |
| `pattaya-kosten-2026` | 3.029 |
| `samusorn-bangkok-eis` | 2.721 |
| `koh-loi-streetfood-sriracha` | 2.677 |
| `sim-karte-vietnam` | 2.483 |
| `wattana-panich-bangkok` | 2.295 |

### Gruppe C · Reine Recherche (9 Artikel)
Visum, SIM-Karte, Behörden, Apps. Kein eigenes Video, kein eigenes Erleben.
**Hier ist am meisten Arbeit nötig**, um daraus wirklich deinen Text zu machen.
Wenn du priorisieren musst, kommt diese Gruppe zuletzt.

| Artikel | Zeichen |
|---|---|
| `vietnam-e-visum` | 4.208 |
| `lebenshaltungskosten-thailand` | 3.590 |
| `7-fehler-auswandern` | 3.326 |
| `vietnam-behoerden` | 3.215 |
| `sim-karte-thailand` | 3.135 |
| `thailand-e-visum` | 2.969 |
| `thailand-tdac` | 2.935 |
| `da-nang-vietnam-entdeckt` | 2.879 |
| `grab-app-einrichten` | 2.402 |

---

## Was ich dir nicht empfehle

**Nicht alle 45 auf Verdacht überarbeiten.** Das sind rund zwanzig Stunden. Wenn
davon nur zehn Artikel die Zugriffsschwelle schaffen, hast du fünfzehn Stunden für
nichts investiert. Erst messen, dann arbeiten.

**Nicht auf die Ausschüttung als Einnahmequelle setzen.** Bei 19,73 € pro Text und
sinkender Tendenz ist das ein Nebeneffekt, kein Hebel. Dein Hebel sind die Ratgeber
und die Beratung.
