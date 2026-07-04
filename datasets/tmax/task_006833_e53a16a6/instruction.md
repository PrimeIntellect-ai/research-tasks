You are acting as a data analyst. You have been provided with two CSV files representing a web graph:
1. `/home/user/pages.csv`: Contains information about web pages. Columns are `page_id,url,topic`.
2. `/home/user/links.csv`: Contains directed links between pages. Columns are `source_id,target_id`.

Your task is to write a Bash script at `/home/user/find_paths.sh` that uses `sqlite3` to perform the following operations:
1. Create an SQLite database at `/home/user/graph.db`.
2. Create tables `pages` and `links` and import the CSV data into them.
3. Design and create appropriate indexes on the `links` and `pages` tables to optimize graph traversal queries (specifically, indexing foreign keys/join columns).
4. Write a recursive CTE (Hierarchical Query) in SQLite to find all pages that are reachable within exactly or up to 3 hops (edges) starting from the page with the URL `http://example.com/start`.
5. Filter these reachable pages to only include those that have the topic `Data Querying`.
6. Output the URLs of these filtered pages, sorted alphabetically, to `/home/user/reachable.txt`. One URL per line.
7. Output the database schema (including your created indexes) to `/home/user/schema.txt` by running the `.schema` command in `sqlite3`.

Ensure your Bash script is executable and runs without errors. Run your script so that the output files are generated.