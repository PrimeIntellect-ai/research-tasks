You are a data engineer building an ETL pipeline to process a simple knowledge graph exported from our company's architecture repository.

We have exported our knowledge graph into two CSV files located in `/home/user/graph/`:
1. `/home/user/graph/nodes.csv` (columns: `id`, `label`, `name`)
2. `/home/user/graph/edges.csv` (columns: `src`, `dst`, `relation`)

Your task is to identify specific companies based on their technology stack, aggregate their full stack, and materialize the results into a JSON report.

Specifically, you need to:
1. **Graph Pattern Matching:** Find all `Company` nodes that use at least one technology belonging to the "Database" category.
   - The graph schema is: `(Company) -[USES]-> (Technology) -[BELONGS_TO]-> (Category)`
   - You are looking for paths where the `Category` node has the name `Database`.
2. **Cross-query Aggregation:** For the companies identified in step 1, retrieve *all* technologies they use (not just the databases).
3. **Graph Projection & Materialization:** Aggregate this data and write it to `/home/user/output/tech_summary.json`.

The output file `/home/user/output/tech_summary.json` must contain a single JSON array of objects.
Each object must have the following keys:
- `"company_name"`: The name of the company.
- `"total_techs"`: The integer count of total technologies used by this company.
- `"tech_list"`: An array of strings containing the names of all the technologies used by this company, sorted alphabetically.

The JSON array itself must be sorted alphabetically by `company_name`.
You may use Python, SQLite, `jq`, `awk`, or any standard Linux utilities available to write your ETL script and generate the output. Make sure the output directory exists before writing to it.