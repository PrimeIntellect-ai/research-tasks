You are acting as a data researcher organizing and analyzing a recent export from our NoSQL citation graph database. 

You have been provided with two JSON Lines (JSONL) files in the `/home/user/dataset/` directory:
1. `/home/user/dataset/nodes.jsonl`: Contains metadata for scientific papers (nodes). Each line is a JSON object with at least a `node_id` (string) and an `authors` array (list of strings).
2. `/home/user/dataset/edges.jsonl`: Contains the directed citation edges. Each line is a JSON object with a `src` (string) indicating the citing paper's `node_id`, and a `dst` (string) indicating the cited paper's `node_id`.

Your task is to calculate a specific "self-citation" metric. We define a "self-citation edge" as any edge where the `src` paper and the `dst` paper share **at least one** author in common.

Using only standard Linux command-line tools (like `bash`, `jq`, `awk`, `join`, `grep`, `sort`, etc.), write a pipeline or a short bash script to count the total number of self-citation edges in the dataset. 

You must output the final count as a single integer into the file: `/home/user/self_cite_count.txt`.

Constraints:
- Do not use Python, Perl, Ruby, or Node.js. You must solve this using shell commands and standard CLI utilities.
- The output file `/home/user/self_cite_count.txt` should contain *only* the integer count.