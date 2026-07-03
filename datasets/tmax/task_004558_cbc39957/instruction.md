You are a database reliability engineer tasked with recovering corrupted graph database backups. We recently received an automated voice alert regarding a critical backup failure. 

First, locate the automated voice alert at `/app/incident_alert.wav`. You will need to transcribe this audio to determine the specific graph node type and timestamp range affected by the corruption.

Next, you will find a large, raw backup dump in `/home/user/graph_backup/`. The dump consists of two files: `nodes.csv` (format: `node_id,node_type,timestamp,value`) and `edges.csv` (format: `source_id,target_id,relationship_type`). 

Your task is to write a C program at `/home/user/recovery_processor.c` that performs the following operations:
1. Parses the CSV files and builds an efficient in-memory index (e.g., a hash table or adjacency list) to quickly traverse the graph.
2. Identifies all nodes of the type and within the timestamp range specified in the audio alert.
3. For each identified node, calculates a rolling moving average (a window function of size 3, ordered by timestamp) of the `value` of its immediate neighbors connected by a `DEPENDS_ON` relationship.
4. Aggregates the results and writes the summary to `/home/user/recovery_summary.txt` in the format: `node_id,moving_average`.

Because the backup files are massive, your C program must implement an efficient index strategy. A naive $O(N^2)$ approach will fail our performance checks. Your code must compile to `/home/user/recovery_processor` using standard `gcc`.

Finally, execute your program and generate the `recovery_summary.txt` log file.