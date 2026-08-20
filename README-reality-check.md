# Reality-Check Seite (reality-check.html)

Interaktiver Selbsttest „Passt Auswandern wirklich zu dir?", 10 Fragen, ehrliche Auswertung,
danach freiwillige E-Mail-Erfassung. Reines HTML, CSS und Vanilla JavaScript in einer Datei.
Kein Framework, keine Bibliothek, kein Backend. Läuft direkt auf GitHub Pages.

Angelegt: 18.08.2026

---

## Was noch zu tun ist

### 1 · Brevo anschließen

Die Brevo-Anbindung liegt seit 20.08.2026 **zentral** in `js/brevo.js`, nicht mehr in dieser Seite.
Dort wird die Formular-Adresse EIN Mal eingetragen, danach hängen Reality-Check,
Monatsrechnung-Landingpage und die Newsletter-Box der Startseite gemeinsam daran.

Vollständige Anleitung: **`README-brevo.md`**.

Solange dort noch der Platzhalter steht, funktioniert die Seite trotzdem: der Versand läuft über
Web3Forms (`js/w3f.js`), die Anfrage landet als Mail im Postfach, inklusive Ergebnis-Typ, Punktzahl
und den zehn Antworten. Die Adresse muss dann von Hand in die Brevo-Liste übernommen werden.

Sobald Brevo steht, geht die Anmeldung an Brevo **und** die Auswertung zusätzlich als Info-Mail
ins Gmail-Postfach, damit du die persönliche Antwort schreiben kannst.

### 2 · Lead Magnet fertigstellen

Auf der Seite ist der Guide „Die echte Monatsrechnung. Was das Leben im Ausland wirklich kostet."
angekündigt. Der Guide ist fertig und liegt unter `pdfs/die-echte-monatsrechnung.pdf`.
Die passende Automation und der fertige Mailtext stehen in `README-brevo.md` und in
`../outputs/_bausteine/brevo-mails.md`, Abschnitt „Reality-Check".

### 3 · Vor dem Live-Gang testen

- [ ] Alle 10 Fragen durchklicken, Zurück-Button auf jeder Stufe testen
- [ ] Ergebnis auf dem Handy prüfen (iPhone Safari) und auf dem Tablet
- [ ] Formular mit falscher Adresse testen (Fehlermeldung muss kommen)
- [ ] Formular ohne Häkchen testen (Hinweis muss kommen, Ergebnis bleibt sichtbar)
- [ ] Formular korrekt absenden und prüfen, ob die Mail ankommt
- [ ] „Ergebnis ausdrucken" einmal prüfen
- [ ] Datenschutz-Link im Formular prüfen

### 4 · Nach dem Live-Gang

- [ ] Link in die YouTube-Videobeschreibungen aufnehmen (passt in den Block „Zusammenarbeiten mit Nihat")
- [ ] Community-Post: „Ich habe einen ehrlichen Selbsttest gebaut" mit Link
- [ ] Nach 4 Wochen prüfen: wie viele starten den Test, wie viele tragen sich ein

---

## Wie die Auswertung rechnet

Vier Bereiche, insgesamt 30 Punkte:

| Bereich | Fragen | Maximum |
|---|---|---|
| Geld und Absicherung | 1 (Puffer), 2 (Krankenversicherung) | 6 |
| Praxis und Alltag | 3, 5, 6, 7, 8 | 15 |
| Was zu Hause bleibt | 4 | 3 |
| Motiv und Zeitplan | 9, 10 | 6 |

Reihenfolge der Zuordnung (die erste zutreffende Regel gewinnt):

1. Gesamt 10 Punkte oder weniger → „Noch zu früh, und das ist keine schlechte Nachricht."
2. Motiv 2 Punkte oder weniger → „Du willst eher weg als hin."
3. Gesamt 14 Punkte oder weniger → „Noch zu früh."
4. Geld 3 Punkte oder weniger → „Dir fehlt vor allem das Geldpolster."
5. Gesamt 20 Punkte oder mehr → „Du bist weiter, als du denkst."
6. Alles andere → „Noch zu früh."

Die zwei Baustellen sind nicht fest an den Ergebnistyp gebunden, sondern werden aus den zwei
schwächsten Einzelantworten gezogen. Wer bei keiner Frage schwach antwortet, bekommt statt
Baustellen einen Hinweis auf den Praxistest vor Ort. Alle Texte stehen im Script in den Objekten
`QUESTIONS` (Fragen, Antworten, Baustellen-Texte) und `TYPES` (die vier Ergebnistypen).

Fragen ändern oder ergänzen: nur in `QUESTIONS` arbeiten, `dim` bestimmt den Bereich, `p` die
Punkte (0 bis 3). Wenn die Anzahl der Fragen sich ändert, die Maximalwerte in `DIMS` und die
Schwellen in `pickType()` mitziehen.

---

## Datenschutz

- Ohne Eintrag der E-Mail-Adresse verlässt nichts den Browser. Es gibt kein Tracking,
  keine Cookies, kein LocalStorage auf dieser Seite.
- Das Ergebnis ist immer sichtbar, auch ohne Adresse. Das ist eine bewusste Entscheidung
  und soll so bleiben.
- Die Einwilligung ist eine Pflicht-Checkbox, nicht vorausgewählt, mit Zweckangabe,
  Hinweis auf jederzeitige Abmeldung und Link auf `datenschutz.html`.
- Übertragen werden E-Mail-Adresse, optional der Vorname und das Testergebnis.
  Genau das steht auch im Text der Checkbox.
- Double-Opt-in in Brevo aktivieren (Schritt 2.3 in README-brevo.md).
- Die Datenschutzerklärung hat bereits einen Newsletter-Abschnitt. Wenn der Guide und der
  Reality-Check dauerhaft laufen, dort einen Satz zum Reality-Check ergänzen
  (Verarbeitung des Testergebnisses zum Versand der Auswertung).

---

## Verlinkung im Rest der Website

Die Seite hängt an vier Stellen in `index.html`:

1. Mega-Menü, Kachel „Reality-Check"
2. Schnellauswahl-Raster, Kachel „Reality-Check"
3. Eigene Sektion `#reality-check` zwischen „Über mich" und „Angebote"
4. Footer-Spalte „Angebote"

Dazu ein Eintrag in `sitemap.xml`.

---

## Regeln, die in dieser Datei eingehalten sind

- Keine Gedankenstriche, keine Emojis
- Wohnort-Regel: nirgends „ich lebe in X" oder „ich bin ausgewandert",
  stattdessen „seit sieben Jahren unterwegs", „über 70 Länder", „Monate in X gelebt"
- Keine Rechts-, Steuer- oder Versicherungsberatung. Auf der Ergebnisseite steht
  dazu ein eigener Hinweis
- Design-System der Homepage-Welt: Playfair Display plus Inter, Erdtöne, Nav und Footer
  wie auf `interview.html` und `ratgeber.html`
- Für die Zielgruppe 55+ bewusst größer gesetzt: Grundschrift 18 px, Antwortflächen
  mindestens 68 px hoch, Eingabefelder 60 px, hoher Kontrast, sichtbare Fokus-Rahmen
