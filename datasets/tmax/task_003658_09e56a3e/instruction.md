You are an AI assistant helping a data researcher organize a massive, interconnected network of experimental datasets. 

The researcher has an SQLite database at `/app/datasets.db` containing two tables:
1. `datasets` (id TEXT, name TEXT, size INTEGER, created_at TEXT)
2. `dependencies` (source_id TEXT, target_id TEXT) - indicating that `source_id` depends on `target_id`.

We also have a compiled, stripped binary oracle at `/app/dataset_oracle`. This binary takes a root dataset ID and a page number, recursively traverses the dependency graph to find all downstream datasets, sorts them by `size` descending, and returns a specific page of results (page size = 50). Unfortunately, the binary is a black box and we need a maintainable Python implementation that replicates its exact logic while being highly optimized.

Your task:
1. Write a Python script at `/home/user/query_datasets.py`.
2. The script must take two command-line arguments: `<root_dataset_id>` and `<page_number>`.
3. It should recursively query the `datasets.db` database to find all indirect and direct dependencies of the `<root_dataset_id>`.
4. Implement proper indexing strategies on the SQLite database to ensure the recursive queries execute in under 100 milliseconds. Your script should create any necessary indexes in the database if they don't exist.
5. Sort the final resolved list of dependent datasets by `size` (descending), then by `created_at` (ascending), and finally by `id` (ascending).
6. Implement pagination with a page size of 50. Filter out any datasets whose size is less than 1024 bytes.
7. Output the resulting list of dataset IDs for the requested page as a JSON array of strings, printed to standard output.
8. Save the final JSON array of the executed command `python3 /home/user/query_datasets.py root_001 2` to a file at `/home/user/results.json`.

Ensure your Python code is highly optimized. The evaluation will measure the Jaccard similarity of your paginated outputs against the black-box binary, as well as checking if your query execution time falls within the required threshold.