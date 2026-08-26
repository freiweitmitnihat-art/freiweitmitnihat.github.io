# TODO · Video-IDs in den Blogartikeln nachtragen

**Angelegt:** 25.08.2026
**Warum das zählt:** Artikel ohne eingebettetes Video bekommen von
`tools/seo-strukturdaten.py` kein `VideoObject`. Sie tauchen dadurch nicht in der
Video-Suche und nicht in den Video-Karussells von Google auf. Von 48 Artikeln haben
**36 ein Video, 12 nicht.**

---

## Die zwölf Artikel ohne Video-Einbettung

| Artikel | Gibt es dazu ein Video? | Was zu tun ist |
|---|---|---|
| `cha-am-beach-hua-hin.html` | **ja, aber noch nicht hochgeladen** | ID nachtragen, sobald das Cha-Am-Video online ist |
| `bang-saen-villa-1.html` | Artikel wurde zurückgezogen | nichts. Steht laut `README-seo.md` bewusst auf noindex |
| `bang-saray-villa-pool.html` | vermutlich ja | im Kanal suchen, ID eintragen |
| `da-nang-vietnam-entdeckt.html` | vermutlich ja | im Kanal suchen, ID eintragen |
| `lebenshaltungskosten-thailand.html` | vermutlich ja, mehrere in Frage kommend | passendstes Video wählen |
| `7-fehler-auswandern.html` | nein, das ist der Lead Magnet | nichts, oder ein thematisch passendes Video verlinken |
| `grab-app-einrichten.html` | nein, reiner Ratgeber | optional |
| `sim-karte-thailand.html` | nein, reiner Ratgeber | optional |
| `thailand-e-visum.html` | nein, reiner Ratgeber | optional |
| `thailand-tdac.html` | nein, reiner Ratgeber | optional |
| `vietnam-behoerden.html` | nein, reiner Ratgeber | optional |
| `vietnam-e-visum.html` | nein, reiner Ratgeber | optional |

**Ehrlich eingeordnet:** Wirklich fehlen tun nur **vier** (Cha-Am, Bang Saray Villa,
Da Nang, Lebenshaltungskosten). Die sieben Ratgeber sind Textseiten ohne eigenes Video,
da wäre ein eingebettetes Video eher Beiwerk als Substanz. `bang-saen-villa-1` bleibt außen vor.

---

## Was ich brauche

Für jeden Artikel die **YouTube-Video-ID**, also den Teil hinter `watch?v=`.
Beispiel: `https://www.youtube.com/watch?v=0Pb2j6Ku4KI` → `0Pb2j6Ku4KI`

Schick mir einfach die Zuordnung, etwa so:
```
cha-am-beach-hua-hin        = ABC123xyz
bang-saray-villa-pool       = DEF456uvw
da-nang-vietnam-entdeckt    = GHI789rst
lebenshaltungskosten        = JKL012mno
```

---

## Was dann automatisch passiert

1. Video-Kasten in den Artikel (gleiche Bauart wie in den anderen 36).
2. Eintrag in `tools/videodaten.json` mit Titel, Laufzeit und Upload-Datum.
3. `python3 tools/seo-strukturdaten.py` schreibt das `VideoObject`.
4. Vorschaubild nach `img/yt/<ID>-mqdefault.jpg` und `-maxresdefault.jpg`.
5. Bei Bedarf neue Kachel im Abschnitt „Neu auf dem Kanal" in `index.html`.

---

## Nebenbefund

`img/yt/BtcDUyr4_g8-maxresdefault.jpg` (319 KB) wird von keiner öffentlichen Seite
eingebunden und ist der größte ungenutzte Brocken im Bilderordner. Entweder gehört das
Bild in einen Artikel, oder es kann weg. Steht auch in der SEO-Prüfung.
