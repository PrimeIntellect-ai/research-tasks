I need you to help me process some dictated research logs regarding a series of database transactions that deadlocked our cluster last night. 

I recorded a voice memo detailing the exact sequence of lock acquisitions and block requests across several concurrent transactions. The audio file is located at `/app/research_log.wav`. 

Your task is to:
1. Transcribe the audio file (you may need to install and use tools like `whisper` or `ffmpeg`). 
2. Reverse-engineer the data model from the transcript to build a wait-for graph of the transactions. The transcript details which transaction holds a lock on which resource, and which transactions are waiting for locks.
3. Write a Python script at `/home/user/query_graph.py` that acts as a parameterized querying engine for this graph.

The script must accept exactly three arguments: `node_id` (a transaction ID), `limit` (integer), and `offset` (integer). 
Example: `python3 /home/user/query_graph.py TX_A 5 0`

For the given `node_id`, the script must:
- Project the materialized wait-for graph.
- Compute all traversal paths (up to a maximum length of 5) starting from `node_id` that end in a deadlock cycle (meaning the path loops back to any node already in the current path).
- Format each path as a string (e.g., `TX_A -> RES_1 -> TX_B -> RES_2 -> TX_A`).
- Sort these path strings alphabetically.
- Apply the `offset` and `limit` to the sorted list for pagination.
- Print each resulting path string on a new line to `stdout`.

Ensure your final script perfectly handles edge cases and strict pagination, as it will be rigorously tested against a reference implementation with randomized inputs.