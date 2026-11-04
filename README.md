# PlantCell Library

A plant single-cell literature workbench and reusable agent pipeline, inspired by the search/read workflow of [Paperclip](https://paperclip.gxl.ai/). This independent implementation uses Europe PMC and PubMed metadata; Paperclip access is optional.

**Private web app:** https://plantcell-library.mpengchong.chatgpt.site

## What it does

Discover → retrieve primary sources → review the experimental design → save evidence → export CSV.

- Searches plant single-cell, single-nucleus and spatial RNA literature from January 1, 2023 onward.
- Starts with 80 reviewed papers and a separate unreviewed search queue.
- Classifies spatial, time, or both using measured RNA locations and actual sampled times or sequential stages. Pseudotime alone does not qualify.
- Preserves evidence, source links, date corrections and an audit trail. New search matches are never automatically approved.
- Exports exactly `data_type,year,title,PMID`.
- Offers six agent tools: search, catalog, read, review, export and status.

The GitHub repository contains the code and public scientific metadata. The hosted application and its saved reviews remain owner-private.

## Repository layout

| Folder | Contents |
| --- | --- |
| `web/` | React/Vinext web app, durable D1 catalog, API routes, authenticated hosted MCP server and schema migrations |
| `agent/` | Standalone Python pipeline, stdio MCP server, agent guide, optional Paperclip reader and tests |
| `data/` | Original 80-paper CSV and source/screening notes |

The hosted website and hosted agent tools share one catalog. The downloadable/local Python kit is an independent backup; it does not silently synchronize its decisions with the hosted database.

## Run the local agent pipeline

Python 3.10 or later; the core pipeline uses the standard library. An optional `certifi` installation supplies certificate roots on systems that need it.

```bash
cd agent
python3 pipeline.py init --baseline baseline.json
python3 pipeline.py status
python3 pipeline.py fetch
python3 agent_mcp.py --help
```

Read [the agent guide](agent/AGENT_GUIDE.md) before automating scientific review. Retrieval gathers candidates; the connected agent or human must read evidence and submit explicit decisions. Never paste credentials into decision files or the CSV.

```bash
python3 -m unittest test_pipeline test_paperclip test_agent_mcp
```

## Run the web app locally

Node.js 22.13+ is required.

```bash
cd web
npm run install:ci
npm run build
```

Apply the two D1 schema migrations to the local preview database, in order:

```bash
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_cheerful_prism.sql
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0001_secret_komodo.sql
npm run dev
```

Open the printed loopback URL. For development sign-in, visit `/signin-with-chatgpt?return_to=/`. This mock identity is development-only; hosted sign-in is provided by Sites.

```bash
npx tsc --noEmit
node --experimental-transform-types --test lib/plant-validation.test.mjs
```

See [web documentation](web/README.md) for architecture, source handling, and deployment notes. Preserve applied migrations and the existing Site identity when updating this app.

## Validation

The initial release passed 27 Python tests, nine web validation/CSV tests, TypeScript checking, a production build, authenticated HTTP/MCP integration checks, live Europe PMC lookup and full-text retrieval, and browser checks of the library/discovery/review interfaces.

Open-access full text is not available for every article. Missing or failed source retrieval is reported explicitly; papers with unresolved sampling designs remain pending. This is a curated research tool, not a guarantee of exhaustive literature coverage or automatic scientific correctness.
