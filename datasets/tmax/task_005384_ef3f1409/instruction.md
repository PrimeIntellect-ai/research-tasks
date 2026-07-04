You are an AI assistant helping a data researcher organize and process a dataset of academic publications, authors, and citation metadata. The researcher has been struggling with a SQL query that returns massively inflated counts due to an implicit cross join, and needs help integrating relational data with a NoSQL document dataset.

Your task consists of three phases:

**Phase 1: Fix the SQL Query and Apply Window Functions**
In `/home/user/data/research.db` (a SQLite database), there are three tables:
- `Authors` (author_id, name)
- `Papers` (paper_id, title, year)
- `Author_Paper` (author_id, paper_id)

The researcher wrote a query located at `/home/user/scripts/bad_query.sql` to find the number of papers each author published per year, but it currently does an implicit cross join, resulting in wrong counts.
1. Fix the query so it correctly calculates the number of papers per author per year.
2. Add a Window Function to the query to calculate the `cumulative_papers` for each author over time (ordered by year).
3. The final columns should be `name`, `year`, `yearly_papers`, `cumulative_papers`.
4. Run the fixed query and save the CSV output (with headers) to `/home/user/output/author_stats.csv`.

**Phase 2: NoSQL Aggregation Pipeline**
You are provided with a JSON lines file `/home/user/data/metadata.jsonl` acting as a document dump. Each document represents a paper's metadata, including a `tags` array.
Write a Python script `/home/user/scripts/aggregate.py` that processes this file (simulating a NoSQL aggregation pipeline) to:
1. Unwind the `tags` array.
2. Group by tag.
3. Count the number of papers per tag.
4. Sort in descending order of count, then alphabetically by tag.
5. Save the output as a JSON array of objects `[{"tag": "...", "count": N}, ...]` to `/home/user/output/tag_aggregation.json`.

**Phase 3: Graph Projection and Schema Validation**
Write a script `/home/user/scripts/build_graph.py` that reads the SQLite DB and outputs a graph representation to `/home/user/output/graph.json`.
The output must be a JSON object with:
- `nodes`: Array of objects. Each author node: `{"id": "A_<author_id>", "type": "Author", "label": "<name>"}`. Each paper node: `{"id": "P_<paper_id>", "type": "Paper", "label": "<title>"}`.
- `edges`: Array of objects representing authorship: `{"source": "A_<author_id>", "target": "P_<paper_id>", "relation": "AUTHORED"}`.

Validate your `graph.json` against the JSON Schema located at `/home/user/data/graph_schema.json`. If it passes, create an empty file at `/home/user/output/VALIDATION_PASSED`.

*Constraints:*
- You may use any standard Linux tools, Python, or SQLite CLI.
- Ensure all output files are placed in `/home/user/output/` which you must create.