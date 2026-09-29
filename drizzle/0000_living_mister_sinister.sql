CREATE TABLE `attempts` (
	`id` text PRIMARY KEY NOT NULL,
	`exercise_id` text NOT NULL,
	`correct` integer NOT NULL,
	`created_at` text NOT NULL,
	`day` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `idx_attempts_exercise` ON `attempts` (`exercise_id`);--> statement-breakpoint
CREATE INDEX `idx_attempts_day` ON `attempts` (`day`);