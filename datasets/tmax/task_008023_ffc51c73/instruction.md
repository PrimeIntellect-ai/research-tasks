You are a data engineer building an ETL pipeline to process a raw knowledge graph export. You must write a robust Bash script that extracts a specific subgraph pattern from raw text dumps, utilizing native shell utilities (`awk`, `join`, `sort`, `grep`, etc.) to simulate query execution.

**Background:**
You have been provided with a raw, undocumented export of a company's organizational knowledge graph in `/home/user/raw_data/`. The data consists of two files:
1. `/home/user/raw_data/nodes.dump`: A delimited file containing entities. You must reverse-engineer its schema by inspecting it. It contains at least an ID, an entity type, a primary name, and some JSON-like properties.
2. `/home/user/raw_data/edges.dump`: A delimited file containing relationships. It contains a source ID, a target ID, and a relationship type.

**Your Goal:**
Write an ETL script in Bash at `/home/user/run_etl.sh` that performs the following steps:

1. **Reverse Engineering & Data Prep (Indexing):** 
   Identify the delimiter used in the dump files. Prepare optimized "indexes" (sorted intermediate files) necessary for fast joining, as processing large graphs requires properly sorted keys.
   
2. **Knowledge Graph Pattern Matching:**
   Using bash built-ins and coreutils, find all instances of the following graph pattern:
   `(Employee) -[REPORTS_TO]-> (Manager) -[MANAGES]-> (Project)`
   *Condition:* The Project node MUST have a property indicating `"status":"active"` in its properties field.

3. **Output Generation & Schema Validation:**
   The output must be written to `/home/user/output/active_project_paths.tsv`.
   The final output must be strictly Tab-Separated Values (TSV) with exactly three columns:
   `Employee_Name` \t `Manager_Name` \t `Project_Name`
   
   The output must be sorted alphabetically by `Employee_Name`, then `Project_Name`.

**Constraints:**
- Your script `/home/user/run_etl.sh` must be executable and run entirely in Bash without using external databases (no SQLite, PostgreSQL, etc.) or high-level languages like Python.
- Rely solely on standard Linux tools (`awk`, `sed`, `grep`, `sort`, `join`, etc.).
- Ensure `/home/user/output/` exists before writing the output.
- Do not hardcode the expected final output; your script must dynamically process the files in `/home/user/raw_data/`.

Once your script is written, execute it so the final output file is generated.