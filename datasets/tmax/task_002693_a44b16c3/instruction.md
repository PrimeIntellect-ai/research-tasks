You are an ETL data engineer managing a new data ingestion pipeline. Our system relies on multiple cooperating services: Nginx (reverse proxy), a Rust-based ingestion listener, MongoDB (document storage), and Redis (caching graph query plans). 

There are two primary objectives you need to complete:

**1. Fix the Service Composition**
We have a startup script at `/home/user/app/start.sh` that brings up Nginx (port 8080), MongoDB (port 27017), and Redis (port 6379). A mock ETL listener runs on port 9000. However, the Nginx configuration at `/home/user/app/nginx.conf` is misconfigured. It is currently dropping API requests instead of proxying them. You must adjust `/home/user/app/nginx.conf` so that any HTTP request to `http://localhost:8080/api/` is properly forwarded to the ETL listener at `http://127.0.0.1:9000/api/`. 

**2. Write the ETL Payload Sanitizer**
Our NoSQL aggregation pipelines and shortest-path graph algorithms are vulnerable to malformed or malicious JSON payloads from upstream data sources. 
You must write a Rust command-line tool that acts as a payload filter. 
Create a Rust project at `/home/user/etl_filter` and build a release binary (`/home/user/etl_filter/target/release/etl_filter`). 

The binary must accept exactly one argument: the absolute path to a JSON file.
It must parse the JSON and determine if the payload is "clean" or "evil".
*   Exit code `0`: The payload is clean.
*   Exit code `1` (or any non-zero): The payload is evil.

A JSON payload has the following structure:
```json
{
  "nodes": ["A", "B", "C"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "B", "to": "C"}
  ],
  "metadata": {
    "source": "api_v1",
    "priority": 5
  }
}
```

A payload is considered **EVIL** if it meets *either* of the following conditions:
*   **NoSQL Injection Attempt:** The `metadata` object (or any nested object within `metadata`) contains a key that starts with a `$` (e.g., `$where`, `$gt`). 
*   **Graph Cycle:** The `edges` define a directed cycle (e.g., A -> B -> C -> A). Cyclic graphs cause infinite loops in our Redis shortest-path caching layer.

A payload is considered **CLEAN** if it contains no `$` keys in its metadata and its edges form a Directed Acyclic Graph (DAG). 

You can test your tool against the sample files in `/home/user/corpus/clean/` and `/home/user/corpus/evil/`. 

Your final deliverables are the corrected `/home/user/app/nginx.conf` and the compiled `/home/user/etl_filter/target/release/etl_filter` binary. Ensure your Rust project compiles without interaction.