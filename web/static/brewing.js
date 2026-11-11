// Brewing methods: list with category/difficulty filters, a method page with parameters, and the brewing timer.
import { route, api, app, esc, list } from './core.js';
import { listPage, kv, sections, crumb, trim, or } from './ui.js';
import { mountTimer, parseBrewTime } from './timer.js';

route('brewing', async (_args, query) => {
  const f = (await api('/facets')).brewing;
  await listPage({
    routeName: 'brewing', kind: 'brewing', kicker: 'Brew', title: 'Brewing methods', query,
    lead: 'From espresso to cold brew: grind, water temperature, time and ratio for each method, with a timer for when you brew.',
    placeholder: 'e.g. immersion, paper filter, coarse',
    filters: [
      { id: 'category', label: 'Category', options: f.category },
      { id: 'difficulty', label: 'Difficulty', options: f.difficulty },
    ],
    extra: '<p><a class="btn alt" href="#/timer">Open the brewing timer</a></p>',
    card: m => `<a class="card" href="#/method/${m.id}"><small>${esc(m.category)} · ${esc(m.difficulty_level)}</small>
      <b>${esc(m.name)}</b><span>${esc(trim(m.description, 110))}</span>
      <div class="meta"><span>${esc(or(m.grind_size, ''))} grind</span><span>${m.water_temp_c ? m.water_temp_c + ' °C' : ''} · ${esc(or(m.brew_time, ''))}</span></div></a>`,
  });
});

route('method', async ([id]) => {
  const m = await api('/brewing/' + encodeURIComponent(id));
  const temp = m.water_temp_c ? `${m.water_temp_c} °C (${m.water_temp_f} °F)` : '—';
  app().innerHTML = `
    ${crumb('#/brewing', 'Brewing methods', m.category)}
    <h1>${esc(m.name)}</h1>
    <p class="lead">${esc(m.description || '')}</p>
    <div class="side rev">
      <div>
        ${kv([['grind size', m.grind_size], ['water temperature', temp], ['brew time', m.brew_time],
          ['coffee : water', m.coffee_water_ratio], ['difficulty', m.difficulty_level], ['category', m.category]])}
        ${sections([['Equipment', m.equipment_needed], ['Flavour characteristics', m.flavor_characteristics]])}
      </div>
      <div id="timer"></div>
    </div>`;
  const preset = parseBrewTime(m.brew_time);
  mountTimer(document.getElementById('timer'), preset, m.name);
  if (preset === null) {
    document.getElementById('timer').insertAdjacentHTML('beforeend',
      `<p class="small mute">Brew time "${esc(m.brew_time)}" is not a countdown in minutes; set the timer yourself.</p>`);
  }
});

route('timer', async () => {
  const methods = await api('/brewing');
  app().innerHTML = `<p class="kicker">Brew</p><h1>Brewing timer</h1>
    <p class="lead">Set minutes and seconds, or pick a method to load its brew time.</p>
    <div class="side rev"><div><label for="t-method">Method</label><select id="t-method"><option value="">Custom</option>
      ${list(methods, m => `<option value="${m.id}">${esc(m.name)} (${esc(m.brew_time)})</option>`)}</select>
      <p class="small mute">Presets use the start of each method's brew-time range.</p></div><div id="timer"></div></div>`;
  const host = document.getElementById('timer');
  mountTimer(host);
  document.getElementById('t-method').addEventListener('change', e => {
    const m = methods.find(x => String(x.id) === e.target.value);
    mountTimer(host, m ? parseBrewTime(m.brew_time) : null, m ? m.name : '');
  });
});
