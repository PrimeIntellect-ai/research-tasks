You are assisting a researcher who is organizing a large dataset of academic papers to study the influence of early foundational research. The dataset is stored in a SQLite database located at `/home/user/research_data.db`.

The database contains two tables:
1. `papers`: Contains information about research papers.
   Columns: `paper_id` (TEXT PRIMARY KEY), `title` (TEXT), `year` (INTEGER), `field_of_study` (TEXT)
2. `citations`: Contains the citation graph.
   Columns: `citing_id` (TEXT), `cited_id` (TEXT)
   *(This means the paper with `citing_id` references the paper with `cited_id`)*

The researcher wants to find the "influence lineage" of a seminal paper with the `paper_id` of `'ROOT-01'`. An influenced paper is any paper that cites `'ROOT-01'` directly, or cites a paper that cites `'ROOT-01'`, and so on (recursive descendants in the citation graph).

Your task is to write and execute a Python script that queries this database to find these influenced papers and exports the results based on the following strict requirements:
1. **Filtering**: Only include papers in the lineage that belong to the `field_of_study` = `'Artificial Intelligence'` and were published in the `year` >= 2020.
2. **Hierarchy/Depth**: Calculate the citation distance (depth) from `'ROOT-01'`. A paper directly citing `'ROOT-01'` has a depth of 1. A paper citing a depth-1 paper has a depth of 2, etc. If a paper is reachable via multiple paths, use the shortest path (minimum depth).
3. **Sorting**: Sort the final filtered results by `year` descending. If there's a tie, sort by `depth` ascending. If there's still a tie, sort by `paper_id` ascending.
4. **Pagination**: Return only the top 5 results based on the sorting criteria.
5. **Export**: Save the results as a strictly formatted JSON array to `/home/user/lineage_results.json`. Each object in the array must have the following keys:
   `paper_id` (string), `title` (string), `year` (integer), `depth` (integer).

You may use the `sqlite3` and `json` modules in standard Python. Do not modify the original database. Create the Python script, execute it to generate the JSON file, and ensure the output file exists at the specified path.