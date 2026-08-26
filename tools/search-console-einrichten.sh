#!/bin/bash
# Legt den Dienstkonto-Schluessel der Search Console dort ab, wo das
# Leseskript ihn findet.
#
# Aufruf:  ./tools/search-console-einrichten.sh ~/Downloads/name-der-datei.json
#
# Warum eine Datei und nicht der Schluesselbund: security schneidet ueber die
# Standardeingabe bei 128 Zeichen ab, der Schluessel ist rund 2400 Zeichen lang.
# Als Kommandozeilen-Argument stuende er kurz in der Prozessliste. Deshalb eine
# Datei, die nur Nihat lesen darf, ausserhalb des Projektordners und damit
# ausserhalb von Git.

set -euo pipefail

ZIEL_ORDNER="$HOME/.config/freiweit"
ZIEL="$ZIEL_ORDNER/search-console.json"
DATEI="${1:-}"

if [ -z "$DATEI" ]; then
  echo "So geht es:  $0 ~/Downloads/deine-datei.json"
  echo
  echo "Die Datei ist die, die Google dir beim Erstellen des Dienstkonto-"
  echo "Schluessels heruntergeladen hat. Sie endet auf .json."
  exit 1
fi

if [ ! -f "$DATEI" ]; then
  echo "Diese Datei gibt es nicht: $DATEI"
  exit 1
fi

ADRESSE=$(python3 -c '
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    sys.exit("Das ist keine lesbare JSON-Datei.")
if d.get("type") != "service_account" or "private_key" not in d:
    sys.exit("Das sieht nicht nach einem Dienstkonto-Schluessel aus.")
print(d["client_email"])
' "$DATEI")

echo "Gefundenes Dienstkonto: $ADRESSE"

mkdir -p "$ZIEL_ORDNER"
chmod 700 "$ZIEL_ORDNER"
# Erst die Rechte setzen, dann den Inhalt hineinschreiben. Andersherum waere
# der Schluessel einen Moment lang fuer alle lesbar.
umask 177
cat "$DATEI" > "$ZIEL"
chmod 600 "$ZIEL"

echo "Abgelegt unter $ZIEL, lesbar nur fuer dich."

rm -P "$DATEI"
echo "Die heruntergeladene Datei ist sicher geloescht."
echo
echo "Falls noch nicht geschehen, fehlt jetzt nur noch ein Schritt:"
echo "In der Search Console unter Einstellungen, Nutzer und Berechtigungen"
echo "diese Adresse als Nutzer hinzufuegen:"
echo
echo "    $ADRESSE"
echo
echo "Danach testen mit:  python3 tools/search-console.py --tage 7"
