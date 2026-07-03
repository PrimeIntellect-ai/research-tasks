You are an AI assistant helping a data analyst who is trying to process an organizational hierarchy into a graph. 

The analyst has exported two CSV files containing company data:
1. `/home/user/employees.csv` (columns: `id`, `name`, `department`)
2. `/home/user/reporting.csv` (columns: `emp_id`, `manager_id`)

They have started building a pipeline to calculate the PageRank of employees based on the reporting structure (where an edge goes from an employee to their manager, and recursively to their manager's manager, etc.).

There are three problems you must solve:

1. **Vendored Package Bug:** The analyst is using a custom local graph library located at `/app/tinygraph`. However, it fails to install via `pip install -e /app/tinygraph` because of a typo in its dependencies. You need to fix the package and install it in the environment.
2. **SQL Bug:** The analyst wrote a SQL script `/home/user/build_graph.sql` to generate the edges. Unfortunately, it contains an implicit cross join that explodes the dataset, linking everyone in the same department instead of following the reporting chain. You must rewrite `/home/user/build_graph.sql` using a **Recursive CTE** (SQLite syntax) to generate all pairs of `(source, target)` where `source` is an employee and `target` is *any* direct or indirect manager above them in the hierarchy.
3. **Pipeline Execution:** Once the SQL is fixed, run the provided script `python /home/user/pipeline.py`. This script reads the CSVs into an in-memory SQLite database, runs your `build_graph.sql`, passes the extracted hierarchical edges to the `tinygraph` library, and outputs the final PageRank scores to `/home/user/pagerank.json`.

**Your Goal:**
- Fix the package at `/app/tinygraph`.
- Rewrite `/home/user/build_graph.sql` so it correctly maps the hierarchical relational data into a graph edge list (columns must be exactly `source` and `target`).
- Ensure `/home/user/pagerank.json` is generated successfully and contains the correct network metrics.

Format of `/home/user/pagerank.json`:
```json
{
  "1": 0.05,
  "2": 0.12,
  ...
}
```