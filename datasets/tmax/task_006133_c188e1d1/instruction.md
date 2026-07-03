You are a data engineer tasked with building an ETL pipeline to extract and summarize project allocation data from an undocumented legacy SQLite database.

You have been provided with a database file at `/home/user/legacy_corp.db`. However, the original developers left no schema documentation. 

Your objectives are:
1. **Reverse Engineer the Data Model**: Inspect `/home/user/legacy_corp.db` to understand how employees, their reporting hierarchy (who reports to whom), and their project allocations are stored.
2. **Hierarchical Extraction**: Write a Python script at `/home/user/etl_pipeline.py` that connects to this database. It must use a recursive query (or equivalent recursive logic) to identify all employees in the organizational subtree reporting to the manager named exactly `'Eleanor Vance'`. This includes Eleanor herself, her direct reports, their direct reports, and so on.
3. **Parameterized Data Fetching**: For the identified employees, query the database to fetch their logged project hours. You must use parameterized queries in your Python script to prevent SQL injection and ensure safe query construction.
4. **Pipeline Aggregation**: Chain these extractions into a pipeline that calculates the total hours logged across the entire department (Eleanor and all her descendants), aggregated by the project code.
5. **Output**: The Python script should output the final aggregated data to a JSON file located at `/home/user/department_summary.json`. 

The format of `/home/user/department_summary.json` must be a single JSON object where the keys are the project codes (sorted alphabetically) and the values are the total hours logged as integers. 

Example of expected output format:
```json
{
  "PRJ-ALPHA": 120,
  "PRJ-BETA": 45
}
```

Write and execute the Python script to generate the required JSON file.