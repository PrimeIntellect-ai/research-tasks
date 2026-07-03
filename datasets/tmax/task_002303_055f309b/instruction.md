You are an assistant helping a researcher organize and analyze a dataset of academic papers. The researcher wants to identify the most influential authors based on a "citation impact score" that accounts for both direct and indirect citations.

You have been provided with an SQLite database at `/home/user/citations.db` with the following schema:
- `authors` (id INTEGER PRIMARY KEY, name TEXT)
- `papers` (id INTEGER PRIMARY KEY, title TEXT, author_id INTEGER, year INTEGER)
- `citations` (citing_paper_id INTEGER, cited_paper_id INTEGER)

Your task is to write a Python script at `/home/user/analyze.py` that calculates the citation impact score for each author and ranks them.

The citation impact score is calculated as follows:
1. **Direct Citations (Depth 1)**: 1.0 point for every paper that directly cites one of the author's papers.
2. **Indirect Citations (Depth 2)**: 0.5 points for every paper that cites a paper, which in turn cites one of the author's papers. (i.e., paths of exactly length 2 in the citation graph).
3. Sum these points across all papers written by the author.

Requirements:
- Compute the score for all authors.
- Use a window function (or Python equivalent sorting/ranking) to determine the dense rank (1st, 2nd, 3rd...) of each author based on their total impact score in descending order. If scores are tied, rank them alphabetically by name in ascending order.
- Save the top 3 ranked authors to `/home/user/results.json`.

The output file `/home/user/results.json` must contain a JSON array of objects with the following exact keys:
`author_name` (string), `score` (float), `rank` (integer).

Example format:
```json
[
  {"author_name": "Jane Doe", "score": 4.5, "rank": 1},
  {"author_name": "John Smith", "score": 3.0, "rank": 2}
]
```

Run your script to generate the `results.json` file.