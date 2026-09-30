import data from './exercises.json';
import additional from './additional-exercises.json';
export type Exercise = typeof data[number];
export const exercises: Exercise[] = [...data, ...additional];
export const totalWeight = exercises.reduce((sum,e)=>sum+({easy:1,medium:2,hard:3}[e.level] || 1),0);
export const topics = [{id:'if',label:'if'},{id:'if-else',label:'if / else'},{id:'else-if',label:'else if'},{id:'switch',label:'switch'},{id:'ternary',label:'ternário'},{id:'for',label:'for'},{id:'while',label:'while'},{id:'do-while',label:'do / while'},{id:'for-of',label:'for…of'},{id:'for-in',label:'for…in'},{id:'return',label:'return'},{id:'try-catch',label:'try / catch'},{id:'async-await',label:'async / await'}];
export const levels = [{id:'easy',label:'Fácil'},{id:'medium',label:'Médio'},{id:'hard',label:'Difícil'}];
export type Attempt = {id:string;exercise_id:string;correct:number;created_at:string;day:string};
export function dayKey(date = new Date()) {return new Intl.DateTimeFormat('en-CA',{timeZone:'America/Sao_Paulo',year:'numeric',month:'2-digit',day:'2-digit'}).format(date);}
// Token comparison preserves string contents, unlike blindly stripping whitespace.
export function normalize(code:string) {
 const tokens=code.match(/"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`|\/\*[\s\S]*?\*\/|\/\/[^\n]*|===|!==|=>|\*\*|&&|\|\||\?\?=|\?\?|==|!=|<=|>=|\+\+|--|\+=|-=|\*=|\/=|\d+(?:\.\d+)?|[\p{L}_$][\p{L}\p{N}_$]*|[^\s]/gu)||[];
 return tokens.filter(t=>!t.startsWith('//')&&!t.startsWith('/*')).map(t=>t.startsWith("'")?'"'+t.slice(1,-1).replace(/\\'/g,"'").replace(/"/g,'\\"')+'"':t).join(' ').replace(/ ;$/,'');
}
export function grade(exercise:Exercise, answers:string[]) {return answers.length===exercise.answers.length && exercise.answers.every((variants,i)=>variants.some(v=>normalize(v)===normalize(answers[i]||'')));}
