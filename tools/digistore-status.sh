#!/bin/bash
# Prueft, welche Digistore24-Produkte oeffentlich kaufbar sind.
# Kein Login noetig: eine nicht genehmigte Produktseite antwortet mit
# "Das Produkt wurde noch nicht genehmigt."
# Aufruf: ./homepage/tools/digistore-status.sh

produkte=(
  "724576|Welches Visum passt zu dir"
  "724580|Wohnung finden in Thailand und Vietnam"
  "724581|Krankenversicherung im Ausland ab 55"
  "724582|Deutschland abwickeln"
  "724584|Plan B: Rueckkehr"
  "724588|Die 7 groessten Fehler beim Auswandern"
  "724589|Die komplette Bibliothek (Buendel)"
)

offen=0
echo "Digistore24-Status  ($(date '+%d.%m.%Y %H:%M'))"
echo "---------------------------------------------------------------"

for eintrag in "${produkte[@]}"; do
  id="${eintrag%%|*}"
  name="${eintrag#*|}"
  seite=$(curl -sL --max-time 20 "https://www.checkout-ds24.com/product/$id")

  if echo "$seite" | grep -q "noch nicht genehmigt"; then
    echo "WARTET   $id  $name"
    offen=$((offen+1))
  elif echo "$seite" | grep -q "nicht verfügbar"; then
    grund=$(echo "$seite" | tr '\n' ' ' | sed -n 's/.*nicht verfügbar:[^A-Za-zÄÖÜ]*\([^<]*\).*/\1/p' | cut -c1-70)
    echo "GESPERRT $id  $name  ($grund)"
    offen=$((offen+1))
  else
    flach=$(printf '%s' "$seite" | tr '\n' ' ' | LC_ALL=C perl -pe 's/\xc2\xa0/ /g' | tr -s ' ')
    preis=$(echo "$flach" | grep -o '[0-9]\{1,4\},[0-9]\{2\} €' | head -1)
    mwst=$(echo "$flach" | grep -o 'MwSt ([0-9]\+%)' | head -1)
    echo "KAUFBAR  $id  $name  ${preis:-Preis?}  ${mwst:-MwSt?}"
  fi
done

echo "---------------------------------------------------------------"
if [ "$offen" -eq 0 ]; then
  echo "Alle sieben Produkte sind kaufbar."
  echo "Jetzt faellig: Kauflinks in homepage/bibliothek.html eintragen,"
  echo "den Hinweisbalken entfernen und Kaufhilfe-Screenshot 3 neu aufnehmen."
else
  echo "$offen Produkt(e) noch nicht freigegeben. Die Kauflinks bleiben draussen,"
  echo "sonst landen Kaeufer auf einer Fehlerseite von Digistore."
fi
