You are a data analyst working with exported CSV data representing a corporate knowledge graph. The data is located in `/home/user/data/` and consists of four files:
1. `persons.csv` (columns: `id`, `name`)
2. `companies.csv` (columns: `id`, `name`)
3. `board_members.csv` (columns: `person_id`, `company_id`)
4. `investments.csv` (columns: `investor_company_id`, `target_company_id`, `amount`)

Your task is to write a Bash script at `/home/user/find_conflicts.sh` that uses `sqlite3` to ingest these CSVs, optimize the schema, and find "conflict of interest" patterns. A conflict of interest is defined as a pattern where a Person sits on the board of Company A, and also sits on the board of Company B, and Company A has invested in Company B. 

Your Bash script must perform the following actions sequentially when executed:
1. Create a new SQLite database at `/home/user/graph.db`.
2. Import the four CSV files into corresponding tables (`persons`, `companies`, `board_members`, `investments`). Note that the CSVs have headers.
3. Design and create appropriate database indexes to optimize the specific graph query below. 
4. Run a SQL query to find all conflict of interest patterns. The query must return rows in the format: `person_name,investor_company_name,target_company_name`. 
5. Output the results of the query to `/home/user/conflicts.csv` (include headers: `person_name,investor_company_name,target_company_name`). The results must be ordered alphabetically by `person_name`, then `investor_company_name`, then `target_company_name`.
6. Output the `EXPLAIN QUERY PLAN` for your `SELECT` query into `/home/user/plan.txt`.

Constraint: You must design your index strategy so that your query plan uses index lookups (`SEARCH TABLE` using an index) for the `board_members` and `investments` joins. Full table scans (`SCAN TABLE`) on these relation tables during the join execution are not allowed and will fail the query plan check.

Ensure your Bash script is executable (`chmod +x`) and runs successfully without user interaction. Execute the script to generate the final output files.