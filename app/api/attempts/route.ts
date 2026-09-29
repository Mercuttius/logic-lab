import { database } from '@/db/progress';
import { exercises, grade, dayKey } from '@/lib/catalog';
export async function POST(request:Request){
 if(request.headers.get('origin') !== new URL(request.url).origin) return Response.json({error:'Origem não autorizada.'},{status:403});
 try{
  const raw=await request.text(); if(raw.length>12000) return Response.json({error:'Resposta muito longa.'},{status:413});
  const body=JSON.parse(raw);
  const exercise=exercises.find(x=>x.id===body.exerciseId);
  if(!exercise || typeof body.id!=='string' || !/^[\da-f-]{36}$/i.test(body.id) || !Array.isArray(body.answers) || body.answers.length!==exercise.answers.length || body.answers.some((v:unknown)=>typeof v!=='string'||!v.trim()||v.length>4000)) return Response.json({error:'Preencha todas as lacunas antes de verificar.'},{status:400});
  const correct=grade(exercise,body.answers);
  const db=database(); const createdAt=new Date().toISOString();
  await db.prepare('INSERT INTO attempts (id, exercise_id, correct, created_at, day) VALUES (?, ?, ?, ?, ?) ON CONFLICT(id) DO NOTHING').bind(body.id,exercise.id,correct?1:0,createdAt,dayKey()).run();
  const saved=await db.prepare('SELECT * FROM attempts WHERE id = ?').bind(body.id).first();
  if(saved?.exercise_id!==exercise.id) return Response.json({error:'Identificador de tentativa em conflito.'},{status:409});
  return Response.json({attempt:saved,correct:!!saved?.correct,explanation:exercise.explanation});
 }catch(error){console.error('attempt',error);return Response.json({error:'Não foi possível salvar sua tentativa. Suas respostas foram preservadas; tente novamente.'},{status:503});}
}
