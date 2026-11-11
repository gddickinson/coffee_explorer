// Coffee origins: filterable list (like the desktop "Coffee Database" tab) and a detail page per coffee.
import { route, api, app, esc, list, tags } from './core.js';
import { listPage, kv, sections, crumb, trim, words, or } from './ui.js';

// Same roast choices as the desktop app's filter (matched as a substring: "Light" also finds "Light to Medium").
const ROASTS = [['Light', 'Light'], ['Medium', 'Medium'], ['Dark', 'Dark']];

export function coffeeCard(c) {
  return `<a class="card" href="#/coffee/${c.id}"><small>${esc(c.origin_country)}${c.origin_region ? ' · ' + esc(c.origin_region) : ''}</small>
    <b>${esc(c.name)}</b><span>${esc(trim(c.flavor_profile, 110))}</span>
    <div class="meta"><span>${esc(or(c.roast_level, ''))}</span>${c.cupping_score ? `<span class="score">${c.cupping_score}</span>` : ''}</div></a>`;
}

route('coffees', async (_args, query) => {
  const f = (await api('/facets')).coffees;
  await listPage({
    routeName: 'coffees', kind: 'coffees', kicker: 'Database', title: 'Coffee origins', query,
    lead: 'Single-origin coffees from around the world: where they grow, how they are processed, and how they taste. Search by name, country, region, variety or flavour.',
    placeholder: 'e.g. Ethiopia, bergamot, honey, Bourbon',
    filters: [
      { id: 'roast', label: 'Roast level', options: ROASTS },
      { id: 'country', label: 'Country', options: f.country },
      { id: 'process', label: 'Processing', options: f.process },
    ],
    card: coffeeCard,
  });
});

route('coffee', async ([id]) => {
  const c = await api('/coffees/' + encodeURIComponent(id));
  const alt = c.altitude_min || c.altitude_max ? `${or(c.altitude_min, '?')}–${or(c.altitude_max, '?')} m` : '—';
  app().innerHTML = `
    ${crumb('#/coffees', 'Coffee origins', c.origin_country)}
    <h1>${esc(c.name)}</h1>
    <p class="lead">${esc(c.origin_region || '')}${c.origin_region ? ', ' : ''}${esc(c.origin_country)}</p>
    ${kv([['cupping score', c.cupping_score], ['roast level', c.roast_level], ['processing', c.processing_method],
      ['altitude', alt], ['harvest', c.harvest_season], ['caffeine', c.caffeine_content], ['price range', c.price_range]])}
    <div class="two">
      <div>
        <h3>Flavour profile</h3><p>${tags(words(c.flavor_profile), 'a')}</p>
        ${c.tasting_notes ? `<h3>Tasting notes</h3><p>${tags(words(c.tasting_notes), 'b')}</p>` : ''}
        ${sections([['Aroma', c.aroma], ['Body', c.body], ['Acidity', c.acidity]])}
      </div>
      <div>
        <h3>Variety</h3><p>${esc(or(c.variety))}</p>
        ${c.varieties.length ? `<p>${list(c.varieties, v => `<a class="tag c" href="#/variety/${v.id}">${esc(v.name)}</a>`)}</p>` : ''}
        ${sections([['History', c.history]])}
        ${c.regions.length ? `<h3>Growing regions in ${esc(c.regions[0].country)}</h3>
          <p>${list(c.regions, r => `<a class="tag a" href="#/region/${r.id}">${esc(r.name)}</a>`)}</p>` : ''}
      </div>
    </div>
    <p><a class="btn alt" href="#/coffees?country=${encodeURIComponent(c.origin_country)}">More from ${esc(c.origin_country)}</a>
    <a class="btn alt" href="#/journal?coffee=${encodeURIComponent(c.name)}">Log a tasting</a></p>`;
});
