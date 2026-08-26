#!/usr/bin/env python3
"""Holt die Zahlen der Google Search Console und schreibt einen lesbaren Bericht.

Braucht keine Chrome-Extension und keinen Login im Browser. Es meldet sich mit
einem Dienstkonto an, dessen Schluessel im macOS-Schluesselbund liegt.

Einrichtung steht in homepage/README-search-console.md.

Benutzung:
    python3 tools/search-console.py                 # letzte 28 Tage, alles
    python3 tools/search-console.py --tage 7
    python3 tools/search-console.py --was anfragen
    python3 tools/search-console.py --seiten-von /blog/
"""

import argparse
import base64
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile

import requests

SCHLUESSELBUND_DIENST = "GSC_SERVICE_ACCOUNT"
BEREICH = "https://www.googleapis.com/auth/webmasters.readonly"
TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://www.googleapis.com/webmasters/v3"
DOMAIN = "freiweitmitnihat.com"


def raus(text):
    print(text, file=sys.stderr)
    sys.exit(1)


def b64(rohdaten):
    return base64.urlsafe_b64encode(rohdaten).rstrip(b"=")


def schluessel_laden():
    """Dienstkonto-JSON laden. Erst der uebliche Ort, dann Ausweichwege."""
    orte = []
    aus_umgebung = os.environ.get("GSC_SERVICE_ACCOUNT_DATEI")
    if aus_umgebung:
        orte.append(aus_umgebung)
    orte.append(os.path.expanduser("~/.config/freiweit/search-console.json"))

    for ort in orte:
        if os.path.exists(ort):
            with open(ort, encoding="utf-8") as f:
                return json.load(f)

    # Wer den Schluessel frueher von Hand in den Schluesselbund gelegt hat.
    versuch = subprocess.run(
        ["security", "find-generic-password", "-a", os.environ.get("USER", ""),
         "-s", SCHLUESSELBUND_DIENST, "-w"],
        capture_output=True, text=True)
    if versuch.returncode == 0 and versuch.stdout.strip().startswith("{"):
        return json.loads(versuch.stdout.strip())

    raus("Kein Dienstkonto-Schluessel gefunden.\n"
         "Erwartet wird er hier:\n"
         "  ~/.config/freiweit/search-console.json\n\n"
         "Einrichten mit:\n"
         "  ./tools/search-console-einrichten.sh ~/Downloads/deine-datei.json\n\n"
         "Die ganze Anleitung steht in homepage/README-search-console.md.")


def zugangstoken(konto):
    """Baut ein signiertes JWT und tauscht es gegen ein Zugangstoken."""
    jetzt = int(dt.datetime.now(dt.timezone.utc).timestamp())
    kopf = {"alg": "RS256", "typ": "JWT"}
    inhalt = {
        "iss": konto["client_email"],
        "scope": BEREICH,
        "aud": TOKEN_URL,
        "iat": jetzt,
        "exp": jetzt + 3600,
    }
    zu_signieren = (b64(json.dumps(kopf).encode()) + b"." +
                    b64(json.dumps(inhalt).encode()))

    # openssl braucht den Schluessel als Datei. Sie lebt nur Millisekunden,
    # liegt in einem privaten Verzeichnis und wird sicher wieder geloescht.
    ordner = tempfile.mkdtemp()
    pfad = os.path.join(ordner, "dienstkonto.pem")
    try:
        with open(os.open(pfad, os.O_WRONLY | os.O_CREAT, 0o600), "w") as f:
            f.write(konto["private_key"])
        signiert = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", pfad],
            input=zu_signieren, capture_output=True)
    finally:
        if os.path.exists(pfad):
            os.remove(pfad)
        os.rmdir(ordner)

    if signiert.returncode != 0:
        raus("openssl konnte nicht signieren:\n" + signiert.stderr.decode())

    jwt = zu_signieren + b"." + b64(signiert.stdout)
    antwort = requests.post(TOKEN_URL, data={
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt.decode(),
    }, timeout=30)

    if antwort.status_code != 200:
        raus("Anmeldung abgelehnt (HTTP %s):\n%s" % (antwort.status_code, antwort.text))
    return antwort.json()["access_token"]


def property_finden(token):
    """Sucht die passende Property. URL-Praefix zuerst, dann Domain-Property."""
    antwort = requests.get(API + "/sites", timeout=30,
                           headers={"Authorization": "Bearer " + token})
    if antwort.status_code != 200:
        raus("Konnte die Property-Liste nicht laden (HTTP %s):\n%s"
             % (antwort.status_code, antwort.text))

    eintraege = antwort.json().get("siteEntry", [])
    if not eintraege:
        raus("Das Dienstkonto sieht keine einzige Property.\n"
             "Fehlt noch der letzte Schritt: In der Search Console unter\n"
             "Einstellungen, Nutzer und Berechtigungen die Adresse des\n"
             "Dienstkontos als Nutzer hinzufuegen.")

    passend = [e["siteUrl"] for e in eintraege if DOMAIN in e["siteUrl"]]
    for adresse in passend:
        if adresse.startswith("http"):
            return adresse
    if passend:
        return passend[0]

    raus("Keine Property fuer %s dabei. Gefunden wurde nur:\n  %s"
         % (DOMAIN, "\n  ".join(e["siteUrl"] for e in eintraege)))


def abfragen(token, adresse, von, bis, dimension, grenze=25, filter_pfad=None):
    anfrage = {
        "startDate": von,
        "endDate": bis,
        "rowLimit": grenze,
    }
    if dimension:
        anfrage["dimensions"] = [dimension]
    if filter_pfad:
        anfrage["dimensionFilterGroups"] = [{"filters": [
            {"dimension": "page", "operator": "contains", "expression": filter_pfad}]}]

    ziel = "%s/sites/%s/searchAnalytics/query" % (API, requests.utils.quote(adresse, safe=""))
    antwort = requests.post(ziel, json=anfrage, timeout=60,
                            headers={"Authorization": "Bearer " + token})
    if antwort.status_code != 200:
        raus("Abfrage fehlgeschlagen (HTTP %s):\n%s" % (antwort.status_code, antwort.text))
    return antwort.json().get("rows", [])


def kuerzen(text, breite):
    return text if len(text) <= breite else text[:breite - 1] + "…"


def tabelle(ueberschrift, zeilen, spaltenname, breite=52):
    print("\n" + ueberschrift)
    print("=" * (breite + 34))
    if not zeilen:
        print("  noch keine Daten")
        return
    print("  %-*s %8s %7s %6s %6s" % (breite, spaltenname, "Impress.", "Klicks", "CTR", "Pos."))
    print("  " + "-" * (breite + 32))
    for z in zeilen:
        name = z.get("keys", ["gesamt"])[0]
        if name.startswith("https://" + DOMAIN):
            name = name[len("https://" + DOMAIN):] or "/"
        print("  %-*s %8d %7d %5.1f%% %6.1f" % (
            breite, kuerzen(name, breite),
            z["impressions"], z["clicks"], z["ctr"] * 100, z["position"]))


def hauptteil():
    p = argparse.ArgumentParser(description="Zahlen aus der Google Search Console")
    p.add_argument("--tage", type=int, default=28, help="Zeitraum, Vorgabe 28")
    p.add_argument("--was", default="alles",
                   choices=["alles", "anfragen", "seiten", "laender", "geraete"])
    p.add_argument("--anzahl", type=int, default=25, help="Zeilen je Tabelle")
    p.add_argument("--seiten-von", default=None,
                   help="nur Seiten, deren Adresse diesen Teil enthaelt, z. B. /blog/")
    a = p.parse_args()

    # Google liefert die letzten zwei Tage noch nicht vollstaendig.
    bis = dt.date.today() - dt.timedelta(days=2)
    von = bis - dt.timedelta(days=a.tage)

    konto = schluessel_laden()
    token = zugangstoken(konto)
    adresse = property_finden(token)

    print("Search Console: %s" % adresse)
    print("Zeitraum: %s bis %s (%d Tage)" % (von, bis, a.tage))
    if a.seiten_von:
        print("Eingegrenzt auf Adressen mit: %s" % a.seiten_von)

    gesamt = abfragen(token, adresse, str(von), str(bis), None,
                      filter_pfad=a.seiten_von)
    if gesamt:
        g = gesamt[0]
        print("\nGesamt: %d Impressionen, %d Klicks, %.1f%% CTR, "
              "Durchschnittsposition %.1f"
              % (g["impressions"], g["clicks"], g["ctr"] * 100, g["position"]))
    else:
        print("\nGesamt: noch keine Daten in diesem Zeitraum.")
        return

    wahl = a.was
    if wahl in ("alles", "anfragen"):
        tabelle("Wonach die Leute gesucht haben",
                abfragen(token, adresse, str(von), str(bis), "query",
                         a.anzahl, a.seiten_von), "Suchanfrage")
    if wahl in ("alles", "seiten"):
        tabelle("Welche Seiten auftauchen",
                abfragen(token, adresse, str(von), str(bis), "page",
                         a.anzahl, a.seiten_von), "Seite")
    if wahl in ("alles", "laender"):
        tabelle("Aus welchen Laendern",
                abfragen(token, adresse, str(von), str(bis), "country",
                         10, a.seiten_von), "Land", breite=20)
    if wahl in ("alles", "geraete"):
        tabelle("Womit gesucht wird",
                abfragen(token, adresse, str(von), str(bis), "device",
                         10, a.seiten_von), "Geraet", breite=20)

    print("\nHinweis: Die letzten zwei Tage laesst Google bewusst weg,")
    print("die Zahlen dort sind noch unvollstaendig.")


if __name__ == "__main__":
    hauptteil()
