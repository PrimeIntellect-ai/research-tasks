I am a researcher organizing a large collection of scientific datasets. The datasets have complex dependencies (e.g., if a base dataset is updated, several derived datasets must also be recomputed). I have an edge list of these dependencies, but I need a tool to recursively trace the downstream impact of updating a specific dataset.

I have a tab-separated file at `/home/user/dataset_dependencies.tsv`. Each line contains two dataset IDs: the `Upstream` dataset and the `Downstream` dataset that depends on it.

Your task is to:
1. Write a Bash script at `/home/user/trace_lineage.sh` that takes exactly two arguments: a starting dataset ID (parameter 1) and the path to the dependency file (parameter 2).
2. The script must recursively find ALL downstream datasets that would be impacted by a change to the starting dataset (i.e., direct children, children's children, etc.).
3. The script should output the final list of impacted dataset IDs to standard output. The output must be unique (deduplicated), contain ONLY the dataset IDs, and be sorted alphabetically. Do not include the starting dataset ID in the output unless it somehow depends on itself.
4. After writing the script, make it executable and run it to find all impacted datasets for `DS_005`. Save the output to `/home/user/impacted_DS_005.txt`.

Ensure your script uses standard Bash tools (like `grep`, `awk`, `sed`, loops, etc.) and can handle arbitrary directed acyclic graphs.