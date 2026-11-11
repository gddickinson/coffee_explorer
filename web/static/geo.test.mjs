// node geo.test.mjs: the JS projection gives the same pixels as world_shapes.project() (values computed in Python on a
// 1000 x 500 map; tests/test_web.py checks the Python side and that every region marker falls on land).
import assert from 'node:assert/strict';
import { project } from './geo.js';

const cases = [[38.5, 6.0, 606.9444, 233.3333], [-155.9, 19.6, 66.9444, 195.5556], [-76.7, 18.1, 286.9444, 199.7222],
  [0, 0, 500, 250], [180, -90, 1000, 500], [-180, 90, 0, 0]];
for (const [lon, lat, x, y] of cases) {
  const [px, py] = project(lon, lat, 1000, 500);
  assert.ok(Math.abs(px - x) < 1e-3 && Math.abs(py - y) < 1e-3, `${lon},${lat} -> ${px},${py}`);
}
console.log('geo: all ok');
