You are an AI assistant helping a biomedical researcher organize and query their datasets.

The researcher has set up a multi-service data platform consisting of:
1. A PostgreSQL database (relational patient metadata)
2. A MongoDB database (document-based clinical notes)
3. A Flask API that translates JSON payloads into SQL and NoSQL queries, and joins the results.
4. An Nginx reverse proxy meant to expose the Flask API.

However, the system has several issues:
1. **Multi-Service Composition**: The services are not properly connected. You need to fix the Nginx configuration and the Flask environment variables so that a POST request to `http://127.0.0.1:8080/query` correctly routes to the Flask app, and the Flask app can successfully query both PostgreSQL and MongoDB.
2. **Adversarial Queries**: The Flask API takes a custom JSON query DSL. Some researchers have been accidentally submitting queries that omit join conditions between SQL tables. This results in implicit cross joins (Cartesian products), which crash the PostgreSQL server due to unbounded result sets. 

Your task is two-fold:

### Part 1: Service Configuration
The services are started by a script `/home/user/start_services.sh` (already running). 
- **Nginx** is listening on port 8080. Its configuration is located at `/home/user/nginx/nginx.conf`. It needs to proxy all requests to the Flask app.
- **Flask** is running on port 5000. The app is located at `/home/user/app/app.py`. It reads environment variables `POSTGRES_URI` and `MONGO_URI`. You need to set these correctly in the startup environment or wrapper script `/home/user/app/run_flask.sh` so the app connects to PostgreSQL (localhost:5432, db: `biomed`, user: `researcher`, pass: `secret`) and MongoDB (localhost:27017, db: `biomed_notes`). 
Make sure the end-to-end flow works by querying the Nginx endpoint.

### Part 2: Cross-Join Detector (Adversarial Corpus)
You must write a Python CLI tool `/home/user/detect_cross_join.py` that analyzes the JSON query DSL and detects if the SQL portion will result in an implicit cross join.

The JSON query payload looks like this:
```json
{
  "sql_relations": ["patients", "visits", "diagnoses"],
  "join_conditions": ["patients.id = visits.patient_id", "visits.id = diagnoses.visit_id"],
  "mongo_filter": {"note_type": "discharge"},
  "cross_map": "patients.id -> mongo.patient_id"
}
```

A query is **SAFE (ACCEPT)** if the `sql_relations` form a single connected graph based on the `join_conditions`.
A query is **EVIL (REJECT)** if any relation in `sql_relations` is disconnected from the rest of the graph, or if there are multiple disconnected components (which causes an implicit cross join in SQL). Note that a single table with no join conditions is considered connected.

Your script must accept a single argument (the path to a JSON file) and print exactly `ACCEPT` or `REJECT` to standard output.
```bash
python3 /home/user/detect_cross_join.py <path_to_json_file>
```

We have provided two corpora of JSON queries:
- `/home/user/corpora/clean/`: Contains valid queries. Your script MUST output `ACCEPT` for 100% of these.
- `/home/user/corpora/evil/`: Contains queries missing join conditions. Your script MUST output `REJECT` for 100% of these.

Write your script robustly to handle parsing the `join_conditions` (which always take the format `tableA.column = tableB.column`).