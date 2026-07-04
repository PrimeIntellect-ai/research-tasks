You are a database administrator and backend engineer tasked with optimizing and securing a graph data pipeline. 

Your organization uses a multi-service architecture comprising:
1. **Neo4j** (Graph Database) running on `bolt://localhost:7687` (auth: `neo4j/password`).
2. **Redis** (Cache) running on `localhost:6379`.
3. A missing **Go API Proxy** that you must build.

The infrastructure configuration is provided in `/app/docker-compose.yml`. 

Your objectives are:

**1. Create Index Strategy (Graph Optimization)**
We frequently run recursive and hierarchical Cypher queries on `Employee` nodes (filtering by `emp_id`) and `Department` nodes (filtering by `dept_name`).
Create a Cypher script at `/home/user/indexes.cypher` that creates B-tree indexes on `Employee(emp_id)` and `Department(dept_name)`.

**2. Build a Caching Query Proxy in Go**
Write a Go web server at `/home/user/app/proxy.go` that:
- Listens on `http://localhost:8080`.
- Exposes a `POST /query` endpoint accepting raw Cypher queries as plain text in the request body.
- Implements a **Query-to-Pipeline Chain**: 
  - Hash the incoming query string (SHA-256).
  - Check Redis for the hash. If found, return the cached JSON result immediately.
  - If not in Redis, execute the query against Neo4j.
  - Cache the Neo4j JSON response string in Redis with a 60-second TTL.
  - Return the response to the client.

**3. Implement the Adversarial Cypher Firewall**
Your Go proxy must include a query parser/filter to prevent Cypher injection and destructive operations. It must act as a strict firewall:
- **Accept (Clean)**: Safe data retrieval queries, including complex `MATCH`, `WITH`, `RETURN`, `WHERE`, `ORDER BY`, `LIMIT`, and recursive path patterns (e.g., `MATCH (e:Employee)-[:REPORTS_TO*]->(m)`).
- **Reject (Evil)**: Any query containing mutating keywords (`CREATE`, `MERGE`, `SET`, `DELETE`, `REMOVE`, `DETACH`, `DROP`), data loading (`LOAD CSV`), or procedural calls (`CALL apoc`, `CALL db`). If an evil query is detected, return an HTTP 403 Forbidden status code.

**Testing Your Implementation**
We have provided two directories of test payloads:
- `/app/corpus/clean/`: Contains valid, complex read-only queries.
- `/app/corpus/evil/`: Contains malicious queries trying to drop nodes, exfiltrate data via APOC, or bypass basic string matching using varied casing.

Your firewall must accept 100% of the clean corpus and block 100% of the evil corpus. To begin, bring up the services using `docker-compose up -d` in `/app`, write your index setup, and implement the Go proxy.