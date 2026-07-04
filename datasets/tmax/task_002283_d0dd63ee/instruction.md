You are a Database Reliability Engineer managing the migration and restoration of our infrastructure's graph database backups. We have been receiving tainted backup dumps that either contain malicious Cypher queries injected into node properties, violate our strict schema requirements, or contain impossible backup topologies (e.g., circular backup dependencies).

Your task is to build a pre-restore validation tool in Rust to filter these backups. 

1. Setup:
Initialize a Rust CLI tool at `/home/user/graph_filter`. The tool should compile to an executable that takes a single file path as an argument.
Example: `cargo run -- <path_to_json_backup>`

2. Schema Extraction (Image Handling):
Our data architect left the allowed edge types in an image file located at `/app/schema_rules.png`. You must extract the text from this image (e.g., using `tesseract`) to find the comma-separated list of allowed edge relationships. Hardcode or dynamically load this list into your Rust program. Any graph backup containing an edge type NOT in this list must be rejected.

3. Graph Backup Format:
The backups are provided as JSON files containing an array of edge objects. Example:
```json
[
  {
    "source": "db-cluster-1",
    "target": "s3-bucket-a",
    "type": "BACKUP_OF",
    "properties": {
      "post_hook_query": "MATCH (n) RETURN n"
    }
  }
]
```

4. Validation Rules (The Sanitizer):
Your Rust tool must read the JSON file and reject it (exit with a non-zero code) if ANY of the following rules are violated. If all rules are satisfied, it must accept it (exit with code 0).
- **Rule A (Schema)**: Every `type` in the edge list must strictly match one of the allowed edge relationships extracted from `/app/schema_rules.png`.
- **Rule B (Adversarial Injection)**: No `post_hook_query` value inside `properties` may contain the substrings `DELETE`, `DROP`, `REMOVE`, or `SET` (case-insensitive).
- **Rule C (Graph Topology)**: The graph formed by edges of type `BACKUP_OF` must be a Directed Acyclic Graph (DAG). If there is any cycle involving `BACKUP_OF` edges (e.g., A backups to B, B backups to C, C backups to A), the backup is fundamentally corrupt and must be rejected. 

5. Verification:
Test your tool against the two corpora located in `/app/corpora/`.
- `/app/corpora/clean/`: Contains valid backups. Your tool must exit 0 for all of these.
- `/app/corpora/evil/`: Contains malicious or corrupted backups violating one or more of the rules above. Your tool must exit non-zero for all of these.

Ensure your Rust project is built and functions correctly. We will automatically iterate over the files in both corpora and check your program's exit codes.