You are an AI assistant helping a researcher organize and analyze a dataset of academic papers, authors, and citations.

The researcher has provided a SQLite database located at `/home/user/research_data.db`.

The database has the following schema:
- `papers` (id INTEGER PRIMARY KEY, title TEXT, year INTEGER)
- `authors` (id INTEGER PRIMARY KEY, name TEXT)
- `paper_authors` (paper_id INTEGER, author_id INTEGER)
- `citations` (citing_paper_id INTEGER, cited_paper_id INTEGER)

**Your Objective:**
Write a Python script (you can name it anything, but it must be run to produce the output) that queries this database to find specific "knowledge transfer chains". 

A valid "knowledge transfer chain" is a sequence of exactly three papers (Paper A -> Paper B -> Paper C) that satisfies ALL of the following conditions:
1. Paper A cites Paper B.
2. Paper B cites Paper C.
3. All three papers (A, B, and C) were published in the year 2010 or later (>= 2010).
4. The author sets of the three papers must be completely mutually disjoint. This means:
   - Paper A and Paper B share no authors.
   - Paper B and Paper C share no authors.
   - Paper A and Paper C share no authors.

**Output Requirements:**
Your Python script must export the resulting chains into a JSON file located exactly at `/home/user/citation_patterns.json`.

The JSON file must contain a single list of objects. Each object should represent a valid chain and have a single key `"chain"` mapped to a list of the three paper titles `[Title A, Title B, Title C]`.
The list of objects should be sorted alphabetically by the title of Paper A, then by the title of Paper B, and finally by the title of Paper C.

Example output format:
```json
[
  {
    "chain": [
      "Paper A Title",
      "Paper B Title",
      "Paper C Title"
    ]
  }
]
```
Ensure your script executes successfully and generates the required file.