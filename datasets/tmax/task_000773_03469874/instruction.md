You are a Database Reliability Engineer (DBRE) tasked with optimizing our backup scheduling across a complex microservices architecture. 

We have a set of databases that replicate data downstream. When a primary database is backed up, the impact of that backup propagates through the system. We need to identify which databases have the highest "Backup Impact Score" so we can prioritize them.

You have been provided with two pieces of information:
1. An architecture diagram image at `/app/topology.png`. This image contains plain text lines defining the replication topology and latency (distance) between database nodes. The format in the image is `source -> destination : distance` (e.g., `db1 -> db2 : 5`).
2. A JSON dump of our database metadata at `/app/backups.json` containing the backup size of each node in GB.

Your task is to write a Rust program that calculates the Backup Impact Score for each database node.

The "Backup Impact Score" for a node X is defined as:
`Score(X) = size_gb(X) + SUM( size_gb(Y) / shortest_path_distance(X, Y) )`
for all nodes Y that are reachable from X (where shortest_path_distance is the minimum sum of edge weights from X to Y). If Y is not reachable from X, it contributes 0.

Write a Rust project in `/home/user/backup_analyzer` that:
1. Extracts the topology information from the image. (You may use system tools like `tesseract` to OCR the image first, then read the output in your Rust code, or handle it via a shell script that feeds your Rust program).
2. Reads `/app/backups.json`.
3. Computes the shortest paths and the Backup Impact Score for all nodes.
4. Sorts the nodes by their Backup Impact Score in descending order.
5. Saves the top 5 nodes (pagination) to `/home/user/top_backups.json` in the following exact format:
```json
[
  {
    "node": "NodeName",
    "score": 123.45
  },
  ...
]
```

Use double-precision floating point for all score calculations.