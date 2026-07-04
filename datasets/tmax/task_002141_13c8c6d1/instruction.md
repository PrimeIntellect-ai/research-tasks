I am a researcher organizing a dataset of academic papers, citations, and authors. I have a raw SQLite database at `/home/user/papers.db` containing this data, but I need to extract meaningful graph metrics and aggregated rankings from it to prepare for my upcoming publication.

Your task is to analyze this database, perform graph materialization and projection, and generate a validated JSON report of top authors per decade. 

Here are the specific steps you must complete:

1. **Schema Analysis & Graph Materialization**: 
   Analyze the SQLite database `/home/user/papers.db`. It contains tables for `papers`, `authors`, `paper_authors`, and `citations`.
   Materialize a directed citation graph where nodes are papers and edges are citations (`source_paper_id` cites `target_paper_id`).

2. **Graph Metric Calculation**:
   Calculate the PageRank for every paper in the citation graph using the standard formulation (alpha/damping factor = 0.85).

3. **Analytical Aggregation & Window Functions**:
   Compute an "Author Score" for each author, which is the sum of the PageRanks of all papers they have authored.
   Determine each author's "Peak Decade". A decade is defined as the floor of the year down to the nearest 10 (e.g., 2014 -> 2010). An author's Peak Decade is the decade in which they published the highest number of papers. If there is a tie in paper count across multiple decades, choose the *earlier* decade.
   Using window functions (in SQL, Pandas, or equivalent), rank the authors within each Peak Decade based on their Author Score in descending order.

4. **Co-authorship Projection**:
   Construct a projected co-authorship graph. For the top 3 authors in *each* Peak Decade, determine their "max_coauthor_weight" - the maximum number of times they co-authored a paper with any single other author in the entire database.

5. **Output Schema Validation**:
   Write the final results for the top 3 authors of each decade to `/home/user/top_authors.json`.
   The output must strictly validate against the JSON schema located at `/home/user/output_schema.json`.
   The final JSON should be an array of objects containing: `author_id`, `author_name`, `peak_decade`, `author_score` (float), `decade_rank` (integer, 1 to 3), and `max_coauthor_weight` (integer).

You can use any language (Python, bash, standard Unix tools) to accomplish this. Python with `networkx`, `pandas`, `sqlite3`, and `jsonschema` is highly recommended. Please ensure `/home/user/top_authors.json` exactly matches the required schema.