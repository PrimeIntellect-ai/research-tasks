You are a Data Engineer tasked with building an ETL pipeline to extract specific knowledge graph patterns from a raw edge list using Bash shell tools.

Your company analyzes software dependency chains. You have been provided with a dataset of relationships in a tab-separated values (TSV) file.

**Dataset Location:** `/home/user/raw_data/edges.tsv` (You do not need to create this, it will exist when you start).
**Format:** `Subject \t Relation \t Object`

**Your Goal:**
Write a Bash script that processes this edge list to find a specific chain of relationships, converts the results to a structured JSONL format, and validates the output schema.

**The Graph Pattern to find:**
You must find all instances of the following exact chain (Path of length 3):
1. A user follows a repository (`?user --follows--> ?repo`)
2. That repository contains a file (`?repo --contains--> ?file`)
3. That file imports a library (`?file --imports--> ?library`)

**Requirements:**
1. Create a script at `/home/user/pipeline/run_etl.sh`. Ensure it has executable permissions.
2. The script must use standard Unix/Bash command-line tools (e.g., `awk`, `join`, `sort`, `grep`, `jq`) to perform the graph pattern matching. Do not use external database engines like PostgreSQL or Neo4j.
3. The script must pipe the output of the pattern matching to generate a JSON Lines (`.jsonl`) file at `/home/user/pipeline/results.jsonl`.
4. The output must strictly follow this JSON schema for every line:
   `{"user": "...", "repo": "...", "file": "...", "library": "..."}`
5. The script must include an **output schema validation** step at the end. It should read the newly created `results.jsonl` and use `jq` to assert that every line is an object containing exactly the four keys (`user`, `repo`, `file`, `library`) with non-empty string values. If validation fails, the script should exit with a non-zero code. If successful, exit with code 0.
6. Run your script to generate the final `results.jsonl`.

*Note: You can assume `jq` is installed on the system. All files must be saved in the absolute paths specified.*