#!/usr/bin/env python3
# ============================================================
# "KURZ GESAGT" oben in die Ratgeber-Artikel
# ------------------------------------------------------------
# Warum: Google beantwortet immer mehr Fragen direkt in der
# KI-Uebersicht, und ChatGPT, Perplexity und Co. lesen dabei den
# SICHTBAREN Text einer Seite, nicht die Strukturdaten. Zitiert
# wird, wer die Antwort oben hinschreibt statt sie in einen
# langen Fliesstext zu vergraben. Seiten, die zitiert werden,
# bekommen messbar mehr Klicks als Seiten auf derselben
# Trefferliste, die nicht genannt werden.
#
# Nebeneffekt, der genauso wichtig ist: Die Zielgruppe ist 55+
# und ein Drittel schaut auf dem Fernseher. Die wollen die
# Antwort auch nicht erst suchen.
#
# Jeder Kasten steht hier im Klartext und ist aus dem jeweiligen
# Artikel abgeleitet, nicht erfunden. Wer eine Zahl aendert,
# aendert sie hier UND im Artikel.
#
# Vorschau (aendert nichts):  python3 tools/kurz-gesagt.py
# Wirklich schreiben:         python3 tools/kurz-gesagt.py --schreiben
# ============================================================
import pathlib, re, sys

BASIS = pathlib.Path(__file__).resolve().parent.parent
SCHREIBEN = '--schreiben' in sys.argv

KAESTEN = {
 'lebenshaltungskosten-thailand': [
   'Realistisch sind <strong>480 bis 1.200 € im Monat</strong>, je nach Lebensstil. Nicht 300 €, wie manche behaupten, und nicht 3.000 €, wie viele befürchten.',
   'Sparsam gerechnet kommst du auf rund <strong>380 €</strong>, komfortabel auf rund <strong>910 €</strong>. Meine ehrliche Mitte liegt bei etwa <strong>600 €</strong>.',
   'Größter Posten ist die Wohnung: <strong>200 € einfach, 400 € komfortabel</strong>, mit Pool und Gym sind 300 € machbar.',
   'Am häufigsten vergessen: Krankenversicherung, Visum-Verlängerungen und einmalig <strong>300 bis 500 €</strong> für Kaution und Grundausstattung.',
 ],
 'lebenshaltungskosten-vietnam': [
   'In Da Nang reichen sparsam rund <strong>323 € im Monat</strong>, komfortabel rund <strong>825 €</strong>. Realistisch sind etwa <strong>550 €</strong>.',
   'Vietnam ist günstiger als Thailand, aber nicht so günstig wie oft erzählt wird.',
   'Wohnen kostet <strong>180 bis 380 €</strong>, mit Meerblick geht es ab 250 € los. Eine Pho kostet 1,50 €, ein Banh Mi 0,80 €.',
   'Die Sprachbarriere ist höher als in Thailand. Für Behördengänge und Verträge brauchst du Übersetzung oder Hilfe.',
 ],
 'pattaya-kosten-2026': [
   'Meine echte Monatsrechnung für Pattaya: <strong>rund 1.100 €</strong>, davon 480 € Miete und 320 € Essen und Ausgehen.',
   'Für ein gutes 1-Zimmer-Condo im Zentrum rechne mit <strong>12.000 bis 15.000 Baht</strong>, also 320 bis 400 €.',
   'Immer direkt mit dem Vermieter verhandeln, <strong>10 bis 20 % Nachlass</strong> sind oft drin. Kurzzeit über Airbnb ist immer teurer als ein Dreimonatsvertrag.',
   'Streetfood hält die Essenskosten unten: Pad Thai 50 bis 70 Baht, also 1,30 bis 1,90 €.',
 ],
 'thailand-e-visum': [
   'Als Deutscher, Österreicher oder Schweizer kommst du <strong>30 Tage visumfrei</strong> nach Thailand.',
   'Das Touristenvisum (TR) gilt <strong>60 Tage</strong> und lässt sich vor Ort verlängern.',
   'Für einen längeren Aufenthalt gibt es das <strong>LTR-Visum mit 10 Jahren Laufzeit</strong> und das DTV.',
   'Beantragen nur über die offizielle Seite. Alles andere kostet Aufschlag für nichts.',
 ],
 'vietnam-e-visum': [
   'Deutsche Staatsbürger dürfen <strong>bis 45 Tage visumfrei</strong> nach Vietnam. Darunter brauchst du gar kein Visum.',
   'Das E-Visum gilt <strong>90 Tage</strong>, kostet <strong>25 US-Dollar</strong> für einfache Einreise und ist in etwa <strong>3 Werktagen</strong> da.',
   'Du brauchst einen Reisepass, der bei Einreise noch <strong>6 Monate gültig</strong> ist, und ein digitales Passfoto (JPG, quadratisch, heller Hintergrund, maximal 1 MB).',
   'Nur die offizielle Regierungsseite nutzen. Die Kopien im Netz verlangen ein Vielfaches.',
 ],
 'thailand-tdac': [
   'Die Thailand Digital Arrival Card ist <strong>seit 2024 Pflicht</strong> und ersetzt das alte TM6-Papierformular vollständig.',
   'Ausfüllen kannst du sie <strong>bis zu 3 Tage vor Ankunft</strong>, online und <strong>kostenlos</strong>. Offiziell werden keine Gebühren erhoben.',
   'Am Flughafen zeigst du den <strong>QR-Code</strong> auf dem Handy oder ausgedruckt vor.',
   'Sie gilt für alle Einreisearten: Flug, Schiff und Landgrenze.',
 ],
 'sim-karte-thailand': [
   'Für Langzeitreisende und Auswanderer ist <strong>True Move H</strong> (früher DTAC) die beste Wahl, ab <strong>299 Baht, rund 8 €</strong> im Monat.',
   'AIS hat die leicht bessere Abdeckung ab 350 Baht (rund 10 €), für 99 % der Fälle reicht True Move H.',
   'Für kurze Reisen bis zwei Wochen genügt die <strong>Tourist-SIM</strong>: 299 Baht für 8 Tage mit 15 GB.',
   'Kaufen direkt nach dem Zoll am Flughafen oder in jedem 7-Eleven. Reisepass mitbringen, in 10 Minuten bist du online.',
 ],
 'sim-karte-vietnam': [
   '<strong>Viettel</strong> hat die beste Abdeckung und ist günstig. Damit machst du nichts falsch.',
   'Eine Basis-SIM kostet <strong>50.000 bis 80.000 VND</strong>, also etwa 2 bis 3 €.',
   '<strong>30 GB für 30 Tage</strong> liegen bei rund 100.000 VND, also etwa 4 €.',
   'Für die Registrierung brauchst du deinen Reisepass. eSIM geht auch, wenn dein Handy es kann.',
 ],
 'grab-app-einrichten': [
   'Grab ist in Südostasien das, was Uber in Europa ist: Taxi, Motorrad-Taxi, Essen und Pakete in einer App.',
   'Zum Anmelden reicht eine <strong>deutsche +49-Nummer</strong>, SMS-Code, Name, E-Mail. Mehr braucht es nicht.',
   'Die <strong>Preise sind fix</strong>, kein Verhandeln wie beim Tuk-Tuk. Bei Regen und Stau steigen sie trotzdem (Surge Pricing).',
   'In der App gibt es einen Notfallknopf, der das GPS des Fahrers teilt.',
 ],
 'vietnam-behoerden': [
   'Das offizielle Behördenportal Vietnams heißt <strong>Dich Vu Cong</strong> und liegt auf dichvucong.gov.vn.',
   'Online erledigen kannst du unter anderem die <strong>temporäre Wohnsitz-Anmeldung</strong> (je nach Gemeinde), Visum-Formulare, Unternehmens-Registrierung und Dokumenten-Prüfung.',
   'Für die Visum-Verlängerung ist der übliche Weg ein <strong>neues E-Visum</strong> nach kurzer Ausreise.',
   'Ehrlich gesagt: die Behördenwelt ist komplex. In der Praxis sparen lokale Agenten Zeit und Nerven.',
 ],
 '7-fehler-auswandern': [
   'Die sieben Fehler habe ich alle selbst gemacht, in acht Jahren und 70 Ländern. Jeder hat Geld, Zeit oder Nerven gekostet.',
   'Der teuerste ist Fehler eins. <strong>Rechne immer mit mehr, als du denkst.</strong>',
   'Die drei Klassiker: falsche Versicherung, falsches Visum, falscher Vermieter.',
   'Das hier ist kein Lehrbuch, sondern Erfahrung. Genau deshalb tut es weh, wenn man es liest, bevor man losfliegt.',
 ],
}

CSS = ('.kurz{background:var(--cream2,#F4EFE8);border-left:4px solid var(--terra,#A44A18);'
       'border-radius:0 10px 10px 0;padding:22px 26px;margin:0 0 34px}'
       '.kurz-t{font-size:12px;font-weight:700;letter-spacing:.11em;text-transform:uppercase;'
       'color:var(--terra,#A44A18);margin:0 0 12px}'
       '.kurz ul{margin:0;padding-left:20px}'
       '.kurz li{font-size:17px;line-height:1.7;margin-bottom:9px;color:var(--earth,#1A1410)}'
       '.kurz li:last-child{margin-bottom:0}')

# Behaelter, in dem der Artikeltext anfaengt, je nach Alter der Seite
START = re.compile(r'(<main class="article-wrap">|<div class="wrap">|<div class="article-wrap">)')
# Die Brotkrumen sind Navigation und gehoeren vor den Kasten
KRUMEN = re.compile(r'<(?:nav|div)[^>]*class="[^"]*fw-krumen[^"]*"[^>]*>.*?</(?:nav|div)>', re.S)


def main():
    gesetzt, schon_da, offen = [], 0, []
    for stamm, punkte in KAESTEN.items():
        f = BASIS / 'blog' / (stamm + '.html')
        if not f.exists():
            offen.append((stamm, 'Datei fehlt'))
            continue
        t = f.read_text(encoding='utf-8')
        if 'class="kurz"' in t:
            schon_da += 1
            continue
        m = START.search(t)
        if not m:
            offen.append((stamm, 'Textanfang nicht gefunden'))
            continue

        kasten = ('\n<div class="kurz">\n  <p class="kurz-t">Kurz gesagt</p>\n  <ul>\n'
                  + ''.join('    <li>%s</li>\n' % p for p in punkte)
                  + '  </ul>\n</div>\n')
        stelle = m.end()
        km = KRUMEN.search(t, stelle, stelle + 1200)
        if km:
            stelle = km.end()
        t = t[:stelle] + kasten + t[stelle:]

        if '.kurz{' not in t:
            s = t.rindex('</style>')
            t = t[:s] + CSS + t[s:]

        if SCHREIBEN:
            f.write_text(t, encoding='utf-8')
        gesetzt.append(stamm)

    wort = 'gesetzt' if SCHREIBEN else 'zu setzen (Vorschau)'
    print('Kurz-gesagt-Kaesten: %d %s, %d schon vorhanden' % (len(gesetzt), wort, schon_da))
    for n in gesetzt:
        print('  ', n)
    for n, grund in offen:
        print('   offen:', n, '(%s)' % grund)
    if gesetzt and not SCHREIBEN:
        print('\nZum Anwenden: python3 tools/kurz-gesagt.py --schreiben')


if __name__ == '__main__':
    main()
