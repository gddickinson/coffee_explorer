// Search and filter rules for list pages: an exact mirror of web/search.py, used by static_api.js to answer
// /api/<kind>?... and /api/search?q=... on the static site from the exported full lists.
export const SPECS = {
  coffees: { text: ['name', 'origin_country', 'origin_region', 'variety', 'processing_method', 'flavor_profile', 'aroma', 'tasting_notes'],
    exact: { country: 'origin_country' }, contains: { roast: 'roast_level', process: 'processing_method' }, flag: {}, id: 'id' },
  varieties: { text: ['name', 'species', 'origin_country', 'characteristics', 'flavor_notes', 'notes'],
    exact: { species: 'species' }, contains: {}, flag: {}, id: 'id' },
  regions: { text: ['name', 'country', 'climate', 'soil_type', 'famous_coffees', 'description'],
    exact: { country: 'country' }, contains: {}, flag: {}, id: 'id' },
  brewing: { text: ['name', 'category', 'grind_size', 'equipment_needed', 'flavor_characteristics', 'description'],
    exact: { category: 'category', difficulty: 'difficulty_level' }, contains: {}, flag: {}, id: 'id' },
  roasters: { text: ['roaster_name', 'parent_company', 'headquarters_city', 'country_of_origin', 'roasting_style', 'certifications', 'description'],
    exact: { country: 'country_of_origin', segment: 'market_segment' }, contains: { cert: 'certifications' }, flag: {}, id: 'roaster_id' },
  products: { text: ['product_name', 'roaster_name', 'coffee_type', 'roast_level', 'format', 'special_features', 'countries_available'],
    exact: { roaster: 'roaster_id', type: 'coffee_type', roast: 'roast_level', currency: 'price_currency' }, contains: {},
    flag: { organic: 'organic', fair_trade: 'fair_trade', single_origin: 'single_origin' }, id: 'product_id' },
};
export const KINDS = Object.keys(SPECS);

// Python's str(): None -> 'None', True -> 'True', numbers as written. Only used for exact comparisons.
const pyStr = v => v === null || v === undefined ? 'None' : v === true ? 'True' : v === false ? 'False' : String(v);
const has = v => v !== undefined && v !== null && v !== '';

export function filterRows(kind, rows, params = {}) {
  const spec = SPECS[kind];
  const words = String(params.q || '').toLowerCase().split(/\s+/).filter(Boolean);
  return rows.filter(r => {
    for (const [p, col] of Object.entries(spec.exact)) if (has(params[p]) && pyStr(r[col]) !== String(params[p])) return false;
    for (const [p, col] of Object.entries(spec.contains))
      if (params[p] && !String(r[col] || '').toLowerCase().includes(String(params[p]).toLowerCase())) return false;
    for (const [p, col] of Object.entries(spec.flag)) if (String(params[p] || '') === '1' && !r[col]) return false;
    if (words.length) {
      const text = spec.text.map(f => String(r[f] || '')).join(' ').toLowerCase();
      if (!words.every(w => text.includes(w))) return false;
    }
    return true;
  });
}
