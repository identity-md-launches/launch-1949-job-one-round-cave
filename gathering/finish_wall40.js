// Isolate the new pigment from the image tool's output onto the verified wall.
// Usage: node gathering/finish_wall40.js GENERATED_PNG
'use strict';
const fs = require('node:fs');
const zlib = require('node:zlib');
const crypto = require('node:crypto');
const {decode, thumbnail} = require('./thumbnail.js');

const ancestorBytes = fs.readFileSync('artifacts/gathering/wall-v19.png');
const ancestorHash = '98cc7609e4cba7a729ce56471c93acd9a26b841510cdc15cc077d995dd3749da';
if (crypto.createHash('sha256').update(ancestorBytes).digest('hex') !== ancestorHash)
  throw new Error('expected the verified Gathering 39 ancestor');
const freshBytes = fs.readFileSync(process.argv[2]);
const old = decode(ancestorBytes), fresh = decode(freshBytes);
if (old.width !== 1254 || old.height !== 1254 || old.channels !== 3 ||
    fresh.width !== old.width || fresh.height !== old.height || fresh.channels < 3)
  throw new Error('image dimensions or format changed');

// Preserve every ancestor pixel except the new pigment silhouette, placed on bare rock.
// The editor placed the new motif over an earlier faint motif. Transfer ONLY
// the new oval and pebbles, retaining the verified ancestor at that source site.
const width=old.width,height=old.height;
const out=Buffer.from(old.pixels);
const box=[325,855,400,925];
let changed=0,changedBox=[width,height,-1,-1];
for(let y=box[1];y<=box[3];y++)for(let x=box[0];x<=box[2];x++){
 const sx=Math.round((x-363)/.7+601),sy=Math.round((y-890)/.7+1000);
 const ring=Math.abs(Math.hypot((sx-601)/53,(sy-999)/25)-1)<.15;
 const pebbles=[[572,1000,11],[626,1001,11],[598,999,8]].some(([cx,cy,r])=>Math.hypot(sx-cx,sy-cy)<r);
 if(!ring&&!pebbles)continue;
 const q=(sy*width+sx)*fresh.channels,p=(y*width+x)*3;
 const [r,g,b]=fresh.pixels.subarray(q,q+3);
 const pigment=ring ? r<125&&g<90&&b<60 : (r>g*1.35&&g>b*1.45)||(r>140&&g>115&&b>85);
 if(!pigment)continue;
 for(let c=0;c<3;c++)out[p+c]=Math.round(old.pixels[p+c]*.13+fresh.pixels[q+c]*.87);
 if(out[p]!==old.pixels[p]||out[p+1]!==old.pixels[p+1]||out[p+2]!==old.pixels[p+2]){
  changed++;changedBox=[Math.min(changedBox[0],x),Math.min(changedBox[1],y),Math.max(changedBox[2],x),Math.max(changedBox[3],y)];
 }
}
if(changed<200||changed>3500)throw new Error('unexpected new pigment count '+changed);
function crc32(bytes) {
  let crc=0xffffffff;
  for(const v of bytes){crc^=v;for(let b=0;b<8;b++)crc=(crc>>>1)^((crc&1)?0xedb88320:0);}
  return (crc^0xffffffff)>>>0;
}
function chunk(name,data) {
  const kind=Buffer.from(name),length=Buffer.alloc(4),crc=Buffer.alloc(4);
  length.writeUInt32BE(data.length);crc.writeUInt32BE(crc32(Buffer.concat([kind,data])));
  return Buffer.concat([length,kind,data,crc]);
}
const ihdr=Buffer.alloc(13);
ihdr.writeUInt32BE(width);ihdr.writeUInt32BE(height,4);ihdr[8]=8;ihdr[9]=2;
const stride=width*3,scan=Buffer.alloc(height*(stride+1));
for(let y=0;y<height;y++)out.copy(scan,y*(stride+1)+1,y*stride,(y+1)*stride);
const png=Buffer.concat([Buffer.from('89504e470d0a1a0a','hex'),chunk('IHDR',ihdr),
  chunk('IDAT',zlib.deflateSync(scan,{level:9})),chunk('IEND',Buffer.alloc(0))]);
fs.writeFileSync('artifacts/gathering/wall-v20.png',png);
fs.writeFileSync('artifacts/gathering/wall.png',png);
const jpeg=thumbnail(png,512,75);
if(jpeg.length>=100000)throw new Error('JPEG exceeds 100 KB');
fs.writeFileSync('dist/gathering/40.jpg',jpeg);
const result={ancestor_sha256:ancestorHash,
  generated_sha256:crypto.createHash('sha256').update(freshBytes).digest('hex'),
  png:{path:'artifacts/gathering/wall-v20.png',format:'PNG',mode:'RGB',dimensions:[width,height],
    bytes:png.length,sha256:crypto.createHash('sha256').update(png).digest('hex')},
  jpeg:{path:'dist/gathering/40.jpg',format:'JPEG',dimensions:[512,512],bytes:jpeg.length},
  preservation:{rectangle:box,changed_pixels:changed,changed_bounds:changedBox,
                outside_rectangle_changed_pixels:0},
  model:'installed image edit tool; generated pigment isolated over verified ancestor',
  visual_review_completed:false,unmet_visual_requirements:[]};
fs.writeFileSync('gathering/image-checks40.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
