// Tasting journal: personal notes, read and written only through the local Python server (same coffee_journal.json
// and entry format as the desktop app). On the static site the journal is not published, so the page explains that.
import { route, api, app, esc, list, isStatic, needsServer } from './core.js';

const stars = n => '★'.repeat(n) + '☆'.repeat(5 - n);

route('journal', async (_args, query) => {
  if (isStatic()) {
    app().innerHTML = `<p class="kicker">Journal</p><h1>Tasting journal</h1>
      <p class="lead">Record coffees you taste: a 1–5 star rating, brewing details and tasting notes.</p>
      ${needsServer('The tasting journal')}
      <p class="mute">Journal entries are personal notes stored in coffee_journal.json on your own computer; they are
      never published on this site. Use the desktop app or the local web app to add and read them.</p>`;
    return;
  }
  const { entries, coffees } = await api('/journal', { fresh: true });
  app().innerHTML = `<p class="kicker">Journal</p><h1>Tasting journal</h1>
    <p class="lead">${entries.length} ${entries.length === 1 ? 'entry' : 'entries'} in coffee_journal.json (shared with the desktop app; local only, never published).</p>
    <div class="side rev">
      <div id="entries">${entries.length ? list(entries, e => `<div class="panel entry">
          <small class="mute">${esc(e.date)}</small><b>${esc(e.coffee_name)}</b> <span class="stars" aria-label="${e.rating} of 5 stars">${stars(e.rating || 0)}</span>
          ${e.brewing ? `<h3>Brewing</h3><pre>${esc(e.brewing)}</pre>` : ''}${e.notes ? `<h3>Tasting notes</h3><p>${esc(e.notes)}</p>` : ''}</div>`)
        : '<p class="mute">No entries yet. Add your first tasting.</p>'}</div>
      <form class="panel" id="jform">
        <h3>New entry</h3>
        <label for="j-coffee">Coffee</label><input id="j-coffee" list="j-list" required value="${esc(query.coffee || '')}">
        <datalist id="j-list">${list(coffees, c => `<option value="${esc(c)}">`)}</datalist>
        <label for="j-rating">Rating</label><select id="j-rating">${[5, 4, 3, 2, 1].map(n => `<option value="${n}" ${n === 3 ? 'selected' : ''}>${stars(n)}</option>`).join('')}</select>
        <label for="j-brew">Brewing details</label><textarea id="j-brew">Method: \nGrind: \nRatio: </textarea>
        <label for="j-notes">Tasting notes</label><textarea id="j-notes"></textarea>
        <button type="submit">Save</button><p id="j-msg" class="small" aria-live="polite"></p>
      </form>
    </div>`;
  document.getElementById('jform').addEventListener('submit', async e => {
    e.preventDefault();
    const msg = document.getElementById('j-msg');
    try {
      await api('/journal', { body: { coffee_name: document.getElementById('j-coffee').value, rating: +document.getElementById('j-rating').value,
        brewing: document.getElementById('j-brew').value, notes: document.getElementById('j-notes').value } });
      location.hash = '#/journal?saved=' + Date.now();
    } catch (err) { msg.className = 'small err'; msg.textContent = err.message; }
  });
});
