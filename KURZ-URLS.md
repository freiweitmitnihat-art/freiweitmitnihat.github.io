# Kurz-URLs für QR-Codes

**Diese Datei ist die einzige Wahrheitsquelle.** Wenn irgendwo im Projekt eine
Kurz-URL steht, die hier nicht drin ist oder ein anderes Ziel nennt, gilt diese Datei.

---

## Die harte Regel

Ein QR-Code, der einmal in ein Video gerendert wurde, lässt sich nie mehr ändern.
Zuschauer scannen ihn noch Jahre später vom Fernseher ab.

Daraus folgt:

1. **Eine Adresse wird nie umbenannt und nie gelöscht.** Auch dann nicht, wenn das
   Produkt dahinter eingestellt wird. In dem Fall zeigt sie eben auf eine
   Erklärseite, aber sie darf nie ins Leere laufen.
2. **Eine Adresse wird nie auf ein anderes Thema umgebogen.** `/b` bleibt Beratung,
   auch wenn „b" später einmal nach Bibliothek klingt. Wer ein altes Video sieht,
   muss dort landen, was ihm damals versprochen wurde.
3. **Neue Ziele bekommen eine neue Adresse**, nie eine bestehende.
4. **Vor jedem Render prüfen**, ob die Zieldatei existiert und die Weiterleitung
   funktioniert. Ein toter QR im Video ist nicht mehr reparierbar.

---

## Belegte Adressen

| Adresse | Datei | Ziel | Seit | Was der Zuschauer erwartet |
|---|---|---|---|---|
| `freiweitmitnihat.com/r` | `r.html` | `/rechnung?via=qr` | vor Aug 2026 | Die echte Monatsrechnung, kostenloser Lead Magnet |
| `freiweitmitnihat.com/b` | `b.html` | `/beratung?via=qr` | vor Aug 2026 | Beratungsgespräch, 60 Minuten |
| `freiweitmitnihat.com/h` | `h.html` | `/bibliothek?via=qr` | 22.08.2026 | Die Bibliothek, sechs **H**efte |
| `freiweitmitnihat.com/i` | `i.html` | `/interview?via=qr` | 22.08.2026 | **I**nterview-Bewerbung, eigene Geschichte erzählen |
| `freiweitmitnihat.com/w` | `w.html` | `/freiweit-woche?via=qr` | 22.08.2026 | Die Freiweit-**W**oche, Seminarwoche vor Ort |
| `freiweitmitnihat.com/g` | `g.html` | `/city-guides?via=qr` | 22.08.2026 | Die City **G**uides |
| `freiweitmitnihat.com/o` | `o.html` | `/immobilien?via=qr` | 23.08.2026 | Immobilien in Asien, **O**bjekte zum Mieten und Kaufen |

**Merkregel:** ein Kleinbuchstabe, und zwar der Anfangsbuchstabe des Ziels.

**Ausnahme `/o`:** Immobilien fängt mit I an, aber `/i` ist seit dem 22.08.2026 mit
der Interview-Bewerbung belegt und darf nach Regel 2 nicht umgebogen werden.
Deshalb steht `o` für **O**bjekte, so heißt die Seite inhaltlich auch.
Angelegt am 23.08.2026, noch bevor der erste QR-Code damit gerendert wurde.

---

## Warum `/b` auf Beratung zeigt und nicht auf die Bibliothek

In `CLAUDE.md` und in `skills/beschreibung-agent.md` stand bis zum 22.08.2026 die Zeile
„Meine Ratgeber als PDF: freiweitmitnihat.com/b". Das war falsch: `b.html` hat immer
schon auf `/beratung` geleitet, und in bereits veröffentlichten Videos ist `/b` als
Beratungslink gerendert. Ein Umbiegen hätte alte Zuschauer auf die falsche Seite geschickt.

Deshalb wurde `/h` für die Hefte neu angelegt und die falsche Zeile korrigiert.

---

## Freie Buchstaben

`a c d e f j k l m n p q s t u v x y z`

Vorgemerkt für wahrscheinliche Ziele, damit sie niemand anders belegt:

- `q` → Reality-Check (**Q**uiz), `/reality-check`
- `k` → **K**ontakt, `/kontakt`

`m` war bis zum 23.08.2026 für Immobilien vorgemerkt. Seit `/o` vergeben ist,
ist die Vormerkung hinfällig und `m` wieder frei.

---

## Neue Adresse anlegen

1. In dieser Tabelle prüfen, ob der Buchstabe frei ist
2. `homepage/r.html` als Vorlage kopieren, drei Stellen anpassen:
   `meta http-equiv refresh`, `link rel canonical`, beide `href` bzw. `location.replace`
   sowie den Erklärsatz im Body
3. Zeile in die Tabelle oben eintragen, mit Datum
4. Zielseite prüfen: existiert die Datei, lädt die Weiterleitung
5. Erst danach einen QR-Code darauf rendern

---

*Angelegt am 22.08.2026. Grund: Widerspruch zwischen CLAUDE.md und `b.html` fiel beim
Bauen der QR-Animationen für das Stefan-Bramburi-Interview auf.*
