// Coffee varieties / cultivars: list with species filter and a detail page linking to the coffees that grow them.
import { route, api, app, esc, list } from './core.js';
import { listPage, kv, sections, crumb, trim } from './ui.js';
import { coffeeCard } from './coffees.js';

route('varieties', async (_args, query) => {
  const f = (await api('/facets')).varieties;
  await listPage({
    routeName: 'varieties', kind: 'varieties', kicker: 'Database', title: 'Varieties and cultivars', query,
    lead: 'The plants behind the cup: heirloom Arabicas, Robusta, and modern disease-resistant hybrids, with origin, flavour, yield and resistance.',
    placeholder: 'e.g. rust, Kenya, high yield, Geisha',
    filters: [{ id: 'species', label: 'Species', options: f.species }],
    card: v => `<a class="card" href="#/variety/${v.id}"><small>${esc(v.species)} · ${esc(v.origin_country || '')}${v.discovered_year ? ' · ' + v.discovered_year : ''}</small>
      <b>${esc(v.name)}</b><span>${esc(trim(v.characteristics, 120))}</span></a>`,
  });
});

route('variety', async ([id]) => {
  const v = await api('/varieties/' + encodeURIComponent(id));
  app().innerHTML = `
    ${crumb('#/varieties', 'Varieties', v.species)}
    <h1>${esc(v.name)}</h1>
    <p class="lead">${esc(v.characteristics || '')}</p>
    ${kv([['species', v.species], ['origin', v.origin_country], ['discovered / released', v.discovered_year],
      ['yield', v.yield], ['disease resistance', v.disease_resistance]])}
    ${sections([['Flavour notes', v.flavor_notes], ['Notes', v.notes]])}
    <h2>Coffees grown from ${esc(v.name)}</h2>
    ${v.coffees.length ? `<div class="grid">${list(v.coffees, coffeeCard)}</div>`
      : '<p class="mute">No coffee origin in the database lists this variety.</p>'}`;
});
