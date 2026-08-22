// ============================================================
// BREVO · zentrale Newsletter-Anbindung  ·  freiweitmitnihat.com
// ------------------------------------------------------------
// EINZIGE Stelle, an der die Brevo-Adresse eingetragen wird.
// Alle Seiten (rechnung, reality-check, Startseite, Freiweit-Woche)
// benutzen dieses Script. Anleitung: ../README-brevo.md
// ============================================================

/* ---- HIER EINTRAGEN ---------------------------------------
   Variante A (einfach, ohne Konto-Schluessel):
     Brevo -> Kontakte -> Formulare -> Formular veroeffentlichen
     var BREVO_ENDPOINT = 'https://XXXXX.sibforms.com/serve/MUIFAB...';

   Variante B (Cloudflare Worker, bessere Rueckmeldung):
     var BREVO_ENDPOINT = 'https://newsletter.freiweitmitnihat.com/subscribe';
   ----------------------------------------------------------- */
var BREVO_ENDPOINT = 'https://3e474221.sibforms.com/v2/serve/MUIFAMsRuunro-QlG1lnKpxB4g1KMPxa4kA1uyRnqMx2wE2rzrS3FTiA_V6qJOHryM_787rHeSzNAqe9yiZ-5iHrGps5qPvyfJscLSlgDkQzq-JbyRroedYsg4YGQAEtUEy6YpBI1B_5Ndnsm-JVSVR6RKFvqnLhQ3tohnm6nen-ENtN7PUOth-nvsRNRZ56A1IcS-8u91JMd0FUDg==';

/* Steht die Adresse schon drin? */
function brevoConfigured() {
  return !!BREVO_ENDPOINT && BREVO_ENDPOINT.indexOf('TODO-BREVO') === -1;
}

/* Quelle aus der URL lesen (?via=qr | yt | pinned | web).
   Damit ist spaeter sichtbar, welcher Kanal die Anmeldung gebracht hat. */
function brevoQuelle(prefix) {
  var name = prefix || 'Web';
  try {
    var via = new URLSearchParams(window.location.search).get('via') || 'web';
    var map = {
      qr:     'QR',
      yt:     'YouTube-Beschreibung',
      pinned: 'Pinned-Comment',
      web:    'Website'
    };
    var quelle = map[via] || via.replace(/[^a-zA-Z0-9_-]/g, '').slice(0, 40);
    return name + '-' + quelle;
  } catch (e) {
    return name + '-Website';
  }
}

/* ------------------------------------------------------------
   brevoSubscribe(o) -> Promise
   o = {
     email:    Pflicht
     vorname:  optional
     quelle:   z.B. 'Monatsrechnung-QR'
     magnet:   z.B. 'Monatsrechnung' | 'Reality-Check' | 'Newsletter'
     notify:   true  -> zusaetzlich Info-Mail an Nihat (Web3Forms)
     betreff:  Betreff dieser Info-Mail
     text:     Inhalt dieser Info-Mail
   }
   Solange BREVO_ENDPOINT noch der Platzhalter ist, laeuft alles
   ueber Web3Forms an das Postfach von Nihat. Nichts geht verloren.
   ------------------------------------------------------------ */
function brevoSubscribe(o) {
  o = o || {};
  var email   = (o.email || '').trim();
  var vorname = (o.vorname || '').trim();
  var quelle  = o.quelle || brevoQuelle(o.magnet || 'Web');
  var magnet  = o.magnet || 'Newsletter';

  if (!email) return Promise.reject(new Error('keine E-Mail'));

  var fallback = function () {
    if (typeof w3fSend !== 'function') return Promise.reject(new Error('kein Versandweg'));
    return w3fSend({
      subject:   o.betreff || ('Newsletter-Anmeldung (' + magnet + ')'),
      name:      vorname || 'Ohne Namen',
      email:     email,
      replyto:   email,
      from_name: 'Freiweit Website',
      message:   (o.text || '')
                 + '\nName: ' + (vorname || 'ohne Angabe')
                 + '\nE-Mail: ' + email
                 + '\nQuelle: ' + quelle
                 + '\nThema: ' + magnet
                 + '\nEinwilligung erteilt: ja'
                 + '\n\nBitte von Hand in die Brevo-Liste aufnehmen.'
    });
  };

  /* Info-Mail an Nihat, wenn gewuenscht (z.B. Reality-Check-Auswertung).
     Laeuft nebenher und darf die Anmeldung nicht blockieren. */
  var notify = function () {
    /* Anmeldung in der Statistik zaehlen. Wichtigste Kennzahl der Seite,
       deshalb hier zentral und nicht auf jeder Seite einzeln. */
    if (typeof zaehle === 'function') {
      zaehle('newsletter-anmeldung', { magnet: magnet, quelle: quelle });
    }
    if (o.notify && brevoConfigured() && typeof w3fSend === 'function') {
      w3fSend({
        subject:   o.betreff || ('Neue Anmeldung (' + magnet + ')'),
        name:      vorname || 'Ohne Namen',
        email:     email,
        replyto:   email,
        from_name: 'Freiweit Website',
        message:   (o.text || '') + '\nE-Mail: ' + email + '\nQuelle: ' + quelle
      }).catch(function () {});
    }
  };

  if (!brevoConfigured()) return fallback();

  /* Variante A: Brevo-Formular (sibforms). Antwort ist nicht lesbar
     (no-cors), deshalb gilt der Versand als erfolgreich, sobald der
     Request raus ist. */
  if (BREVO_ENDPOINT.indexOf('sibforms.com') !== -1) {
    var fd = new FormData();
    fd.append('EMAIL', email);
    fd.append('VORNAME', vorname);
    fd.append('QUELLE', quelle);
    fd.append('MAGNET', magnet);
    fd.append('OPT_IN', '1');
    fd.append('email_address_check', '');
    fd.append('locale', 'de');
    return fetch(BREVO_ENDPOINT, { method: 'POST', body: fd, mode: 'no-cors' })
      .then(function () { notify(); });
  }

  /* Variante B: eigener Endpunkt (Cloudflare Worker), echte Rueckmeldung. */
  return fetch(BREVO_ENDPOINT, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ email: email, vorname: vorname, quelle: quelle, magnet: magnet })
  }).then(function (r) {
    if (!r.ok) throw new Error('Brevo antwortet mit ' + r.status);
    notify();
  }).catch(function (err) {
    /* Wenn der eigene Endpunkt streikt, geht die Anmeldung trotzdem
       an Nihats Postfach, statt verloren zu gehen. */
    return fallback().then(function () { throw_silent(err); });
  });
}

/* Fehler wird nur in der Konsole vermerkt, der Nutzer sieht Erfolg,
   weil die Adresse ueber den Ersatzweg angekommen ist. */
function throw_silent(err) { try { console.warn('Brevo-Fallback benutzt:', err); } catch (e) {} }
