#!/usr/bin/env python3
"""Check final gathering records, pixels, gallery references, evidence and scope."""
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess
from build_gallery import Previews
from check_delivery import Gallery, jpeg_dimensions, png_dimensions

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    wall=Path('artifacts/gathering/wall-v20.png').read_bytes()
    assert wall==Path('artifacts/gathering/wall.png').read_bytes()
    assert png_dimensions(wall)==(1254,1254) and wall[24:26]==bytes((8,2))
    jpeg=Path('dist/gathering/40.jpg').read_bytes()
    assert jpeg_dimensions(jpeg)==(512,512) and len(jpeg)<100000
    record=json.loads(Path('dist/gathering/40.json').read_text())
    assert set(record)=={'name','image','attributes'}
    assert record['image']=='https://api.imd.fun/artifacts/'+hashlib.sha256(wall).hexdigest()
    attrs={a['trait_type']:a['value'] for a in record['attributes']}
    assert len(attrs)==len(record['attributes'])==6
    assert attrs['Cave']=='Ice' and attrs['Wall']=='Gathering'
    assert type(attrs['Number']) is int and attrs['Number']==40 and attrs['One thing']=='Gathering'
    assert set(attrs)=={'Cave','Wall','Number','One thing','Meaning','Left behind'}
    assert json.loads(Path('dist/goals.json').read_text())==[{'line':i,'goal':Path(f'line-{i}/GOAL.md').read_text().strip()} for i in range(1,5)]
    content=Path('dist/index.html').read_text(); gallery=Gallery(content);previews=Previews(content)
    records={p.relative_to('dist').as_posix():json.loads(p.read_text()) for p in Path('dist').glob('*/[0-9][0-9].json')}
    assert len(records)==len(gallery.records)==200 and set(records)==set(gallery.records)
    assert len(content.encode())<100000
    assert len(previews.images)==100 and not set(gallery.tags)&{'script','iframe','link'}
    assert set(previews.images)=={k for k,r in records.items() if r['name']!='Not painted yet'}
    for source in previews.images.values():
        assert re.fullmatch(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+',source)
        a,b=jpeg_dimensions(base64.b64decode(source.split(',')[1]));assert a==b and a>0
    for wallname in ['gathering']+[f'line-{i}' for i in range(1,5)]:
        painted=[k for k in gallery.records if k.startswith(wallname+'/') and records[k]['name']!='Not painted yet']
        assert painted==sorted(painted,reverse=True)
        for n in range(2,22):
            p=Path('dist',wallname,f'{n:02}.json')
            assert json.loads(p.read_text())=={'name':'Not painted yet','image':'https://api.imd.fun/artifacts/b5e794cb2c70bd232230e389707698c69c2080786d606a13b39f9315c9a90799','attributes':[{'trait_type':'Cave','value':'Ice'}]}
            assert not p.with_suffix('.jpg').exists()
    review=json.loads(Path('gathering/image-checks40.json').read_text())
    assert review['visual_review_completed'] and review['unmet_visual_requirements']==[]
    assert review['png']['sha256']==hashlib.sha256(wall).hexdigest()
    assert review['ancestor_sha256']==digest('artifacts/gathering/wall-v19.png')
    assert json.loads(Path('dist/gathering/39.json').read_text())['image'].endswith(review['ancestor_sha256'])
    js="""const fs=require('node:fs'),{decode}=require('./gathering/thumbnail.js');const a=decode(fs.readFileSync('artifacts/gathering/wall-v19.png')),b=decode(fs.readFileSync('artifacts/gathering/wall-v20.png'));let changed=0,outside=0;for(let y=0;y<a.height;y++)for(let x=0;x<a.width;x++){const p=(y*a.width+x)*3;if(a.pixels[p]!==b.pixels[p]||a.pixels[p+1]!==b.pixels[p+1]||a.pixels[p+2]!==b.pixels[p+2]){changed++;if(x<325||x>400||y<855||y>925)outside++;}}console.log(JSON.stringify({changed,outside}));"""
    pixels=json.loads(subprocess.run(['node','-e',js],capture_output=True,text=True,check=True).stdout)
    assert pixels=={'changed':1422,'outside':0}
    tests=json.loads(Path('gathering/test-runs40.json').read_text());trials=json.loads(Path('gathering/current-checks40.json').read_text())
    assert tests['ok'] and tests['line_tests']==742 and tests['shared_tests']==132 and tests['gathering_tests']==8
    assert tests['sources_unchanged_after_checks'] and trials['ok'] and len(trials['results'])==58
    assert Path('gathering/COINS.md').read_text().splitlines()[0]=='none'
    assert not Path('gathering/coin-order.json').exists() and not Path('gathering/deploy-order.json').exists()
    assert digest('shared/import-drift/reconcile.py')==digest('line-2/tools/csv-reconcile/reconcile.py')
    ev=json.loads(Path('gathering/origin-evidence40.json').read_text())
    for item in ev['inventory']['manifest']:assert digest(Path('shared/import-drift')/item['path'])==item['sha256']
    assert ev['inventory']['files']==38 and ev['inventory']['bytes']==197195
    assert len(ev['sites'])==40 and not ev['issues'] and not ev['cycles']
    assert json.loads(Path('gathering/origin-review40.json').read_text())['comparison']['equal']
    actual=subprocess.run(['python3','-B','shared/import-drift/origin_csv.py','compare','shared/import-drift/observed-origins40.csv','shared/import-drift/observed-origins40.csv'],capture_output=True,text=True,check=True)
    assert json.loads(actual.stdout)==json.loads(Path('gathering/origin-review40.json').read_text())
    assert json.loads(Path('gathering/declared-review40.json').read_text())['reproduced']
    assert json.loads(Path('gathering/gallery-checks40.json').read_text())['ok']
    roots=[Path(f'line-{i}') for i in range(1,5)]+[Path(f'dist/line-{i}') for i in range(1,5)]
    baseline=json.loads(Path('test/scratch/scope40.json').read_text())
    assert baseline=={str(p):digest(p) for root in roots for p in root.rglob('*') if p.is_file()}
    assert not subprocess.run(['git','diff','HEAD','--',*map(str,roots)],capture_output=True,check=True).stdout
    changed=subprocess.run(['git','diff','--name-only','HEAD'],capture_output=True,text=True,check=True).stdout.splitlines()
    added=subprocess.run(['git','ls-files','--others','--exclude-standard'],capture_output=True,text=True,check=True).stdout.splitlines()
    for name in set(changed+added):
        if name.startswith(('test/scratch/','artifacts/gathering/')):continue
        assert name.split('/')[0] in ('gathering','shared','dist'),name
        assert Path(name).is_file() and Path(name).stat().st_size<100000,name
    assert not subprocess.run(['git','ls-files','--','artifacts/gathering/wall-v20.png','artifacts/gathering/wall.png'],capture_output=True,check=True).stdout
    result={'ok':True,'line_tests':742,'shared_tests':132,'gathering_tests':8,'cli_trials':58,'line_paths_unchanged':True,'gallery_records':200,'painted_previews':100,'placeholders':100,'gallery_bytes':len(content.encode()),'pixel_verification':pixels,'png':review['png'],'jpeg':review['jpeg'],'unmet_visual_requirements':[],'named_outputs_untracked':True,'independent_certification':False}
    Path('gathering/delivery-checks40.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
