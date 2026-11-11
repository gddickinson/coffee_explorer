// Equirectangular projection shared by the map pages: the JS copy of world_shapes.project() (geo.test.mjs checks
// both agree). lon -180..180 -> x 0..width, lat 90..-90 -> y 0..height.
export function project(lon, lat, width, height) {
  return [(lon + 180) * width / 360, (90 - lat) * height / 180];
}
