import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const path=new URL('../lib/exercises.json',import.meta.url);
const exercises=JSON.parse(fs.readFileSync(path,'utf8'));
assert.equal(exercises.length,900);
assert.equal(new Set(exercises.map(e=>e.id)).size,900);
const counts=new Map();
for(const e of exercises){
 const group=e.topic+'/'+e.level;counts.set(group,(counts.get(group)||0)+1);
 const slots=[...e.code.matchAll(/___(\d+)___/g)].map(x=>Number(x[1]));
 assert.deepEqual([...new Set(slots)].sort(),e.answers.map((_,i)=>i));
 const code=e.code.replace(/___(\d+)___/g,(_,i)=>e.answers[Number(i)][0]);
 const output=[];
 try{vm.runInNewContext(code,{console:{log:(...args)=>output.push(args.map(String).join(' '))}},{timeout:100});}catch(error){throw new Error(e.id+': '+error.message);}
 assert.equal(output.length,1,e.id); e.expected=output[0];
}
assert.equal(counts.size,30);for(const n of counts.values())assert.equal(n,30);
fs.writeFileSync(path,JSON.stringify(exercises,null,2)+'\n');
console.log('PASS: 900 IDs únicos, 30 exercícios por grupo, todas as lacunas e 900 soluções executadas em Node.js.');
