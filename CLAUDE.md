# CLAUDE.md — Freiweit mit Nihat · Homepage
## Master-Instruction für alle Homepage-Arbeiten

Lies diese Datei vollständig bevor du irgendetwas änderst.
Arbeite autonom, keine Rückfragen bei klaren Aufgaben.

---

## PROJEKT-ÜBERSICHT

**Website:** Freiweit mit Nihat — persönliche Homepage für YouTube-Kanal @FreiweitmitNihat
**Zweck:** Lead-Generierung, Community-Aufbau, Immobilien-Vermittlung, Beratung, Interview-Bewerbungen
**Zielgruppe:** DACH-Raum, 25–70 Jahre, Auswanderer / Nomaden / Rentner / Interessierte
**Sprache:** Deutsch (DACH)
**Hosting:** GitHub Pages (geplant) · Domain: IONOS (geplant)

---

## DATEIEN-STRUKTUR

```
homepage/
├── CLAUDE.md                  ← diese Datei
├── index.html                 ← Hauptseite (vollständig)
├── immobilien.html            ← Immobilien-Seite mit Filter + Modal
├── interview.html             ← Interviewpartner-Bewerbung
├── city-guides.html           ← Google Maps Guides (kaufen)
├── ratgeber.html              ← Kostenloser PDF-Ratgeber (Lead Magnet)
├── impressum.html             ← Separate Impressum-Seite
├── datenschutz.html           ← Separate Datenschutz-Seite
└── brand-context/
    ├── README.md
    ├── voice-profile.md
    ├── body-of-work.md
    └── visual-identity.md
```

---

## DESIGN-SYSTEM (niemals ändern ohne explizite Anweisung)

### Farben
```css
--earth:   #1A1410   /* Haupt-Dunkel */
--terra:   #C4622D   /* Terrakotta — Hauptakzent */
--sand:    #C8A97E   /* Sand — sekundärer Akzent */
--olive:   #6B7C45   /* Olive — sparsam */
--cream:   #FAFAF8   /* Hintergrund hell */
--cream2:  #F4EFE8   /* Hintergrund getönt */
--mid:     #7A7068   /* Fließtext */
--glass:   rgba(250,250,248,0.80)
```

### Typografie
- Headlines: Playfair Display, italic für Akzente, letter-spacing -1px bis -2px
- Body/UI: Inter, letter-spacing -0.1px

### Regeln
- Apple-Stil + warme Erdtöne
- SVG-Icons (Linien) — KEINE Emojis
- Glassmorphism in Nav
- Scroll-Reveal via IntersectionObserver (.reveal → .vis)
- Buttons: border-radius 8px
- KEIN "Bullshit" oder ähnliches

---

## SEITENSTRUKTUR index.html (Reihenfolge)

1. Nav — Destinationen, Blog, Angebote, Immobilien, Stimmen, Newsletter, Interview · CTA: Kontakt
2. Hero — Kyoto-Foto rechts, 6 Buttons, 4 Stats (70+ Länder, 7 Jahre, 100%, 6 Sprachen)
3. Was interessiert dich? — 8 Karten (Auswandern, Nomade, Mieten, Kaufen, Hotel, Business, City Guides, Ratgeber)
4. Über mich — Stadtbild-Foto + Text
5. Blog & Videos — 6 YouTube-Videos mit Thumbnails + Filter
6. Angebote — 6 Cards
7. Interview — "Deine Geschichte. Mein Kanal."
8. Immobilien CTA — Suchen + Anbieten/YouTube-Vorstellen
9. Destinationen — Thailand + Vietnam + Kommt bald
10. Stimmen — Social Proof + Feedback-Modal
11. Newsletter
12. Kontakt — 3-Schritt-Formular
13. Footer — alle Links, Impressum, Datenschutz

---

## KONTAKTDATEN

```
YouTube:      https://www.youtube.com/@FreiweitmitNihat
Instagram:    https://www.instagram.com/nihatbucakli/
BuyMeACoffee: https://buymeacoffee.com/freiweitmitnihat
E-Mail:       freiweit.mit.nihat@gmail.com
Hotel-Aff.:   https://bit.ly/NihatHotels
Versicherung: https://bit.ly/Nihat-Safe
TikTok:       [NOCH OFFEN]
Facebook:     [NOCH OFFEN]
```

---

## YOUTUBE VIDEOS (Blog-Sektion)

IDs: KDYcaHDT2vk · 37Hdj6TEnsc · 24Qr5o9Daxk · 4Udz633KfiI · F8C2oNoItyk · 7xQhax1qLgg
Thumbnails: https://img.youtube.com/vi/[ID]/maxresdefault.jpg
Titel via oEmbed: https://www.youtube.com/oembed?url=...&format=json

---

## BILDER

```
Hero rechts:  Kyoto Fushimi Inari — base64 in index.html
Über mich:    Stadtbild weißes Hemd — base64 in index.html
```

Neue Bilder: PIL, max. 900px Breite, JPEG 85–88%. Immer base64 einbetten.
Ausnahme: YouTube-Thumbnails direkt von img.youtube.com.

---

## OFFENE TO-DOS

### Sofort
- [ ] TikTok + Facebook Links → Social Icons ergänzen
- [ ] Domain IONOS kaufen
- [ ] GitHub Repository + Pages aktivieren
- [ ] MailerLite Account → Formular-ID in ratgeber.html
- [ ] Tally/Formspree in Kontaktformular
- [ ] Calendly Beratungscall (97€)

### Inhalt
- [ ] Echte Bewertungen in Social Proof eintragen
- [ ] Bisherige Interviews auf interview.html eintragen
- [ ] Echte Immobilien-Objekte eintragen
- [ ] Pattaya City Guide fertigstellen
- [ ] Bangkok / Da Nang / Chiang Mai Guides erstellen

### Nächste Phase
- [ ] Partner-Sektion mit Affiliate-Links
- [ ] "Langfristig investieren" Bereich (Trade Republic, ETFs, Crypto)
- [ ] Formulare detaillierter + Backend
- [ ] Blog-Archiv Seite
- [ ] Skool Community Integration

---

## MONETARISIERUNGSPLAN

**Phase 1 (sofort):** Newsletter, Affiliate (Agoda, SafetyWing, eSIM), Beratung 97€, FS Consultings
**Phase 2 (1–3 Monate):** City Guides 9,90€, PDF Lead Magnet, Blog SEO, Facebook-Gruppe
**Phase 3 (3–9 Monate):** Skool Community 15–29€/Monat, Videokurs, Media Kit
**Phase 4 (9–24 Monate):** Gruppenreisen, Meetup Thailand, App, Lifetime-Membership

---

## HOSTING & TECHNIK

```
Hosting:    GitHub Pages
Domain:     IONOS (.de)
Formulare:  Tally (kostenlos)
Newsletter: MailerLite (kostenlos bis 1.000 Abonnenten)
E-Mail:     Cloudflare Email Routing → Gmail
Calls:      Calendly
PDF-Versand: MailerLite Automation
```

---

## CLAUDE CODE AGENTEN (~/Desktop/freiweit-nihat-youtube/)

```
CLAUDE.md               ← Master YouTube-Produktion
beschreibung-agent.md   ← Beschreibung + Kapitel + Pinned Comment
community-post-agent.md ← Community-Post + Bildprompts
karusell-agent.md       ← 7 PNG-Slides
blog-agent.md           ← Blog aus Transkript + Web Search
komplett-paket.md       ← Alle Agenten sequenziell
```

---

## BRAND VOICE (Kurzversion)

- Wir + Du + Ich-Geschichten · Konkrete Zahlen früh
- "Am Ende des Tages..." / "Ich sage es dir so wie es ist:"
- Ehrlich, keine Hochglanz-Versprechen
- Keine Emojis · Kein "Bullshit"

---

*Letzte Aktualisierung: Juni 2026*
