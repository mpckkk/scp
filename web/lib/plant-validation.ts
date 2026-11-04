export type Category = "spatial" | "time" | "spatial, time";
export type PaperStatus = "include" | "pending" | "exclude";
export type Paper = {
  pmid: string; title: string; date: string; year: number; doi?: string; pmcid?: string;
  species?: string; evidence?: string; category?: Category; status: PaperStatus;
  sources: string[]; revision: string; abstract?: string; screeningFlags?: string[]; updatedAt?: string;
};
export class PlantError extends Error {
  status: number;
  constructor(message: string, status = 400) { super(message); this.status = status; }
}

export function plainText(value: unknown): string {
  let text = String(value ?? "").replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, "");
  const entities: Record<string, string> = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " " };
  text = text.replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos|nbsp);/gi, (_, token: string) => {
    if (token.startsWith("#")) {
      const code = token[1].toLowerCase() === "x" ? parseInt(token.slice(2), 16) : parseInt(token.slice(1), 10);
      return code > 0 && code <= 0x10ffff ? String.fromCodePoint(code) : "";
    }
    return entities[token.toLowerCase()] ?? "";
  });
  return text.replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, "").replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}
export function normalizedTitle(value: unknown) { return plainText(value).toLowerCase().replace(/[^a-z0-9]/g, ""); }
export function normalizedDoi(value: unknown) {
  return String(value ?? "").trim().replace(/^(https?:\/\/(dx\.)?doi\.org\/|doi:\s*)/i, "").toLowerCase().replace(/\.$/, "");
}
export function chicagoToday() {
  const parts = new Intl.DateTimeFormat("en-US", { timeZone: "America/Chicago", year: "numeric", month: "2-digit", day: "2-digit" }).formatToParts(new Date());
  const get = (type: string) => parts.find((part) => part.type === type)?.value;
  return `${get("year")}-${get("month")}-${get("day")}`;
}
export function checkPmid(value: unknown): string {
  const pmid = String(value ?? "").trim();
  if (!/^[1-9]\d{0,11}$/.test(pmid)) throw new PlantError("A numeric PubMed ID is required.");
  return pmid;
}
export function checkDate(value: unknown, today = chicagoToday()): string {
  const date = String(value ?? "");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !Number.isFinite(Date.parse(date)) || new Date(date).toISOString().slice(0, 10) !== date || date < "2023-01-01" || date > today) {
    throw new PlantError(`Use a publication date between 2023-01-01 and ${today}.`);
  }
  return date;
}
export function safeSources(value: unknown): string[] {
  if (!Array.isArray(value)) return [];
  return [...new Set(value.map(String).filter((source) => {
    try { const url = new URL(source); return ["http:", "https:"].includes(url.protocol) && !!url.hostname; } catch { return false; }
  }))].slice(0, 15);
}
export async function resolveArchiveId(paper: Pick<Paper, "pmid" | "pmcid">, lookup: (pmid: string) => Promise<unknown>): Promise<string | undefined> {
  if (paper.pmcid && /^PMC\d+$/.test(paper.pmcid)) return paper.pmcid;
  const response = await lookup(paper.pmid) as { resultList?: { result?: { id?: string; pmid?: string; pmcid?: string }[] } };
  const records = response?.resultList?.result;
  const found = Array.isArray(records) ? records.find((record) => String(record.pmid ?? record.id) === paper.pmid) : undefined;
  if (!found) throw new PlantError("Europe PMC could not resolve this PubMed record. Full-text availability could not be checked; retry later.", 502);
  return found.pmcid && /^PMC\d+$/.test(found.pmcid) ? found.pmcid : undefined;
}
export function validateReview(input: Record<string, unknown>, existing: Paper): Paper {
  const pmid = checkPmid(input.pmid);
  if (!existing.revision || input.expectedRevision !== existing.revision) throw new PlantError("This paper changed since you opened it. Reload it and review the latest version.", 409);
  const status = input.status as PaperStatus;
  if (!["include", "exclude", "pending"].includes(status)) throw new PlantError("Choose include, exclude, or pending.");
  if (existing.status === "include" && input.correction !== true) throw new PlantError("Changing an included paper requires an explicit correction.", 409);
  const evidence = plainText(input.evidence);
  const sources = safeSources(input.sources);
  if (evidence.length < 20) throw new PlantError("Describe the study evidence or review reason in at least 20 characters.");
  if (status !== "pending" && !sources.length) throw new PlantError("Add at least one supporting source URL.");
  const merged: Paper = { ...existing, pmid, status, evidence, sources, revision: crypto.randomUUID(), updatedAt: new Date().toISOString() };
  for (const key of ["title", "date", "species"] as const) if (input[key] !== undefined) merged[key] = plainText(input[key]);
  if (input.category !== undefined) {
    const category = String(input.category).replace(/^spatialtime$/, "spatial, time").replace(/^spatial,time$/, "spatial, time");
    if (!["spatial", "time", "spatial, time"].includes(category)) throw new PlantError("Choose spatial, time, or spatial, time.");
    merged.category = category as Category;
  }
  if (status === "include") {
    if (!merged.title.trim()) throw new PlantError("An included paper needs its verified title.");
    merged.date = checkDate(merged.date);
    merged.year = Number(merged.date.slice(0, 4));
    if (!merged.category) throw new PlantError("An included paper needs a spatial/time category.");
  }
  return merged;
}
export function catalogCsv(papers: Paper[], status: PaperStatus = "include") {
  const quote = (value: unknown) => { let text = String(value ?? ""); if (/^[\s\u0000-\u001f]*[=+\-@]/.test(text)) text = "'" + text; return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text; };
  return "\uFEFF" + [["data_type", "year", "title", "PMID"], ...papers.filter((paper) => paper.status === status).sort((a, b) => a.date.localeCompare(b.date) || Number(a.pmid) - Number(b.pmid)).map((paper) => [paper.category ?? "", paper.year, paper.title, paper.pmid])].map((row) => row.map(quote).join(",")).join("\r\n") + "\r\n";
}
