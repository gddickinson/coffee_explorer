// World map of coffee-growing regions (inline SVG, equirectangular, using the desktop app's simplified continent
// outlines from world_shapes.py) plus a searchable region list and a page per region.
import { route, api, app, esc, list } from './core.js';
import { listPage, kv, sections, crumb, trim } from './ui.js';
import { coffeeCard } from './coffees.js';

const W = 1000, H = 500;
const px = lon => ((lon + 180) / 360) * W;
const py = lat => ((90 - lat) / 180) * H;

// SVG map; regions are links to their pages. focus: id of a region to highlight.
export function worldSvg(world, focus = null, { crop = null } = {}) {
  const view = crop ? crop.join(' ') : `0 0 ${W} ${H}`;
  let s = `<svg class="world" viewBox="${view}" role="img" aria-label="World map of coffee-growing regions">`;
  // Tropic lines bound the "coffee belt" (23.4° N / S).
  s += `<rect x="0" y="${py(23.4)}" width="${W}" height="${py(-23.4) - py(23.4)}" class="belt"/>`;
  for (const lat of [23.4, 0, -23.4]) s += `<line x1="0" x2="${W}" y1="${py(lat)}" y2="${py(lat)}" class="${lat ? 'tropic' : 'equator'}"/>`;
  for (const [name, pts] of Object.entries(world.continents)) {
    s += `<polygon class="land" points="${pts.map(([lo, la]) => `${px(lo).toFixed(1)},${py(la).toFixed(1)}`).join(' ')}"><title>${esc(name)}</title></polygon>`;
  }
  for (const r of world.regions) {
    const x = px(r.longitude), y = py(r.latitude), on = r.id === focus;
    s += `<a href="#/region/${r.id}" class="pin${on ? ' on' : ''}" aria-label="${esc(r.name)}, ${esc(r.country)}">
      <circle cx="${x}" cy="${y}" r="${on ? 11 : 8}" class="halo"/><circle cx="${x}" cy="${y}" r="${on ? 6 : 4.5}" class="dot"/>
      <title>${esc(r.name)} (${esc(r.country)})</title></a>`;
  }
  return s + `<text x="${W - 8}" y="${py(23.4) - 6}" text-anchor="end" class="axisl">Tropic of Cancer</text>
    <text x="${W - 8}" y="${py(-23.4) + 16}" text-anchor="end" class="axisl">Tropic of Capricorn</text></svg>`;
}

route('map', async (_args, query) => {
  const [world, f] = await Promise.all([api('/world'), api('/facets')]);
  await listPage({
    routeName: 'map', kind: 'regions', kicker: 'Atlas', title: 'Coffee-growing regions', query,
    lead: 'Major growing regions with their coordinates, elevation, climate and soil. Almost all lie in the "coffee belt" between the tropics (shaded). Click a marker or a card.',
    placeholder: 'e.g. volcanic, Ethiopia, monsoon',
    extra: `<div class="stage map">${worldSvg(world)}</div>
      <p class="small mute">Continent outlines are the simplified shapes drawn by the desktop app; marker positions are the database coordinates.</p>`,
    filters: [{ id: 'country', label: 'Country', options: f.regions.country }],
    card: r => `<a class="card" href="#/region/${r.id}"><small>${esc(r.country)} · ${r.elevation_min}–${r.elevation_max} m</small>
      <b>${esc(r.name)}</b><span>${esc(trim(r.description, 110))}</span></a>`,
  });
});

route('region', async ([id]) => {
  const [r, world] = await Promise.all([api('/regions/' + encodeURIComponent(id)), api('/world')]);
  const x = px(r.longitude), y = py(r.latitude);
  const crop = [Math.max(0, Math.min(W - 400, x - 200)), Math.max(0, Math.min(H - 200, y - 100)), 400, 200];
  const ns = r.latitude >= 0 ? 'N' : 'S', ew = r.longitude >= 0 ? 'E' : 'W';
  app().innerHTML = `
    ${crumb('#/map', 'Regions', r.country)}
    <h1>${esc(r.name)}</h1>
    <p class="lead">${esc(r.description || '')}</p>
    <div class="two">
      <div>
        ${kv([['country', r.country], ['coordinates', `${Math.abs(r.latitude)}° ${ns}, ${Math.abs(r.longitude)}° ${ew}`],
          ['elevation', `${r.elevation_min}–${r.elevation_max} m`]])}
        ${sections([['Climate', r.climate], ['Soil', r.soil_type], ['Famous coffees', r.famous_coffees]])}
      </div>
      <div class="stage map">${worldSvg(world, r.id, { crop })}</div>
    </div>
    <h2>Coffee origins from ${esc(r.country)}</h2>
    ${r.coffees.length ? `<div class="grid">${list(r.coffees, coffeeCard)}</div>`
      : `<p class="mute">The database has no coffee origin entry for ${esc(r.country)}.</p>`}`;
});
