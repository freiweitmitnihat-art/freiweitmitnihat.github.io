#!/usr/bin/env python3
# ============================================================
# STATISTIK-BERICHT · holt die Zahlen aus Umami
# ------------------------------------------------------------
# Zeigt auf einen Blick, was auf der Website passiert ist:
# Besucher, meistgelesene Seiten, Herkunft, wichtige Klicks.
#
#   python3 tools/statistik-bericht.py           (letzte 7 Tage)
#   python3 tools/statistik-bericht.py 30        (letzte 30 Tage)
#   python3 tools/statistik-bericht.py 1         (gestern und heute)
#
# Der Schluessel steht NICHT in dieser Datei. Er wird gelesen aus
#   1. der Umgebungsvariablen UMAMI_API_KEY, sonst
#   2. dem macOS-Schluesselbund unter dem Namen UMAMI_API_KEY
#
# Einmalig hinterlegen (fragt interaktiv, landet nicht in der Historie):
#   security add-generic-password -U -a "$USER" -s UMAMI_API_KEY -w
# ============================================================
import json, os, subprocess, sys, time, urllib.request, urllib.error

WEBSITE = 'd7f43baf-1cee-4bbb-aae6-74d680202c71'
REGIONEN = ['https://api.umami.is/v1/eu', 'https://api.umami.is/v1']


def schluessel():
    k = os.environ.get('UMAMI_API_KEY')
    if k:
        return k.strip()
    try:
        aus = subprocess.run(['security', 'find-generic-password', '-a', os.environ.get('USER', ''),
                              '-s', 'UMAMI_API_KEY', '-w'], capture_output=True, text=True, timeout=10)
        if aus.returncode == 0:
            return aus.stdout.strip()
    except Exception:
        pass
    return None


def hole(basis, pfad, key, params):
    frage = '&'.join('%s=%s' % (a, b) for a, b in params.items())
    anfrage = urllib.request.Request('%s%s?%s' % (basis, pfad, frage),
                                     headers={'x-umami-api-key': key, 'Accept': 'application/json'})
    with urllib.request.urlopen(anfrage, timeout=20) as a:
        return json.loads(a.read().decode('utf-8'))


def zeitraum(tage):
    jetzt = int(time.time() * 1000)
    return {'startAt': jetzt - tage * 86400000, 'endAt': jetzt}


def tabelle(titel, zeilen, breite=44):
    print('\n%s' % titel)
    print('-' * (breite + 10))
    if not zeilen:
        print('  (noch nichts)')
        return
    for z in zeilen:
        name = str(z.get('x') or '(direkt)')[:breite]
        print('  %-*s %6d' % (breite, name, z.get('y', 0)))


def main():
    tage = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7
    key = schluessel()
    if not key:
        print('Kein Umami-Schluessel gefunden.')
        print('In Umami unter Settings -> API Keys einen Schluessel anlegen, dann:')
        print('  security add-generic-password -U -a "$USER" -s UMAMI_API_KEY -w')
        return 1

    z = zeitraum(tage)
    basis_ok = None
    for basis in REGIONEN:
        try:
            werte = hole(basis, '/websites/%s/stats' % WEBSITE, key, z)
            basis_ok = basis
            break
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                print('Schluessel wird abgelehnt (HTTP %d). Stimmt der API-Key?' % e.code)
                return 1
            continue
        except Exception:
            continue
    if not basis_ok:
        print('Keine Verbindung zur Umami-API.')
        return 1

    def wert(feld):
        v = werte.get(feld, {})
        return v.get('value', 0) if isinstance(v, dict) else v

    print('=' * 54)
    print('FREIWEIT MIT NIHAT · letzte %d Tage' % tage)
    print('=' * 54)
    print('  Besucher        %6d' % wert('visitors'))
    print('  Seitenaufrufe   %6d' % wert('pageviews'))
    print('  Besuche         %6d' % wert('visits'))
    absprung = wert('bounces')
    besuche = wert('visits') or 1
    print('  Absprungquote   %5d %%' % round(absprung * 100 / besuche))
    dauer = wert('totaltime')
    print('  Zeit je Besuch  %5d Sek.' % (dauer / besuche if besuche else 0))

    for feld, titel in [('url', 'MEISTGELESENE SEITEN'), ('referrer', 'WOHER DIE LEUTE KOMMEN'),
                        ('country', 'LAENDER'), ('device', 'GERAETE')]:
        try:
            p = dict(z); p['type'] = feld; p['limit'] = 10
            tabelle(titel, hole(basis_ok, '/websites/%s/metrics' % WEBSITE, key, p))
        except Exception as e:
            print('\n%s: nicht abrufbar (%s)' % (titel, e))

    try:
        p = dict(z); p['type'] = 'event'; p['limit'] = 20
        tabelle('WICHTIGE KLICKS UND ANMELDUNGEN', hole(basis_ok, '/websites/%s/metrics' % WEBSITE, key, p))
    except Exception as e:
        print('\nEreignisse: nicht abrufbar (%s)' % e)

    print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
