You are a data analyst evaluating a mock natural language "inference" heuristic on customer reviews. You need to build a reproducible data processing and benchmarking pipeline.

Your workspace contains three data sources that need to be combined:
1. `/home/user/data/source1.csv` (Columns: `id`, `text`, `date`)
2. `/home/user/data/source2.csv` (Columns: `req_id`, `review_body`, `timestamp`)
3. `/home/user/data/meta.csv` (Columns: `item_id`, `category_code`)

Write a multi-language pipeline (e.g., using Bash and Python) to perform the following steps. You must create a master execution script at `/home/user/pipeline.sh` that runs the entire process from start to finish.

**Phase 1: Multi-source Data Joining**
Combine `source1.csv` and `source2.csv` into a standardized format with columns `id` and `text` (map `req_id` to `id`, and `review_body` to `text`). Discard date/timestamp columns. 
Then, join this combined dataset with `meta.csv` by matching `id` (and `req_id`) to `item_id`. The resulting dataset should have columns: `id`, `text`, `category_code`. Rows with no matching category should be dropped.

**Phase 2: Tokenization and Dataset Preparation**
Process the joined dataset's `text` column with the following strict tokenization rules:
1. Convert all text to lowercase.
2. Remove all characters except alphanumeric characters and spaces (e.g., punctuation).
3. Split the text into tokens by spaces.
4. Remove any tokens that are less than 3 characters long.
5. Count the remaining valid tokens to create a `token_count` integer for each row.

**Phase 3: Inference Simulation & Benchmarking**
Simulate an inference scoring algorithm on each row using this formula:
`score = (token_count * length_of(category_code)) modulo 10`

Write a benchmarking wrapper in your script that runs this inference scoring process over the entire dataset exactly 100 times in a loop to test execution performance. 

**Phase 4: Reporting**
Your `pipeline.sh` script must output a summary report at `/home/user/report.json` with the exact following schema:
```json
{
  "total_rows": <integer, number of rows in the final joined dataset>,
  "sum_scores": <integer, the sum of the 'score' for all rows computed in a single pass>,
  "benchmark_runs": 100
}
```

Constraints:
- You must create `/home/user/pipeline.sh` and make it executable. running `./pipeline.sh` should generate `/home/user/report.json`.
- Do not use external ML libraries like HuggingFace or spaCy; standard libraries and tools like `pandas`, `csv`, `awk`, or `sed` are sufficient and expected.