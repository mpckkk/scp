import assert from "node:assert/strict";
import test from "node:test";
import { catalogCsv, checkDate, checkPmid, normalizedDoi, normalizedTitle, plainText, resolveArchiveId, validateReview } from "./plant-validation.ts";

const pending = { pmid: "12345", title: "A measured plant study", date: "2024-04-12", year: 2024, status: "pending", sources: [], revision: "seed-12345" };
const decision = { pmid: "12345", expectedRevision: "seed-12345", status: "include", category: "time", evidence: "Single-cell RNA was sampled at 0, 12 and 24 hours.", sources: ["https://pubmed.ncbi.nlm.nih.gov/12345/"] };

test("source HTML and encoded tags are plain text, never active instructions", () => {
  assert.equal(plainText('<script>alert(1)</script>A &lt;i&gt;plant&lt;/i&gt; study &amp; atlas'), "A plant study & atlas");
  assert.equal(normalizedTitle("An <i>Arabidopsis</i> atlas"), normalizedTitle("An &lt;i&gt;Arabidopsis&lt;/i&gt; atlas"));
  assert.equal(normalizedDoi("https://doi.org/10.1/ABC"), "10.1/abc");
});
test("include requires reviewed evidence, sources, category, and a real eligible date", () => {
  assert.equal(validateReview(decision, pending).status, "include");
  assert.throws(() => validateReview({ ...decision, evidence: "keywords" }, pending));
  assert.throws(() => validateReview({ ...decision, sources: ["javascript:alert(1)"] }, pending));
  assert.throws(() => validateReview({ ...decision, category: undefined }, pending));
  assert.throws(() => validateReview({ ...decision, date: "2099-01-01" }, pending));
  assert.throws(() => checkDate("2024-02-30"));
  assert.throws(() => checkDate("2022-12-31"));
  assert.throws(() => checkPmid("not-a-pmid"));
});
test("included records cannot be silently removed or rewritten", () => {
  const included = validateReview(decision, pending);
  const exclusion = { ...decision, expectedRevision: included.revision, status: "exclude", evidence: "Full methods establish only one measured time point." };
  assert.throws(() => validateReview(exclusion, included), /explicit correction/);
  assert.equal(validateReview({ ...exclusion, correction: true }, included).status, "exclude");
  assert.equal(included.status, "include");
});
test("pending and exclusion decisions require a meaningful reason", () => {
  assert.throws(() => validateReview({ ...decision, status: "pending", evidence: "" }, pending));
  assert.throws(() => validateReview({ ...decision, status: "exclude", sources: [] }, pending));
});
test("CSV has exact four columns, escapes quotes and commas, and omits pending", () => {
  const included = validateReview({ ...decision, title: 'A "cell", plant atlas' }, pending);
  const csv = catalogCsv([pending, included]);
  assert.equal(csv.split("\r\n")[0], "\uFEFFdata_type,year,title,PMID");
  assert.match(csv, /time,2024,"A ""cell"", plant atlas",12345/);
  assert.equal(csv.split("\r\n").length, 3);
});
test("untrusted spreadsheet formula prefixes are neutralized", () => {
  const included = validateReview({ ...decision, title: '=HYPERLINK("https://example.com")' }, pending);
  assert.match(catalogCsv([included]), /'=/);
});
test("a reviewer cannot overwrite a change committed before its request begins", () => {
  const firstReview = validateReview(decision, pending);
  assert.notEqual(firstReview.revision, pending.revision);
  assert.throws(() => validateReview({ ...decision, correction: true }, firstReview), /changed since you opened/);
  assert.throws(() => validateReview({ ...decision, expectedRevision: undefined }, pending), /changed since you opened/);
  assert.equal(validateReview({ ...decision, expectedRevision: firstReview.revision, correction: true }, firstReview).status, "include");
});
test("missing seed PMCID is resolved by PMID before declaring full text unavailable", async () => {
  let calls = 0;
  const lookup = async (pmid) => { calls++; return { resultList: { result: [{ id: pmid, pmcid: "PMC123" }] } }; };
  assert.equal(await resolveArchiveId({ pmid: "12345" }, lookup), "PMC123");
  assert.equal(calls, 1);
  assert.equal(await resolveArchiveId({ pmid: "12345", pmcid: "PMC456" }, lookup), "PMC456");
  assert.equal(calls, 1);
});
test("metadata with no archive is distinct from failed or incomplete source lookup", async () => {
  assert.equal(await resolveArchiveId({ pmid: "12345" }, async () => ({ resultList: { result: [{ id: "12345" }] } })), undefined);
  await assert.rejects(resolveArchiveId({ pmid: "12345" }, async () => { throw new Error("network unavailable"); }), /network unavailable/);
  await assert.rejects(resolveArchiveId({ pmid: "12345" }, async () => ({ resultList: { result: [] } })), /availability could not be checked/);
});
