You are acting as a data assistant for a researcher organizing academic datasets. The researcher has data spread across two different SQLite databases and a JSONLines document. They need you to construct a specific dataset mapping international collaboration networks.

Here are the input files provided in `/home/user/`:
1. `authors.db`: An SQLite database containing an `authors` table with columns `id` (INTEGER), `name` (TEXT), and `institution_id` (INTEGER).
2. `institutions.db`: An SQLite database containing an `institutions` table with columns `id` (INTEGER), `name` (TEXT), and `country` (TEXT).
3. `papers.jsonl`: A JSONLines file where each line is a JSON object representing a paper. The format is `{"paper_id": "...", "title": "...", "author_ids": [...]}`.

**Your Goal:**
Write and execute a Python script `/home/user/process_network.py` that processes this data to find all pairs of co-authors (authors who appear together in the same `author_ids` list of a paper) who belong to institutions in *different* countries.

**Requirements for the output:**
1. Aggregate the results into a single CSV file named `/home/user/cross_country_collaborations.csv`.
2. The CSV must have the following headers exactly: `author1_name,author2_name,author1_country,author2_country,paper_count`.
3. To avoid duplicate edges (e.g., A-B and B-A), ensure that `author1_name` is alphabetically less than `author2_name` for every row.
4. Only include pairs where `author1_country` is not equal to `author2_country`.
5. The `paper_count` should represent the total number of papers they have co-authored together.
6. Sort the final CSV by `paper_count` descending. If there is a tie, sort by `author1_name` ascending, then `author2_name` ascending.

Use standard Python libraries (`sqlite3`, `json`, `csv`, etc.) to complete this task. Run your script to ensure the output CSV is generated correctly.