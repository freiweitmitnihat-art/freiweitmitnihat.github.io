#!/usr/bin/env python3
# ============================================================
# GEDANKENSTRICHE aufraeumen
# ------------------------------------------------------------
# Lange Striche (— und –) wirken nach Maschine. Diese Datei
# ersetzt sie nach Kontext durch normale Satzzeichen:
#
#   Zahlenbereich   2–3 Zeilen      ->  2-3 Zeilen
#   vor und/oder    Sprachen — und  ->  Sprachen und
#   vor Kleinwort   97 € — einmalig ->  97 €, einmalig
#   vor Grosswort   Beratung — 60   ->  Beratung: 60
#
# Vorschau (aendert nichts):  python3 tools/gedankenstriche.py
# Wirklich aendern:           python3 tools/gedankenstriche.py --schreiben
# ============================================================
import pathlib, re, sys

BASIS = pathlib.Path(__file__).resolve().parent.parent
SCHREIBEN = '--schreiben' in sys.argv


def aufraeumen(t):
    # Entities zuerst zu Zeichen, damit die Regeln greifen
    t = t.replace('&mdash;', '—').replace('&ndash;', '–')

    # 1. Zahlenbereiche: 2–3, 20–30€, 1.000–2.000
    t = re.sub(r'(\d)\s*[–—]\s*(?=\d)', r'\1-', t)

    # 2. Strich vor Bindewort faellt ganz weg
    t = re.sub(r'\s*[–—]\s+(?=(und|oder|aber|sowie)\b)', ' ', t)

    # 3. Strich direkt nach einem Trennzeichen faellt weg
    t = re.sub(r'([·:,;])\s*[–—]\s*', r'\1 ', t)

    # 4. vor Kleinbuchstabe: Komma
    t = re.sub(r'\s*[–—]\s+(?=[a-zäöüß])', ', ', t)

    # 5. vor Grossbuchstabe oder Zahl: Doppelpunkt,
    #    ausser die Stelle traegt schon einen Doppelpunkt
    def gross(m):
        vor = m.group(1)
        return (vor + ' ') if vor.endswith(':') else (vor + ': ')
    t = re.sub(r'(\S)\s*[–—]\s+(?=[A-ZÄÖÜ0-9])', gross, t)

    # 6. was jetzt noch uebrig ist, wird zum einfachen Bindestrich
    t = t.replace('—', '-').replace('–', '-')
    return t


def main():
    gesamt, dateien = 0, 0
    for f in sorted(list(BASIS.glob('*.html')) + list((BASIS / 'blog').glob('*.html'))):
        t = f.read_text(encoding='utf-8')
        vorher = t.count('—') + t.count('–') + t.count('&mdash;') + t.count('&ndash;')
        if not vorher:
            continue
        neu = aufraeumen(t)
        gesamt += vorher; dateien += 1
        if SCHREIBEN:
            f.write_text(neu, encoding='utf-8')
        else:
            for m in re.finditer(r'.{30}[–—].{30}', t):
                pass
    print('%s: %d Striche in %d Dateien' % ('geaendert' if SCHREIBEN else 'gefunden (Vorschau)', gesamt, dateien))
    if not SCHREIBEN:
        print('Zum Anwenden: python3 tools/gedankenstriche.py --schreiben')


if __name__ == '__main__':
    main()
