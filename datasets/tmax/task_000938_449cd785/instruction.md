You are a researcher organizing a dataset of academic papers to identify the most influential works and their citation networks. 

You have an SQLite database at `/home/user/papers.db` with the following schema:
- `papers` (`id` INTEGER PRIMARY KEY, `title` TEXT, `year` INTEGER)
- `citations` (`citing_id` INTEGER, `cited_id` INTEGER)

You also have a JSON schema file at `/home/user/schema.json` defining the required output format.

Write a Python script at `/home/user/process.py` that performs the following steps:
1. Queries the database to calculate the total number of direct citations each paper has received.
2. Uses a SQL window function to rank the papers within their publication `year` based on their total direct citations (Rank 1 = highest citations). In case of a tie in citations, order by `id` ASC.
3. Filters the results to only include papers that achieved Rank 1 in their respective year.
4. Sorts these Rank 1 papers by `year` DESCENDING and retrieves only the top 2 results (Pagination/Limiting).
5. For each of these 2 papers, traverses the citation graph to find its "indirect citations" — specifically, the `title`s of papers that cite a paper which directly cites the target paper (Pattern: C cites B, B cites A; find C's title given A). Sort the indirect citation titles alphabetically.
6. Constructs a Python dictionary/list structure representing these 2 papers, including their `id`, `title`, `year`, `total_citations`, and `indirect_citations` (as a list of strings).
7. Validates this data structure against the schema in `/home/user/schema.json` using the Python `jsonschema` library.
8. If validation passes, writes the final JSON array to `/home/user/results.json` with 2-space indentation.

You can install `jsonschema` via pip if needed. Run your script so that `/home/user/results.json` is successfully generated.