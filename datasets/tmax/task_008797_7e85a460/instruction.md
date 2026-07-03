You are an AI assistant helping a bioinformatics researcher organize and query a complex metadata dataset. 

The researcher has a file located at `/home/user/metadata.jsonl`. Each line is a JSON object representing a research paper, its authors, the datasets it used, and the papers it cites.

Your objective is to build a multi-language querying pipeline that performs NoSQL-style aggregation, knowledge graph pattern matching, and schema validation.

Here are your instructions:

**Phase 1: NoSQL Aggregation Pipeline**
Write a script (Python, Node.js, or `jq`) that processes `/home/user/metadata.jsonl` to find the "Top Datasets".
A dataset's "Impact Score" is the sum of the `citation_count` of all papers that use that dataset.
Find the dataset IDs of the top 2 datasets with the highest Impact Score.
Output this strictly as a JSON array of strings (the dataset IDs) to `/home/user/top_datasets.json`.

**Phase 2: Knowledge Graph Pattern Matching**
Write a Python script (`/home/user/graph_query.py`) that builds a directed knowledge graph from `/home/user/metadata.jsonl` (using a library like `networkx`).
The graph should include:
- Nodes for Papers (using `paper_id`)
- Nodes for Datasets (using `dataset_id`)
- Directed edges from Paper to Dataset (`USES_DATASET`)
- Directed edges from Paper to Paper (`CITES`) - if Paper A's `citations` list includes Paper B's ID, draw an edge A -> B.

Using the dataset IDs from `/home/user/top_datasets.json` as your starting point, find the following graph pattern:
A Top Dataset ($D$) is used by Paper ($P_1$). $P_1$ is cited by ($P_2$). $P_2$ uses another dataset ($E$) where $E \neq D$.
Collect all such unique dataset pairs $(D, E)$.

**Phase 3: Pipeline Chaining and Schema Validation**
Create a Bash wrapper script `/home/user/run_pipeline.sh` that:
1. Runs the aggregation script.
2. Runs the graph query script.
3. Outputs the final pairs into `/home/user/final_pairs.json`.
4. Validates `/home/user/final_pairs.json` against this exact JSON schema (you may use a python script for validation):
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "source_dataset": { "type": "string" },
      "target_dataset": { "type": "string" }
    },
    "required": ["source_dataset", "target_dataset"]
  }
}
```
If the schema validation passes, the bash script should exit with code 0 and print "VALID" to standard output. If it fails, exit with code 1.

Execute your pipeline so that `/home/user/final_pairs.json` is generated and fully validated.