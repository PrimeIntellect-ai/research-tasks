You are an expert database administrator and systems programmer. We have a multi-service graph database stack serving a web application. The stack consists of:
1. A Graph Database (mocked backend) listening on TCP port 7687.
2. A Flask REST API listening on port 5000 that constructs and executes Cypher queries against the database.
3. An Nginx reverse proxy listening on port 8080 that routes external traffic to the Flask API.

We are experiencing denial-of-service and data-exfiltration attacks via maliciously crafted Graph queries (e.g., unbounded path traversals like `MATCH p=()-[*]-() RETURN p`, Cartesian products without relationship constraints, and schema discovery calls like `CALL db.schema()`).

Your task has two parts:

**Part 1: The C-based Query Classifier**
Write a C program located at `/home/user/app/cypher_sanitizer.c` and compile it to `/home/user/app/cypher_sanitizer`. 
This program must read a single Cypher query from standard input (up to 4096 bytes).
It must analyze the query strings and implement a set of rules to detect malicious graph patterns:
- Reject any query containing unbounded variable-length paths (e.g., `[*` or `*..]`).
- Reject any query attempting to call database schema functions (e.g., `CALL db.`).
- Reject any query containing a `MATCH` clause with multiple disconnected nodes (Cartesian product indicators, defined here as multiple comma-separated nodes in a MATCH without relationship links, e.g., `MATCH (a), (b)` without a corresponding `WHERE` or relationship).
- Accept all other standard queries (e.g., `MATCH (n:User)-[:KNOWS]->(m) RETURN n`).

If the query is safe, print `CLEAN` to stdout and exit with code 0.
If the query is malicious, print `EVIL` to stdout and exit with code 1.

**Part 2: Service Composition**
The multi-service stack is currently misconfigured. The Flask API is trying to connect directly to Nginx instead of the Graph DB, and Nginx is not correctly routing to the Flask app.
Reconfigure the Nginx configuration file at `/home/user/app/nginx.conf` and the Flask `.env` file at `/home/user/app/.env` so that:
- External requests to `http://localhost:8080/query` are routed to the Flask API at `127.0.0.1:5000/query`.
- The Flask API connects to the Graph DB at `127.0.0.1:7687`.

To verify your work, we will run an automated script that tests your compiled `cypher_sanitizer` against a hidden dataset of clean and evil queries. We will also test the end-to-end Nginx -> Flask -> GraphDB flow. Ensure all services can be started via `/home/user/app/start_services.sh`.