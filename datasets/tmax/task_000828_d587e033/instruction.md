You are a Database Reliability Engineer (DBRE) tasked with recovering a critical transaction graph from a fragmented relational backup. We recently experienced a partial disk failure, and a frantic on-call engineer left an audio incident report detailing which backup shards were corrupted.

Your objective is to extract the clean data, transform the relational backup into a graph representation, compute network centrality, and output the exact scores for downstream restoration pipelines.

Here are the details of your task:

1. **Audio Incident Report:**
   An audio file is located at `/app/incident_report.wav`. You must transcribe or listen to this file (e.g., using `ffmpeg` and Python speech recognition libraries or whisper) to identify the specific numeric `shard_id`s that the engineer says are corrupted.

2. **Relational Backup DB:**
   The partial backup is stored in a SQLite database at `/app/backup.db`.
   It contains two tables:
   - `entities` (`id` VARCHAR, `entity_type` VARCHAR, `shard_id` INT)
   - `relations` (`src` VARCHAR, `dst` VARCHAR, `rel_type` VARCHAR, `weight` FLOAT, `shard_id` INT)

3. **Data Cleaning & Cross-Representation Mapping:**
   You must query the SQLite database to extract the valid graph.
   - A node (entity) is valid if its `shard_id` is NOT one of the corrupted shards mentioned in the audio.
   - An edge (relation) is valid ONLY IF its own `shard_id` is not corrupted AND both its `src` and `dst` nodes are valid entities. (You will need a query with complex joins/subqueries to filter this correctly).

4. **Graph Analytics:**
   Using the valid nodes and edges, construct a directed graph. The edges should be weighted by the `weight` column. 
   Compute the **PageRank** centrality for every valid node in the graph. Use a damping factor ($\alpha$) of `0.85` and weight the edges by the `weight` attribute. (Python's `networkx` library is highly recommended for this).

5. **Output Schema:**
   Save your final PageRank scores in a strict JSON format at `/home/user/pagerank.json`.
   The schema must be a simple key-value mapping of the entity `id` (string) to its PageRank score (float).
   Example:
   ```json
   {
     "node_A": 0.0452,
     "node_B": 0.0121
   }
   ```

To succeed, your PageRank scores must be highly accurate. An automated metric verifier will compute the Mean Absolute Error (MAE) between your output and the true mathematical PageRank of the uncorrupted subgraph. Your output must achieve an MAE of $\le 10^{-4}$.