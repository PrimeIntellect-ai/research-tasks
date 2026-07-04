You are a Data Engineer building out an ETL pipeline and analytics environment for a network security firm. Your task involves processing video telemetry, optimizing database queries, and building an adversarial filter for network graph data.

Complete the following three steps:

**Step 1: Video Telemetry Extraction**
We receive visual telemetry feeds of network dashboards. A sample video is located at `/app/data_feed.mp4`.
Extract the frames from this video at exactly 1 frame per second (1 fps) using `ffmpeg`. Save the extracted frames as JPEG images into the directory `/home/user/frames/` (you will need to create this directory).
Count the total number of frames extracted and write this integer to `/home/user/frame_count.txt`.

**Step 2: Database Index Strategy**
You are given a SQLite database at `/app/metrics.db` containing network performance logs in two tables:
- `nodes` (id, hostname, region)
- `traffic_logs` (id, source_node_id, target_node_id, bytes_transferred, timestamp)

We frequently run the following cross-query aggregation to find the total bytes transferred out of each region over a specific time window:
```sql
SELECT n.region, SUM(t.bytes_transferred)
FROM nodes n
JOIN traffic_logs t ON n.id = t.source_node_id
WHERE t.timestamp >= '2024-01-01' AND t.timestamp < '2024-02-01'
GROUP BY n.region;
```
Design an index strategy to optimize this query. Create a file at `/home/user/indexes.sql` containing the exact `CREATE INDEX` statements needed to maximize the performance of this aggregation.

**Step 3: Graph Analytics ETL Filter (Adversarial Corpus)**
Our pipeline ingests network topology snapshots in JSON format. Unfortunately, some ingested files are either malformed or contain adversarial "botnet" topologies designed to skew our analytics.

Write a Python script at `/home/user/validate_graphs.py` that acts as an ETL filter.
The script must be executable and accept exactly two arguments:
`python3 /home/user/validate_graphs.py <input_dir> <output_dir>`

For every `.json` file in `<input_dir>`, your script must:
1. **Validate Output Schema:** Ensure the JSON object contains a `"nodes"` key (a list of dictionaries, each with an `"id"` string) and an `"edges"` key (a list of dictionaries, each with `"source"` and `"target"` strings). If it lacks this exact schema, reject it.
2. **Graph Analytics:** Using the `networkx` library, construct an undirected graph from the nodes and edges. Calculate the Degree Centrality for all nodes. 
3. **Filtering:** If *any* node in the graph has a Degree Centrality greater than or equal to `0.80`, the graph is considered adversarial (botnet star-topology) and must be rejected.
4. **Action:** If a file passes both schema validation and the centrality check, copy it unmodified to `<output_dir>`.

Your script will be tested against two hidden corpora: an "evil" dataset containing malformed schemas and high-centrality botnets, and a "clean" dataset of normal topologies. To succeed, your script must reject 100% of the evil corpus and preserve 100% of the clean corpus.