You are a Database Reliability Engineer investigating a corrupted backup topology. Your team uses a graph structure to track which databases are backed up to which storage nodes, but the system of record was partially lost. 

You have three sources of information to reconstruct the backup knowledge graph:
1. **Relational Database Dump**: `/app/sql_dump.db` (SQLite). It contains a table `edges` with columns `src_id` and `dst_id` representing backup data flows between node IDs.
2. **Document Store Export**: `/app/nodes.jsonl`. A JSON-lines file containing the metadata for all nodes. Each line is a JSON object with at least `id` and `name` fields.
3. **Audio Log**: `/app/backup_log.wav`. A voicemail left by a departing engineer detailing three critical new backup routing links that were never entered into the database. The engineer uses the exact node *names* in the recording.

Your task:
1. Write a Python script to transcribe the audio file (you may install and use packages like `openai-whisper` or `SpeechRecognition`).
2. Extract the new backup routing edges mentioned in the audio.
3. Extract the existing backup edges from `/app/sql_dump.db` and map their `src_id` and `dst_id` to their respective node `name`s using `/app/nodes.jsonl`.
4. Combine all edges (from both the DB and the audio log) into a unified graph.
5. Output the complete list of edges to `/home/user/reconstructed_edges.csv`. The file must have the header `source,target` and contain the mapped *names* of the nodes (e.g., `DB_MAIN,STORAGE_SAN1`).

The automated verifier will evaluate your output by comparing your extracted edges against the ground-truth graph. You must achieve an F1 score of >= 0.90 to pass.