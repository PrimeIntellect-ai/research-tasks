You are a data engineer tasked with building an ETL pipeline to process NoSQL-style document data into a relational graph structure for dependency analysis. 

We have an export of our internal job scheduler in JSON format at `/home/user/raw_pipeline_data.json`. Each document represents a job and contains its `id`, `name`, `compute_cost` (integer), and `depends_on` (a list of job IDs that must complete before this job can start).

Your objective is to write a Python script at `/home/user/etl_graph.py` that performs the following steps:

1. **Graph Projection & Materialization**: Read the JSON data and load it into a new SQLite database at `/home/user/pipeline.db`. You must create two tables:
   - `nodes` (id TEXT PRIMARY KEY, name TEXT, compute_cost INTEGER)
   - `edges` (source TEXT, target TEXT)
   Note: The `edges` table should represent the flow of execution. If Job B's `depends_on` list includes Job A, the edge should be `source = 'A'` and `target = 'B'`.

2. **Index Strategy**: Create appropriate index(es) on the `edges` table to optimize recursive graph traversals starting from a `source` node to find all its downstream `target` nodes.

3. **Parameterized Loading**: Insert the data into these tables safely using parameterized SQL queries.

4. **Graph Query**: Using a single parameterized recursive CTE (Common Table Expression) in SQLite, query the database to find the total combined `compute_cost` of the job `JOB_001` AND all jobs that exist in its downstream execution path (i.e., jobs that depend on `JOB_001`, jobs that depend on those jobs, and so on). 

5. **Output**: Write the final calculated integer total cost to a plain text file at `/home/user/result.txt`.

Ensure your script handles everything from database creation to writing the final result. You may run your script using the terminal once it is written.