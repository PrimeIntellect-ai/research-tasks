You are an AI assistant helping a bioinformatics researcher organize and aggregate complex experimental datasets. The researcher is working with a distributed local microservices architecture that serves different parts of the dataset.

Currently, the system is partially configured. You need to fix the service configurations, start the services, and write a high-performance Bash script to query, aggregate, and format the data.

### System Architecture
The environment contains three cooperating services located in `/app/`:
1. **Nginx API Gateway**: Should listen on port `8080` and route requests to the backend services.
2. **Metadata Service (Flask)**: Runs on port `5001`. Provides dataset schemas and lists of active experiment IDs.
3. **Genomics Data Store (Flask)**: Runs on port `5002`. Provides raw JSON records for specific experiment IDs.

### Task Objectives

**Step 1: Configure the Multi-Service Environment**
The Nginx configuration file at `/app/gateway/nginx.conf` is incomplete. You must modify it so that:
* Requests to `http://localhost:8080/meta/` are proxy-passed to the Metadata Service on port `5001`.
* Requests to `http://localhost:8080/records/` are proxy-passed to the Genomics Data Store on port `5002`.
Once configured, start all services by executing `/app/start_services.sh`.

**Step 2: Data Aggregation Script**
Write a Bash script at `/home/user/aggregate.sh`. This script must:
1. Query the Metadata Service via the gateway (`http://localhost:8080/meta/experiments`) to retrieve a JSON list of active experiment IDs.
2. For each experiment ID, query the Metadata Service (`http://localhost:8080/meta/schema/<experiment_id>`) to get the experiment's schema mapping. The schema maps generic sensor fields (e.g., `s1`, `s2`) to biological markers (e.g., `tp53_level`, `brca1_level`).
3. Query the Genomics Data Store (`http://localhost:8080/records/<experiment_id>`) to get a stream of raw JSON data points.
4. Use standard CLI tools (like `jq`, `awk`, `curl`, etc.) to map the raw fields to their biological markers according to the schema.
5. Filter out any records where the status is `"corrupted"` or `"invalid"`.
6. Output the final aggregated data as a single JSON array of objects to `/home/user/processed_dataset.json`.

**Output Format Requirement**
The file `/home/user/processed_dataset.json` must be a valid JSON array containing the aggregated records. Each record must include the `experiment_id` and the mapped biological markers. Example:
```json
[
  {
    "experiment_id": "exp_101",
    "timestamp": 1690001000,
    "tp53_level": 0.45,
    "brca1_level": 1.2
  },
  ...
]
```

**Evaluation**
The researcher will evaluate your output using a quantitative accuracy metric. A verification script will compare your `/home/user/processed_dataset.json` against the hidden ground-truth dataset, calculating the Jaccard index (intersection over union) of the valid records. To succeed, your script must produce a dataset that achieves an accuracy metric of `accuracy >= 0.99`. Ensure your aggregation script handles all mappings correctly and strictly filters out invalid records.