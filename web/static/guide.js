// The Coffee Guide and Coffee History, rendered from the repo's markdown files with a contents sidebar and a filter
// that hides sections not mentioning the search words.
import { route, api, app, esc, list } from './core.js';
import { render } from './markdown.js';

const PAGES = {
  guide: { title: 'Complete Coffee Guide', kicker: 'Read', lead: 'Species, regions, processing, roasting, brewing, cupping, storage, health, sustainability and a glossary.' },
  history: { title: 'The History of Coffee', kicker: 'Read', lead: 'From Ethiopian legend to the fourth wave: how coffee spread, the cultures it built, and its future.' },
};

async function page(name, query) {
  const meta = PAGES[name];
  const { markdown } = await api('/content/' + name);
  const { html, toc } = render(markdown);
  const top = toc.filter(t => t.level === 2);
  app().innerHTML = `<p class="kicker">${meta.kicker}</p>
    <div class="side doc">
      <aside class="panel toc"><label for="d-q">Find in page</label><input id="d-q" type="search" value="${esc(query.q || '')}" placeholder="e.g. Geisha, crema">
        <p id="d-n" class="small mute"></p>
        <nav aria-label="Contents">${list(top, t => `<a href="#/${name}?s=${t.id}" data-s="${t.id}">${esc(t.text)}</a>`)}</nav></aside>
      <article class="md" id="md">${html}</article>
    </div>`;
  const md = document.getElementById('md');
  // Group the article into sections (each h3 = "##" heading plus everything until the next one) for filtering.
  const groups = [];
  let cur = null;
  for (const el of [...md.children]) {
    if (el.tagName === 'H3' || !cur) { cur = []; groups.push(cur); }
    cur.push(el);
  }
  const filter = () => {
    const words = document.getElementById('d-q').value.toLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const g of groups) {
      const hit = !words.length || words.every(w => g.some(el => el.textContent.toLowerCase().includes(w)));
      g.forEach(el => { el.hidden = !hit; });
      shown += hit && g[0].tagName === 'H3';
    }
    document.getElementById('d-n').textContent = words.length ? `${shown} of ${top.length} sections match` : '';
  };
  document.getElementById('d-q').addEventListener('input', filter);
  filter();
  // Contents links scroll within the page (the hash route stays the same).
  app().querySelector('.toc nav').addEventListener('click', e => {
    const a = e.target.closest('a[data-s]');
    if (!a) return;
    e.preventDefault();
    const h = document.getElementById(a.dataset.s);
    if (h && h.hidden) { document.getElementById('d-q').value = ''; filter(); }
    h?.scrollIntoView({ behavior: 'smooth' });
  });
  if (query.s) setTimeout(() => document.getElementById(query.s)?.scrollIntoView(), 0);
}

route('guide', (_a, q) => page('guide', { ...q }));
route('history', (_a, q) => page('history', { ...q }));
