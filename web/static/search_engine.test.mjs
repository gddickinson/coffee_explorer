// node search_engine.test.mjs: the JS filters must give the same results as web/search.py. Expected ids below were
// computed by running web.search.filter_rows on the same rows (tests/test_web.py also checks parity on the full data).
import assert from 'node:assert/strict';
import { filterRows } from './search_engine.js';
import { parseBrewTime } from './timer.js';

const products = [
  { product_id: 1, roaster_id: 3, product_name: 'Pike Place Roast', roaster_name: 'Starbucks', coffee_type: 'blend', roast_level: 'medium', organic: false, price_currency: 'USD', special_features: null },
  { product_id: 2, roaster_id: 4, product_name: 'Hair Bender', roaster_name: 'Stumptown', coffee_type: 'blend', roast_level: 'medium', organic: true, price_currency: 'USD', special_features: 'Citrus, dark chocolate' },
  { product_id: 3, roaster_id: 3, product_name: 'Ethiopia Kayon', roaster_name: 'Starbucks', coffee_type: 'single-origin', roast_level: 'light', organic: true, price_currency: 'GBP', special_features: 'Floral' },
];
const pcases = [[{}, [1, 2, 3]], [{ q: 'starbucks' }, [1, 3]], [{ q: 'BLEND chocolate' }, [2]], [{ roaster: '3' }, [1, 3]],
  [{ organic: '1' }, [2, 3]], [{ organic: '1', roaster: '3' }, [3]], [{ q: 'none' }, []], [{ roast: 'medium', currency: 'USD' }, [1, 2]], [{ q: 'zzz' }, []]];
for (const [q, ids] of pcases) assert.deepEqual(filterRows('products', products, q).map(r => r.product_id), ids, JSON.stringify(q));

const coffees = [
  { id: 1, name: 'Yirgacheffe', origin_country: 'Ethiopia', roast_level: 'Light to Medium', processing_method: 'Washed', flavor_profile: 'Floral, citrus' },
  { id: 2, name: 'Santos', origin_country: 'Brazil', roast_level: 'Medium to Dark', processing_method: 'Natural (dry)', flavor_profile: 'Nutty' },
];
const ccases = [[{ roast: 'light' }, [1]], [{ roast: 'Dark' }, [2]], [{ roast: 'Medium' }, [1, 2]], [{ process: 'natural' }, [2]],
  [{ country: 'Brazil', q: 'nut' }, [2]], [{ country: 'brazil' }, []]];
for (const [q, ids] of ccases) assert.deepEqual(filterRows('coffees', coffees, q).map(r => r.id), ids, JSON.stringify(q));

// Brew-time presets for the timer (values in the database).
assert.equal(parseBrewTime('25-30 seconds'), 25);
assert.equal(parseBrewTime('2.5-3 minutes'), 150);
assert.equal(parseBrewTime('4 minutes'), 240);
assert.equal(parseBrewTime('12-24 hours'), null);
assert.equal(parseBrewTime(''), null);
console.log('search_engine: all ok');
