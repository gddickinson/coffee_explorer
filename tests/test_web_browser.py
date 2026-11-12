"""Browser checks on the built static site (skipped where Playwright/Chrome is unavailable, e.g. CI).

Run: python -m pytest -q tests/test_web_browser.py
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sync_api = pytest.importorskip("playwright.sync_api")

PIN_FILL = "rgb(255, 107, 107)"  # --accent2 in style_app.css


@pytest.fixture(scope="module")
def page(tmp_path_factory):
    import build_static
    import screenshots
    site = tmp_path_factory.mktemp("s") / "site"
    build_static.build(site)
    base = screenshots.serve(site)
    with sync_api.sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome")
        except Exception:
            try:
                browser = p.chromium.launch()
            except Exception as e:  # no browser installed
                pytest.skip(f"no browser: {e}")
        pg = browser.new_page()
        pg.base = base
        yield pg
        browser.close()


@pytest.mark.parametrize("route", ["", "map", "region/1"])
def test_map_markers_coloured(page, route):
    """Markers keep their colour on every map (the home map has no links, so the class must not live on <a>)."""
    page.goto(page.base + "#/" + route)
    page.wait_for_selector("svg.world .pin .dot")
    fills = page.eval_on_selector_all("svg.world .pin:not(.on) .dot", "els => els.map(e => getComputedStyle(e).fill)")
    assert len(fills) >= 14 and set(fills) == {PIN_FILL}, fills
    assert page.eval_on_selector_all("a a", "els => els.length") == 0  # no nested links
