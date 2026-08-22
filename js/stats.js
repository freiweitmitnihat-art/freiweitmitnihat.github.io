// ============================================================
// STATISTIK · zentrale Besucher-Messung ·  freiweitmitnihat.com
// ------------------------------------------------------------
// EINZIGE Stelle, an der die Umami-Kennung eingetragen wird.
// Cookiefrei, keine IP-Speicherung, kein Cookie-Banner noetig.
// Anleitung: ../README-statistik.md
// ============================================================

/* ---- HIER EINTRAGEN ---------------------------------------
   1. Konto auf cloud.umami.is anlegen, Region EU (Deutschland)
   2. Website "freiweitmitnihat.com" hinzufuegen
   3. Die Website-ID (sieht aus wie 1a2b3c4d-...) hier einsetzen
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
   ------------------------------------------------------------ */
document.addEventListener('click', function (ev) {
  var a = ev.target && ev.target.closest ? ev.target.closest('a') : null;
  if (!a) return;

  var eigen = a.getAttribute('data-zaehl');
  if (eigen) { zaehle(eigen, { seite: window.location.pathname }); return; }

  var href = (a.getAttribute('href') || '').toLowerCase();
  if (!href) return;

  var regeln = [
    ['cal.eu',            'beratung-buchen'],
    ['digistore24',       'kauf-klick'],
    ['checkout-ds24',     'kauf-klick'],
    ['bit.ly/nihathotels','affiliate-hotels'],
    ['bit.ly/nihat-safe', 'affiliate-versicherung'],
    ['buymeacoffee',      'kaffee-klick'],
    ['youtube.com',       'youtube-klick'],
    ['youtu.be',          'youtube-klick'],
    ['instagram.com',     'instagram-klick'],
    ['interview.html',    'interview-bewerbung'],
    ['mailto:',           'mail-klick']
  ];

  for (var i = 0; i < regeln.length; i++) {
    if (href.indexOf(regeln[i][0]) !== -1) {
      zaehle(regeln[i][1], { seite: window.location.pathname, ziel: href.slice(0, 120) });
      return;
    }
  }
}, true);
