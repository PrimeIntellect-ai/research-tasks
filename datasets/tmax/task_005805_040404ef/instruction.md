I am a researcher organizing a massive, hierarchically linked collection of datasets. I have a SQLite3 database located at `/home/user/research.db` with a table named `files`.

The schema for the `files` table is:
`CREATE TABLE files (file_id INTEGER PRIMARY KEY, file_name TEXT, parent_id INTEGER, file_size INTEGER);`

Some datasets are derived from others, represented by the `parent_id` (which points to the `file_id` of the parent dataset). 

I need you to write a C program that uses the SQLite3 C API to analyze a specific dataset tree. Please do the following:

1. Create a C program at `/home/user/analyze.c`.
2. The program should connect to `/home/user/research.db`.
3. It must execute a single SQL query that:
    - Uses a **Recursive CTE** to find the dataset with `file_id = 1` and all of its hierarchical descendants.
    - Calculates the hierarchical `depth` of each file in this tree (where `file_id = 1` is depth 0, its immediate children are depth 1, etc.).
    - Uses a **Window Function** to calculate the running total (`running_total`) of the `file_size` across these descendants. The running total must be evaluated by ordering the rows first by `depth` in ascending order, and then by `file_id` in ascending order.
4. The C program should execute the query and write the results to a file located at `/home/user/report.txt`.
5. The output in `/home/user/report.txt` must be exactly formatted as comma-separated values (without a header row):
   `file_id,depth,file_size,running_total`
6. Compile the C program into an executable at `/home/user/analyze` and run it to generate the report. (You will likely need to link against `sqlite3`, e.g., `gcc analyze.c -o analyze -lsqlite3`).

Ensure your final output file strictly matches the specified CSV format.