// Static-site data layer: answers api(path) calls from the JSON files exported by scripts/build_static.py.
// Plain paths map to files (api/coffees/3.json). List endpoints with a query string and /search are filtered here from
// the exported full lists with the same rules as web/search.py (search_engine.js). The tasting journal is personal and
// local-only: it is never exported, so its pages show needsServer() instead.
import { KINDS, filterRows } from './search_engine.js';

const files = new Map();
async function file(rel) {
  if (!files.has(rel)) {
    files.set(rel, fetch('api/' + rel + '.json').then(r => { if (!r.ok) throw new Error(`${r.status} ${rel}`); return r.json(); }));
  }
  return files.get(rel);
}

export async function staticApi(path, body) {
  const [p, qs] = path.split('?');
  const q = Object.fromEntries(new URLSearchParams(qs || ''));
  const clean = p.replace(/^\/+|\/+$/g, '');
  if (clean.startsWith('journal') || body) throw new Error('The tasting journal needs the full app (Python server).');
  if (clean === 'search') {
    const words = (q.q || '').trim();
    const lists = await Promise.all(KINDS.map(k => words ? file(k) : []));
    return Object.fromEntries(KINDS.map((k, i) => [k, words ? filterRows(k, lists[i], { q: words }) : []]));
  }
  if (KINDS.includes(clean)) return filterRows(clean, await file(clean), q);
  return file(clean);
}
