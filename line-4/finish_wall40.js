// One-time export of generated pigment; ancestor rock and marks stay exact.
'use strict';
const fs=require('node:fs'),zlib=require('node:zlib'),crypto=require('node:crypto');
const {decode,thumbnail}=require('../gathering/thumbnail.js');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const before=fs.readFileSync('artifacts/line-4/wall-v19.png');
const candidateBytes=fs.readFileSync('artifacts/line-4/wall-v20.png');
if(hash(before)!=='b9de39a8803bca8403c12f1bf19d89e9af81833d610edffc039b22e999393e32')throw Error('wrong ancestor');
const old=decode(before),candidate=decode(candidateBytes);
if(old.width!==1254||old.height!==1254||candidate.width!==1254||candidate.height!==1254)throw Error('wrong dimensions');
const pixels=Buffer.from(old.pixels), left=330,top=1000,sx=445,sy=1165,width=74,height=78;
function motif(x,y){
  const dx=x-481,dy=y-1191,angle=-0.62;
  const u=dx*Math.cos(angle)+dy*Math.sin(angle),v=-dx*Math.sin(angle)+dy*Math.cos(angle);
  return (u*u/36**2+v*v/14**2<=1) || [[510,1207],[497,1222],[511,1235]].some(([a,b])=>Math.hypot(x-a,y-b)<7);
}
let changed=0;
for(let y=0;y<height;y++)for(let x=0;x<width;x++){
 const gx=sx+x,gy=sy+y;if(!motif(gx,gy))continue;
 const p=(gy*candidate.width+gx)*candidate.channels;
 const [r,g,b]=candidate.pixels.subarray(p,p+3);
 if(r>150||g>100||b>80)continue;
 const red=r>g*1.4&&r>70;
 const a=Math.min(.9,Math.max(0,(red?150-g:135-r)/110));
 if(a<.18)continue;
 const pigment=red?[142,55,25]:[44,31,22],dest=((top+y)*old.width+left+x)*3;
 for(let c=0;c<3;c++)pixels[dest+c]=Math.round(pixels[dest+c]*(1-a)+pigment[c]*a);
 changed++;
}
if(changed<300)throw Error('insufficient pigment');
function crc32(b){let c=0xffffffff;for(const v of b){c^=v;for(let i=0;i<8;i++)c=(c>>>1)^((c&1)?0xedb88320:0);}return(c^0xffffffff)>>>0;}
function chunk(n,b){const k=Buffer.from(n),s=Buffer.alloc(4),c=Buffer.alloc(4);s.writeUInt32BE(b.length);c.writeUInt32BE(crc32(Buffer.concat([k,b])));return Buffer.concat([s,k,b,c]);}
const header=Buffer.alloc(13);header.writeUInt32BE(old.width);header.writeUInt32BE(old.height,4);header[8]=8;header[9]=2;
const stride=old.width*3,scan=Buffer.alloc(old.height*(stride+1));
for(let y=0;y<old.height;y++)pixels.copy(scan,y*(stride+1)+1,y*stride,(y+1)*stride);
const png=Buffer.concat([Buffer.from('89504e470d0a1a0a','hex'),chunk('IHDR',header),chunk('IDAT',zlib.deflateSync(scan,{level:9})),chunk('IEND',Buffer.alloc(0))]);
const jpg=thumbnail(png,512,75);if(jpg.length>100000)throw Error('preview too large');
let outside=0;
for(let y=0;y<old.height;y++)for(let x=0;x<old.width;x++){
 if(x>=left&&x<left+width&&y>=top&&y<top+height)continue;
 const p=(y*old.width+x)*3;if(!pixels.subarray(p,p+3).equals(old.pixels.subarray(p,p+3)))outside++;
}
if(outside)throw Error('ancestor pixels changed');
for(const name of ['wall-v20.png','wall.png'])fs.writeFileSync('artifacts/line-4/'+name,png);
fs.writeFileSync('dist/line-4/40.jpg',jpg);
const checks={ancestor_sha256:hash(before),generated_candidate_sha256:hash(candidateBytes),
 method:'Built-in imagegen edit; only the generated sieve and three pebble pigment silhouettes transferred onto bare rock. Generated repaint elsewhere discarded; candidate consumed in place.',
 png:{paths:['artifacts/line-4/wall-v20.png','artifacts/line-4/wall.png'],format:'PNG',mode:'RGB',dimensions:[1254,1254],bytes:png.length,sha256:hash(png)},
 jpeg:{path:'dist/line-4/40.jpg',format:'JPEG',dimensions:[512,512],bytes:jpg.length,sha256:hash(jpg)},
 preservation:{rectangle:[left,top,left+width-1,top+height-1],changed_pixels:changed,outside_rectangle_changed_pixels:outside},
 visual_review_completed:false,unmet_visual_requirements:[]};
fs.writeFileSync('line-4/image-checks40.json',JSON.stringify(checks,null,2)+'\n');console.log(JSON.stringify(checks,null,2));
