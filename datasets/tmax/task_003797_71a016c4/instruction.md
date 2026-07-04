You are an AI assistant helping a researcher organize and optimize access to a massive dataset of scientific papers and citations. We have a microservice architecture providing data access to other researchers, but the database is getting overloaded by poorly written or unoptimized queries. 

Your goal is to optimize the database with the correct indexes and write a query validator that intercepts and blocks inefficient queries based on their execution plans.

**System Setup:**
We have a multi-service setup located in `/app/`.
1. Run `/app/start_services.sh` to start the PostgreSQL database (port 5432), Redis cache (port 6379), and a Flask API (port 5000).
2. The PostgreSQL database is named `research_db` (User: `researcher`, Password: `password`, Host: `127.0.0.1`, Port: `5432`).
3. The database contains two large tables: 
   - `papers (id SERIAL PRIMARY KEY, title TEXT, published_year INT, domain_id INT, citation_count INT)`
   - `citations (paper_id INT, cited_paper_id INT)`

**Your Tasks:**
1. **Database Optimization:** Analyze the schema and create the optimal indexes in PostgreSQL to support hierarchical recursive queries (e.g., finding all direct and indirect citations of a paper) and window functions (e.g., ranking papers by citation count within their domain and year). 
2. **Query Validator Script:** Write a Python CLI script at `/home/user/query_filter.py` that takes the path to a file containing a SQL query as its only argument.
   - The script must connect to `research_db` and retrieve the query execution plan using `EXPLAIN (FORMAT JSON)`.
   - The script must print `REJECT` to standard output if the query plan includes any `Seq Scan` node on the `papers` or `citations` tables.
   - The script must also print `REJECT` if the query plan's `Total Cost` at the top level is greater than `50000`.
   - Otherwise, it must print `ACCEPT`.

To ensure your solution is robust, we have provided two corpora of queries:
- `/app/corpus/clean/`: Contains well-structured, indexable queries (including recursive CTEs and analytical window functions). Once your indexes are created, your script MUST output `ACCEPT` for all of these.
- `/app/corpus/evil/`: Contains inherently inefficient queries (e.g., full table scans on unindexed columns, cross joins). Your script MUST output `REJECT` for all of these.

Ensure your Python script uses standard libraries or `psycopg2` (which is already installed). Do not modify the existing data in the tables.