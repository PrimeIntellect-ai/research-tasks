You are a data analyst and C developer tasked with processing a hierarchical Bill of Materials (BOM) from a CSV file. You will use SQLite's C API to parse the CSV into an in-memory database, optimize it, and extract a NoSQL-like JSON document representing the aggregated cost.

Your objective:
1. Ensure the SQLite3 development libraries (`libsqlite3-dev`) are installed on the system.
2. Create a C program at `/home/user/workspace/analyze_bom.c` that does the following:
   - Reads a CSV file located at `/home/user/data/parts.csv`.
   - Initializes an in-memory SQLite database (`:memory:`).
   - Creates a table named `bom` with columns: `part_id` (INTEGER PRIMARY KEY), `parent_id` (INTEGER), `qty_per_parent` (INTEGER), and `unit_cost` (REAL).
   - Parses the CSV file and inserts the records into the `bom` table.
   - Creates an index on the `parent_id` column to optimize hierarchical lookups.
   - Executes an `EXPLAIN QUERY PLAN` for the recursive query (defined below) and writes the resulting plan to `/home/user/workspace/query_plan.txt`.
   - Executes a `WITH RECURSIVE` query to calculate the total accumulated cost of the top-level assembly (where `part_id = 1`). The accumulated cost for a part is its `unit_cost` plus the sum of the accumulated costs of its children multiplied by their `qty_per_parent`.
   - The query must return a single row containing a JSON object using SQLite's JSON functions (simulating a NoSQL aggregation result). The JSON format must be exactly: `{"top_part_id": 1, "total_assembly_cost": <FLOAT>}`.
   - Writes the resulting JSON string to `/home/user/workspace/bom_result.json`.

The CSV file `/home/user/data/parts.csv` contains a header row and comma-separated values. Treat `NULL` strings in the `parent_id` column as SQL NULLs.

Compile your C program into an executable named `/home/user/workspace/analyze_bom` and execute it to produce the required output files.

Requirements for verification:
- `/home/user/workspace/query_plan.txt` must exist and contain the execution plan text from SQLite (it should demonstrate the use of the index you created).
- `/home/user/workspace/bom_result.json` must contain the exact JSON string resulting from your query.