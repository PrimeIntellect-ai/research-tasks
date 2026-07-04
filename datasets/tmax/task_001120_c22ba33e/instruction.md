You are a data engineer tasked with building the C-based query component of an ETL pipeline that analyzes transaction streams. 

Your team lead has provided a database `/home/user/data.db` containing a single table of transactions. The exact table name, column names, and the required window function logic for the ETL feature are documented in a diagram image located at `/app/schema_rules.png`.

Your objective:
1. Analyze the image at `/app/schema_rules.png` to extract the table schema and the specific analytical aggregation (window function) required.
2. Write a C program at `/home/user/etl_query.c` that connects to the SQLite database `/home/user/data.db`.
3. Your C program must accept exactly three command-line arguments: `<u_id> <limit> <offset>`.
4. It must execute a parameterized query fetching data for the given `u_id`.
5. The query must compute the exact rolling/window calculation specified in the image.
6. The query must return results sorted by the timestamp column in DESCENDING order, applying the provided `limit` and `offset` for pagination.
7. Print the results to standard output (stdout) as comma-separated values. Format the floating-point calculations to exactly 2 decimal places (e.g., `105,45.50,42.33`).
8. Compile your program to an executable named `/home/user/etl_query`. Ensure it links against the SQLite3 library (i.e., using `-lsqlite3`).

Note: You can use `tesseract` to read the text from the PNG file if necessary. Handle database connections and statements securely using proper parameterized queries to avoid SQL injection (even though this is internal ETL).