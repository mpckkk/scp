import { index, integer, sqliteTable, text, uniqueIndex } from "drizzle-orm/sqlite-core";
import { sql } from "drizzle-orm";

export const plantPapers = sqliteTable("plant_papers", {
  pmid: text("pmid").primaryKey(),
  doi: text("doi"),
  title: text("title").notNull(),
  status: text("status").notNull(),
  record: text("record").notNull(),
  updatedAt: text("updated_at").notNull(),
}, (table) => [index("plant_papers_doi_idx").on(table.doi), index("plant_papers_status_idx").on(table.status),
  uniqueIndex("plant_papers_included_doi_unique").on(table.doi).where(sql`${table.status}='include' AND ${table.doi} IS NOT NULL AND ${table.doi}<>''`)]);

export const plantMetadata = sqliteTable("plant_metadata", {
  key: text("key").primaryKey(),
  value: text("value").notNull(),
});

export const plantDecisions = sqliteTable("plant_decisions", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  pmid: text("pmid").notNull(),
  data: text("data").notNull(),
  createdAt: text("created_at").notNull(),
});
