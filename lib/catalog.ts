import data from './exercises.json';
import additional from './additional-exercises.json';
import collections from './collections-exercises.json';
export type Exercise = typeof data[number];
export const exercises: Exercise[] = [...data, ...additional, ...collections];
export const totalWeight = exercises.reduce((sum,e)=>sum+({easy:1,medium:2,hard:3}[e.level] || 1),0);
// Ordem sugerida de estudo; os IDs permanecem estáveis para preservar o histórico.
export const topics = [
 {id:'if',label:'if',group:'TOMADA DE DECISÃO'},
 {id:'if-else',label:'if / else',group:'TOMADA DE DECISÃO'},
 {id:'else-if',label:'else if',group:'TOMADA DE DECISÃO'},
 {id:'switch',label:'switch',group:'TOMADA DE DECISÃO'},
 {id:'ternary',label:'ternário',group:'TOMADA DE DECISÃO'},
 {id:'return',label:'return',group:'FUNÇÕES E RETORNO'},
 {id:'arrays',label:'arrays',group:'ARRAYS E OBJETOS'},
 {id:'objects',label:'objetos',group:'ARRAYS E OBJETOS'},
 {id:'for',label:'for',group:'LAÇOS DE REPETIÇÃO'},
 {id:'while',label:'while',group:'LAÇOS DE REPETIÇÃO'},
 {id:'do-while',label:'do / while',group:'LAÇOS DE REPETIÇÃO'},
 {id:'for-of',label:'for…of',group:'LAÇOS DE REPETIÇÃO'},
 {id:'for-in',label:'for…in',group:'LAÇOS DE REPETIÇÃO'},
 {id:'try-catch',label:'try / catch',group:'TRATAMENTO DE ERROS'},
 {id:'async-await',label:'async / await',group:'ASSINCRONISMO'},
];
export const levels = [{id:'easy',label:'Fácil'},{id:'medium',label:'Médio'},{id:'hard',label:'Difícil'}];
export type Attempt = {id:string;exercise_id:string;correct:number;created_at:string;day:string};
export function dayKey(date = new Date()) {return new Intl.DateTimeFormat('en-CA',{timeZone:'America/Sao_Paulo',year:'numeric',month:'2-digit',day:'2-digit'}).format(date);}
// Token comparison preserves string contents, unlike blindly stripping whitespace.
export function normalize(code:string) {
 const tokens=code.match(/"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`|\/\*[\s\S]*?\*\/|\/\/[^\n]*|===|!==|=>|\*\*|&&|\|\||\?\?=|\?\?|==|!=|<=|>=|\+\+|--|\+=|-=|\*=|\/=|\d+(?:\.\d+)?|[\p{L}_$][\p{L}\p{N}_$]*|[^\s]/gu)||[];
 return tokens.filter(t=>!t.startsWith('//')&&!t.startsWith('/*')).map(t=>t.startsWith("'")?'"'+t.slice(1,-1).replace(/\\'/g,"'").replace(/"/g,'\\"')+'"':t).join(' ').replace(/ ;$/,'');
}
export function grade(exercise:Exercise, answers:string[]) {return answers.length===exercise.answers.length && exercise.answers.every((variants,i)=>variants.some(v=>normalize(v)===normalize(answers[i]||'')));}
