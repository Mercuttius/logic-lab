import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import ts from 'typescript';
const base=JSON.parse(fs.readFileSync(new URL('../lib/exercises.json',import.meta.url),'utf8'));
const extra=JSON.parse(fs.readFileSync(new URL('../lib/additional-exercises.json',import.meta.url),'utf8'));
const exercises=[...base,...extra];
const compiled=ts.transpileModule(fs.readFileSync(new URL('../lib/catalog.ts',import.meta.url),'utf8'),{compilerOptions:{esModuleInterop:true,module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText;
const api={exports:{},require:name=>{if(name==='./exercises.json')return base;if(name==='./additional-exercises.json')return extra;throw Error(name);}};
vm.runInNewContext(compiled,api);
assert.equal(base.length,900);assert.equal(extra.length,270);assert.equal(exercises.length,1170);
assert.equal(new Set(exercises.map(e=>e.id)).size,1170);
assert.equal(new Set(extra.map(e=>e.title)).size,270);
assert.equal(new Set(extra.map(e=>e.code)).size,270);
const counts=new Map();let executions=0,negativeChecks=0;
async function execute(e,answers){
 const source=e.code.replace(/___(\d+)___/g,(_,i)=>answers[Number(i)]);
 const output=[],handles=new Set();
 const context={console:{log:(...args)=>output.push(args.map(String).join(' '))},AbortController, setTimeout:(fn,ms)=>{const id=setTimeout(()=>{handles.delete(id);fn();},ms);handles.add(id);return id;},clearTimeout:id=>{clearTimeout(id);handles.delete(id);}};
 let timeout;
 try{
  const result=vm.runInNewContext(source,context,{timeout:300});
  await Promise.race([Promise.resolve(result),new Promise((_,reject)=>{timeout=setTimeout(()=>reject(Error('Promise não terminou')),1500);})]);
  assert.deepEqual(output,[e.expected],e.id+' não corresponde ao oráculo declarado');
  executions++;
 }catch(error){throw new Error(e.id+": "+error.message,{cause:error});}finally{clearTimeout(timeout);for(const id of handles)clearTimeout(id);}
}
for(const e of exercises){
 const key=e.topic+'/'+e.level;counts.set(key,(counts.get(key)||0)+1);
 const slots=[...e.code.matchAll(/___(\d+)___/g)].map(x=>Number(x[1]));
 assert.deepEqual([...new Set(slots)].sort((a,b)=>a-b),e.answers.map((_,i)=>i),e.id);
 const canonical=e.answers.map(a=>a[0]);
 assert(api.exports.grade(e,canonical),e.id+' gabarito rejeitado');
 await execute(e,canonical);
 if(extra.includes(e)){
  for(let i=0;i<e.answers.length;i++){
   for(const variant of e.answers[i].slice(1)){
    const values=[...canonical];values[i]=variant;
    assert(api.exports.grade(e,values),e.id+' alternativa rejeitada');await execute(e,values);
   }
   const wrong=[...canonical];wrong[i]='__resposta_incorreta__';
   assert.equal(api.exports.grade(e,wrong),false,e.id+' aceitou lacuna incorreta');negativeChecks++;
  }
  assert.equal(api.exports.grade(e,[]),false,e.id+' aceitou lacunas vazias');
 }
}
assert.equal(counts.size,39);for(const [name,count] of counts)assert.equal(count,30,name);
assert.equal(api.exports.totalWeight,2340);
console.log(`PASS: 1.170 exercícios; 39 grupos de 30; 270 novos títulos/códigos únicos; ${executions} execuções e ${negativeChecks} verificações negativas.`);
console.log('Os 270 novos oráculos são declarados no conteúdo autoral. Os 900 antigos foram apenas verificados por regressão contra as saídas já existentes. Nenhum gabarito ou saída é reescrito pelo teste.');
