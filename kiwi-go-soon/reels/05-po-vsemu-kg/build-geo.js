// Builds geo.js (SVG path data in map-local pixels) from real boundary data:
//  - country outline: Natural Earth 1:10m via world-atlas (ISO 3166 numeric 417)
//  - Lake Issyk-Kul: OpenStreetMap-derived lakes via @geo-maps/earth-lakes-1km (largest polygon in 76–78.5°E, 42–43°N)
//  - oblast (admin-1) shapes: Natural Earth admin-1 via @highcharts/map-collection (data/kg-admin1.topo.json)
// Projection: equirectangular, x scaled by cos(41.5°), fitted to MAP_W px wide.
const fs = require('fs');
const tj = require('topojson-client');
const MAP_W = 840, LAT0 = 41.5, K = Math.cos(LAT0 * Math.PI / 180);

const wa = require('world-atlas/countries-10m.json');
const kgGeom = wa.objects.countries.geometries.filter(g => +g.id === 417);
const country = tj.feature(wa, { type: 'GeometryCollection', geometries: kgGeom }).features[0].geometry;
const rings = country.type === 'Polygon' ? country.coordinates : country.coordinates.flat();

let mnx = 1e9, mny = 1e9, mxx = -1e9, mxy = -1e9;
for (const [lo, la] of rings[0]) { const x = lo * K, y = -la; mnx = Math.min(mnx, x); mxx = Math.max(mxx, x); mny = Math.min(mny, y); mxy = Math.max(mxy, y); }
const S = MAP_W / (mxx - mnx);
const P = ([lo, la]) => [(lo * K - mnx) * S, (-la - mny) * S];
const MAP_H = (mxy - mny) * S;
const d = ring => ring.map((p, i) => { const [x, y] = P(p); return (i ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1); }).join('') + 'Z';

const ad = JSON.parse(fs.readFileSync(__dirname + '/data/kg-admin1.topo.json'));
const geoms = ad.objects.default.geometries;
const regions = {};
function centroid(ring) { // area centroid in projected space
  let a = 0, cx = 0, cy = 0; const pts = ring.map(P);
  for (let i = 0; i < pts.length - 1; i++) { const [x0, y0] = pts[i], [x1, y1] = pts[i + 1]; const c = x0 * y1 - x1 * y0; a += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c; }
  return [cx / (3 * a), cy / (3 * a)];
}
for (const g of geoms) {
  const f = tj.feature(ad, g).geometry;
  const rs = f.type === 'Polygon' ? f.coordinates : f.coordinates.flat();
  regions[g.id] = { d: rs.map(d).join(''), c: centroid(rs[0]).map(v => +v.toFixed(1)) };
}
const inner = tj.mesh(ad, ad.objects.default, (a, b) => a !== b);
const innerD = inner.coordinates.map(l => l.map((p, i) => { const [x, y] = P(p); return (i ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1); }).join('')).join('');
const all = rings[0].map(P); let cx = 0, cy = 0; { const c = centroid(rings[0]); cx = c[0]; cy = c[1]; }
const lakes = JSON.parse(fs.readFileSync(require.resolve('@geo-maps/earth-lakes-1km/map.geo.json')));
let best = null;
for (const g of lakes.geometries) for (const poly of (g.type === 'MultiPolygon' ? g.coordinates : [g.coordinates])) {
  const r = poly[0], xs = r.map(p => p[0]), ys = r.map(p => p[1]);
  if (Math.min(...xs) > 76 && Math.max(...xs) < 78.5 && Math.min(...ys) > 42 && Math.max(...ys) < 43 && (!best || r.length > best.length)) best = r;
}
const lake = d(best);
console.log('issyk-kul pts', best.length);
const out = { lake, W: MAP_W, H: +MAP_H.toFixed(1), outer: d(rings[0]), holes: rings.slice(1).map(d), regions, inner: innerD, hub: [+cx.toFixed(1), +cy.toFixed(1)] };
fs.writeFileSync(__dirname + '/geo.js', 'window.GEO = ' + JSON.stringify(out) + ';\n');
console.log('W', MAP_W, 'H', out.H, 'pts', rings[0].length, 'holes', out.holes.length, 'hub', out.hub);
for (const [k, v] of Object.entries(regions)) console.log(k, v.c);
