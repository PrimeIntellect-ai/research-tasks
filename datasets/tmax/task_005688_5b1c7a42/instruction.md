You are an AI assistant helping a data researcher organize and trace the lineage of their computational datasets.

The researcher has a complex hierarchy of datasets. Some datasets are "raw" data, while others are "derived" from one or more upstream datasets. The metadata and dependency graph for these datasets are stored in an SQLite database located at `/home/user/research.db`.

The database has the following schema:
- `datasets` (id INTEGER PRIMARY KEY, name TEXT UNIQUE, file_path TEXT)
- `dependencies` (source_id INTEGER, derived_id INTEGER) 

Your task is to create a set of tools to trace this lineage and aggregate the raw data sources for any given derived dataset.

Step 1: Write a Python script `/home/user/trace.py`
This script must:
1. Accept exactly one command-line argument: the `name` of a dataset.
2. Connect to `/home/user/research.db`.
3. Use a parameterized **Recursive Common Table Expression (CTE)** in SQL to dynamically traverse the graph and find all ancestors (upstream dependencies) of the given dataset.
4. Filter these ancestors to identify ONLY the "raw" datasets. A raw dataset is defined as one that has NO upstream dependencies (it never appears as a `derived_id` in the `dependencies` table).
5. Print the `file_path` of each raw dataset to standard output, one per line, sorted alphabetically.

Step 2: Write a Bash script `/home/user/summarize.sh`
This script must:
1. Accept exactly one command-line argument: the `name` of a target dataset.
2. Chain the output of your Python script: It should call `python3 /home/user/trace.py "$1"`.
3. Take the file paths outputted by the Python script, read the contents of each corresponding file on the filesystem, and concatenate their contents.
4. Write the final concatenated content to `/home/user/raw_data_summary.txt`.

Do not modify the database. When you are done, run `/home/user/summarize.sh "Final_Analysis_V3"` to generate the summary for the dataset named `Final_Analysis_V3`.