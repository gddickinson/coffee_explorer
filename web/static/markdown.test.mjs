// node markdown.test.mjs: the guide/history renderer handles the constructs used in coffee_*.md and never passes raw HTML.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { render, inline } from './markdown.js';

const { html, toc } = render('# Title\n\n## Coffee Species\n\n### Coffea Arabica\n**60-70% of global production**\n\nText *soft* and `code`.\n\n- one\n- two\n  continued\n\n1. first\n2. second\n\n---\n\n## Coffee Species\n');
assert.match(html, /<h2 id="title">Title<\/h2>/);
assert.match(html, /<h3 id="coffee-species">Coffee Species<\/h3>/);
assert.match(html, /<h3 id="coffee-species-1">/, 'duplicate headings get unique ids');
assert.match(html, /<h4 id="coffea-arabica">/);
assert.match(html, /<p><strong>60-70% of global production<\/strong><\/p>/);
assert.match(html, /<em>soft<\/em>/);
assert.match(html, /<code>code<\/code>/);
assert.match(html, /<ul><li>one<\/li><li>two continued<\/li><\/ul>/);
assert.match(html, /<ol><li>first<\/li><li>second<\/li><\/ol>/);
assert.match(html, /<hr>/);
assert.deepEqual(toc.map(t => t.level), [1, 2, 3, 2]);

// Safety: HTML in the source is escaped; only http(s) links become anchors.
assert.equal(inline('<script>alert(1)</script>'), '&lt;script&gt;alert(1)&lt;/script&gt;');
assert.equal(inline('[x](javascript:alert(1))'), '[x](javascript:alert(1))');
assert.match(inline('[SCA](https://sca.coffee)'), /<a href="https:\/\/sca.coffee" target="_blank" rel="noopener">SCA<\/a>/);
assert.equal(inline('2 * 3 * 4'), '2 * 3 * 4');

// The real files render without leftover markdown markers in headings.
for (const f of ['coffee_guide.md', 'coffee_history.md']) {
  const r = render(readFileSync(new URL('../../' + f, import.meta.url), 'utf8'));
  assert.ok(r.toc.length > 10, f);
  assert.ok(!/<h\d[^>]*>#/.test(r.html), f);
}
console.log('markdown: all ok');
