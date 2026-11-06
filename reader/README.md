# reader/ (owner: Dler)
Input: PDF or scan. Output: `schema.Extraction` JSON.
Every non-empty value needs `source` (page, bbox, snippet) and `confidence`.
Fill `reader` (model/version) and `cost_eur` for cost tracking.
Develop against `data/fixtures/golden/*/extraction.json`.
