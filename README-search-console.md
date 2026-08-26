# Search-Console-Zahlen ohne Browser

Stand: 26.08.2026. Bis jetzt kam Claude nur über die Chrome-Extension an die
Zahlen der Google Search Console. Wenn die nicht verbunden ist, ging gar nichts.
Der Weg hier braucht keinen Browser, keinen Login und keine Extension. Einmal
eingerichtet, läuft er für immer.

---

## Was du einmal tun musst

Das kann nur Nihat machen, weil überall der Google-Login dahintersteht.
Dauert etwa zehn Minuten.

### 1. Ein Google-Cloud-Projekt anlegen

Auf https://console.cloud.google.com oben auf die Projektauswahl klicken,
dann **Neues Projekt**. Name zum Beispiel `freiweit-search-console`.
Erstellen, warten, dann oben auf das neue Projekt umschalten.

### 2. Die Search Console API einschalten

Im Menü links **APIs und Dienste**, dann **Bibliothek**. Oben nach
`Google Search Console API` suchen, draufklicken, **Aktivieren**.

### 3. Ein Dienstkonto anlegen

**APIs und Dienste**, dann **Anmeldedaten**. Oben **Anmeldedaten erstellen**,
dann **Dienstkonto**.

- Name: `claude-leser`
- Beschreibung: `liest die Search-Console-Zahlen`
- **Erstellen und fortfahren**
- Rolle: keine nötig, einfach **Weiter**
- **Fertig**

### 4. Den Schlüssel herunterladen

In der Liste auf das neue Dienstkonto klicken, Reiter **Schlüssel**, dann
**Schlüssel hinzufügen**, **Neuen Schlüssel erstellen**, Typ **JSON**,
**Erstellen**. Die Datei landet in deinem Download-Ordner.

**Die Datei ist ein Schlüssel. Nicht per Mail verschicken, nicht ins Projekt
legen, nicht auf GitHub.** Das nächste Kommando räumt sie selbst weg.

### 5. Die Adresse des Dienstkontos freigeben

Auf der Seite steht eine Adresse, die auf `.iam.gserviceaccount.com` endet.
Kopieren. Dann auf https://search.google.com/search-console:

**Einstellungen**, dann **Nutzer und Berechtigungen**, dann **Nutzer
hinzufügen**. Adresse einfügen, Berechtigung **Eingeschränkt** genügt (nur
lesen), **Hinzufügen**.

### 6. Den Schlüssel ablegen

Im Terminal, im Ordner `homepage`:

```bash
./tools/search-console-einrichten.sh ~/Downloads/DEINE-DATEI.json
```

Das Skript prüft die Datei, legt sie unter `~/.config/freiweit/search-console.json`
ab, wo nur du sie lesen darfst, und löscht das Original sicher. Es sagt dir zum
Schluss noch einmal die Adresse für Schritt 5, falls du den übersprungen hast.

Fertig. Ab jetzt kommt Claude jederzeit an die Zahlen.

---

## Wie du danach die Zahlen holst

Alles im Ordner `homepage`:

```bash
python3 tools/search-console.py
```

Das gibt die letzten 28 Tage: Gesamtzahlen, wonach die Leute gesucht haben,
welche Seiten auftauchen, aus welchen Ländern und mit welchem Gerät.

Weitere Möglichkeiten:

| Kommando | Was es zeigt |
|---|---|
| `python3 tools/search-console.py --tage 7` | nur die letzte Woche |
| `python3 tools/search-console.py --was anfragen` | nur die Suchanfragen |
| `python3 tools/search-console.py --was seiten` | nur die Seiten |
| `python3 tools/search-console.py --seiten-von /blog/` | nur die Blogartikel |
| `python3 tools/search-console.py --anzahl 50` | längere Listen |

---

## Wie du die Zahlen liest

- **Impressionen**: wie oft eine Seite in den Ergebnissen auftauchte.
- **Klicks**: wie oft jemand tatsächlich draufging.
- **CTR**: Klicks geteilt durch Impressionen. Unter 2 Prozent bei guter
  Position heißt meistens, dass Titel oder Beschreibung nicht ziehen.
- **Position**: der Durchschnittsplatz. Alles über 10 ist Seite zwei und
  bringt praktisch nichts.

**Das lohnendste Muster:** viele Impressionen, kaum Klicks, Position unter 10.
Da steht die Seite schon gut, nur der Titel überzeugt nicht. Das ist eine
Textänderung von fünf Minuten und wirkt sofort.

---

## Wenn etwas nicht klappt

| Meldung | Was los ist |
|---|---|
| `Kein Dienstkonto-Schluessel gefunden` | Schritt 6 fehlt noch |
| `Das Dienstkonto sieht keine einzige Property` | Schritt 5 fehlt noch, oder die Freigabe ist noch nicht durch |
| `invalid_grant: account not found` | der Schlüssel gehört zu einem gelöschten Dienstkonto, in Schritt 4 einen neuen erstellen |
| `Keine Property fuer freiweitmitnihat.com dabei` | in der Search Console ist eine andere Property freigegeben als erwartet |
| `Gesamt: noch keine Daten` | für diesen Zeitraum liegt wirklich nichts vor, mit `--tage 90` gegenprüfen |

Google lässt die letzten zwei Tage bewusst weg, deren Zahlen sind noch
unvollständig. Das Skript rechnet das schon ein.

---

## Was das Ganze technisch tut

Das Dienstkonto meldet sich mit einem signierten Token an, statt mit
Nutzername und Passwort. Die Signatur macht `openssl`, das auf jedem Mac
vorhanden ist. Es gibt deshalb keine zusätzlichen Bibliotheken zu installieren,
die irgendwann kaputtgehen könnten. Das Dienstkonto darf nur lesen und kommt an
nichts anderes im Google-Konto heran.
