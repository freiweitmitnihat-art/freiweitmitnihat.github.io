# VG WORT Schritt für Schritt

Die VG WORT zahlt Autoren Geld für Texte, die im Internet gelesen werden. Das Geld kommt
nicht von den Lesern, sondern aus gesetzlichen Abgaben (unter anderem auf Drucker, Kopierer
und Speichermedien). Du musst dafür nichts verkaufen und niemandem etwas berechnen.

**Größenordnung:** in den letzten Jahren etwa 20 bis 45 Euro je Text, der die Hürden schafft.
Die Höhe wird jedes Jahr neu festgelegt.

**Zwei Hürden pro Text:**
1. mindestens **1.800 Zeichen** (alle 44 Artikel schaffen das)
2. mindestens **1.500 Zugriffe im Kalenderjahr**

**Wichtig:** Gezählt wird erst ab dem Tag, an dem die Zählmarke im Artikel steht.
Rückwirkend geht nichts. Deshalb lohnt es sich, das früh zu machen, auch wenn die
Zugriffszahlen heute noch nicht reichen.

---

## Schritt 1: Konto anlegen (einmalig, etwa 20 Minuten)

1. Auf **vgwort.de** gehen, oben rechts auf **Anmelden**, dann **Neu registrieren**
2. Du legst zuerst ein Konto für das Portal **T.O.M.** an (das ist das Meldesystem der VG WORT)
3. Bestätigungsmail abwarten und Konto freischalten

**Was du bereithalten solltest:** Personalausweis, Steuer-Identifikationsnummer,
Bankverbindung (IBAN), Adresse.

## Schritt 2: Wahrnehmungsvertrag abschließen (einmalig)

1. In T.O.M. den **Wahrnehmungsvertrag für Urheber** aufrufen
2. Als Vertragsart **Urheber** wählen, nicht Verlag
3. Bereich: **Texte im Internet (METIS)** ankreuzen, weitere Bereiche schaden nicht
4. Absenden. Der Vertrag ist kostenlos und kann jederzeit gekündigt werden

Die Freischaltung dauert in der Regel einige Tage. Ohne diesen Vertrag bekommst du
keine Zählmarken.

## Schritt 3: Zählmarken bestellen (dauert 2 Minuten)

1. In T.O.M. auf **METIS** → **Zählmarken bestellen**
2. Anzahl: **50** eintragen (44 Artikel plus Reserve für neue)
3. Bestellen. Die Marken erscheinen sofort in deiner Übersicht

## Schritt 4: Marken exportieren und mir schicken

1. In der Zählmarken-Übersicht auf **Export** oder **CSV herunterladen**
2. Die Datei enthält pro Marke zwei Codes: einen **öffentlichen** (der in die Website kommt)
   und einen **privaten** (den brauchst du später zum Melden, der bleibt geheim)
3. **Schick mir die Datei.** Ich ordne die Marken den 44 Artikeln zu, baue die Pixel ein
   und schalte den passenden Abschnitt in der Datenschutzerklärung frei.

Falls du es selbst machen willst: die öffentlichen Adressen in `tools/vgwort-marken.txt`
hinter die Dateinamen schreiben und `python3 tools/vgwort-einbau.py` ausführen.

## Schritt 5: Einmal im Jahr melden

- **Frist: 31. Januar** für das jeweils vorherige Jahr
- In T.O.M. unter METIS siehst du, welche Texte die 1.500 Zugriffe erreicht haben
- Nur diese meldest du, mit Titel, Datum und dem privaten Code
- Die Auszahlung kommt üblicherweise im Herbst

---

## Was du dabei beachten musst

**Nur eigene Texte melden.** Die VG WORT zahlt für Werke, also für eigene schöpferische
Leistung. Ein Text, der nur aus einem Sprachmodell kommt, ist urheberrechtlich kein Werk
und darf nicht gemeldet werden. Deine Artikel beruhen auf deinen eigenen Drehs, Gesprächen
und Zahlen, das ist die Grundlage. Geh jeden Artikel vor der Veröffentlichung trotzdem
selbst durch und schreib ihn in deiner Sprache um. Dann ist die Meldung sauber.

**Die Zählmarke ist ein Zählpixel.** Sie gehört deshalb in die Datenschutzerklärung.
Der passende Abschnitt ist bereits vorbereitet und wird automatisch sichtbar, sobald
die erste Marke eingebaut ist.

**Ein Text, eine Marke.** Marken nie doppelt verwenden, sonst zählt die VG WORT falsch.
