You are a data analyst tasked with securing a knowledge graph querying pipeline. We have a multi-service architecture consisting of a Neo4j database, a Redis cache, and a Python Flask API. 

Your goals are twofold:
1. **Service Reconfiguration**: The startup script at `/app/start_services.sh` brings up Neo4j (port 7687), Redis (port 6379), and a Flask application (port 5000). The Flask app currently fails to connect to the databases because its configuration file `/home/user/config.json` has empty placeholders for the connection URIs. Reconfigure `/home/user/config.json` so that the Flask app successfully connects to Neo4j at `bolt://localhost:7687` (user: `neo4j`, password: `password`) and Redis at `redis://localhost:6379/0`. You must ensure that hitting `curl http://localhost:5000/health` returns `{"status": "ok"}`.

2. **Adversarial Query Sanitizer**: The API accepts parameters to search a graph of company data imported from CSVs. However, it is vulnerable to Cypher injection. You must write a Python CLI script at `/home/user/sanitizer.py` that takes a single command-line argument (the search parameter) and prints exactly `SAFE` to stdout if the parameter is a valid search string, or `EVIL` if it contains malicious Cypher injection patterns (such as `CALL`, `YIELD`, `DELETE`, `REMOVE`, `SET`, `MERGE`, `CREATE`, or comment syntax `//`). 

Your `sanitizer.py` must correctly classify inputs. We have provided two corpora of query parameters:
- `/home/user/corpora/clean.csv` (contains legitimate company names and alphanumeric search terms)
- `/home/user/corpora/evil.csv` (contains adversarial injection payloads)

An automated verifier will call your script against both corpora. You must reject 100% of the evil corpus and preserve 100% of the clean corpus. 

Do not modify the startup script. Ensure your `sanitizer.py` has executable permissions.