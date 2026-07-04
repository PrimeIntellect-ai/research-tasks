You are an AI assistant helping a researcher organize and analyze a dataset of academic papers and their citation network.

The dataset consists of two CSV files located in `/home/user/`:
1. `papers.csv` - Contains columns: `paper_id`, `title`, `year`, `author_id`
2. `citations.csv` - Contains columns: `source_paper_id`, `target_paper_id` (meaning the source paper cites the target paper)

Your task is to write a Python script `/home/user/analyze.py` that processes these files (you may use an in-memory SQLite database to leverage SQL and recursive CTEs) and outputs a final report in `/home/user/report.json`.

The JSON report must contain exactly the following keys:
1. `"shortest_path"`: A list of `paper_id` strings representing the shortest citation path from paper `"P10"` to paper `"P1"`. The path should start with `"P10"`, follow citations (source -> target), and end with `"P1"`.
2. `"pattern_matches"`: A list of lists of `paper_id` strings. Each sublist should represent a citation chain of exactly 3 papers `[A, B, C]` where:
   - Paper A was published in 2020
   - Paper A cites Paper B
   - Paper B was published in 2018
   - Paper B cites Paper C
   - Paper C was published in 2015
   Sort the outer list lexicographically by the `paper_id` of the first paper in each chain.
3. `"top_authors"`: A list of `author_id` strings representing the top 3 authors who have received the most citations from papers published in the year 2021 or earlier. Count how many times an author's papers are cited by source papers where `source_paper.year <= 2021`. Order the result by citation count descending, and break ties by `author_id` ascending.

Requirements:
- Only use standard library Python modules (e.g., `sqlite3`, `csv`, `json`). No external libraries like `pandas` or `networkx` are installed.
- Your script should be completely self-contained and executed by running `python3 /home/user/analyze.py`.
- Ensure `/home/user/report.json` exactly matches the required keys and formats.