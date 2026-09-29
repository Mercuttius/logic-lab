import { integer, sqliteTable, text, index } from 'drizzle-orm/sqlite-core';
export const attempts = sqliteTable('attempts', {
 id: text('id').primaryKey(),
 exerciseId: text('exercise_id').notNull(),
 correct: integer('correct').notNull(),
 createdAt: text('created_at').notNull(),
 day: text('day').notNull(),
}, t => [index('idx_attempts_exercise').on(t.exerciseId), index('idx_attempts_day').on(t.day)]);
