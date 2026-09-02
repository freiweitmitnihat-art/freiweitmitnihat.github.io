# Newsletter-Anbindung Brevo

**Status 20.08.2026: eingerichtet und getestet. Anmeldungen laufen.**

| Was | Wert |
|---|---|
| Liste | `Newsletter` (ID 3) |
| Formular | `Website Anmeldung` (gehostet/eingebettet) |
| Bestaetigung | Double-Opt-in, Standard-Vorlage |
| Weiterleitung nach Bestaetigung | `https://freiweitmitnihat.com/danke` |
| Sendeziel | steht in `js/brevo.js`, Variable `BREVO_ENDPOINT` |
| Captcha | keins aktiv (Honeypot `email_address_check` wird mitgeschickt) |

Getestet am 20.08.2026: POST liefert HTTP 200 und die eigene Erfolgsmeldung zurueck.
Der Kontakt erscheint erst nach Klick auf den Bestaetigungslink in der Liste, das ist
bei Double-Opt-in so gewollt.

## Erledigt: VORNAME, QUELLE, MAGNET kommen an (geprueft 02.09.2026)

`VORNAME`, `QUELLE` und `MAGNET` stehen inzwischen im Brevo-Formular `Website Anmeldung`
und werden korrekt uebernommen. Live am Kontakt "Stefan" geprueft: VORNAME "Stefan",
QUELLE "Monatsrechnung-QR", MAGNET "Monatsrechnung", alle drei korrekt befuellt.
Am Code aendert sich nichts, das Formular nimmt die Felder wie vorgesehen an.

---

## 1 · Die einzige Stelle im Code

Datei: `js/brevo.js`, Zeile 18.

```js
var BREVO_ENDPOINT = 'TODO-BREVO-FORM-ID';
```

Solange dort der Platzhalter steht, geht jede Anmeldung über Web3Forms an
`freiweit.mit.nihat@gmail.com`. Nichts geht verloren, aber nichts landet automatisch in Brevo.

Diese Seiten hängen daran und brauchen keine weitere Änderung:

| Seite | Formular | MAGNET-Wert |
|---|---|---|
| `rechnung.html` | Lead Magnet „Die echte Monatsrechnung" | `Monatsrechnung` |
| `reality-check.html` | Auswertung anfordern | `Reality-Check` |
| `index.html` | Newsletter-Box unten | `Newsletter` |

---

## 2 · In Brevo vorbereiten (einmalig, ca. 20 Minuten)

### 2.1 Attribute anlegen
Kontakte → Einstellungen → Kontakt-Attribute → „Attribut hinzufügen":

| Name | Typ | Wofür |
|---|---|---|
| `VORNAME` | Text | persönliche Anrede in den Mails |
| `QUELLE` | Text | woher die Anmeldung kam, z. B. `Monatsrechnung-QR` |
| `MAGNET` | Text | welches Thema, z. B. `Monatsrechnung` |

`VORNAME` gibt es bei Brevo oft schon als `VORNAME` oder `FIRSTNAME`.
**Wenn dort `FIRSTNAME` steht:** entweder umbenennen oder in `js/brevo.js`
`fd.append('VORNAME', vorname)` in `fd.append('FIRSTNAME', vorname)` ändern.

### 2.2 Listen anlegen
Kontakte → Listen:

- **Newsletter** (Hauptliste, hier landet jeder)
- **Monatsrechnung** (alle, die den Guide angefordert haben)
- **Reality-Check** (alle aus dem Test)

Grund für getrennte Listen: du siehst sofort, welcher Einstieg zieht,
und kannst später gezielt anschreiben.

### 2.3 Formular anlegen
Kontakte → Formulare → „Neues Formular":

1. Felder ins Formular ziehen: `EMAIL` (Pflicht), `VORNAME`, `QUELLE`, `MAGNET`.
   `QUELLE` und `MAGNET` auf **versteckt** stellen, die füllt die Website automatisch.
2. Einwilligungs-Checkbox aktivieren, Text kann kurz sein, die lange Fassung steht schon
   auf der Website.
3. Liste auswählen: **Newsletter**.
4. **Double-Opt-in einschalten** (Reiter „Einstellungen" → „Bestätigungs-E-Mail").
   Pflicht für die DSGVO und schützt die Zustellrate.
5. Bestätigungsmail: Absender `kontakt@freiweitmitnihat.com`, Text aus
   `../outputs/_bausteine/brevo-mails.md`, Abschnitt „DOI".
6. Nach dem Speichern zeigt Brevo den Einbettungscode. Darin steht eine Zeile wie:

```html
<form action="https://XXXXX.sibforms.com/serve/MUIFABc123..." method="POST">
```

Nur diese **action-Adresse** kopieren.

### 2.4 Adresse eintragen

```js
var BREVO_ENDPOINT = 'https://XXXXX.sibforms.com/serve/MUIFABc123...';
```

Speichern, hochladen, fertig.

---

## 3 · PDF-Versand automatisieren

Das PDF liegt jetzt unter `pdfs/die-echte-monatsrechnung.pdf`, also live erreichbar unter:

```
https://freiweitmitnihat.com/pdfs/die-echte-monatsrechnung.pdf
```

Automations → „Automation erstellen" → Auslöser **„Kontakt tritt einer Liste bei"**
→ Liste `Newsletter` → Bedingung `MAGNET ist Monatsrechnung` → Aktion „E-Mail senden".

Der fertige Mail-Text steht in `../outputs/_bausteine/brevo-mails.md`, Abschnitt „Mail 1".

Danach dieselbe Automation als Willkommensstrecke verlängern:
Mail 2 nach 2 Tagen, Mail 3 nach 5 Tagen, Mail 4 nach 9 Tagen. Texte liegen alle in derselben Datei.

---

## 4 · Absenderadresse und Zustellbarkeit

- Absender immer `kontakt@freiweitmitnihat.com`, Antwortadresse `freiweit.mit.nihat@gmail.com`.
- Cloudflare Email Routing leitet Antworten bereits ins Gmail-Postfach.
- In Brevo einmal prüfen: Domain-Authentifizierung (DKIM, DMARC) auf grün.
- Abmeldelink ist bei Brevo automatisch in jeder Mail, nicht entfernen.

---

## 5 · Test-Checkliste nach dem Eintragen

- [ ] `rechnung.html` im Browser öffnen, mit eigener Adresse anmelden
- [ ] Bestätigungsmail kommt an, Link führt zurück auf die Website
- [ ] Kontakt taucht in Brevo auf, mit `QUELLE` = `Monatsrechnung-Website`
- [ ] `rechnung.html?via=qr` testen, `QUELLE` muss `Monatsrechnung-QR` sein
- [ ] PDF-Mail kommt automatisch, Link im PDF-Button funktioniert
- [ ] `reality-check.html` testen, Info-Mail mit Auswertung kommt zusätzlich ins Gmail-Postfach
- [ ] Newsletter-Box auf der Startseite testen
- [ ] Auf dem Handy gegenprüfen, die Zielgruppe liest überwiegend mobil

---

## 6 · Wenn du lieber vollen Zugriff willst (Variante B, optional)

Statt des Brevo-Formulars kann ein kleiner Cloudflare Worker die Anmeldung annehmen und
per API an Brevo geben. Vorteil: echte Fehlermeldungen auf der Seite, freie Feldwahl,
kein Brevo-Formular-Layout. Nachteil: ein Bauteil mehr und ein API-Schlüssel, der in
Cloudflare als Secret liegt.

Der Code dafür liegt fertig in `../scripts/brevo-worker.js`.
`js/brevo.js` erkennt automatisch, welche der beiden Varianten eingetragen ist.
