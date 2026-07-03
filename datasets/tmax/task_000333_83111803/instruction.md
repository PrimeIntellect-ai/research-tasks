You are an AI assistant helping a researcher organize their dataset of academic citations.

The researcher has an SQLite database located at `/home/user/dataset/citations.db` containing a graph of paper citations. The database has two tables:
1. `papers` (`id` INTEGER PRIMARY KEY, `title` TEXT)
2. `citations` (`source_id` INTEGER, `target_id` INTEGER) - represents a directed edge meaning "source paper cites target paper".

Your task is to write an executable Bash script at `/home/user/find_path.sh` that computes the shortest citation path between two papers using standard SQLite commands.

Requirements for `/home/user/find_path.sh`:
- It must take exactly two arguments: a `source_id` and a `target_id`.
- Example invocation: `./find_path.sh 101 105`
- It must execute a query against `/home/user/dataset/citations.db` to find the shortest path from the source to the target (graph traversal using SQL recursive CTEs).
- It must output **only** a valid JSON array of the paper IDs representing the shortest path, starting with the source and ending with the target. For example: `[101, 108, 105]`
- If multiple paths have the same shortest length, output any one of them.
- If no path exists, it should output `[]`.
- Do not output any other text, warnings, or column headers.

Ensure the script is executable (`chmod +x /home/user/find_path.sh`).