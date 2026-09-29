import { readProgress } from '@/db/progress';
export async function GET(){try{return Response.json({attempts:await readProgress()},{headers:{'Cache-Control':'no-store'}});}catch(error){console.error('progress',error);return Response.json({error:'Não foi possível carregar o histórico. Tente novamente.'},{status:503});}}
