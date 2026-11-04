# Plant single-cell spatial and temporal studies

Search cutoff: 2026-11-03. Eligible first online publication dates: 2023-01-01 through 2026-11-03, inclusive.

The CSV contains 80 original research papers across all plant species: 29 labelled `spatial, time`, 17 labelled `spatial`, and 34 labelled `time`. Its four columns match the supplied example: data_type, year, title, PMID. Rows are sorted by first online publication date and title. Titles and identifiers were checked against PubMed/Europe PMC metadata; HTML tags and terminal title periods were removed.

## Scope and definitions

- **Single-cell scope:** original plant single-cell or single-nucleus RNA studies, related single-cell multiomics, cell-resolved spatial RNA assays, and spatial RNA datasets integrated with an actual single-cell/nucleus reference. Single-nucleus sequencing is included. Pure bulk RNA-seq and spatial spots without a single-cell/nucleus reference or cell segmentation are excluded. A spatial study may use a previously published single-cell reference.
- **spatial:** experimentally measured RNA locations, including cell-resolved spatial platforms or spatial tissue RNA maps integrated with single-cell data. This label does not guarantee that every spatial measurement represents one cell: integrated Visium spots and laser-dissected tissue regions can contain multiple cells. Isolated marker validation, cell-type labels, inferred spatial coordinates, or spatial metabolomics alone do not qualify.
- **time:** separately profiled samples from at least two recorded chronological ages, collection times, storage ages, or named sequential developmental stages. Sparse comparisons are included and identified below. A pre-perturbation sample followed by a timed response can qualify when both are actual sampled temporal states; a treatment and a time-matched control at one endpoint do not establish a time course. Alternative organ fates, tissue positions, inferred pseudotime, RNA velocity, and bulk-only time series do not qualify by themselves.
- **spatial, time:** meets both criteria. This does not imply the same cells were continuously tracked or every spatial assay was performed at every single-cell time point. Most sequencing datasets are destructive snapshots from different cells.
- **year:** first online journal publication year, rather than print-issue year or preprint year. For example, the soybean Cell atlas (PMID 39742806) is listed as 2024 because it appeared online on 2024-12-31, although its issue is dated 2025. PMID 41388990 appeared online in December 2025 and is listed as 2025 despite its 2026 issue. Preprints, reviews, protocols, corrections, and purely computational reanalyses were not included.

## The supplied Marchantia paper

PMID 37321217 profiles actual ages D0, D1, D3, D6, D11 and D31 after germination. Its spatial component uses RNA-seq from six 1-mm tip-to-base strips of D31 thalli, integrated with scRNA-seq and reporter microscopy. It is retained as `spatial, time` to preserve the supplied example, with this distinction from native spatial single-cell sequencing made explicit. [Primary article](https://www.sciencedirect.com/science/article/pii/S1534580723002472).

## Search coverage

Sources searched were PubMed/Europe PMC, primary publisher pages and full texts, and primary dataset records such as GEO. A broad plant-title-focused Europe PMC query returned 667 records; targeted searches and reference checks supplied further candidates. Selection required evidence for the relevant experimental design, rather than matching words such as “dynamic” or “spatiotemporal” in a title. The exact broad query is recorded below. This is a curated, source-checked bibliography, not an exhaustive systematic review. Papers without a verifiable PMID or without enough accessible experimental-design information may be missing.

```text
(TITLE_ABS:"single-cell" OR TITLE_ABS:"single-nucleus" OR TITLE_ABS:"single-nuclei" OR TITLE_ABS:"spatial transcriptomics") AND (TITLE:"plant" OR TITLE:"Arabidopsis" OR TITLE:"rice" OR TITLE:"maize" OR TITLE:"wheat" OR TITLE:"soybean" OR TITLE:"cotton" OR TITLE:"tomato" OR TITLE:"Marchantia" OR TITLE:"moss" OR TITLE:"Physcomitrium" OR TITLE:"barley" OR TITLE:"Brassica" OR TITLE:"Populus" OR TITLE:"poplar" OR TITLE:"cucumber" OR TITLE:"pepper" OR TITLE:"potato" OR TITLE:"peanut" OR TITLE:"sorghum" OR TITLE:"Medicago" OR TITLE:"lotus" OR TITLE:"strawberry" OR TITLE:"tea" OR TITLE:"tobacco" OR TITLE:"cassava" OR TITLE:"grape" OR TITLE:"bamboo" OR TITLE:"seed" OR TITLE:"root" OR TITLE:"leaf" OR TITLE:"leaves" OR TITLE:"nodule" OR TITLE:"endosperm" OR TITLE:"meristem" OR TITLE:"fruit" OR TITLE:"floral" OR TITLE:"flower" OR TITLE:"pollen" OR TITLE:"shoot" OR TITLE:"callus" OR TITLE:"anther" OR TITLE:"stomatal" OR TITLE:"crop" OR TITLE:"Camellia" OR TITLE:"mesophyll" OR TITLE:"nodulation" OR TITLE:"physcomitrella" OR TITLE:"cambium" OR TITLE:"xylem" OR TITLE:"guard cell" OR TITLE:"dendrobium" OR TITLE:"lycopersicum") AND FIRST_PDATE:[2023-01-01 TO 2026-11-03] AND SRC:MED NOT PUB_TYPE:review
```

## Evidence and sources for included papers

### 2023 — High-resolution anatomical and spatial transcriptome analyses reveal two types of meristematic cell pools within the secondary vascular tissue of poplar stem

PMID: 36895162. Category: **spatial**. Plant: Populus. First online date used for eligibility/sorting: 2023-03-09.

High-resolution anatomy and ST maps poplar vascular meristems; results confirmed by single-cell sequencing and in situ hybridization. Primarily positional developmental gradient.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/36895162/); [Source 1](https://doi.org/10.1016/j.molp.2023.03.005).

### 2023 — Brassinosteroid gene regulatory networks at cellular resolution in the Arabidopsis root

PMID: 36996230. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2023-03-31.

scRNA-seq at six measured times: BRZ depleted control 0 h, followed by BL 0.5, 1, 2, 4, 8 h; 70,223 cells from the BL time experiment.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/36996230/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10119888/).

### 2023 — Integrated single-nucleus and spatial transcriptomics captures transitional states in soybean nodule maturation

PMID: 37055554. Category: **spatial, time**. Plant: Glycine max. First online date used for eligibility/sorting: 2023-04-13.

snRNA-seq nodules at 12 and 21 days postinfection; matched Stereo-seq.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/37055554/); [Source 1](https://www.nature.com/articles/s41477-023-01387-z).

### 2023 — Multiplexed single-cell 3D spatial gene expression analysis in plant tissue using PHYTOMap

PMID: 37308583. Category: **spatial**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2023-06-12.

PHYTOMap multiplexed FISH at individual-cell 3D resolution; 28 marker genes in roots.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/37308583/); [Source 1](https://www.nature.com/articles/s41477-023-01439-4).

### 2023 — The maturation and aging trajectory of Marchantia polymorpha at single-cell resolution

PMID: 37321217. Category: **spatial, time**. Plant: Marchantia polymorpha. First online date used for eligibility/sorting: 2023-06-14.

scRNA-seq at D0 (dormant gemmae), D1, D3, D6, D11 and D31 after germination. Spatial evidence is bulk RNA-seq from six 1-mm tip-to-base strips of D31 thalli integrated with scRNA-seq and reporters; not a native spatial single-cell assay.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/37321217/); [Source 1](https://www.sciencedirect.com/science/article/pii/S1534580723002472).

### 2023 — Single-cell resolution analysis reveals the preparation for reprogramming the fate of stem cell niche in cotton lateral meristem

PMID: 37626404. Category: **time**. Plant: Gossypium hirsutum. First online date used for eligibility/sorting: 2023-08-25.

scRNA-seq hypocotyls 0, 1, 6, 12 h after callus induction, two replicates per time point in two cultivars.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/37626404/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10463415/).

### 2023 — Cell-type-specific responses to fungal infection in plants revealed by single-cell transcriptomics

PMID: 37741284. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2023-09-22.

95,040-cell leaf atlas from Colletotrichum higginsianum infection at 24 and 40 hpi, with corresponding mock samples. Spatial response described through reporter/in situ validation, not native transcriptome-wide ST.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/37741284/); [Source 1](https://ueaeprints.uea.ac.uk/id/eprint/93104/1/Tang_etal_2023_CellHostAndMicrobe.pdf).

### 2023 — Single-nucleus transcriptomes reveal spatiotemporal symbiotic perception and early response in Medicago

PMID: 37749242. Category: **time**. Plant: Medicago truncatula. First online date used for eligibility/sorting: 2023-09-25.

snRNA-seq after 30 min, 6 h, 24 h Nod factor treatment, with control; 25,276 nuclei. Spatial in title means cell-type specificity; no native ST established.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/37749242/); [Source 1](https://www.nature.com/articles/s41477-023-01524-8).

### 2023 — Time series single-cell transcriptional atlases reveal cell fate differentiation driven by light in Arabidopsis seedlings

PMID: 37903986. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2023-10-30.

scRNA-seq etiolated, de-etiolating, and light-grown seedlings; Figure 1 time-series root and shoot atlases across light exposure times.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/37903986/).

### 2023 — Single-cell analysis identifies genes facilitating rhizobium infection in Lotus japonicus

PMID: 37935666. Category: **time**. Plant: Lotus japonicus. First online date used for eligibility/sorting: 2023-11-07.

Independent scRNA datasets at 5 and 10 dpi with Mesorhizobium loti and matched controls. 10 dpi sampled whole roots; 5 dpi sampled susceptible zones and included cyclops mutant. Real ages but tissue scope differs between ages.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/37935666/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC10630511/).

### 2024 — Decoding the gene regulatory network of endosperm differentiation in maize

PMID: 38167709. Category: **time**. Plant: Zea mays. First online date used for eligibility/sorting: 2024-01-02.

scRNA 17,022 cells from endosperm at 6 and 7 days after pollination; genuine sampled age comparison and cluster-specific temporal changes, plus DAP-seq.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/38167709/); [Source 1](https://www.nature.com/articles/s41467-023-44369-7); [Source 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC10762121/).

### 2024 — The single-cell transcriptome program of nodule development cellular lineages in Medicago truncatula

PMID: 38329875. Category: **time**. Plant: Medicago truncatula. First online date used for eligibility/sorting: 2024-02-07.

snRNA at 0, 24, 48, 96 h after S. meliloti inoculation; WT Jemalong A17 and hypernodulating sunn-4; integrated 16,211 nuclei. GEO explicitly gives time series.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/38329875/); [Source 1](https://www.cell.com/article/S2211124724000755/pdf); [Source 2](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE224539).

### 2024 — Spatial co-transcriptomics reveals discrete stages of the arbuscular mycorrhizal symbiosis

PMID: 38589485. Category: **spatial**. Plant: Medicago truncatula. First online date used for eligibility/sorting: 2024-04-08.

snRNA-seq plus 10x Visium of mycorrhizal roots. Spatial sample at 28 dpi; asynchronous colonization stages are not a measured time course.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/38589485/); [Source 1](https://www.nature.com/articles/s41477-024-01666-3.pdf).

### 2024 — Single-cell and spatial RNA sequencing reveal the spatiotemporal trajectories of fruit senescence

PMID: 38600080. Category: **spatial, time**. Plant: Hylocereus undatus. First online date used for eligibility/sorting: 2024-04-10.

scRNA-seq compares freshly harvested mature fruit with senescent fruit after approximately nine days of storage; 10x Visium of mature pericarp supplies spatial annotation. A sparse storage-age comparison, not a dense time series.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/38600080/); [Source 1](https://www.nature.com/articles/s41467-024-47329-x).

### 2024 — A single-cell transcriptome atlas reveals the trajectory of early cell fate transition during callus induction in Arabidopsis

PMID: 38720464. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2024-05-07.

scRNA-seq root explants after 0, 1, 4 days in callus induction medium.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/38720464/).

### 2024 — A spatial transcriptome map of the developing maize ear

PMID: 38745100. Category: **spatial**. Plant: Zea mays. First online date used for eligibility/sorting: 2024-05-14.

Stereo-seq and scRNA-seq of developing ear primordium; 12 cell types. Measured multi-time point sampling not established.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/38745100/); [Source 1](https://www.nature.com/articles/s41477-024-01683-2).

### 2024 — Single-nucleus RNA and ATAC sequencing analyses provide molecular insights into early pod development of peanut fruit

PMID: 38794796. Category: **time**. Plant: Arachis hypogaea. First online date used for eligibility/sorting: 2024-05-24.

snRNA-seq and snATAC-seq at three separately sampled pod stages: aerial peg; subterranean peg 2–3 days after soil entry; expanded pod about 4–7 days after soil entry. Marker in situ validation alone is not counted as spatial transcriptomics.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/38794796/).

### 2024 — Single-cell transcriptome atlases of soybean root and mature nodule reveal new regulatory programs that control the nodulation process

PMID: 38845198. Category: **spatial, time**. Plant: Glycine max. First online date used for eligibility/sorting: 2024-06-06.

snRNA-seq nodules at 12, 14, 21 and 28 days post inoculation. Molecular Cartography in situ mapping root/nodule sections with marker gene panels.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/38845198/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11369782/).

### 2024 — Spatiotemporal transcriptomic landscape of rice embryonic cells during seed germination

PMID: 38848718. Category: **spatial, time**. Plant: Oryza sativa. First online date used for eligibility/sorting: 2024-06-06.

Stereo-seq with single-cell segmentation and scRNA-seq; embryos at 6, 24, 36 and 48 h after imbibition.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/38848718/); [Source 1](https://www.sciencedirect.com/science/article/pii/S1534580724003344); [Source 2](https://db.cngb.org/stomics/project/STT0000049/spatialGeneExpression).

### 2024 — Spatiotemporal transcriptome atlas reveals gene regulatory patterns during the organogenesis of the rapid growing bamboo shoots

PMID: 39140996. Category: **spatial, time**. Plant: Phyllostachys edulis. First online date used for eligibility/sorting: 2024-08-14.

Single-nucleus RNA-seq and 10x spatial transcriptomics across three sampled early bamboo-shoot developmental stages, including longitudinal and transverse tissue sections.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/39140996/); [Source 1](https://nph.onlinelibrary.wiley.com/doi/abs/10.1111/nph.20059).

### 2024 — Establishment of single-cell transcriptional states during seed germination

PMID: 39256563. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2024-09-10.

scRNA-seq germinating embryos at 12, 24 and 48 h post stratification, supported by primary Figure 1 and methods.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/39256563/); [Source 1](https://www.nature.com/articles/s41477-024-01771-3).

### 2024 — Exaptation of ancestral cell-identity networks enables C4 photosynthesis

PMID: 39567684. Category: **time**. Plant: Oryza sativa; Sorghum bicolor. First online date used for eligibility/sorting: 2024-11-20.

Single-nucleus RNA atlas through measured de-etiolation time course: 0, 0.5, 1, 2, 4, 6, 8, 12, 48 h after light exposure; snATAC at 0 and 12 h. 190,569 rice and 265,701 sorghum nuclei. Data GSE248919.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/39567684/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11618092/); [Source 2](https://www.nature.com/articles/s41586-024-08204-3).

### 2024 — Integrating single nuclei and bulk RNA sequencing in rice shoot apical meristems uncovers candidate early floral transition gene networks

PMID: 39609296. Category: **time**. Plant: Oryza sativa. First online date used for eligibility/sorting: 2024-11-29.

Supplementary methods pages 1–4 confirm snRNA of shoot apices after 0, 5, 9 and 13 days short-day induction. Samples are barcoded separately and aggregated by time point for comparison with bulk. Journal issue 2025, first online 2024.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/39609296/); [Source 1](https://link.springer.com/article/10.1007/s00497-024-00514-w); [Source 2](https://media.springernature.com/original/springer-static/esm/art%3A10.1007%2Fs00497-024-00514-w/MediaObjects/497_2024_514_MOESM1_ESM.pdf).

### 2024 — A spatially resolved multi-omic single-cell atlas of soybean development

PMID: 39742806. Category: **spatial, time**. Plant: Glycine max. First online date used for eligibility/sorting: 2024-12-31.

snRNA-seq/scATAC across ten tissues, Visium matching root/hypocotyl and three seed developmental stages. First online 2024-12-31, journal issue 2025.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/39742806/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12136577/).

### 2025 — A rare PRIMER cell state in plant immunity

PMID: 39779856. Category: **spatial, time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2025-01-08.

Time-resolved snMultiome and MERFISH map immune responses; PRIMER cell state.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/39779856/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11798839/).

### 2025 — Multiplexed transcriptomic analyzes of the plant embryonic hourglass

PMID: 39824817. Category: **spatial**. Plant: Zea mays. First online date used for eligibility/sorting: 2025-01-18.

Single-cell RNA-seq of 11,459 protoplasts and eight Visium sections, all from Stage 1 embryos, with organ-specific LCM RNA maps. The multi-stage embryo series is bulk LCM RNA-seq and does not earn a single-cell time label.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/39824817/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11742662/).

### 2025 — Spatiotemporal transcriptome and metabolome landscapes of cotton fiber during initiation and early development

PMID: 39833150. Category: **spatial, time**. Plant: Gossypium hirsutum. First online date used for eligibility/sorting: 2025-01-20.

scRNA-seq plus Visium and spatial metabolomics. Spatial stages -1.5,-1,0,1,3,5 DPA; scRNA -1.5 to 1DPA.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/39833150/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11746981/).

### 2025 — Spatiotemporal transcriptome and metabolome landscapes of cotton somatic embryos

PMID: 39833155. Category: **spatial, time**. Plant: Gossypium hirsutum. First online date used for eligibility/sorting: 2025-01-20.

scRNA-seq plus Visium/metabolomics of nonembryogenic callus, globular, torpedo and cotyledonary embryos; genuine sampled development stages.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/39833155/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11747644/).

### 2025 — A single-cell and spatial wheat root atlas with cross-species annotations delineates conserved tissue-specific marker genes and regulators

PMID: 39893633. Category: **spatial**. Plant: Triticum aestivum. First online date used for eligibility/sorting: 2025-02-01.

scRNA-seq atlas of soil-grown roots validated with untargeted spatial transcriptomics (Stereo-seq).

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/39893633/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11860762/).

### 2025 — Spatial transcriptome and single-cell RNA sequencing reveal the molecular basis of cotton fiber initiation development

PMID: 40084712. Category: **spatial, time**. Plant: Gossypium hirsutum. First online date used for eligibility/sorting: 2025-03-01.

Spatial ovule maps -1,0,1 DPA plus scRNA-seq; fiber initiation.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40084712/); [Source 1](https://onlinelibrary.wiley.com/doi/10.1111/tpj.70064).

### 2025 — Single-Cell and Spatial Transcriptomics Reveals a Stereoscopic Response of Rice Leaf Cells to Magnaporthe oryzae Infection

PMID: 40123572. Category: **spatial, time**. Plant: Oryza sativa. First online date used for eligibility/sorting: 2025-03-24.

snRNA-seq mock, 24 hpi and 48 hpi; spatial RNA at 6, 12 and 24 hpi across Magnaporthe infection progression.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40123572/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12097076/).

### 2025 — An Arabidopsis single-nucleus atlas decodes leaf senescence and nutrient allocation

PMID: 40220755. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2025-04-11.

Over one million nuclei from 20 tissues encompassing multiple developmental stages, explicitly time-resolved leaf senescence sampling in abstract.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40220755/).

### 2025 — Resolving floral development dynamics using genome and single-cell temporal transcriptome of Dendrobium devonianum

PMID: 40238860. Category: **time**. Plant: Dendrobium devonianum. First online date used for eligibility/sorting: 2025-04-16.

31,511 cells across three actual sampled stages S1 early bud~0.2cm; S6 midbud~0.9cm fringe initiation; S15 fully open flowers.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40238860/); [Source 1](https://onlinelibrary.wiley.com/doi/10.1111/pbi.70094).

### 2025 — Single-cell transcriptomics reveal how root tissues adapt to soil stress

PMID: 40307555. Category: **spatial**. Plant: Oryza sativa. First online date used for eligibility/sorting: 2025-04-30.

Rice scRNA-seq + Molecular Cartography (smFISH); gel/soil and compaction comparisons, measured time course not established.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40307555/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12176638/).

### 2025 — 48-Hour and 24-Hour Time-lapse Single-nucleus Transcriptomics Reveal Cell-type specific Circadian Rhythms in Arabidopsis

PMID: 40324996. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2025-05-05.

snRNA-seq seedlings 13 points at 4 h intervals over 48 h, and 12 points at 2 h intervals over 24 h.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40324996/); [Source 1](https://www.nature.com/articles/s41467-025-59424-8).

### 2025 — Time-resolved single-cell atlas identifies the spatiotemporal transcription dynamics in vernalization response in Brassica rapa

PMID: 40378040. Category: **time**. Plant: Brassica rapa ssp. pekinensis. First online date used for eligibility/sorting: 2025-05-15.

58,282 scRNA transcriptomes at nonvernalized and weeks 1, 2, 3, 4 of cold treatment (NV,V1,V2,V3,V4); primary Figure 2.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40378040/); [Source 1](https://www.cell.com/action/showPdf?pii=S2211124725004966).

### 2025 — Single-cell and spatial multiomics identifies heterogeneous xylem development driven by mechanical stress in Populus

PMID: 40701155. Category: **spatial**. Plant: Populus. First online date used for eligibility/sorting: 2025-07-22.

scRNA-seq normal, tension and opposite xylem, validated by spatial transcriptomics+metabolomics. No measured temporal sampling established.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40701155/); [Source 1](https://doi.org/10.1016/j.devcel.2025.06.038).

### 2025 — STEMIN transcription factor drives selective chromatin remodeling for gene activation within a relaxed chromatin during reprogramming in the moss Physcomitrium patens

PMID: 40749217. Category: **time**. Plant: Physcomitrium patens. First online date used for eligibility/sorting: 2025-08-01.

snRNA-seq and snATAC-seq of untreated tissue and post-wounding windows 3–6 h, 10–14 h and 24–36 h. The last window was pooled with one-week protonemata; time windows are pooled snapshots, not continuous cell tracking.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40749217/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12316476/).

### 2025 — Single-cell transcriptome sequencing reveals the sphingolipid metabolism pathway plays an important role in leaf senescence in tobacco

PMID: 40764913. Category: **time**. Plant: Nicotiana tabacum. First online date used for eligibility/sorting: 2025-08-06.

Single-cell RNA-seq of 17,100 cells from mature and senescent leaves on three-month-old plants. Two independently sampled ageing stages; elapsed leaf ages were not specified.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40764913/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12326597/).

### 2025 — A single-cell, spatial transcriptomic atlas of the Arabidopsis life cycle

PMID: 40830271. Category: **spatial, time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2025-08-19.

snRNA-seq and paired spatial transcriptomics across ten actual developmental time points; seed, seedlings, rosettes, stem, flowers, siliques.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40830271/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12416547/).

### 2025 — Single-nucleus RNA-sequencing reveals the cellular programs driving nematode-induced giant cell formation in tomato

PMID: 41209832. Category: **time**. Plant: Solanum lycopersicum. First online date used for eligibility/sorting: 2025-08-22.

Single-nucleus RNA-seq of 35,393 nuclei in four libraries: galls and nearby root controls at five and ten days post-inoculation.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41209832/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12596086/).

### 2025 — Drought recovery in plants triggers a cell-state-specific immune activation

PMID: 40883303. Category: **spatial, time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2025-08-29.

snRNA-seq compares the end-of-drought state with 15 minutes after rehydration, with well-watered and irrigation controls; MERFISH localizes cell states. This is a sparse pre/post-rehydration comparison; the denser 15-minute to six-hour series uses bulk RNA-seq.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40883303/); [Source 1](https://www.nature.com/articles/s41467-025-63467-2); [Source 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC12397292/).

### 2025 — Single-nucleus multi-omics reveals the impact of drought stress on the development of soybean endosperm

PMID: 40886050. Category: **time**. Plant: Glycine max. First online date used for eligibility/sorting: 2025-08-29.

Single-nucleus RNA/ATAC multiome at proembryo (2–3 DAP), cotyledon (12–15 DAP), and early maturation (20–22 DAP) stages, under normal and drought conditions.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40886050/).

### 2025 — Spatial and single-cell transcriptomics capture two distinct cell states in soybean defense response to Phakopsora pachyrhizi infection

PMID: 41019740. Category: **spatial, time**. Plant: Glycine max. First online date used for eligibility/sorting: 2025-09-11.

snRNA at 1, 3 and 5 DPI; Visium at 4 and 7 DPI after Phakopsora infection.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41019740/); [Source 1](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2025.1637176/full).

### 2025 — Single-cell RNA sequencing reveals developmental trajectories and environmental regulation of callus formation in Arabidopsis

PMID: 40938467. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2025-09-12.

Actual scRNA-seq of leaf/root-derived initial callus, proliferating callus, and greening callus (6 samples total,3 stages per explant). Chronological day-to-sample mapping not perfectly explicit but physical stages verified.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40938467/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12431987/).

### 2025 — Time-resolved reprogramming of single somatic cells into totipotent states during plant regeneration

PMID: 40961939. Category: **spatial, time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2025-09-16.

Time-course single-nucleus RNA-seq and live imaging, integrated with spatial laser-capture microdissection RNA-seq during LEC2-mediated somatic embryo reprogramming.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/40961939/).

### 2025 — Single-cell and spatial omics reveal progressive loss of xylem developmental complexity across seed plants

PMID: 41109686. Category: **spatial**. Plant: Cunninghamia lanceolata. First online date used for eligibility/sorting: 2025-10-01.

scRNA-seq of conifer xylem plus spatial transcriptomics/proteomics/metabolomics. Cross-species evolutionary change is not real-time course.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41109686/); [Source 1](https://doi.org/10.1093/plcell/koaf253).

### 2025 — Spatial and single-cell expression analyses reveal complex expression domains in early wheat spike development

PMID: 41084016. Category: **spatial, time**. Plant: Triticum turgidum. First online date used for eligibility/sorting: 2025-10-13.

scRNA-seq plus Molecular Cartography smFISH across wheat spike W1.5, W2.5 and W3.5 stages (single-cell W2.5/W3.5).

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41084016/); [Source 1](https://link.springer.com/article/10.1186/s13059-025-03811-3).

### 2025 — The role of FRUITFULL controlling cell cycle during early flower development revealed by time-series snRNA-seq experiments

PMID: 41146337. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2025-10-27.

Single-nucleus RNA-seq of synchronized AP1-GR flowers at 0, 2, 4 and 8 days after dexamethasone induction.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41146337/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12557869/).

### 2025 — Spatial transcriptomics reveals expression gradients in developing wheat inflorescences at cellular resolution

PMID: 41388990. Category: **spatial, time**. Plant: Triticum aestivum. First online date used for eligibility/sorting: 2025-12-13.

MERFISH 200 genes at cellular resolution across 4 actual development stages. First online 2025-12-13, issue 2026.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41388990/).

### 2025 — Single-nucleus and spatial transcriptomics reveal the cell populations of intercalary meristems in bamboo

PMID: 41410774. Category: **spatial, time**. Plant: Phyllostachys edulis. First online date used for eligibility/sorting: 2025-12-18.

snRNA-seq+spatial across initial division,rapid division,rapid elongation stages of intercalary meristem.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41410774/); [Source 1](https://doi.org/10.1073/pnas.2511701122).

### 2025 — A single-cell-resolution spatial transcriptomic atlas decodes wheat spike development and yield potential

PMID: 41437568. Category: **spatial, time**. Plant: Triticum aestivum. First online date used for eligibility/sorting: 2025-12-23.

Spatial transcriptomes across 5 wheat spike stages plus W3.5 snRNA-seq. First online 2025-12-23, issue 2026.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41437568/); [Source 1](https://www.sciencedirect.com/science/article/pii/S1674205225004502).

### 2026 — Host microenvironment in potato-Phytophthora infestans interaction revealed by single-cell spatiotemporal transcriptome

PMID: 41495460. Category: **spatial, time**. Plant: Solanum tuberosum. First online date used for eligibility/sorting: 2026-01-06.

Stereo-seq single-cell segmented potato leaf atlas 3,6,12,24 hpi with time-matched mocks.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41495460/).

### 2026 — Serial Spatial Transcriptomes Reveal Regulatory Transitions in Maize Leaf Development

PMID: 41493197. Category: **spatial**. Plant: Zea mays. First online date used for eligibility/sorting: 2026-01-06.

Visium serial sections of SAME seedling SAM/P1-P5 leaf primordia integrated with public scRNA using Seurat anchors/SPOTlight. Positional leaf stages not chronological course.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41493197/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC13110159/).

### 2026 — Imputation integrates single-cell and spatial gene expression data to resolve transcriptional networks in barley shoot meristem development

PMID: 41501532. Category: **spatial**. Plant: Hordeum vulgare. First online date used for eligibility/sorting: 2026-01-07.

scRNA-seq W3.5 spikes plus Molecular Cartography smFISH segmented cells (vegetative SAM and inflorescence). Most developmental progression is positional apical-basal primordium gradient; conservative spatial-only.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41501532/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12830361/).

### 2026 — Single-cell transcriptomic analysis of plant quiescent center by third-generation sequencing reveals developmental trajectories

PMID: 41664205. Category: **time**. Plant: Arabidopsis thaliana; Oryza sativa comparison. First online date used for eligibility/sorting: 2026-02-09.

Single-cell long-read RNA-seq of isolated QC cells at 5 and 10 days after germination.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41664205/).

### 2026 — Cell fate acquisition at a de novo developmental boundary in the maize leaf

PMID: 41746728. Category: **time**. Plant: Zea mays. First online date used for eligibility/sorting: 2026-02-26.

scRNA-seq protoplasts independently sampled from Early-Fringe, Mid-Fringe, Late-Mid-Fringe blade-sheath boundary stages. Also lineage mapping and confocal morphometry.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41746728/); [Source 1](https://doi.org/10.1073/pnas.2533591123).

### 2026 — A single-nucleus transcriptome atlas of soybean anthers

PMID: 41831752. Category: **time**. Plant: Glycine max. First online date used for eligibility/sorting: 2026-03-12.

snRNA-seq of anthers collected in five bud-length groups spanning 1–5 mm; sampled stages span pollen mother cells to bicellular microspores. Developmental stage series, not elapsed-time tracking.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41831752/); [Source 1](https://www.sciencedirect.com/science/article/pii/S1673852726000767).

### 2026 — Integrated Single-Cell and Spatial Transcriptomics Reveal Cell-Type-Specific Immune Regulatory Networks in Maize Responding to Southern Corn Rust

PMID: 41837846. Category: **spatial, time**. Plant: Zea mays. First online date used for eligibility/sorting: 2026-03-16.

snRNA-seq+spatial leaves at 24 and 48 hpi with Puccinia polysora.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41837846/); [Source 1](https://doi.org/10.1002/advs.202512295).

### 2026 — Dynamic and cell-type specific transcriptional reprogramming underlies the floral transition in the maize shoot apical meristem

PMID: 41851888. Category: **time**. Plant: Zea mays. First online date used for eligibility/sorting: 2026-03-18.

scRNA-seq of shoot apical meristems at 14, 22 and 26 days after sowing. Bulk RNA time course is denser, but only these three times are single-cell sampled.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41851888/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC13112620/).

### 2026 — Stress drives plasticity in leaf ageing transcriptional dynamics in Arabidopsis thaliana

PMID: 41857406. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2026-03-19.

1,226 leaves, approximately 1 million nuclei across ageing/drought. Figure1: 647 leaves spanning 15 leaf stages over 9-day course at single-nucleus resolution.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41857406/).

### 2026 — A single-nucleus and spatial transcriptomic atlas of poplar leaves reveals the regulation of leaf polarity and cuticle deposition

PMID: 41866110. Category: **spatial**. Plant: Populus alba var. pyramidalis. First online date used for eligibility/sorting: 2026-03-20.

snRNA-seq and Stereo-seq of leaves from two-month-old plantlets; polarity and cuticle.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41866110/); [Source 1](https://www.sciencedirect.com/science/article/pii/S1673852726001037).

### 2026 — A single-cell transcriptome atlas reveals the transcriptionally earliest state in rice callus

PMID: 41882557. Category: **time**. Plant: Oryza sativa. First online date used for eligibility/sorting: 2026-03-25.

Separate scRNA-seq of embryonic callus after two weeks induction plus seven days subculture, and differentiated callus after seven additional days on differentiation medium. Two sampled culture stages, not a dense time series.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41882557/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC13141360/).

### 2026 — Histone deacetylases and cell-cycle regulators orchestrate cell-identity transitions during Arabidopsis root regeneration

PMID: 41889170. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2026-03-25.

scRNA-seq in uncut and 4, 9, 14, 24 and 36 h post-cut roots; full text line170. Also single-cell RNA/ATAC multiome.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41889170/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC13180275/).

### 2026 — Single-cell and spatial transcriptomics reveals the spatiotemporal trajectory of the small peptide TAP4 in delaying postharvest fruit senescence

PMID: 41947460. Category: **spatial, time**. Plant: Hylocereus undatus (Selenicereus undatus). First online date used for eligibility/sorting: 2026-04-07.

scRNA-seq compares fresh mature fruit with untreated and TAP4-treated fruit after 12 days of storage; Visium and RNA-FISH provide spatial annotation. A sparse storage-age comparison.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/41947460/); [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC13589556/).

### 2026 — Single-cell and spatial transcriptomics in Phragmites australis reveal the association of B chromosomes with plant invasiveness

PMID: 42021342. Category: **spatial**. Plant: Phragmites australis. First online date used for eligibility/sorting: 2026-04-22.

scRNA-seq+spatial common garden shoots from European and North American populations.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42021342/); [Source 1](https://doi.org/10.1186/s13059-026-04079-x).

### 2026 — Laminar patterning transcription factors orchestrate spatial metabolite partitioning in Capsicum fruit

PMID: 42086737. Category: **spatial, time**. Plant: Capsicum annuum. First online date used for eligibility/sorting: 2026-05-05.

332,468 nuclei across 57 samples spanning seedlings to mature fruits, integrated spatial transcriptomics.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42086737/); [Source 1](https://www.nature.com/articles/s41477-026-02293-w).

### 2026 — Single-cell and spatial transcriptomics reveal the regulatory continuum from initial substrates to storage compounds during wheat grain development

PMID: 42160834. Category: **spatial**. Plant: Triticum aestivum. First online date used for eligibility/sorting: 2026-05-14.

Single-nucleus RNA-seq integrated with spatial transcriptomics at a single milk stage, 25 days after flowering. Multiple chronological single-cell samples were not established.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42160834/); [Source 1](https://www.sciencedirect.com/science/article/pii/S0981942826003621).

### 2026 — Super-resolution multimodal spatial transcriptomics reveals an ovoid stem cell niche structuring de novo shoot regeneration

PMID: 42141722. Category: **spatial, time**. Plant: Solanum lycopersicum. First online date used for eligibility/sorting: 2026-05-14.

Super-resolution multimodal spatial transcriptomics ~1.2 million cells during shoot regeneration from wounding to organogenesis. Published successor to bioRxiv February 2026.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42141722/); [Source 1](https://doi.org/10.1016/j.molp.2026.05.008).

### 2026 — A transcriptional atlas of early Arabidopsis seed development suggests mechanisms for inter-tissue coordination

PMID: 42168363. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2026-05-21.

snRNA-seq of developing seeds at 3, 5 and 7 days after pollination, two biological replicates per time point. Targeted HCR validation is not counted as a spatial transcriptomic atlas.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42168363/); [Source 1](https://www.nature.com/articles/s41477-026-02295-8).

### 2026 — Spatial and single-cell transcriptomics uncover brassinosteroid-mediated coordination of sepal elongation in Arabidopsis

PMID: 42304499. Category: **spatial**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2026-06-17.

Single-cell and spatial RNA-seq compare drmy1-mutant and wild-type early sepal tissues. A chronological single-cell course was not established.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42304499/); [Source 1](https://doi.org/10.1186/s13059-026-04156-1).

### 2026 — Cell-type specific early perception of nine phytohormones revealed by single-nucleus transcriptomics in Arabidopsis

PMID: 42669725. Category: **time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2026-07-31.

snRNA-seq ~500,000 nuclei at 0.5 h and 3 h responses to 9 hormones, time-matched controls.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42669725/).

### 2026 — A single-nucleus transcriptomic atlas reveals distinct cell identities and key regulators of cellular differentiation during early rice seed development

PMID: 42605496. Category: **time**. Plant: Oryza sativa. First online date used for eligibility/sorting: 2026-08-17.

snRNA-seq of SJ2 caryopses at 3, 5 and 7 DAP, two replicates per stage; osbzr4 mutants at 3 and 5 DAP. Separate stage datasets documented in the primary data-availability statement.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42605496/); [Source 1](https://onlinelibrary.wiley.com/doi/10.1111/jipb.70373).

### 2026 — Single-Cell Transcriptomics Reveals the FA9-VAP Module Regulating Fatty Acid Accumulation in Soybean Seeds

PMID: 42633702. Category: **spatial**. Plant: Glycine max. First online date used for eligibility/sorting: 2026-08-23.

scRNA-seq plus 10x Visium, late maturity seeds WT vs FA9 knockout; one stage; first online 2026-08-23.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42633702/); [Source 1](https://onlinelibrary.wiley.com/doi/10.1111/pbi.70750).

### 2026 — Tangential single-cell spatial transcriptomics resolves early ray lineage trajectory in poplar

PMID: 42725656. Category: **spatial**. Plant: Populus tremula x Populus alba. First online date used for eligibility/sorting: 2026-09-01.

Tangential single-cell-resolution spatial atlas with public scRNA references. Two-year time-series is bulk stem transcriptomes/anatomy, so time label not warranted for single-cell data.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42725656/); [Source 1](https://academic.oup.com/plcell/advance-article-abstract/doi/10.1093/plcell/koag275/8790456).

### 2026 — A spatiotemporal single-cell transcriptomic atlas reveals fertilization-induced auxin signaling driving strawberry fruit set and development

PMID: 42827106. Category: **spatial, time**. Plant: Fragaria vesca. First online date used for eligibility/sorting: 2026-09-23.

Spatial transcriptomics + snRNA-seq + spatial metabolomics sampled postfertilization, fruit set, enlargement stages.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42827106/); [Source 1](https://doi.org/10.1038/s41467-026-77874-6).

### 2026 — Single-nucleus transcriptome atlas of Brassica developing seeds provides cellular and molecular insights into embryo abortion in interspecific hybrids

PMID: 42823797. Category: **time**. Plant: Brassica rapa (B. campestris) ssp. chinensis; B. oleracea crosses. First online date used for eligibility/sorting: 2026-10-01.

Abstract explicitly time-series snRNA-seq on developing seeds of interspecific versus intraspecific crosses.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42823797/).

### 2026 — Spatial and single-nucleus transcriptomic profiling reveal polarity and intracellular responses to mitochondrial dysfunction

PMID: 42848931. Category: **spatial, time**. Plant: Arabidopsis thaliana. First online date used for eligibility/sorting: 2026-10-05.

Single-nucleus RNA-seq after mitochondrial-inhibitor treatment at 1, 3, 6 and 12 hours, integrated with a 465-probe Xenium spatial RNA panel.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42848931/); [Source 1](https://academic.oup.com/plcell/article/38/10/koag308/8885782).

### 2026 — A spatiotemporal lifecycle atlas decodes spatial coordination in rice

PMID: 42838048. Category: **spatial, time**. Plant: Oryza sativa. First online date used for eligibility/sorting: 2026-10-06.

851,725 nuclei+347,640 Stereo-seq spatial bins; 10 organs and 61 stages from seed to seed.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42838048/); [Source 1](https://www.sciencedirect.com/science/article/pii/S0092867426011256).

### 2026 — Single-nucleus and spatial transcriptomics reveal dynamic cell differentiation and storage product accumulation in rice endosperm

PMID: 42933868. Category: **spatial, time**. Plant: Oryza sativa. First online date used for eligibility/sorting: 2026-10-26.

177,820 nuclei + 60,003 spatial spots across four actual caryopsis developmental stages.

Sources: [PubMed](https://pubmed.ncbi.nlm.nih.gov/42933868/); [Source 1](https://doi.org/10.1093/plcell/koag320).

## Selected exclusions and unresolved candidates

These are examples that explain the screening boundary, not a complete rejection log.

| PMID | Reason |
| --- | --- |
| [36928543](https://pubmed.ncbi.nlm.nih.gov/36928543/) | Undetermined, vegetative and floral buds represent alternative developmental fates; a sequential chronological single-cell series was not established. |
| [36684718](https://pubmed.ncbi.nlm.nih.gov/36684718/) | Cassava roots differ in diameter but were collected on the same date; chronological age progression was not established. |
| [37974530](https://pubmed.ncbi.nlm.nih.gov/37974530/) | Cotton anther single-nucleus data are tetrad-stage snapshots under different temperatures; inferred differentiation is pseudotime. |
| [37235696](https://pubmed.ncbi.nlm.nih.gov/37235696/) | Longan embryogenic-callus replicates are the same sampled stage; later chronological assays are validation, rather than single-cell RNA sampling. |
| [36896807](https://pubmed.ncbi.nlm.nih.gov/36896807/) | Cotton cotyledons sampled at one week in two genotypes; no measured temporal single-cell series. |
| [39046878](https://pubmed.ncbi.nlm.nih.gov/39046878/) | Moss scRNA samples are 14-day cultures; developmental dynamics are inferred by pseudotime. |
| [41213451](https://pubmed.ncbi.nlm.nih.gov/41213451/) | Marchantia sexual-organ atlas uses cross-sectional organ comparisons and pseudotime; no qualifying spatial or measured-time design established. |
| [40415399](https://pubmed.ncbi.nlm.nih.gov/40415399/) | Pearl millet single-cell data compare control with a single two-hour heat endpoint; the heat-memory time series is bulk RNA. |
| [40826955](https://pubmed.ncbi.nlm.nih.gov/40826955/) | Pinewood-nematode single-nucleus data are seven-day infected/control snapshots; other time points are bulk RNA or qPCR. |
| [39080318](https://pubmed.ncbi.nlm.nih.gov/39080318/) | Lotus has spatial time-series bins but no confirmed actual cell segmentation or single-cell/nucleus reference integration. |
| [42581385](https://pubmed.ncbi.nlm.nih.gov/42581385/) | Tomato gall BMKMANU spatial time series uses spot clusters; no qualifying single-cell/nucleus reference integration or cell segmentation established. |
| [42880234](https://pubmed.ncbi.nlm.nih.gov/42880234/) | Recent Medicago spatial time series; accessible sources did not establish single-cell resolution or a qualifying single-cell reference. |
| [42002027](https://pubmed.ncbi.nlm.nih.gov/42002027/) | Tobacco herbivory paper reports time-series single-cell data, but exact single-cell sampling design could not be confirmed in accessible sources; spatial metabolomics alone does not establish spatial RNA. Potential addition on full-text verification. |

Definitions: DAP, days after pollination; DPA, days post anthesis; DPI/dpi, days post inoculation/infection; hpi, hours post inoculation/infection; LCM, laser-capture microdissection; scRNA-seq, single-cell RNA sequencing; snRNA-seq, single-nucleus RNA sequencing; WT, wild type.
