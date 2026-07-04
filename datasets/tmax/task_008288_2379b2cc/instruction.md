You are helping a researcher organize a massive hierarchy of scientific datasets. The dataset metadata is currently stored in a JSON Lines format, representing a graph of datasets where each dataset can have a parent dataset.

Your task is to write a C program that reads this document-based representation, maps it to a relational SQLite database, creates an optimized index strategy for hierarchical lookups, and uses a recursive query to calculate the total size of a specific dataset and all its descendants.

Here are the specific requirements:
1. You are provided with a file at `/home/user/datasets.jsonl`. Each line is a JSON object with the following fields: `id` (integer), `parent_id` (integer or null), `name` (string), and `size` (integer).
2. Install any necessary development libraries for SQLite3 and JSON parsing in C (e.g., `libsqlite3-dev`, `libjson-c-dev`).
3. Write a C program at `/home/user/process_datasets.c`.
4. The C program must:
   - Create a new SQLite database at `/home/user/research.db`.
   - Create a table named `datasets` with appropriate columns (`id`, `parent_id`, `name`, `size`).
   - Parse the `/home/user/datasets.jsonl` file and insert all records into the `datasets` table.
   - Create an index on `parent_id` to optimize recursive and hierarchical queries.
   - Execute a query using a Recursive Common Table Expression (CTE) to find the dataset with the `name` exactly equal to `"Astrophysics"`, find all of its recursive descendants, and calculate the sum of the `size` of the "Astrophysics" dataset and all its descendants combined.
   - Write the resulting total sum (a single integer) to the file `/home/user/result.txt`.
5. Compile and run your C program to produce the final output.

Ensure your C program is robust and properly closes database connections and frees memory.