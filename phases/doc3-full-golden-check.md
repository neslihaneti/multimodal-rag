# doc3 full index: development set check (5 November 2026)

The whole doc3.pdf was indexed: 200 pages, 562 chunks. The doc3 questions of the development set had been written from
the sample PDF (40 pages). Two things were checked on the full text:

1. Are the unanswerable questions still unanswerable?
2. Do the answerable questions have other valid pages?

Source: the OCR text in the index (`rag_pages.ocr_text`).

## Unanswerable questions: no change needed

| id | question | search over 200 pages |
|---|---|---|
| d3u01 | NASA budget in dollars for the LOT | No amount for the LOT. The only dollar amount belongs to the balloon programme: "about \$2.0 million for the three-year period" (p.170). The LOT table only says "Approved by NASA, but not funded" (p.29). |
| d3u02 | When was the Hubble Space Telescope launched? | "Hubble" appears only as "Hubble radius" (p.151) and "Hubble constant" (p.198). |
| d3u03 | Discovery of pulsars | "pulsar" never appears (the report is from 1965, the discovery from 1967). Neutron stars are discussed (p.147, p.149), pulsars are not. |

## Extra valid pages: PROPOSAL (awaiting the user's approval)

The report's recommendations repeat almost word for word in both the summary and the working-group sections.

| id | current page | proposed addition | evidence |
|---|---|---|---|
| d3q01 | 4 | **39** | "the Solar Astronomy Working Group met at Woods Hole, Massachusetts, from June 21 to July 3, 1965" (place + date) |
| d3q02 | 11 | **24** | Recommendation 8: "with a resolution corresponding to an aperture of at least 120 inches" (matches the golden answer exactly) |
| d3q09 | 157 (figure) | **156** | "The reflecting surfaces of the objective were a paraboloid and a hyperboloid. A ray diagram for these two surfaces is shown in Figure 4." |
| d3q14 | 102 | **111** | Recommendation 2: "aperture of the order of 20 km … With larger apertures, effects due to irregularities in the interplanetary medium …" |
| d3q19 | 102 + 103 (both needed) | **111** (enough on its own) | p.111 contains the full text: "within about ten years … a design study, of perhaps two years' duration". |
| d3q07 | 140 (figure) | 139 (borderline) | The text describing the figure: "a concentration toward the galactic plane, which implies that the sources are galactic objects". The question says "summary figure"; adding it is optional. |

The golden format is a problem for d3q19: `pages` + `needs_all_pages` cannot say "either {102, 103} or {111}". My
proposal: `pages: [102, 103, 111]`, `needs_all_pages: false`. It then leaves the "all pages" metric, and any one of the
pages is enough for Recall@k.

Near matches with no change proposed:

- d3q16 p.181: "high vacuum, gravity-free condition, and low temperature". Partial; no low pressure and weak field.
- d3q17 p.51: "11 years at least and may be as long as 22 years". An instrument lifetime, not the definition of the cycle.
- d3q20 p.149: "proton-antiproton annihilation". A different process.
