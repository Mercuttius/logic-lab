import assert from 'node:assert/strict';
const origin='http://127.0.0.1:5173';
const ids=[crypto.randomUUID(),crypto.randomUUID()];
for(const [i,answer] of ['idade >= 16','idade < 16'].entries()){
 const body={id:ids[i],exerciseId:'if-easy-01',answers:[answer]};
 for(let n=0;n<2;n++){
  const r=await fetch(origin+'/api/attempts',{method:'POST',headers:{'content-type':'application/json',origin},body:JSON.stringify(body)});const data=await r.json();assert.equal(r.status,200,JSON.stringify(data));assert.equal(data.correct,i===0);
 }
}
const progress=await (await fetch(origin+'/api/progress')).json();
for(const id of ids)assert.equal(progress.attempts.filter(a=>a.id===id).length,1);
const invalid=await fetch(origin+'/api/attempts',{method:'POST',headers:{'content-type':'application/json',origin},body:JSON.stringify({id:crypto.randomUUID(),exerciseId:'bad',answers:['x']})});assert.equal(invalid.status,400);
console.log('PASS: acerto, erro, persistência, deduplicação e entrada inválida. IDs de teste: '+ids.join(','));
