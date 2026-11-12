// Home (hero, live counts, entry cards), search across every table, and About.
import { route, api, app, esc, list, isStatic } from './core.js';
import { worldSvg } from './regions.js';
import { trim } from './ui.js';

const DOORS = [
  ['#/coffees', 'Coffee origins', 'Single-origin coffees with flavour, processing, altitude, harvest and cupping scores.', 'coffees'],
  ['#/varieties', 'Varieties', 'Typica, Bourbon, Geisha, SL28, Robusta and modern hybrids: what each plant brings to the cup.', 'varieties'],
  ['#/roasters', 'Roasters and brands', 'Mass-market, premium and specialty roasters: owners, history, style, certifications.', 'roasters'],
  ['#/products', 'Products', 'The roasters\' catalogue: type, roast, size, price, organic and Fair Trade.', 'products'],
  ['#/brewing', 'Brewing methods', 'Grind, temperature, time and ratio for each method, plus a brewing timer.', 'brewing_methods'],
  ['#/map', 'Regions map', 'Coffee-growing regions on a world map, with climate, soil and elevation.', 'regions'],
  ['#/guide', 'Coffee guide', 'Species, processing, roasting, cupping, storage, health and a glossary.', null],
  ['#/history', 'Coffee history', 'From Ethiopian legend to the fourth wave and the future of coffee.', null],
  ['#/journal', 'Tasting journal', 'Rate and note the coffees you taste (local app only).', null],
];

route('home', async () => {
  const [s, world] = await Promise.all([api('/stats'), api('/world')]);
  app().innerHTML = `
  <section class="hero">
    <p class="kicker">Origins · Varieties · Roasters · Brewing</p>
    <h1 class="glow">Coffee Collection Explorer</h1>
    <p class="lead">Explore coffee varieties, brewing methods, roasters and brands, and the regions where coffee grows,
    with a complete coffee guide and history.</p>
    <form id="hsearch" role="search" class="row"><div><label for="hs-q">Search everything</label>
      <input id="hs-q" type="search" placeholder="e.g. Geisha, Kenya, French press, Blue Bottle"></div>
      <div style="flex:0"><button type="submit">Search</button></div></form>
  </section>
  <div class="tiles">
    <a class="tile" href="#/coffees"><b>${s.coffees}</b><span>coffee origins</span></a>
    <a class="tile" href="#/varieties"><b>${s.varieties}</b><span>varieties</span></a>
    <a class="tile" href="#/roasters"><b>${s.roasters}</b><span>roasters and brands</span></a>
    <a class="tile" href="#/products"><b>${s.products}</b><span>products</span></a>
    <a class="tile" href="#/brewing"><b>${s.brewing_methods}</b><span>brewing methods</span></a>
    <a class="tile" href="#/map"><b>${s.regions}</b><span>growing regions</span></a>
  </div>
  <div class="grid wide">${list(DOORS, ([href, t, d, k]) => `<a class="card door" href="${href}"><b>${t}${k ? ` <em class="n">${s[k]}</em>` : ''}</b><span>${d}</span></a>`)}</div>
  <h2>Where coffee grows</h2>
  <a class="stage map" href="#/map" aria-label="Open the regions map">${worldSvg(world, null, { links: false })}</a>`;
  document.getElementById('hsearch').addEventListener('submit', e => {
    e.preventDefault();
    location.hash = '#/search?q=' + encodeURIComponent(document.getElementById('hs-q').value.trim());
  });
});

const GROUPS = [
  ['coffees', 'Coffee origins', c => [`#/coffee/${c.id}`, c.name, c.origin_country, c.flavor_profile]],
  ['varieties', 'Varieties', v => [`#/variety/${v.id}`, v.name, v.species, v.characteristics]],
  ['roasters', 'Roasters', r => [`#/roaster/${r.roaster_id}`, r.roaster_name, r.country_of_origin, r.description]],
  ['products', 'Products', p => [`#/product/${p.product_id}`, p.product_name, p.roaster_name, p.special_features]],
  ['brewing', 'Brewing methods', m => [`#/method/${m.id}`, m.name, m.category, m.description]],
  ['regions', 'Regions', r => [`#/region/${r.id}`, r.name, r.country, r.description]],
];

route('search', async (_args, query) => {
  app().innerHTML = `<p class="kicker">Search</p><h1>Search everything</h1>
    <div class="panel"><label for="s-q">Search coffees, varieties, roasters, products, brewing methods and regions</label>
    <input id="s-q" type="search" value="${esc(query.q || '')}" placeholder="e.g. chocolate, Italy, volcanic"></div>
    <div id="s-out" aria-live="polite"></div>`;
  const input = document.getElementById('s-q');
  let seq = 0;
  async function run() {
    const n = ++seq, q = input.value.trim();
    history.replaceState(null, '', '#/search' + (q ? '?q=' + encodeURIComponent(q) : ''));
    const res = await api('/search?q=' + encodeURIComponent(q));
    if (n !== seq) return;
    const total = GROUPS.reduce((a, [k]) => a + res[k].length, 0);
    document.getElementById('s-out').innerHTML = !q ? '<p class="mute">Type a word or two; every word must match.</p>'
      : `<p class="mute small">${total} results</p>` + list(GROUPS.filter(([k]) => res[k].length), ([k, title, fn]) =>
        `<h2>${title} <span class="mute small">${res[k].length}</span></h2><div class="grid">${list(res[k], r => {
          const [href, name, sub, text] = fn(r);
          return `<a class="card" href="${href}"><small>${esc(sub || '')}</small><b>${esc(name)}</b><span>${esc(trim(text, 100))}</span></a>`;
        })}</div>`);
  }
  input.addEventListener('input', run);
  input.focus();
  await run();
});

route('about', async () => {
  const s = await api('/stats');
  app().innerHTML = `<p class="kicker">About</p><h1>Coffee Collection Explorer</h1>
    <p class="lead">A Python application for exploring coffee varieties, brewing methods, roasters and brands, and
    coffee-growing regions around the world. This web interface shows the same SQLite database as the desktop app:
    ${s.coffees} coffee origins, ${s.varieties} varieties, ${s.roasters} roasters with ${s.products} products,
    ${s.brewing_methods} brewing methods and ${s.regions} regions, plus the coffee guide and history.</p>
    ${isStatic() ? '<p class="callout">This is the static (GitHub Pages) version: everything is browsable and searchable, but the tasting journal only works in the local app.</p>' : ''}
    <h2>Run the desktop app</h2>
    <pre>pip install -r requirements.txt
python run_coffee_explorer.py</pre>
    <p>A Tkinter app with tabs for the coffee database, varieties, roasters, brewing methods and timer, tasting journal,
    guide, history and a world map.</p>
    <h2>Run the web app</h2>
    <pre>pip install -r requirements-web.txt
python run_web.py        # http://127.0.0.1:8104</pre>
    <p>The local web app reads coffee_collection.db read-only and can add tasting-journal entries to coffee_journal.json
    (the same file the desktop app uses). <code>python scripts/build_static.py</code> exports the static site.</p>
    <h2>Credits</h2>
    <p>Database content compiled from Specialty Coffee Association standards, world coffee competition results, coffee
    quality grading systems, roaster websites and product catalogs, coffee research publications and industry trade
    publications. Product and company information synthesized from publicly available sources; check with the roaster
    before relying on a price.</p>
    <p>Built with Python, Tkinter, SQLite and Pillow (desktop) and FastAPI with plain JavaScript (web), with AI
    assistance from <a href="https://claude.com/" target="_blank" rel="noopener">Claude (Anthropic)</a>.
    Released under the MIT licence. <a href="https://github.com/gddickinson/coffee_explorer" target="_blank" rel="noopener">Source on GitHub</a>.</p>`;
});
