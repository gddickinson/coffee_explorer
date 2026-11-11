"""Web interface tests: every exported endpoint answers, the static build is complete, and the JS engine tests pass.

Run: python -m pytest -q tests/test_web.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from web.app import STATIC, STATIC_ENDPOINTS, app  # noqa: E402

client = TestClient(app)


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200 and "static/main.js" in r.text


@pytest.mark.parametrize("path", STATIC_ENDPOINTS)
def test_endpoint(path):
    r = client.get("/api" + path)
    assert r.status_code == 200, r.text
    assert r.json() is not None


def test_static_build(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert (tmp_path / "site" / "index.html").read_text().count("APP_STATIC") == 1
    for path in STATIC_ENDPOINTS:
        assert (tmp_path / "site" / "api" / (path.strip("/") + ".json")).exists()


def test_static_assets_referenced_exist():
    html = (STATIC / "index.html").read_text()
    for name in ("style.css", "main.js"):
        assert f"static/{name}" in html and (STATIC / name).exists()


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_js_engine():
    tests = sorted(STATIC.glob("*.test.mjs"))
    for t in tests:
        r = subprocess.run(["node", str(t)], capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr


# --- Coffee Collection Explorer: project-specific API tests ---------------------------------------------------------
import hashlib  # noqa: E402
import json  # noqa: E402

from web import data  # noqa: E402
from web.app import KIND_TABLE  # noqa: E402


def _md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def test_counts_match_database():
    s = client.get("/api/stats").json()
    assert (s["coffees"], s["varieties"], s["roasters"], s["products"], s["brewing_methods"], s["regions"]) == (29, 20, 28, 61, 12, 15)
    for kind in KIND_TABLE:
        assert len(client.get(f"/api/{kind}").json()) == len(data.rows(KIND_TABLE[kind]))


def test_database_opened_read_only():
    before = _md5(data.DB_PATH)
    conn = data.connect()
    with pytest.raises(Exception):
        conn.execute("UPDATE coffees SET name = 'x'")
    conn.close()
    for path in STATIC_ENDPOINTS[:20]:
        client.get("/api" + path)
    assert _md5(data.DB_PATH) == before


def test_filters():
    light = client.get("/api/coffees", params={"roast": "Light"}).json()
    assert light and all("light" in c["roast_level"].lower() for c in light)
    eth = client.get("/api/coffees", params={"country": "Ethiopia"}).json()
    assert {c["name"] for c in eth} == {"Yirgacheffe", "Sidamo", "Harrar"}
    usa = client.get("/api/roasters", params={"country": "USA", "segment": "specialty"}).json()
    assert usa and all(r["country_of_origin"] == "USA" and r["market_segment"] == "specialty" for r in usa)
    org = client.get("/api/products", params={"organic": "1"}).json()
    assert org and all(p["organic"] for p in org)
    assert client.get("/api/varieties", params={"q": "zzzz-none"}).json() == []
    res = client.get("/api/search", params={"q": "bourbon"}).json()
    assert set(res) == set(KIND_TABLE) and res["varieties"] and res["coffees"]


def test_details_and_links():
    assert client.get("/api/coffees/99999").status_code == 404
    assert client.get("/api/content/nope").status_code == 404
    jbm = next(c for c in client.get("/api/coffees").json() if c["name"] == "Jamaica Blue Mountain")
    d = client.get(f"/api/coffees/{jbm['id']}").json()
    assert [v["name"] for v in d["varieties"]] == ["Typica"] and d["regions"][0]["name"] == "Blue Mountain"
    sb = next(r for r in client.get("/api/roasters").json() if r["roaster_name"] == "Starbucks")
    prods = client.get(f"/api/roasters/{sb['roaster_id']}").json()["products"]
    assert prods and all(p["roaster_id"] == sb["roaster_id"] for p in prods)
    w = client.get("/api/world").json()
    assert len(w["regions"]) == 15 and "Africa" in w["continents"]
    assert client.get("/api/content/guide").json()["markdown"].startswith("# Complete Coffee Guide")


def test_journal_local_only(tmp_path, monkeypatch):
    jf = tmp_path / "journal.json"
    monkeypatch.setenv("COFFEE_JOURNAL", str(jf))
    assert client.get("/api/journal").json()["entries"] == []
    r = client.post("/api/journal", json={"coffee_name": "Kona", "rating": 4, "notes": "nutty"})
    assert r.status_code == 200 and json.loads(jf.read_text())[0]["coffee_name"] == "Kona"
    assert client.post("/api/journal", json={"coffee_name": "", "rating": 4}).status_code == 400
    assert client.post("/api/journal", json={"coffee_name": "Kona", "rating": 9}).status_code == 400
    assert not any(p.startswith("/journal") for p in STATIC_ENDPOINTS)


def test_static_build_has_no_journal(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert not list((tmp_path / "site").rglob("*journal*.json"))


PARITY = [("coffees", {"roast": "Medium"}), ("coffees", {"q": "chocolate", "process": "Washed"}), ("coffees", {"q": "kenya"}),
          ("varieties", {"species": "Arabica", "q": "kenya"}), ("roasters", {"cert": "Direct Trade"}),
          ("roasters", {"country": "USA", "q": "portland"}), ("products", {"fair_trade": "1"}),
          ("products", {"roaster": "1", "q": "roast"}), ("products", {"type": "espresso", "currency": "USD"}),
          ("brewing", {"category": "Immersion"}), ("regions", {"q": "volcanic"}), ("regions", {"country": "Brazil"})]


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_static_search_parity(tmp_path):
    """static_api.js filtering (search_engine.js) returns the same ids as the server for the same queries."""
    full = {kind: client.get(f"/api/{kind}").json() for kind in KIND_TABLE}
    (tmp_path / "full.json").write_text(json.dumps(full))
    (tmp_path / "cases.json").write_text(json.dumps(PARITY))
    script = (f"import {{ filterRows, SPECS }} from {json.dumps((STATIC / 'search_engine.js').as_uri())};\n"
              "import { readFileSync } from 'node:fs';\n"
              f"const full = JSON.parse(readFileSync({json.dumps(str(tmp_path / 'full.json'))}, 'utf8'));\n"
              f"const cases = JSON.parse(readFileSync({json.dumps(str(tmp_path / 'cases.json'))}, 'utf8'));\n"
              "console.log(JSON.stringify(cases.map(([k, q]) => filterRows(k, full[k], q).map(r => r[SPECS[k].id]))));")
    r = subprocess.run(["node", "--input-type=module", "-e", script], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    js = json.loads(r.stdout)
    from web.search import SPECS
    for (kind, q), got in zip(PARITY, js):
        want = [row[SPECS[kind]["id"]] for row in client.get(f"/api/{kind}", params=q).json()]
        assert got == want, (kind, q)
        assert want, (kind, q)  # every case should exercise a non-empty result
