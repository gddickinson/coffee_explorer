// Brewing countdown timer (the desktop Brewing tab's timer, in the browser): minutes + seconds, start/pause/reset,
// a chime and a message when the coffee is ready. Runs entirely client-side, so it also works on the static site.
import { esc, onLeave } from './core.js';

// "25-30 seconds" -> 25, "2.5-3 minutes" -> 150, "4 minutes" -> 240; hours (cold brew) -> null (too long for a timer).
export function parseBrewTime(text) {
  const m = String(text || '').match(/([\d.]+)\s*(?:-\s*[\d.]+\s*)?(seconds?|secs?|minutes?|mins?|hours?)/i);
  if (!m) return null;
  const n = parseFloat(m[1]), unit = m[2].toLowerCase();
  if (unit.startsWith('h')) return null;
  return Math.round(unit.startsWith('s') ? n : n * 60);
}

const fmt = s => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;

function chime() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    [0, 0.35, 0.7].forEach(t => {
      const o = ctx.createOscillator(), g = ctx.createGain();
      o.frequency.value = 880; g.gain.setValueAtTime(0.15, ctx.currentTime + t);
      g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + t + 0.3);
      o.connect(g).connect(ctx.destination); o.start(ctx.currentTime + t); o.stop(ctx.currentTime + t + 0.3);
    });
  } catch { /* audio unavailable */ }
}

// Renders the timer into host. preset: seconds to prefill (or null).
export function mountTimer(host, preset = null, label = '') {
  if (host._stopTimer) host._stopTimer();
  const total = preset ?? 240;
  host.innerHTML = `<div class="timer panel">
    <h3>Brewing timer${label ? ' · ' + esc(label) : ''}</h3>
    <div class="clock mono" id="t-clock" role="timer" aria-live="off">${fmt(total)}</div>
    <div class="row">
      <div><label for="t-min">Minutes</label><input id="t-min" type="number" min="0" max="99" value="${Math.floor(total / 60)}"></div>
      <div><label for="t-sec">Seconds</label><input id="t-sec" type="number" min="0" max="59" value="${total % 60}"></div>
    </div>
    <button id="t-start">Start</button><button class="alt" id="t-pause" disabled>Pause</button><button class="alt" id="t-reset">Reset</button>
    <p id="t-msg" class="ok" aria-live="polite"></p></div>`;
  const $ = id => host.querySelector('#' + id);
  let left = 0, iv = 0;
  const read = () => Math.max(0, (parseInt($('t-min').value, 10) || 0) * 60 + (parseInt($('t-sec').value, 10) || 0));
  const show = () => { $('t-clock').textContent = fmt(left); };
  const stop = () => { clearInterval(iv); iv = 0; $('t-start').disabled = false; $('t-pause').disabled = true; };
  ['t-min', 't-sec'].forEach(id => $(id).addEventListener('input', () => { if (!iv) { left = read(); show(); } }));
  $('t-start').onclick = () => {
    if (!left) left = read();
    if (!left) return;
    $('t-msg').textContent = '';
    $('t-start').disabled = true; $('t-pause').disabled = false;
    iv = setInterval(() => {
      left -= 1; show();
      if (left <= 0) { stop(); left = 0; $('t-msg').textContent = 'Coffee is ready!'; chime(); }
    }, 1000);
  };
  $('t-pause').onclick = stop;
  $('t-reset').onclick = () => { stop(); left = read(); show(); $('t-msg').textContent = ''; };
  host._stopTimer = () => clearInterval(iv);
  onLeave(host._stopTimer);
}
