// Exercise the delivered page in Chromium; retain only JSON, no extra pictures.
import {chromium} from '/opt/imd-tools/playwright-mcp/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import http from 'node:http';
const content=fs.readFileSync('dist/index.html');
const server=http.createServer((req,res)=>{res.writeHead(200,{'content-type':'text/html'});res.end(content)});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
let browser;
try {
 browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const page=await browser.newPage(); const errors=[];
 page.on('pageerror',e=>errors.push(String(e)));
 const results=[];
 for(const width of [320,390,1440]){
  await page.setViewportSize({width,height:900});
  await page.goto(`http://127.0.0.1:${server.address().port}/`,{waitUntil:'load'});
  results.push(await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
   articles:document.querySelectorAll('article').length,
   paintedUses:document.querySelectorAll('article use').length,
   unresolvedUses:[...document.querySelectorAll('article use')].filter(x=>!document.querySelector(x.getAttribute('href'))).length,
   visibleFirstRecord:document.querySelector('article').getBoundingClientRect().top<innerHeight,
   loadedDefinitions:[...document.querySelectorAll('defs image')].filter(x=>x.getAttribute('href').startsWith('data:image/jpeg;base64,')).length})));
 }
 if(errors.length||results.some(r=>r.scrollWidth>r.width||r.articles!==100||r.unresolvedUses||!r.visibleFirstRecord))throw Error(JSON.stringify({errors,results}));
 fs.writeFileSync('gathering/gallery-checks40.json',JSON.stringify({ok:true,errors,results,limitations:'DOM and layout checks only; no independent visual review.'},null,2)+'\n');
 console.log(JSON.stringify({ok:true,results}));
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
