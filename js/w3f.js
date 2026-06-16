// ============================================================
// Web3Forms API Key — freiweitmitnihat.com
// ============================================================
const W3F_KEY = '9f0b39d4-60d7-472e-bb85-4c78ea575f2b';

// ── Validation helpers ────────────────────────────────────────
// Gilt für alle Seiten, die dieses Script einbinden

function isEmail(v) {
  if (!v || !v.includes('@')) return false;
  // Mindestens: zeichen@domain.tld (tld min. 2 Zeichen)
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim());
}

function showErr(id, msg) {
  var el = document.getElementById(id);
  if (!el) return;
  el.style.outline = '2px solid #c0392b';
  el.style.borderColor = '#c0392b';
  var errId = id + '-verr';
  var existing = document.getElementById(errId);
  if (!existing) {
    var err = document.createElement('div');
    err.id = errId;
    err.style.cssText = 'color:#c0392b;font-size:12px;margin-top:5px;font-family:Inter,sans-serif;line-height:1.4;';
    err.textContent = msg;
    el.parentNode.insertBefore(err, el.nextSibling);
  } else {
    existing.textContent = msg;
    existing.style.display = '';
  }
}

function clearErr(id) {
  var el = document.getElementById(id);
  if (el) { el.style.outline = ''; el.style.borderColor = ''; }
  var err = document.getElementById(id + '-verr');
  if (err) err.style.display = 'none';
}

// Budget-Check: erkennt reine Zahlen ≤ 1 als ungültig
function isBudgetPlausible(v) {
  if (!v) return true; // optional — leer ist ok
  var num = parseFloat(v.replace(/[^0-9.,]/g, '').replace(',', '.'));
  if (!isNaN(num) && num <= 1) return false;
  return true;
}

// ── Web3Forms Absende-Helper ──────────────────────────────────
// Schickt ein Formular an Web3Forms und gibt das fetch-Promise zurück.
// botcheck: false ist Pflicht — ohne es blockiert Web3Forms als Spam.
function w3fSend(payload) {
  return fetch('https://api.web3forms.com/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(Object.assign({ access_key: W3F_KEY, botcheck: false }, payload))
  });
}
