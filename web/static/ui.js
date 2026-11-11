// Shared building blocks for the database pages: filterable list pages that keep their filters in the URL, and
// key/value detail panels.
import { api, app, esc, list } from './core.js';

export const trim = (s, n) => { s = s || ''; return s.length > n ? s.slice(0, n - 1) + '…' : s; };
export const words = s => String(s || '').split(',').map(t => t.trim()).filter(Boolean);
export const or = (v, dash = '—') => (v === null || v === undefined || v === '' ? dash : v);

// <option>s from a {value: count} facet or a [value, label] list.
export function options(src, current, names = {}) {
  const pairs = Array.isArray(src) ? src : Object.entries(src || {}).map(([v, n]) => [v, `${names[v] || v} (${n})`]);
  return '<option value="">All</option>' + list(pairs, ([v, label]) =>
    `<option value="${esc(v)}" ${String(v) === String(current ?? '') ? 'selected' : ''}>${esc(label)}</option>`);
}

// A list page: search box + selects/checkboxes, results rendered by card(row), URL kept in step (#/<route>?...).
// filters: [{ id, label, options: facet-or-pairs, names?, checkbox? }]; render(rows) overrides the card grid (e.g. a table).
export async function listPage({ routeName, kind, kicker, title, lead, placeholder, filters = [], card, render, query, grid = 'grid', extra = '' }) {
  app().innerHTML = `
    <p class="kicker">${esc(kicker)}</p><h1>${esc(title)}</h1>
    <p class="lead">${lead}</p>${extra}
    <div class="filters panel">
      <div class="fq"><label for="f-q">Search</label><input id="f-q" type="search" placeholder="${esc(placeholder)}" value="${esc(query.q || '')}"></div>
      ${list(filters, f => f.checkbox
        ? `<div class="fchk"><label><input type="checkbox" id="f-${f.id}" ${query[f.id] === '1' ? 'checked' : ''}> ${esc(f.label)}</label></div>`
        : `<div><label for="f-${f.id}">${esc(f.label)}</label><select id="f-${f.id}">${options(f.options, query[f.id], f.names)}</select></div>`)}
      <div class="freset"><button class="alt" id="f-reset" type="button">Clear</button></div>
    </div>
    <p id="count" class="mute small" aria-live="polite"></p>
    <div id="results" class="${grid}"></div>`;
  const ids = ['q', ...filters.map(f => f.id)];
  const el = id => document.getElementById('f-' + id);
  const read = () => Object.fromEntries(ids.map(k => [k, el(k).type === 'checkbox' ? (el(k).checked ? '1' : '') : el(k).value]));
  let seq = 0;
  async function refresh() {
    const n = ++seq;
    const qs = new URLSearchParams(Object.entries(read()).filter(([, v]) => v)).toString();
    history.replaceState(null, '', `#/${routeName}${qs ? '?' + qs : ''}`);
    const rows = await api(`/${kind}${qs ? '?' + qs : ''}`);
    if (n !== seq) return;
    document.getElementById('count').textContent = `${rows.length} shown`;
    document.getElementById('results').innerHTML = !rows.length ? '<p class="mute">Nothing matches these filters.</p>'
      : render ? render(rows) : list(rows, card);
  }
  ids.forEach(k => el(k).addEventListener(k === 'q' ? 'input' : 'change', refresh));
  el('reset').addEventListener('click', () => {
    ids.forEach(k => { if (el(k).type === 'checkbox') el(k).checked = false; else el(k).value = ''; });
    refresh();
  });
  await refresh();
}

// Grid of labelled values: [[label, value, raw?]] (raw values are trusted HTML built by the caller).
export function kv(pairs) {
  return `<div class="kv">${list(pairs.filter(p => p[1] !== undefined), ([label, value, raw]) =>
    `<div><b>${raw ? value : esc(or(value))}</b><span>${esc(label)}</span></div>`)}</div>`;
}

// Titled text sections, skipping empty ones.
export function sections(pairs) {
  return list(pairs.filter(([, v]) => v), ([h, v]) => `<h3>${esc(h)}</h3><p>${esc(v)}</p>`);
}

export const crumb = (href, label, rest = '') => `<p class="kicker"><a href="${href}">${esc(label)}</a>${rest ? ' / ' + esc(rest) : ''}</p>`;
