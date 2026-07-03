You are an AI assistant helping a research scientist organize and query a mixed-format dataset of academic publications. 

The researcher has three data files representing different aspects of the publication network in different formats:
1. **Relational Data**: `/home/user/data/authors.csv` - Contains author information.
   Format: `author_id,name,institution_id`
   (e.g., `1,Alice,INST_A`)

2. **Document Data**: `/home/user/data/papers.json` - Contains paper metadata, including an array of author IDs.
   Format: A single JSON array of objects, e.g.,
   `[{"paper_id": 101, "title": "Deep Learning", "author_ids": [1, 2]}, ...]`

3. **Graph Data**: `/home/user/data/citations.csv` - An edge list representing citations between papers.
   Format: `citing_paper_id,cited_paper_id`
   (e.g., `101,102` means paper 101 cites paper 102)

**Your Task:**
Write a C program located at `/home/user/analyzer.c` that programmatically orchestrates a query using the `sqlite3` command-line tool to find instances of "intra-institutional citation" — where an author of a paper cites another paper that has at least one author from the *same* institution.

Your C program must:
1. Generate an SQLite script or execute shell commands via `popen()`/`system()` to load the datasets into an in-memory or temporary SQLite database.
2. Use SQLite's JSON capabilities (`json_each`, `readfile`, etc.) to map the document-based `papers.json` into a relational format linking `paper_id` to `author_id`.
3. Construct a complex query joining the authors, mapped papers, and citation graph to find any `author_id` who wrote a `citing_paper_id` that cited a `cited_paper_id` authored by *any* author in the same `institution_id`.
4. Output the results to `/home/user/intra_institutional_citations.csv`.

**Output Schema Validation:**
The output file `/home/user/intra_institutional_citations.csv` must strictly be a comma-separated values file with the following header:
`author_id,author_name,citing_paper_id,cited_paper_id,institution_id`
Ensure there are no duplicates in the output (e.g., if a paper cites another paper and two authors share the institution, list the citing author once per paper citation). Order the results by `author_id` ascending, then `citing_paper_id` ascending.

Compile your program (e.g., `gcc -o /home/user/analyzer /home/user/analyzer.c`) and run it so the final CSV file is generated.