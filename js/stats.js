// ============================================================
// STATISTIK · zentrale Besucher-Messung ·  freiweitmitnihat.com
// ------------------------------------------------------------
// EINZIGE Stelle, an der die Umami-Kennung eingetragen wird.
// Cookiefrei, keine IP-Speicherung, kein Cookie-Banner noetig.
// Anleitung: ../README-statistik.md
// ============================================================

/* ---- Kennung ----------------------------------------------
   Website-ID aus dem Umami-Konto. Oeffentlich sichtbar, das ist
   so vorgesehen und kein Geheimnis. Bei einem Kontowechsel hier
   austauschen, sonst nirgends.
   ----------------------------------------------------------- */
var UMAMI_ID  = 'd7f43baf-1cee-4bbb-aae6-74d680202c71';
var UMAMI_SRC = 'https://cloud.umami.is/script.js';

/* Steht die Kennung schon drin? */
function statsAktiv() {
  return !!UMAMI_ID && UMAMI_ID.indexOf('TODO-UMAMI') === -1;
}

/* ------------------------------------------------------------
   Messung laden
   ------------------------------------------------------------ */
(function ladeStatistik() {
  if (!statsAktiv()) return;
  var s = document.createElement('script');
  s.defer = true;
  s.src = UMAMI_SRC;
  s.setAttribute('data-website-id', UMAMI_ID);
  // Nur die eigene Domain messen, nie lokale Testaufrufe
  s.setAttribute('data-domains', 'freiweitmitnihat.com');
  document.head.appendChild(s);
})();

/* ------------------------------------------------------------
   zaehle(name, daten) -> ein Ereignis melden
   Beispiel: zaehle('beratung-klick', { seite: 'immobilien' })
   Faellt still aus, solange keine Kennung eingetragen ist.
   ------------------------------------------------------------ */
function zaehle(name, daten) {
  try {
    if (window.umami && typeof window.umami.track === 'function') {
      window.umami.track(name, daten || {});
    }
  } catch (e) { /* Messung darf die Seite nie stoeren */ }
}

/* ------------------------------------------------------------
   Herkunft aus ?via= als Ereignis melden.
   Passt zum Schema aus brevo.js: qr | yt | pinned | web
   Damit ist sichtbar, ob die QR-Codes aus den Videos wirken.
   ------------------------------------------------------------ */
document.addEventListener('DOMContentLoaded', function () {
  try {
    var p   = new URLSearchParams(window.location.search);
    var via = p.get('via');
    if (via) {
      zaehle('herkunft', {
        via:   via.replace(/[^a-zA-Z0-9_-]/g, '').slice(0, 40),
        seite: window.location.pathname
      });
    }
  } catch (e) { /* still */ }
});

/* ------------------------------------------------------------
   Wichtige Klicks automatisch zaehlen.
   Kein zusaetzlicher Code in den Seiten noetig: erkannt wird
   am Ziel-Link. Wer eigene Ereignisse setzen will, schreibt
   data-zaehl="name" an den Link.

   Umgesetzt ueber Umamis eigenes Attribut data-umami-event.
   Wichtig, weil der Browser bei einem Klick auf einen externen
   Link sofort wegspringt: Umami haelt die Navigation so lange
   zurueck, bis das Ereignis gesendet ist. Ein eigener
   Klick-Zaehler wuerde dabei abgeschnitten.
   ------------------------------------------------------------ */
var ZIELE = [
  ['cal.eu',             'beratung-buchen'],
  ['digistore24',        'kauf-klick'],
  ['checkout-ds24',      'kauf-klick'],
  ['bit.ly/nihathotels', 'affiliate-hotels'],
  ['bit.ly/nihat-safe',  'affiliate-versicherung'],
  ['buymeacoffee',       'kaffee-klick'],
  ['youtube.com',        'youtube-klick'],
  ['youtu.be',           'youtube-klick'],
  ['instagram.com',      'instagram-klick'],
  ['mailto:',            'mail-klick'],
  ['/beratung',          'beratung-seite'],
  ['/interview',         'interview-bewerbung'],
  ['/immobilien',        'immobilien-seite'],
  ['/rechnung',          'monatsrechnung'],
  ['/reality-check',     'reality-check'],
  ['/city-guides',       'city-guides'],
  ['/bibliothek',        'bibliothek'],
  ['/hotel-reise',       'reise-angebot'],
  ['/reise-buchen',      'reise-angebot'],
  ['/freiweit-woche',    'freiweit-woche'],
  ['/kontakt',           'kontakt-seite'],
  ['beratung.html',      'beratung-seite'],
  ['interview.html',     'interview-bewerbung'],
  ['immobilien.html',    'immobilien-seite'],
  ['rechnung.html',      'monatsrechnung'],
  ['reise.html',         'reise-warteliste']
];

function markiereLinks() {
  var links = document.querySelectorAll('a[href]:not([data-umami-event])');
  for (var i = 0; i < links.length; i++) {
    var a = links[i];
    var name = a.getAttribute('data-zaehl');
    if (!name) {
      var href = (a.getAttribute('href') || '').toLowerCase();
      if (!href) continue;
      for (var j = 0; j < ZIELE.length; j++) {
        if (href.indexOf(ZIELE[j][0]) !== -1) { name = ZIELE[j][1]; break; }
      }
    }
    if (!name) continue;
    a.setAttribute('data-umami-event', name);
    a.setAttribute('data-umami-event-seite', window.location.pathname);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  markiereLinks();
  // Nachladen abfangen: manche Seiten bauen Inhalte per JavaScript auf
  setTimeout(markiereLinks, 1200);
  setTimeout(markiereLinks, 4000);
});
