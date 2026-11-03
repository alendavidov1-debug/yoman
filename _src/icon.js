const { chromium } = require('playwright');
const svg = (pad) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" fill="#17181b"/>
<g transform="translate(256 ${pad?262:250}) scale(${pad?1.9:2.4}) translate(-90 -45)" fill="none" stroke-linecap="round">
<path d="M50 45h80" stroke="#fff" stroke-opacity=".9" stroke-width="7"/>
<path d="M42 20v50M138 20v50" stroke="#e10600" stroke-width="14"/>
<path d="M27 29v32M153 29v32" stroke="#e10600" stroke-width="10"/></g>
<rect x="${pad?176:156}" y="${pad?380:396}" width="${pad?160:200}" height="${pad?10:12}" rx="5" fill="#e10600"/></svg>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const [name, size, pad] of [['icon-512.png',512,0],['icon-192.png',192,0],['apple-touch-icon.png',180,0],['maskable-512.png',512,1]]) {
    await p.setViewportSize({ width: size, height: size });
    await p.setContent(`<html><body style="margin:0">${svg(pad).replace('<svg ', `<svg width="${size}" height="${size}" `)}</body></html>`);
    await p.screenshot({ path: 'site/icons/' + name, omitBackground: false });
  }
  await b.close();
})();
