// Roasters and brands (filters: country, market segment, certification), roaster pages with their product catalogue,
// and a filterable product list with product detail pages.
import { route, api, app, esc, list, tags } from './core.js';
import { listPage, kv, sections, crumb, trim, words, or } from './ui.js';

const SEG = { 'mass-market': 'Mass-market', premium: 'Premium', specialty: 'Specialty', luxury: 'Luxury' };
const yes = b => (b ? 'yes' : 'no');
export const price = p => (p.price != null ? `${p.price.toFixed(2)} ${esc(p.price_currency || '')}` : '—');
const weight = p => [p.weight_g ? `${p.weight_g} g` : '', p.weight_oz ? `${p.weight_oz} oz` : ''].filter(Boolean).join(' / ') || '—';
const flags = p => tags([p.organic && 'Organic', p.fair_trade && 'Fair Trade', p.single_origin && 'Single origin'].filter(Boolean), 'a');

route('roasters', async (_args, query) => {
  const f = (await api('/facets')).roasters;
  await listPage({
    routeName: 'roasters', kind: 'roasters', kicker: 'Database', title: 'Roasters and brands', query,
    lead: 'Coffee companies from mass-market giants to specialty roasters: who owns them, where they roast, what they are known for.',
    placeholder: 'e.g. Seattle, Nordic, light roast, B Corp',
    filters: [
      { id: 'country', label: 'Country', options: f.country },
      { id: 'segment', label: 'Market segment', options: f.segment, names: SEG },
      { id: 'cert', label: 'Certification', options: f.cert },
    ],
    card: r => `<a class="card" href="#/roaster/${r.roaster_id}"><small>${esc(r.headquarters_city || '')}, ${esc(r.country_of_origin)}${r.founded_year ? ' · since ' + r.founded_year : ''}</small>
      <b>${esc(r.roaster_name)}</b><span>${esc(trim(r.description, 120))}</span>
      <div class="meta"><span class="seg-${esc(r.market_segment)}">${esc(SEG[r.market_segment] || r.market_segment || '')}</span><span>${esc(trim(r.roasting_style, 40))}</span></div></a>`,
  });
});

export function productTable(rows, withRoaster = false) {
  return `<div class="scroll"><table><tr><th>Product</th>${withRoaster ? '<th>Roaster</th>' : ''}<th>Type</th><th>Roast</th><th>Format</th><th>Price</th><th></th></tr>
    ${list(rows, p => `<tr class="click" data-href="#/product/${p.product_id}"><td><a href="#/product/${p.product_id}">${esc(p.product_name)}</a></td>
      ${withRoaster ? `<td>${esc(p.roaster_name)}</td>` : ''}<td>${esc(or(p.coffee_type))}</td><td>${esc(or(p.roast_level))}</td>
      <td>${esc(or(p.format))}</td><td class="mono">${price(p)}</td><td>${flags(p)}</td></tr>`)}</table></div>`;
}

// Whole-row click on product tables.
document.addEventListener('click', e => {
  const tr = e.target.closest('tr[data-href]');
  if (tr && !e.target.closest('a')) location.hash = tr.dataset.href;
});

route('roaster', async ([id]) => {
  const r = await api('/roasters/' + encodeURIComponent(id));
  const site = r.website ? `<a href="https://${esc(r.website.replace(/^https?:\/\//, ''))}" target="_blank" rel="noopener">${esc(r.website)}</a>` : '—';
  app().innerHTML = `
    ${crumb('#/roasters', 'Roasters', r.country_of_origin)}
    <h1>${esc(r.roaster_name)}</h1>
    <p class="lead">${esc(r.description || '')}</p>
    ${kv([['founded', r.founded_year], ['headquarters', [r.headquarters_city, r.country_of_origin].filter(Boolean).join(', ')],
      ['parent company', r.parent_company], ['market segment', SEG[r.market_segment] || r.market_segment], ['website', site, true]])}
    ${sections([['Roasting style', r.roasting_style]])}
    ${r.certifications ? `<h3>Certifications</h3><p>${tags(words(r.certifications), 'c')}</p>` : ''}
    <h2>Products (${r.products.length})</h2>
    ${r.products.length ? productTable(r.products) : '<p class="mute">No products listed for this roaster.</p>'}
    <p><a class="btn alt" href="#/roasters?country=${encodeURIComponent(r.country_of_origin)}">More roasters in ${esc(r.country_of_origin)}</a></p>`;
});

route('products', async (_args, query) => {
  const [f, roasters] = await Promise.all([api('/facets'), api('/roasters')]);
  const names = Object.fromEntries(roasters.map(r => [r.roaster_id, r.roaster_name]));
  await listPage({
    routeName: 'products', kind: 'products', kicker: 'Database', title: 'Products', query, grid: '',
    lead: 'Bags, capsules and cans from the roasters in the database, with type, roast, size, price and certifications.',
    placeholder: 'e.g. Pike Place, decaf, capsules, Colombia',
    filters: [
      { id: 'roaster', label: 'Roaster', options: f.products.roaster, names },
      { id: 'type', label: 'Type', options: f.products.type },
      { id: 'roast', label: 'Roast', options: f.products.roast },
      { id: 'currency', label: 'Currency', options: f.products.currency },
      { id: 'organic', label: 'Organic', checkbox: true },
      { id: 'fair_trade', label: 'Fair Trade', checkbox: true },
      { id: 'single_origin', label: 'Single origin', checkbox: true },
    ],
    render: rows => productTable(rows, true),
  });
});

route('product', async ([id]) => {
  const p = await api('/products/' + encodeURIComponent(id));
  app().innerHTML = `
    ${crumb('#/products', 'Products', p.roaster_name)}
    <h1>${esc(p.product_name)}</h1>
    <p class="lead">by <a href="#/roaster/${p.roaster_id}">${esc(p.roaster_name)}</a></p>
    ${kv([['type', p.coffee_type], ['roast', p.roast_level], ['format', p.format], ['weight', weight(p)], ['price', price(p), true],
      ['organic', yes(p.organic)], ['Fair Trade', yes(p.fair_trade)], ['single origin', yes(p.single_origin)]])}
    ${sections([['Special features', p.special_features], ['Available in', p.countries_available]])}`;
});
