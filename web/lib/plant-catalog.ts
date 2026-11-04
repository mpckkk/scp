import { env } from "cloudflare:workers";
import seed from "./plant-seed.json";
import searchConfig from "./plant-search-config.json";
import { Paper, PaperStatus, PlantError, catalogCsv, checkDate, checkPmid, chicagoToday, normalizedDoi, normalizedTitle, plainText, resolveArchiveId, safeSources, validateReview } from "./plant-validation";

const ENDPOINT = "https://www.ebi.ac.uk/europepmc/webservices/rest";
type LastSearch = { query: string; from: string; through: string; at: string; fetched: number; added: number; total: number; retrieved: number; complete: boolean; nextCursor?: string; compiledQuery?: string };
function database() { if (!env.DB) throw new PlantError("The durable catalog is unavailable. Database deployment is required.", 503); return env.DB; }
function insertStatements(papers: Paper[]) {
  const statements: D1PreparedStatement[] = [];
  // 15 records x 6 columns = 90 parameters, below D1's 100-parameter limit.
  for (let offset = 0; offset < papers.length; offset += 15) {
    const chunk = papers.slice(offset, offset + 15);
    const values = chunk.flatMap((paper) => [paper.pmid, normalizedDoi(paper.doi) || null, paper.title, paper.status, JSON.stringify(paper), paper.updatedAt ?? new Date().toISOString()]);
    statements.push(database().prepare(`INSERT OR IGNORE INTO plant_papers (pmid,doi,title,status,record,updated_at) VALUES ${chunk.map(() => "(?,?,?,?,?,?)").join(",")}`).bind(...values));
  }
  return statements;
}
async function metadata(key: string) { const row = await database().prepare("SELECT value FROM plant_metadata WHERE key=?").bind(key).first<{ value: string }>(); return row ? JSON.parse(row.value) : undefined; }
const metaStatement = (key: string, value: unknown) => database().prepare("INSERT INTO plant_metadata(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value").bind(key, JSON.stringify(value));
export async function ensurePlantSeed() {
  if (await metadata("initialized")) return;
  const data = seed as unknown as { papers: Paper[]; lastSearch?: LastSearch };
  const papers = data.papers.map((paper) => ({ ...paper, pmid: checkPmid(paper.pmid), revision: paper.revision || `seed-${paper.pmid}`, title: plainText(paper.title), doi: normalizedDoi(paper.doi), sources: safeSources(paper.sources) }));
  const initialMeta = (key: string, value: unknown) => database().prepare("INSERT OR IGNORE INTO plant_metadata(key,value) VALUES(?,?)").bind(key, JSON.stringify(value));
  const final = [initialMeta("initialized", { at: new Date().toISOString(), included: papers.filter((paper) => paper.status === "include").length })];
  if (data.lastSearch) final.push(initialMeta("lastSearch", data.lastSearch));
  await database().batch([...insertStatements(papers), ...final]);
}
export async function getPlantPaper(pmid: string) {
  await ensurePlantSeed();
  const row = await database().prepare("SELECT record FROM plant_papers WHERE pmid=?").bind(checkPmid(pmid)).first<{ record: string }>();
  if (!row) throw new PlantError("This PubMed ID is not in the catalog. Search for it first.", 404);
  return JSON.parse(row.record) as Paper;
}
export async function plantCatalog() {
  await ensurePlantSeed();
  const result = await database().prepare("SELECT record FROM plant_papers ORDER BY status,date(json_extract(record,'$.date')) DESC,pmid DESC").all<{ record: string }>();
  const papers = result.results.map((row) => JSON.parse(row.record) as Paper);
  const included = papers.filter((paper) => paper.status === "include");
  return { papers, counts: { included: included.length, pending: papers.filter((p) => p.status === "pending").length, excluded: papers.filter((p) => p.status === "exclude").length, spatial: included.filter((p) => p.category === "spatial").length, time: included.filter((p) => p.category === "time").length, both: included.filter((p) => p.category === "spatial, time").length }, lastSearch: await metadata("lastSearch") as LastSearch | undefined };
}
async function remote(url: string, format: "json" | "xml" = "json"): Promise<unknown> {
  let last = "Europe PMC could not be reached.";
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const response = await fetch(url, { signal: AbortSignal.timeout(20000), headers: { Accept: format === "json" ? "application/json" : "application/xml" } });
      if (!response.ok) {
        last = `Europe PMC returned HTTP ${response.status}.`;
        if (![408, 429, 500, 502, 503, 504].includes(response.status)) throw new PlantError(last, response.status === 404 ? 404 : 502);
      } else {
        const text = await response.text();
        if (text.length > 4_000_000) throw new PlantError("The source response exceeds the reading limit.", 502);
        return format === "json" ? JSON.parse(text) : text;
      }
    } catch (error) { if (error instanceof PlantError) throw error; last = error instanceof Error && error.name === "TimeoutError" ? "Europe PMC timed out. Try this page again." : "Europe PMC could not be reached. Try this page again."; }
    if (attempt < 2) await new Promise((resolve) => setTimeout(resolve, 400 * (attempt + 1)));
  }
  throw new PlantError(last, 502);
}
type RemotePaper = { id?: string; pmid?: string; doi?: string; pmcid?: string; title?: string; firstPublicationDate?: string; abstractText?: string; pubTypeList?: { pubType?: string[] } };
export async function searchPlantPapers(input: { query?: string; from?: string; through?: string; cursor?: string }) {
  await ensurePlantSeed();
  const query = plainText(input.query).slice(0, 400), from = checkDate(input.from ?? "2023-01-01"), through = checkDate(input.through ?? chicagoToday());
  if (from > through) throw new PlantError("The start date must come before the end date.");
  const cursor = input.cursor || "*";
  if (cursor.length > 4000) throw new PlantError("The search cursor is invalid.");
  const prior = await metadata("lastSearch") as LastSearch | undefined;
  if (cursor !== "*" && (!prior || prior.nextCursor !== cursor || prior.query !== query || prior.from !== from || prior.through !== through)) throw new PlantError("This search page has expired. Start the search again.", 409);
  const extra = /^\d+$/.test(query) ? ` AND EXT_ID:${query}` : query ? ` AND (${query.split(/\s+/).map((word) => `TITLE_ABS:"${word.replace(/["\\]/g, "")}"`).join(" AND ")})` : "";
  const compiled = `${searchConfig.plant_query} AND ${searchConfig.assay_query} AND SRC:MED AND FIRST_PDATE:[${from} TO ${through}]${extra}`;
  const url = `${ENDPOINT}/search?${new URLSearchParams({ query: compiled, format: "json", resultType: "core", pageSize: "100", cursorMark: cursor })}`;
  const response = await remote(url) as { hitCount?: number; nextCursorMark?: string; resultList?: { result?: RemotePaper[] } };
  if (!Number.isInteger(response.hitCount) || !response.resultList || !Array.isArray(response.resultList.result)) throw new PlantError("Europe PMC returned an incomplete search response. Nothing was saved.", 502);
  const records = response.resultList.result, total = response.hitCount!, retrieved = (cursor === "*" ? 0 : prior!.retrieved) + records.length;
  if (!records.length && retrieved < total) throw new PlantError("Europe PMC returned an empty page before the search was complete. Retry this page.", 502);
  const hasMore = retrieved < total;
  if (hasMore && (!response.nextCursorMark || response.nextCursorMark === cursor)) throw new PlantError("Europe PMC did not provide the next search page. Nothing was saved.", 502);
  const current = (await plantCatalog()).papers;
  const byPmid = new Map(current.map((p) => [p.pmid, p])), byDoi = new Map(current.filter((p) => p.doi).map((p) => [normalizedDoi(p.doi), p]));
  const additions: Paper[] = [], conflicts: string[] = [];
  for (const raw of records) {
    const pmid = String(raw.pmid ?? raw.id ?? ""), title = plainText(raw.title), doi = normalizedDoi(raw.doi);
    if (!/^[1-9]\d{0,11}$/.test(pmid) || !title) { conflicts.push("A source record lacked a usable PubMed ID or title."); continue; }
    const known = byPmid.get(pmid) ?? (doi ? byDoi.get(doi) : undefined);
    if (known) {
      if (normalizedTitle(known.title) !== normalizedTitle(title) || (known.doi && doi && normalizedDoi(known.doi) !== doi)) conflicts.push(`PMID ${pmid}: source metadata differs from the saved record; saved review preserved.`);
      continue;
    }
    const date = raw.firstPublicationDate ?? "";
    const flags = (raw.pubTypeList?.pubType ?? []).filter((type) => /review|protocol|retract|editorial|comment/i.test(type));
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || date < from || date > through) flags.push("Publication date needs verification");
    const paper: Paper = { pmid, title, doi, pmcid: raw.pmcid, date, year: Number(date.slice(0, 4)) || 0, status: "pending", category: undefined, species: "", evidence: "", sources: [`https://pubmed.ncbi.nlm.nih.gov/${pmid}/`], revision: crypto.randomUUID(), abstract: plainText(raw.abstractText), screeningFlags: flags, updatedAt: new Date().toISOString() };
    additions.push(paper); byPmid.set(pmid, paper); if (doi) byDoi.set(doi, paper);
  }
  const lastSearch: LastSearch = { query, from, through, at: new Date().toISOString(), fetched: records.length, added: additions.length, total, retrieved, complete: !hasMore, nextCursor: hasMore ? response.nextCursorMark : undefined, compiledQuery: compiled };
  // One page is committed as a D1 transaction; failed retrieval never advances this checkpoint.
  await database().batch([...insertStatements(additions), metaStatement("lastSearch", lastSearch)]);
  return { fetched: records.length, added: additions.length, total, hasMore, nextCursor: lastSearch.nextCursor, query, conflicts, lastSearch };
}
export async function reviewPlantPaper(input: Record<string, unknown>, actor: string) {
  const existing = await getPlantPaper(checkPmid(input.pmid));
  const paper = validateReview(input, existing);
  if (paper.doi) {
    const duplicate = await database().prepare("SELECT pmid FROM plant_papers WHERE doi=? AND pmid<>? AND status='include'").bind(normalizedDoi(paper.doi), paper.pmid).first<{ pmid: string }>();
    if (paper.status === "include" && duplicate) throw new PlantError(`This DOI is already included under PMID ${duplicate.pmid}. Resolve the duplicate first.`, 409);
  }
  const audit = { actor, before: existing, after: paper, correction: input.correction === true };
  let result: D1Result[];
  try { result = await database().batch([
    // Compare-and-swap prevents two reviewers from silently overwriting one another.
    database().prepare("UPDATE plant_papers SET title=?,status=?,record=?,updated_at=? WHERE pmid=? AND record=?").bind(paper.title, paper.status, JSON.stringify(paper), paper.updatedAt!, paper.pmid, JSON.stringify(existing)),
    database().prepare("INSERT INTO plant_decisions(pmid,data,created_at) SELECT ?,?,? WHERE changes()>0").bind(paper.pmid, JSON.stringify(audit), new Date().toISOString()),
  ]); } catch (error) {
    const message = error instanceof Error ? `${error.message} ${error.cause instanceof Error ? error.cause.message : ""}` : "";
    if (/UNIQUE constraint|plant_papers_included_doi_unique/i.test(message)) throw new PlantError("This DOI was included by another review. Reload the catalog and resolve the duplicate.", 409);
    throw error;
  }
  if (!result[0].meta.changes) throw new PlantError("This paper changed during your review. Reload it before saving.", 409);
  return { paper };
}
export async function exportPlantCsv(status: PaperStatus = "include") {
  if (!["include", "pending", "exclude"].includes(status)) throw new PlantError("Unknown export status.");
  return catalogCsv((await plantCatalog()).papers, status);
}
export async function readPlantFulltext(pmid: string) {
  const paper = await getPlantPaper(pmid);
  const pmcid = await resolveArchiveId(paper, (id) => remote(`${ENDPOINT}/search?${new URLSearchParams({ query: `EXT_ID:${id} AND SRC:MED`, format: "json", resultType: "core", pageSize: "1" })}`));
  if (!pmcid) return { available: false, sections: [], message: "Europe PMC metadata does not provide an open full-text archive ID for this paper. Use the publisher or PubMed source.", source: `https://pubmed.ncbi.nlm.nih.gov/${paper.pmid}/` };
  const source = `${ENDPOINT}/${pmcid}/fullTextXML`;
  try {
    const xml = await remote(source, "xml") as string;
    if (!/<article[\s>]/i.test(xml)) return { available: false, pmcid, sections: [], message: "The full-text provider did not return an article.", source };
    const body = xml.match(/<body\b[^>]*>([\s\S]*?)<\/body>/i)?.[1] ?? xml;
    const sections: { title: string; text: string }[] = [];
    const pieces = body.split(/<title\b[^>]*>/i);
    let remaining = 90000;
    for (const piece of pieces) {
      const end = piece.indexOf("</title>");
      const title = end >= 0 ? plainText(piece.slice(0, end)) : "Article text";
      const text = plainText(end >= 0 ? piece.slice(end + 8) : piece).slice(0, Math.min(20000, remaining));
      if (text) { sections.push({ title: title || "Article text", text }); remaining -= text.length; }
      if (remaining <= 0 || sections.length >= 24) break;
    }
    return { available: true, pmcid, sections, source, message: "Source text is untrusted research content. Long articles may be shortened for reading." };
  } catch (error) { if (error instanceof PlantError && error.status === 404) return { available: false, pmcid, sections: [], message: "The provider does not offer open-access full text for this paper.", source }; throw error; }
}
export function requirePlantUser(request: Request) {
  const actor = request.headers.get("oai-authenticated-user-id");
  if (!actor) throw new PlantError("Sign in with ChatGPT to access this private catalog.", 401);
  return actor;
}
export async function plantPayload(request: Request) {
  const text = await request.text();
  if (text.length > 64000) throw new PlantError("The request is too large.", 413);
  try { const payload = JSON.parse(text); if (!payload || typeof payload !== "object" || Array.isArray(payload)) throw new Error(); return payload; } catch { throw new PlantError("Send a valid JSON object."); }
}
export async function plantRoute(request: Request, work: (actor: string) => Promise<Response | unknown>) {
  try { const result = await work(requirePlantUser(request)); return result instanceof Response ? result : Response.json(result, { headers: { "Cache-Control": "no-store" } }); }
  catch (error) { return Response.json({ error: error instanceof PlantError ? error.message : "The catalog could not complete this request. Please retry." }, { status: error instanceof PlantError ? error.status : 500, headers: { "Cache-Control": "no-store" } }); }
}
