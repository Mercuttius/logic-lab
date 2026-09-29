import { env } from 'cloudflare:workers';
export function database(){if(!env.DB) throw new Error('Banco de dados indisponível');return env.DB;}
export async function readProgress(){const rows=await database().prepare('SELECT id, exercise_id, correct, created_at, day FROM attempts ORDER BY created_at DESC').all();return rows.results;}
