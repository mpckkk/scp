CREATE TABLE `plant_decisions` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`pmid` text NOT NULL,
	`data` text NOT NULL,
	`created_at` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `plant_metadata` (
	`key` text PRIMARY KEY NOT NULL,
	`value` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `plant_papers` (
	`pmid` text PRIMARY KEY NOT NULL,
	`doi` text,
	`title` text NOT NULL,
	`status` text NOT NULL,
	`record` text NOT NULL,
	`updated_at` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `plant_papers_doi_idx` ON `plant_papers` (`doi`);--> statement-breakpoint
CREATE INDEX `plant_papers_status_idx` ON `plant_papers` (`status`);