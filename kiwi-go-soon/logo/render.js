const fs=require('fs');const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const svg=fs.readFileSync('kiwi-go-logo.svg','utf8');
for(const s of [181,512,1024]){const p=await b.newPage({viewport:{width:s,height:s}});
await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ',`<svg width="${s}" height="${s}" `)}</body></html>`);
await p.screenshot({path:s==181?'/tmp/claude-0/prev/cmp181.png':`kiwi-go-logo-${s}.png`,omitBackground:true});await p.close();}
await b.close();})();
