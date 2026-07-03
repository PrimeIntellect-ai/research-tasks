You are a localization engineer at a software company. The community has submitted a large batch of raw translation suggestions, but the data is messy, contains duplicates, and uses inconsistent typography. You need to build an automated ETL pipeline to process these contributions.

Your task is to write two Python scripts and one Bash orchestration script to process a JSONL file of translations. 

Input File: `/home/user/raw_translations.jsonl`
Format: Each line is a JSON object with the following keys:
- `id` (string): The message ID.
- `lang` (string): The locale code (e.g., "es-ES").
- `raw_text` (string): The suggested translation text.
- `timestamp` (integer): Epoch timestamp of the submission.
- `contributor_score` (integer): Reputation score of the submitter.

**Step 1: Tokenization and Normalization (`/home/user/normalize.py`)**
Write a Python script that reads standard input (JSONL) and writes normalized JSONL to standard output.
The script must apply the following normalization rules to the `raw_text` field:
1. Trim all leading and trailing whitespace.
2. Replace any internal sequence of whitespace characters (spaces, tabs, newlines) with a single space character.
3. Unify smart/typographic quotes to standard ASCII quotes:
   - Replace `“`, `”`, `«`, and `»` with `"` (double quote).
   - Replace `‘` and `’` with `'` (single quote).
Keep all other fields identical.

**Step 2: Sorting and Grouping (`/home/user/aggregate.py`)**
Write a Python script that reads the normalized JSONL from standard input.
It must group the records by `lang` and `id`. 
For each `(lang, id)` pair, it must select exactly ONE best translation based on the following rules:
1. Pick the translation with the highest `contributor_score`.
2. If there is a tie in `contributor_score`, pick the one with the highest `timestamp` (newest).
3. Output the result as a CSV file to standard output. The CSV must have the header exactly: `lang,id,normalized_text`.
4. The CSV rows must be sorted alphabetically by `lang` (ascending), and then alphabetically by `id` (ascending). Use standard CSV escaping (e.g., via Python's `csv` module).

**Step 3: Pipeline DAG Orchestration (`/home/user/pipeline.sh`)**
Write a Bash script that chains these operations together. 
1. It must pipe `/home/user/raw_translations.jsonl` through `normalize.py`.
2. It must pipe the output of `normalize.py` directly into `aggregate.py`.
3. It must redirect the final CSV output to `/home/user/final_translations.csv`.
4. The script must use `set -e` to fail if any step fails.
5. Make sure the script is executable and execute it to generate the final CSV.

Ensure `/home/user/final_translations.csv` is correctly generated before considering the task complete.